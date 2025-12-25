from BaseClasses import CollectionState
from typing import TYPE_CHECKING

from .Options import EggsBehaviour, LogicType, RandomizeBKMoveList, VictoryCondition
from .Names import regionName, itemName, locationName
from worlds.generic.Rules import set_rule

# I don't know what is going on here, but it works.
if TYPE_CHECKING:
    from . import BanjoTooieWorld

# Shamelessly Stolen from KH2 :D

class BanjoTooieRules:
    world: "BanjoTooieWorld"

    def __init__(self, world: "BanjoTooieWorld") -> None:
        self.player = world.player
        self.world = world

        self.solo_moves = [
            itemName.PACKWH,
            itemName.TAXPACK,
            itemName.SNPACK,
            itemName.SHPACK,
            itemName.SAPACK,
            itemName.WWHACK,
            itemName.HATCH,
            itemName.LSPRING,
            itemName.GLIDE
        ]

        if self.world.options.skip_puzzles.value:
            self.access_rules = {
                locationName.W1: self.world_1_unlocked,
                locationName.W2: self.world_2_unlocked,
                locationName.W3: self.world_3_unlocked,
                locationName.W4: self.world_4_unlocked,
                locationName.W5: self.world_5_unlocked,
                locationName.W6: self.world_6_unlocked,
                locationName.W7: self.world_7_unlocked,
                locationName.W8: self.world_8_unlocked,
                locationName.W9: self.world_9_unlocked
            }

        if self.world.options.victory_condition.value == VictoryCondition.option_minigame_hunt\
            or self.world.options.victory_condition.value == VictoryCondition.option_wonderwing_challenge:

            self.gametoken_rules = {
                locationName.MUMBOTKNGAME1: self.jiggy_mayahem_kickball,
                locationName.MUMBOTKNGAME2: self.jiggy_ordnance_storage,
                locationName.MUMBOTKNGAME3: self.jiggy_hoop_hurry,
                locationName.MUMBOTKNGAME4: self.jiggy_dodgem,
                locationName.MUMBOTKNGAME5: self.jiggy_peril,
                locationName.MUMBOTKNGAME6: self.jiggy_balloon_burst,
                locationName.MUMBOTKNGAME7: self.jiggy_sub_challenge,
                locationName.MUMBOTKNGAME8: self.jiggy_chompa,
                locationName.MUMBOTKNGAME9: self.jiggy_clinkers,
                locationName.MUMBOTKNGAME10: self.jiggy_twinkly,
                locationName.MUMBOTKNGAME11: self.jiggy_hfp_kickball,
                locationName.MUMBOTKNGAME12: self.jiggy_pot_of_gold,
                locationName.MUMBOTKNGAME13: self.jiggy_zubbas,
                locationName.MUMBOTKNGAME14: self.jiggy_trash_can,
                locationName.MUMBOTKNGAME15: self.jiggy_cc_canary_mary,

            }

        if self.world.options.victory_condition.value == VictoryCondition.option_boss_hunt\
            or self.world.options.victory_condition.value == VictoryCondition.option_wonderwing_challenge\
            or self.world.options.victory_condition.value == VictoryCondition.option_boss_hunt_and_hag1:
            self.bosstoken_rules = {
                locationName.MUMBOTKNBOSS1: self.jiggy_targitzan,
                locationName.MUMBOTKNBOSS2: self.can_beat_king_coal,
                locationName.MUMBOTKNBOSS3: self.jiggy_patches,
                locationName.MUMBOTKNBOSS4: self.jiggy_lord_woo,
                locationName.MUMBOTKNBOSS5: self.can_beat_terry,
                locationName.MUMBOTKNBOSS6: self.can_beat_weldar,
                locationName.MUMBOTKNBOSS7: self.jiggy_dragons_bros,
                locationName.MUMBOTKNBOSS8: self.jiggy_mingy,
            }

        if self.world.options.victory_condition.value == VictoryCondition.option_jinjo_family_rescue\
            or self.world.options.victory_condition.value == VictoryCondition.option_wonderwing_challenge:
            self.jinjotoken_rules = {
                locationName.MUMBOTKNJINJO1: self.jiggy_white_jinjo_family,
                locationName.MUMBOTKNJINJO2: self.jiggy_orange_jinjo_family,
                locationName.MUMBOTKNJINJO3: self.jiggy_yellow_jinjo_family,
                locationName.MUMBOTKNJINJO4: self.jiggy_brown_jinjo_family,
                locationName.MUMBOTKNJINJO5: self.jiggy_green_jinjo_family,
                locationName.MUMBOTKNJINJO6: self.jiggy_red_jinjo_family,
                locationName.MUMBOTKNJINJO7: self.jiggy_blue_jinjo_family,
                locationName.MUMBOTKNJINJO8: self.jiggy_purple_jinjo_family,
                locationName.MUMBOTKNJINJO9: self.jiggy_black_jinjo_family,
            }

        if self.world.options.cheato_rewards.value:
            self.cheato_rewards_rules = {
                locationName.CHEATOR1: self.cheato_reward_1,
                locationName.CHEATOR2: self.cheato_reward_2,
                locationName.CHEATOR3: self.cheato_reward_3,
                locationName.CHEATOR4: self.cheato_reward_4,
                locationName.CHEATOR5: self.cheato_reward_5,
            }

        if self.world.options.honeyb_rewards.value:
            self.honeyb_rewards_rules = {
                locationName.HONEYBR1: self.honey_b_reward_1,
                locationName.HONEYBR2: self.honey_b_reward_2,
                locationName.HONEYBR3: self.honey_b_reward_3,
                locationName.HONEYBR4: self.honey_b_reward_4,
                locationName.HONEYBR5: self.honey_b_reward_5,
            }



        self.train_rules = {
            locationName.CHUFFY: self.can_beat_king_coal,
            locationName.TRAINSWIH: self.train_switch_ioh,
            locationName.TRAINSWHP2: self.humbaHFP,
            locationName.TRAINSWHP1: self.tswitch_lavaside,
            locationName.TRAINSWWW: self.tswitch_ww,
            locationName.TRAINSWTD: self.tswitch_tdl,
            #locationName.TRAINSWGI: self.tswitch_gi,
        }

        self.jiggy_chunks_rules = {
            locationName.CHUNK1: self.jiggy_crushing_shed,
            locationName.CHUNK2: self.jiggy_crushing_shed,
            locationName.CHUNK3: self.jiggy_crushing_shed,
        }

        self.scrit_scrat_scrut_rules = {
            locationName.SCRUT: self.scrut,
            locationName.SCRAT: self.scrat,
            locationName.SCRIT: self.scrit
        }

        self.boggy_kids_rules = {
            locationName.MOGGY: self.moggy,
            locationName.SOGGY: self.soggy,
            locationName.GROGGY: self.groggy
        }

        self.alien_kids_rules = {
            locationName.ALPHETTE: self.alphette,
            locationName.BETETTE: self.betette,
            locationName.GAMETTE: self.gamette
        }

        self.skivvy_rules = {
            locationName.SKIVOU: self.skivvy_outside,
            locationName.SKIVWQ: self.skivvy_worker_quarters,
            locationName.SKIVF1: self.skivvy_floor_1,
            locationName.SKIVF2: self.skivvy_floor_2,
            locationName.SKIVF3: self.skivvy_floor_3,
            locationName.SKIVF5: self.skivvy_floor_5,
        }

        self.mr_fit_rules = {
            locationName.FITHJ: self.mr_fit_high_jump,
            locationName.FITSR: self.mr_fit_sack_race,
        }

        self.jiggy_rules = {
            locationName.JIGGYMT1: self.jiggy_targitzan,
            locationName.JIGGYMT2: self.jiggy_sschamber,
            locationName.JIGGYMT3: self.jiggy_mayahem_kickball,
            locationName.JIGGYMT4: self.jiggy_bovina,
            locationName.JIGGYMT5: self.jiggy_treasure_chamber,
            locationName.JIGGYMT6: self.jiggy_golden_goliath,
            locationName.JIGGYMT7: self.jiggy_prison_quicksand,
            locationName.JIGGYMT8: self.jiggy_pillars,
            locationName.JIGGYMT9: self.jiggy_top,
            locationName.JIGGYMT10: self.jiggy_ssslumber,

            locationName.JIGGYGM1: self.can_beat_king_coal,
            locationName.JIGGYGM2: self.canary_mary_free,
            locationName.JIGGYGM3: self.jiggy_generator_cavern,
            locationName.JIGGYGM4: self.jiggy_waterfall_cavern,
            locationName.JIGGYGM5: self.jiggy_ordnance_storage,
            locationName.JIGGYGM6: self.dilberta_free,
            locationName.JIGGYGM7: self.jiggy_crushing_shed,
            locationName.JIGGYGM8: self.jiggy_waterfall,
            locationName.JIGGYGM9: self.jiggy_power_hut,
            locationName.JIGGYGM10: self.jiggy_flooded_caves,

            locationName.JIGGYWW1: self.jiggy_hoop_hurry,
            locationName.JIGGYWW2: self.jiggy_dodgem,
            locationName.JIGGYWW3: self.jiggy_patches,
            locationName.JIGGYWW4: self.jiggy_peril,
            locationName.JIGGYWW5: self.jiggy_balloon_burst,
            locationName.JIGGYWW6: self.jiggy_dive_of_death,
            locationName.JIGGYWW7: self.jiggy_mrs_boggy,
            locationName.JIGGYWW8: self.jiggy_star_spinner,
            locationName.JIGGYWW9: self.jiggy_inferno,
            locationName.JIGGYWW10: self.jiggy_cactus,

            locationName.JIGGYJR1: self.jiggy_sub_challenge,
            locationName.JIGGYJR2: self.jiggy_tiptup,
            locationName.JIGGYJR3: self.jiggy_bacon,
            locationName.JIGGYJR4: self.jiggy_pig_pool,
            locationName.JIGGYJR5: self.jiggy_smuggler,
            locationName.JIGGYJR6: self.jiggy_merry_maggie,
            locationName.JIGGYJR7: self.jiggy_lord_woo,
            locationName.JIGGYJR8: self.jiggy_see_mee,
            locationName.JIGGYJR9: self.jiggy_pawno,
            locationName.JIGGYJR10: self.jiggy_ufo,

            locationName.JIGGYTD1: self.jiggy_terry_nest,
            locationName.JIGGYTD2: self.jiggy_dippy,
            locationName.JIGGYTD3: self.jiggy_scrotty,
            locationName.JIGGYTD4: self.can_beat_terry,
            locationName.JIGGYTD5: self.jiggy_oogle_boogle,
            locationName.JIGGYTD6: self.jiggy_chompa,
            locationName.JIGGYTD7: self.jiggy_terry_kids,
            locationName.JIGGYTD8: self.jiggy_stomping_plains,
            locationName.JIGGYTD9: self.jiggy_rocknuts,
            locationName.JIGGYTD10: self.jiggy_roar_cage,

            locationName.JIGGYGI1: self.jiggy_underwater_waste_disposal,
            locationName.JIGGYGI2: self.jiggy_weldar,
            locationName.JIGGYGI3: self.jiggy_clinkers,
            locationName.JIGGYGI4: self.jiggy_skivvy,
            locationName.JIGGYGI5: self.jiggy_floor5,
            locationName.JIGGYGI6: self.jiggy_quality_control,
            locationName.JIGGYGI7: self.jiggy_guarded,
            locationName.JIGGYGI8: self.jiggy_trash_compactor,
            locationName.JIGGYGI9: self.jiggy_twinkly,
            locationName.JIGGYGI10: self.jiggy_waste_disposal_box,

            locationName.JIGGYHP1: self.jiggy_dragons_bros,
            locationName.JIGGYHP2: self.jiggy_volcano,
            locationName.JIGGYHP3: self.jiggy_sabreman,
            locationName.JIGGYHP4: self.jiggy_boggy,
            locationName.JIGGYHP5: self.jiggy_icy_side_station,
            locationName.JIGGYHP6: self.jiggy_oil_drill,
            locationName.JIGGYHP7: self.jiggy_hfp_stomping,
            locationName.JIGGYHP8: self.jiggy_hfp_kickball,
            locationName.JIGGYHP9: self.jiggy_aliens,
            locationName.JIGGYHP10: self.jiggy_colosseum_split,

            locationName.JIGGYCC1: self.jiggy_mingy,
            locationName.JIGGYCC2: self.jiggy_mr_fit,
            locationName.JIGGYCC3: self.jiggy_pot_of_gold,
            locationName.JIGGYCC4: self.jiggy_cc_canary_mary,
            locationName.JIGGYCC5: self.jiggy_zubbas,
            locationName.JIGGYCC6: self.jiggy_jiggium_plant,
            locationName.JIGGYCC7: self.jiggy_cheese,
            locationName.JIGGYCC8: self.jiggy_trash_can,
            locationName.JIGGYCC9: self.jiggy_superstash,
            locationName.JIGGYCC10: self.jiggy_jelly_castle,

            locationName.JIGGYIH1: self.jiggy_white_jinjo_family,
            locationName.JIGGYIH2: self.jiggy_orange_jinjo_family,
            locationName.JIGGYIH3: self.jiggy_yellow_jinjo_family,
            locationName.JIGGYIH4: self.jiggy_brown_jinjo_family,
            locationName.JIGGYIH5: self.jiggy_green_jinjo_family,
            locationName.JIGGYIH6: self.jiggy_red_jinjo_family,
            locationName.JIGGYIH7: self.jiggy_blue_jinjo_family,
            locationName.JIGGYIH8: self.jiggy_purple_jinjo_family,
            locationName.JIGGYIH9: self.jiggy_black_jinjo_family,

        }
        self.cheato_rules = {
            locationName.CHEATOMT1: self.cheato_snakehead,
            locationName.CHEATOMT2: self.cheato_prison,
            locationName.CHEATOMT3: self.cheato_jade_snake_grove,

            locationName.CHEATOGM1: self.canary_mary_free,
            locationName.CHEATOGM2: self.cheato_gm_entrance,
            locationName.CHEATOGM3: self.cheato_water_storage,

            locationName.CHEATOWW1: self.cheato_haunted_cavern,
            locationName.CHEATOWW2: self.cheato_inferno,
            locationName.CHEATOWW3: self.cheato_saucer_of_peril,

            locationName.CHEATOJR1: self.cheato_pawno,
            locationName.CHEATOJR2: self.cheato_seemee,
            locationName.CHEATOJR3: self.cheato_ancient_swimming_baths,

            locationName.CHEATOTL1: self.cheato_dippy_pool,
            locationName.CHEATOTL2: self.cheato_trex,
            locationName.CHEATOTL3: self.cheato_tdlboulder,

            locationName.CHEATOGI1: self.cheato_loggo,
            locationName.CHEATOGI2: self.cheato_window,
            locationName.CHEATOGI3: self.can_beat_weldar,

            locationName.CHEATOHP1: self.cheato_colosseum,
            locationName.CHEATOHP2: self.cheato_icicle_grotto,
            locationName.CHEATOHP3: self.cheato_icy_pillar,

            locationName.CHEATOCC1: self.cheato_canary_mary,
            locationName.CHEATOCC2: self.cheato_potgold,
            locationName.CHEATOCC3: self.cheato_zubbas,

            locationName.CHEATOSM1: self.cheato_spiral
        }
        self.honey_rules = {
            locationName.HONEYCMT1: self.honeycomb_mt_entrance,
            locationName.HONEYCMT2: self.honeycomb_bovina,
            locationName.HONEYCMT3: self.honeycomb_treasure_chamber,

            locationName.HONEYCGM1: self.ggm_boulders,
            locationName.HONEYCGM2: self.honeycomb_prospector,
            locationName.HONEYCGM3: self.honeycomb_gm_station,

            locationName.HONEYCWW1: self.honeycomb_space_zone,
            locationName.HONEYCWW3: self.honeycomb_crazy_castle,

            locationName.HONEYCJR1: self.honeycomb_seemee,
            locationName.HONEYCJR3: self.honeycomb_jrl_pipes,

            locationName.HONEYCTL1: self.honeycomb_lakeside,
            locationName.HONEYCTL2: self.honeycomb_styracosaurus,
            locationName.HONEYCTL3: self.honeycomb_river,

            locationName.HONEYCGI1: self.honeycomb_floor3,
            locationName.HONEYCGI2: self.honeycomb_gi_station,

            locationName.HONEYCHP1: self.honeycomb_volcano,
            locationName.HONEYCHP2: self.honeycomb_hfp_station,
            locationName.HONEYCHP3: self.honeycomb_lava_side,

            locationName.HONEYCCC1: self.bill_drill,
            locationName.HONEYCCC2: self.honeycomb_trash,
            locationName.HONEYCCC3: self.honeycomb_pot,

            locationName.HONEYCIH1: self.plateau_top

        }
        self.glowbo_rules = {
            locationName.GLOWBOGM1: self.glowbo_entrance_ggm,

            locationName.GLOWBOWW2: self.glowbo_wigwam,

            locationName.GLOWBOJR1: self.pawno_shelves,
            locationName.GLOWBOJR2: self.glowbo_underwigwam,

            locationName.GLOWBOTL1: self.glowbo_tdl,
            locationName.GLOWBOTL2: self.glowbo_tdl_mumbo,

            locationName.GLOWBOGI2: self.glowbo_floor_3,

            locationName.GLOWBOHP2: self.glowbo_icy_side,

            locationName.GLOWBOCC1: self.ccl_glowbo_pool,
            locationName.GLOWBOCC2: self.glowbo_cavern,

            locationName.GLOWBOIH1: self.glowbo_cliff,
            locationName.GLOWBOMEG: self.mega_glowbo

        }
        self.doubloon_rules = {
            #Alcove
            locationName.JRLDB22: self.doubloon_ledge,
            locationName.JRLDB23: self.doubloon_ledge,
            locationName.JRLDB24: self.doubloon_ledge,
            #Underground
            locationName.JRLDB19: self.doubloon_dirtpatch,
            locationName.JRLDB20: self.doubloon_dirtpatch,
            locationName.JRLDB21: self.doubloon_dirtpatch,
            #Underwater
            locationName.JRLDB11: self.doubloon_water,
            locationName.JRLDB12: self.doubloon_water,
            locationName.JRLDB13: self.doubloon_water,
            locationName.JRLDB14: self.doubloon_water,
            locationName.JRLDB27: self.doubloon_water,
            locationName.JRLDB28: self.doubloon_water,
            locationName.JRLDB29: self.doubloon_water,
            locationName.JRLDB30: self.doubloon_water,

        }
        self.treble_clef_rules = {
            locationName.TREBLEJV: self.treble_jv,
            locationName.TREBLEGM: self.treble_gm,
            locationName.TREBLEWW: self.treble_ww,
            locationName.TREBLEJR: self.treble_jrl,
            locationName.TREBLETL: self.treble_tdl,
            locationName.TREBLEGI: self.treble_gi,
            locationName.TREBLEHP: self.treble_hfp,
            locationName.TREBLECC: self.treble_ccl,
        }

        self.silo_rules = {
            ## Faster swimming and double air rules are here ##
            locationName.ROYSTEN1: self.bill_drill,
            locationName.ROYSTEN2: self.bill_drill,

            locationName.EGGAIM: self.silo_egg_aim,
            locationName.BBLASTER: self.silo_breegull_blaster,
            locationName.GGRAB: self.silo_grip_grab,

            locationName.BDRILL: self.silo_bill_drill,
            locationName.BBAYONET: self.silo_beak_bayonet,

            locationName.AIREAIM: self.silo_airborne_egg_aiming,
            locationName.SPLITUP: self.silo_split_up,
            locationName.PACKWH: self.silo_pack_whack,

            locationName.AUQAIM: self.silo_sub_aqua_egg_aiming,
            locationName.TTORP: self.silo_talon_torpedo,
            locationName.WWHACK: self.silo_wing_whack,

            locationName.SPRINGB: self.silo_springy_step_shoes,
            locationName.TAXPACK: self.silo_taxi_pack,
            locationName.HATCH: self.silo_hatch,

            locationName.SNPACK: self.silo_snooze,
            locationName.LSPRING: self.silo_leg_spring,
            locationName.CLAWBTS: self.silo_claw_clamber_boots,

            locationName.SHPACK: self.silo_shack_pack,
            locationName.GLIDE: self.silo_glide,

            locationName.SAPACK: self.silo_sack_pack,

            locationName.FEGGS: self.silo_fire_eggs,
            locationName.GEGGS: self.silo_grenade_eggs,
            locationName.IEGGS: self.silo_ice_eggs,
            locationName.CEGGS: self.silo_clockwork_eggs
        }

        self.jinjo_rules = {
            locationName.JINJOIH5: self.jinjo_spiral_mountain,
            locationName.JINJOIH4: self.jinjo_plateau,
            locationName.JINJOIH3: self.jinjo_clifftop,
            locationName.JINJOIH2: self.jinjo_wasteland,

            locationName.JINJOMT1: self.jinjo_jadesnakegrove,
            locationName.JINJOMT2: self.jinjo_stadium,
            locationName.JINJOMT4: self.jinjo_pool,

            #Water Storage Jinjo always true because it's in the GMWSJT area
            locationName.JINJOGM2: self.jinjo_jail,
            locationName.JINJOGM4: self.jinjo_boulder,

            locationName.JINJOWW1: self.jinjo_tent,
            locationName.JINJOWW2: self.jinjo_cave_of_horrors,
            locationName.JINJOWW3: self.jinjo_van_door,
            locationName.JINJOWW4: self.jinjo_dodgem,
            locationName.JINJOWW5: self.jinjo_cactus,

            locationName.JINJOJR1: self.jinjo_alcove,
            locationName.JINJOJR2: self.jinjo_blubber,
            locationName.JINJOJR3: self.jinjo_big_fish,
            locationName.JINJOJR4: self.jinjo_seaweed_sanctum,
            locationName.JINJOJR5: self.jinjo_sunken_ship,

            locationName.JINJOTL2: self.jinjo_tdl_entrance,
            locationName.JINJOTL1: self.jinjo_talon_torpedo,
            locationName.JINJOTL3: self.clockwork_eggs,
            locationName.JINJOTL4: self.jinjo_big_t_rex,
            locationName.JINJOTL5: self.jinjo_stomping_plains,

            locationName.JINJOGI2: self.jinjo_legspring,
            locationName.JINJOGI3: self.jinjo_waste_disposal,
            locationName.JINJOGI4: self.jinjo_boiler,
            locationName.JINJOGI5: self.jinjo_gi_outside,

            locationName.JINJOHP1: self.jinjo_hot_waterfall,
            locationName.JINJOHP2: self.jinjo_hot_pool,
            locationName.JINJOHP3: self.jinjo_wind_tunnel,
            locationName.JINJOHP4: self.jinjo_icicle_grotto,
            locationName.JINJOHP5: self.jinjo_mildred,

            locationName.JINJOCC1: self.jinjo_trash_can,
            locationName.JINJOCC2: self.jinjo_cheese,
            locationName.JINJOCC3: self.jinjo_central,
            locationName.JINJOCC5: self.jinjo_humba_ccl,
        }

        self.notes_rules = {
            locationName.NOTEIH1: self.notes_plateau_sign,
            locationName.NOTEIH2: self.notes_plateau_sign,
            locationName.NOTEIH3: self.plateau_top,
            locationName.NOTEIH4: self.plateau_top,
            locationName.NOTEIH13: self.notes_bottom_clockwork,
            locationName.NOTEIH14: self.notes_top_clockwork,

            locationName.NOTEGGM1: self.notes_green_pile,
            locationName.NOTEGGM2: self.notes_green_pile,
            locationName.NOTEGGM3: self.notes_green_pile,
            locationName.NOTEGGM4: self.notes_green_pile,
            locationName.NOTEGGM5: self.notes_prospector_easy,
            locationName.NOTEGGM6: self.notes_prospector_easy,
            locationName.NOTEGGM7: self.notes_prospector_hard,
            locationName.NOTEGGM8: self.notes_prospector_easy,
            locationName.NOTEGGM9: self.notes_prospector_easy,
            locationName.NOTEGGM10: self.notes_gm_mumbo_easy,
            locationName.NOTEGGM11: self.notes_gm_mumbo_hard,
            locationName.NOTEGGM12: self.notes_gm_mumbo_hard,
            locationName.NOTEGGM13: self.notes_easy_fuel_depot,
            locationName.NOTEGGM14: self.notes_hard_fuel_depot,
            locationName.NOTEGGM15: self.notes_easy_fuel_depot,
            locationName.NOTEGGM16: self.notes_easy_fuel_depot,


            locationName.NOTEWW9: self.notes_ww_area51_left,
            locationName.NOTEWW10: self.notes_ww_area51_right,
            locationName.NOTEWW13: self.notes_dive_of_death,
            locationName.NOTEWW14: self.notes_dive_of_death,

            locationName.NOTEJRL4: self.notes_jrl_blubs,
            locationName.NOTEJRL5: self.notes_jrl_blubs,
            locationName.NOTEJRL6: self.notes_jrl_eels,
            locationName.NOTEJRL7: self.notes_jrl_eels,
            locationName.NOTEJRL11: self.pawno_shelves,
            locationName.NOTEJRL12: self.pawno_shelves,
            locationName.NOTEJRL13: self.pawno_shelves,
            locationName.NOTEJRL14: self.notes_jolly,
            locationName.NOTEJRL15: self.notes_jolly,
            locationName.NOTEJRL16: self.notes_jolly,

            locationName.NOTETDL1: self.notes_tdl_station_right,
            locationName.NOTETDL10: self.notes_roar_cage,
            locationName.NOTETDL11: self.notes_roar_cage,
            locationName.NOTETDL12: self.notes_roar_cage,
            locationName.NOTETDL13: self.notes_river_passage,
            locationName.NOTETDL14: self.notes_river_passage,
            locationName.NOTETDL15: self.notes_river_passage,
            locationName.NOTETDL16: self.notes_river_passage,

            locationName.NOTEGI1: self.notes_gi_train_station_hard,
            locationName.NOTEGI2: self.notes_gi_train_station_easy,
            locationName.NOTEGI3: self.notes_gi_train_station_easy,
            locationName.NOTEGI4: self.notes_gi_floor1,
            locationName.NOTEGI5: self.notes_gi_floor1,
            locationName.NOTEGI6: self.notes_leg_spring,
            locationName.NOTEGI7: self.notes_leg_spring,
            locationName.NOTEGI8: self.notes_leg_spring,
            locationName.NOTEGI9: self.notes_short_stack,
            locationName.NOTEGI11: self.notes_waste_disposal,
            locationName.NOTEGI12: self.notes_waste_disposal,
            locationName.NOTEGI13: self.notes_aircon_hard,
            locationName.NOTEGI15: self.notes_floor_3,
            locationName.NOTEGI16: self.notes_floor_3,

            locationName.NOTEHFP1: self.hfp_top,
            locationName.NOTEHFP2: self.hfp_top,
            locationName.NOTEHFP5: self.hfp_top,
            locationName.NOTEHFP6: self.hfp_top,
            locationName.NOTEHFP7: self.notes_ladder,
            locationName.NOTEHFP8: self.notes_ladder,
            locationName.NOTEHFP9: self.notes_oil_drill,
            locationName.NOTEHFP10: self.notes_oil_drill,
            locationName.NOTEHFP11: self.notes_upper_icy_side,
            locationName.NOTEHFP12: self.notes_upper_icy_side,
            locationName.NOTEHFP13: self.notes_boggy,
            locationName.NOTEHFP14: self.notes_boggy,
            locationName.NOTEHFP15: self.notes_lower_icy_side,
            locationName.NOTEHFP16: self.notes_lower_icy_side,

            locationName.NOTECCL2: self.notes_ccl_low,
            locationName.NOTECCL3: self.notes_ccl_silo,
            locationName.NOTECCL4: self.notes_ccl_silo,
            locationName.NOTECCL5: self.notes_cheese,
            locationName.NOTECCL6: self.notes_ccl_low,
            locationName.NOTECCL7: self.notes_dippy,
            locationName.NOTECCL8: self.notes_ccl_low,
            locationName.NOTECCL9: self.notes_ccl_low,
            locationName.NOTECCL10: self.notes_sack_race,
            locationName.NOTECCL11: self.notes_ccl_high,
            locationName.NOTECCL12: self.notes_ccl_high,
            locationName.NOTECCL13: self.ccl_glowbo_pool,
            locationName.NOTECCL14: self.notes_ccl_low,
            locationName.NOTECCL15: self.notes_ccl_low,
            locationName.NOTECCL16: self.notes_ccl_low,
        }

        self.stopnswap_rules = {
            locationName.IKEY: self.ice_key,
            locationName.PMEGG: self.pink_mystery_egg,
            locationName.PMEGGH: self.pink_egg_hatched,
            locationName.BMEGG: self.blue_mystery_egg,
            locationName.BMEGGH: self.blue_egg_hatched,
            locationName.YMEGGH: self.yellow_egg_hatched
        }

        self.nest_rules = {
            locationName.NESTSM4: self.nest_lair_top,
            locationName.NESTSM5: self.nest_lair_top,
            locationName.NESTSM6: self.nest_lair_top,

            locationName.NESTSM22: self.nest_sm_waterfall_top,
            locationName.NESTSM23: self.nest_sm_waterfall_platform,
            locationName.NESTSM24: self.nest_sm_waterfall_platform,


            locationName.NESTIH16: self.nest_bottles_house,
            locationName.NESTIH17: self.nest_bottles_house,

            locationName.NESTIH32: self.nest_pl_dirt_pile,
            locationName.NESTIH33: self.nest_pl_dirt_pile,

            locationName.NESTIH43: self.nest_cliff_top_hard,

            locationName.NESTIH56: self.nest_another_digger_tunnel,
            locationName.NESTIH57: self.nest_another_digger_tunnel,

            locationName.NESTIH58: self.nest_quagmire_medium,
            locationName.NESTIH59: self.nest_quagmire_easy,
            locationName.NESTIH60: self.nest_quagmire_hard,

            locationName.NESTMT11: self.nest_mt_stadium,
            locationName.NESTMT12: self.nest_mt_stadium,

            locationName.NESTMT15: self.nest_pillars,
            locationName.NESTMT16: self.nest_pillars,
            locationName.NESTMT17: self.nest_pillars,
            locationName.NESTMT18: self.nest_mt_cell_right,
            locationName.NESTMT21: self.nest_mt_cell_left,

            locationName.NESTMT22: self.nest_code_chamber,

            locationName.NESTGM3: self.nest_bill_drill,
            locationName.NESTGM4: self.nest_bill_drill,

            locationName.NESTGM13: self.nest_flooded_caves,
            locationName.NESTGM14: self.nest_flooded_caves,

            locationName.NESTGM16: self.nest_outside_power_hut,
            locationName.NESTGM17: self.nest_outside_power_hut,
            locationName.NESTGM18: self.ggm_boulders,
            locationName.NESTGM19: self.ggm_boulders,

            locationName.NESTGM21: self.ggm_boulders,

            locationName.NESTGM26: self.notes_prospector_hard,

            locationName.NESTGM27: self.nest_ggm_mumbo,
            locationName.NESTGM28: self.nest_ggm_mumbo,
            locationName.NESTGM29: self.nest_ggm_mumbo,

            locationName.NESTGM30: self.nest_toxic_gas_cave,
            locationName.NESTGM31: self.nest_toxic_gas_cave,

            locationName.NESTGM32: self.nest_canary_high,
            locationName.NESTGM33: self.nest_canary_low,
            locationName.NESTGM34: self.nest_canary_low,
            locationName.NESTGM35: self.nest_canary_low,

            locationName.NESTGM36: self.ggm_boulders,
            locationName.NESTGM37: self.ggm_boulders,
            locationName.NESTGM38: self.ggm_boulders,


            locationName.NESTWW15: self.nest_pump_room,
            locationName.NESTWW16: self.nest_pump_room,

            locationName.NESTJR3: self.nest_jr_sub_aqua_1,
            locationName.NESTJR4: self.nest_jr_sub_aqua_2,
            locationName.NESTJR5: self.nest_jolly_gunpowder,
            locationName.NESTJR6: self.nest_jolly_gunpowder,

            locationName.NESTJR10: self.nest_seaweed_bottom,
            locationName.NESTJR11: self.nest_seaweed_others,
            locationName.NESTJR12: self.nest_seaweed_top,
            locationName.NESTJR13: self.nest_seaweed_others,

            locationName.NESTJR14: self.jiggy_merry_maggie,
            locationName.NESTJR15: self.jiggy_merry_maggie,

            locationName.NESTJR16: self.nest_bacon,
            locationName.NESTJR17: self.nest_bacon,
            locationName.NESTJR18: self.nest_bacon,
            locationName.NESTJR19: self.nest_bacon,

            locationName.NESTJR20: self.nest_lord_woo,
            locationName.NESTJR21: self.nest_lord_woo,
            locationName.NESTJR22: self.nest_lord_woo,
            locationName.NESTJR23: self.nest_lord_woo,

            locationName.NESTJR27: self.notes_jrl_blubs,

            locationName.NESTJR33: self.talon_torpedo,

            locationName.NESTJR37: self.nest_big_fish_cavern,
            locationName.NESTJR38: self.nest_big_fish_cavern,
            locationName.NESTJR39: self.talon_torpedo,
            locationName.NESTJR40: self.talon_torpedo,


            locationName.NESTTL4: self.nest_tdl_waterfall_alcove,
            locationName.NESTTL5: self.nest_tdl_waterfall_alcove,

            locationName.NESTTL12: self.nest_tdl_wall_with_holes,
            locationName.NESTTL13: self.nest_tdl_wall_with_holes,
            locationName.NESTTL14: self.nest_tdl_wall_with_holes,
            locationName.NESTTL15: self.nest_tdl_wall_with_holes,
            locationName.NESTTL18: self.nest_river_passage_entrance,

            locationName.NESTTL23: self.enter_tdl_train_station,
            locationName.NESTTL24: self.enter_tdl_train_station,
            locationName.NESTTL25: self.enter_tdl_train_station,
            locationName.NESTTL26: self.enter_tdl_train_station,

            locationName.NESTTL27: self.access_oogle_boogle,
            locationName.NESTTL28: self.access_oogle_boogle,
            locationName.NESTTL29: self.access_oogle_boogle,
            locationName.NESTTL30: self.access_oogle_boogle,

            locationName.NESTTL31: self.nest_mountain_flight_pad,
            locationName.NESTTL32: self.nest_mountain_flight_pad,
            locationName.NESTTL33: self.nest_mountain_underwater,
            locationName.NESTTL34: self.nest_mountain_underwater,

            locationName.NESTTL35: self.nest_river_passage,

            locationName.NESTTL42: self.nest_unga_egg,
            locationName.NESTTL43: self.nest_unga_egg,
            locationName.NESTTL44: self.nest_unga_egg,


            locationName.NESTTL45: self.nest_stomping_plains_footprint,
            locationName.NESTTL47: self.nest_stomping_plains_footprint,
            locationName.NESTTL48: self.nest_stomping_plains_footprint,
            locationName.NESTTL49: self.nest_stomping_plains_footprint,
            locationName.NESTTL50: self.nest_stomping_plains_footprint,
            locationName.NESTTL51: self.nest_stomping_plains_footprint,


            locationName.NESTGI4: self.nest_gi_outside_right,
            locationName.NESTGI5: self.nest_gi_outside_left,

            locationName.NESTGI6: self.nest_gi_floor1_top_pipe,
            locationName.NESTGI7: self.nest_gi_floor1_high_pipe,
            locationName.NESTGI8: self.nest_gi_outside_waste_disposal,
            locationName.NESTGI9: self.nest_gi_outside_waste_disposal,
            locationName.NESTGI10: self.nest_gi_floor1_high_pipe,
            locationName.NESTGI11: self.nest_outside_trash_compactor,

            locationName.NESTGI13: self.nest_gi_train_station_small_box,
            locationName.NESTGI14: self.nest_gi_train_station_medium_box,

            locationName.NESTGI17: self.nest_trash_compactor,
            locationName.NESTGI18: self.nest_trash_compactor,

            locationName.NESTGI19: self.nest_elevator_shaft_floor2,
            locationName.NESTGI20: self.nest_elevator_shaft_floor3,
            locationName.NESTGI21: self.nest_elevator_shaft_floor4,

            locationName.NESTGI23: self.nest_funny_platform,
            locationName.NESTGI26: self.cheato_window,
            locationName.NESTGI27: self.nest_funny_platform,
            locationName.NESTGI28: self.nest_funny_platform,
            locationName.NESTGI29: self.nest_funny_platform,
            locationName.NESTGI30: self.nest_funny_platform,
            locationName.NESTGI31: self.nest_gi_unscrewable_platform,

            locationName.NESTGI33: self.nest_magnet,
            locationName.NESTGI34: self.nest_magnet,

            locationName.NESTGI35: self.nest_floor3_high_box,
            locationName.NESTGI36: self.nest_floor3_under_notes_boxes,
            locationName.NESTGI37: self.nest_floor3_shortcut,
            locationName.NESTGI38: self.nest_floor3_corner_box,
            locationName.NESTGI39: self.nest_floor3_feather,
            locationName.NESTGI40: self.nest_floor3_feather,

            locationName.NESTGI43: self.nest_floor4_front,
            locationName.NESTGI44: self.nest_floor4_front,
            locationName.NESTGI45: self.nest_floor4_front,
            locationName.NESTGI46: self.nest_floor4_front,
            locationName.NESTGI49: self.nest_outside_QC,

            locationName.NESTGI50: self.nest_quality_control,
            locationName.NESTGI51: self.nest_quality_control,
            locationName.NESTGI52: self.nest_quality_control,

            locationName.NESTGI53: self.nest_floor5_small_stack,

            locationName.NESTGI56: self.nest_outside_repair_depot,
            locationName.NESTGI57: self.nest_egg_fan_easy,
            locationName.NESTGI58: self.nest_egg_fan_easy,
            locationName.NESTGI59: self.nest_egg_fan_hard,
            locationName.NESTGI60: self.nest_outside_repair_depot,

            locationName.NESTGI61: self.can_beat_weldar,
            locationName.NESTGI62: self.can_beat_weldar,

            locationName.NESTGI63: self.nest_waste_disposal_water_pump,
            locationName.NESTGI64: self.jinjo_waste_disposal,
            locationName.NESTGI65: self.jinjo_waste_disposal,
            locationName.NESTGI66: self.nest_waste_disposal_water_pump,

            locationName.NESTGI67: self.jiggy_clinkers,
            locationName.NESTGI68: self.jiggy_clinkers,
            locationName.NESTGI69: self.jiggy_clinkers,
            locationName.NESTGI70: self.jiggy_clinkers,
            locationName.NESTGI71: self.jiggy_clinkers,
            locationName.NESTGI72: self.jiggy_clinkers,
            locationName.NESTGI73: self.jiggy_clinkers,
            locationName.NESTGI74: self.jiggy_clinkers,

            locationName.NESTGI75: self.nest_clinkers_lobby,
            locationName.NESTGI76: self.nest_clinkers_lobby,
            locationName.NESTGI77: self.nest_clinkers_lobby,
            locationName.NESTGI78: self.nest_clinkers_lobby,


            locationName.NESTHP1: self.tswitch_lavaside,
            locationName.NESTHP9: self.nest_hfp_entrance_shelter,
            locationName.NESTHP10: self.hfp_top,
            locationName.NESTHP11: self.hfp_top,

            locationName.NESTHP12: self.nest_ice_cube,
            locationName.NESTHP13: self.nest_ice_cube,
            locationName.NESTHP14: self.nest_ice_cube,
            locationName.NESTHP15: self.nest_ice_cube,
            locationName.NESTHP16: self.nest_ice_cube,
            locationName.NESTHP17: self.nest_ice_cube,
            locationName.NESTHP18: self.nest_ice_cube,

            locationName.NESTHP19: self.hfp_top,
            locationName.NESTHP20: self.hfp_top,

            locationName.NESTHP21: self.nest_icy_side_train_station_easy,
            locationName.NESTHP22: self.nest_icy_side_train_station_hard,

            locationName.NESTHP23: self.nest_chilli_billi_crater,

            locationName.NESTHP24: self.nest_chilly_willy,

            locationName.NESTHP25: self.nest_hfp_kickball_egg,
            locationName.NESTHP26: self.nest_hfp_kickball_egg,
            locationName.NESTHP27: self.nest_hfp_kickball_egg,
            locationName.NESTHP28: self.nest_hfp_kickball_egg,
            locationName.NESTHP29: self.nest_hfp_kickball_feather,
            locationName.NESTHP30: self.nest_hfp_kickball_feather,

            locationName.NESTHP31: self.nest_ice_cube,
            locationName.NESTHP32: self.nest_ice_cube,
            locationName.NESTHP33: self.nest_ice_cube,
            locationName.NESTHP34: self.nest_hfp_spring_pad,
            locationName.NESTHP35: self.nest_icicle_grotto_top,
            locationName.NESTHP36: self.nest_icicle_grotto_top,

            locationName.NESTHP39: self.hfp_top,
            locationName.NESTHP40: self.hfp_top,


            locationName.NESTCC1: self.nest_ccl_flight,
            locationName.NESTCC2: self.nest_ccl_flight,
            locationName.NESTCC3: self.nest_ccl_flight,
            locationName.NESTCC4: self.nest_ccl_flight,
            locationName.NESTCC8: self.nest_jelly_castle,
            locationName.NESTCC9: self.nest_jelly_castle,
            locationName.NESTCC10: self.nest_jelly_castle,
            locationName.NESTCC11: self.nest_jelly_castle,
            locationName.NESTCC12: self.nest_ccl_dippy,
            locationName.NESTCC13: self.nest_ccl_dippy,
            locationName.NESTCC14: self.nest_ccl_dippy,
            locationName.NESTCC15: self.nest_ccl_dippy,
            locationName.NESTCC16: self.nest_ccl_flight,
            locationName.NESTCC17: self.nest_ccl_flight,
            locationName.NESTCC18: self.nest_ccl_flight,
            locationName.NESTCC19: self.nest_ccl_flight,

            locationName.NESTCC25: self.nest_outside_trash_can,
            locationName.NESTCC26: self.nest_outside_trash_can,
            locationName.NESTCC27: self.nest_outside_trash_can,
            locationName.NESTCC28: self.nest_outside_trash_can,

            locationName.NESTCC34: self.bill_drill,
            locationName.NESTCC35: self.bill_drill,

            locationName.NESTCC36: self.nest_inside_trash_can,
            locationName.NESTCC37: self.nest_inside_trash_can,

            locationName.NESTCC38: self.flight_pad,
            locationName.NESTCC39: self.flight_pad,

            locationName.NESTCC42: self.nest_ccl_flight,
            locationName.NESTCC43: self.nest_ccl_flight,
            locationName.NESTCC44: self.nest_near_superstash,
            locationName.NESTCC45: self.nest_near_superstash,

            locationName.NESTCC47: self.nest_pot_of_gold,
            locationName.NESTCC48: self.nest_pot_of_gold,
        }

        self.signpost_rules = {
            locationName.SIGNIH3: self.signpost_jiggywiggy_back,
            locationName.SIGNIH4: self.signpost_jiggywiggy_back,
            locationName.SIGNIH5: self.signpost_jiggywiggy_back,

            locationName.SIGNMT3: self.signpost_pillars,

            locationName.SIGNMT7: self.signpost_code_chamber,

            locationName.SIGNGM1: self.signpost_gloomy_cavern,
            locationName.SIGNGM4: self.signpost_chuffy,

            locationName.SIGNWW6: self.signpost_pump_master,
            locationName.SIGNWW7: self.signpost_gobi,

            locationName.SIGNJR3: self.signpost_smugglers,
            locationName.SIGNJR4: self.signpost_jrl_pipes,

            locationName.SIGNTL1: self.notes_roar_cage,
            locationName.SIGNTL2: self.signpost_trex,
            locationName.SIGNTL3: self.signpost_mountain_top,
            locationName.SIGNTL4: self.signpost_river_passage,

            locationName.SIGNGI1: self.signpost_gi_outside,
            locationName.SIGNGI3: self.signpost_elevator_shaft,
            locationName.SIGNGI4: self.signpost_elevator_shaft,

            locationName.SIGNHP2: self.hfp_top,
            locationName.SIGNHP3: self.jiggy_volcano,
            locationName.SIGNHP4: self.jiggy_volcano,
            locationName.SIGNHP5: self.jiggy_volcano,

            locationName.SIGNCC1: self.signpost_ccl_underwater,
            locationName.SIGNCC2: self.can_access_sack_pack_silo,
            locationName.SIGNCC3: self.signpost_pool_rim,
        }

        self.warp_pad_rules = {
            locationName.WARPGM2: self.warp_pad_ggm_mumbo,
            locationName.WARPGM3: self.warp_pad_ggm_wumba,
            locationName.WARPWW4: self.warp_pad_ww_wumba,
            locationName.WARPTL3: self.warp_pad_tdl_mumbo,
            locationName.WARPTL4: self.warp_pad_tdl_wumba,
            locationName.WARPGI1: self.warp_pad_floor_1,
            locationName.WARPGI4: self.warp_pad_floor_4,
            locationName.WARPHP2: self.hfp_top,
            locationName.WARPHP3: self.hfp_top,
            locationName.WARPHP4: self.hfp_top,
            locationName.WARPHP5: self.warp_pad_icicle_grotto,
            locationName.WARPCK2: self.warp_pad_ck_top,
        }

        if self.world.options.randomize_tickets.value:
            self.big_top_tickets_rules = {
                locationName.BTTICK1: self.can_kill_fruity,
                locationName.BTTICK2: self.can_kill_fruity,
                locationName.BTTICK3: self.can_kill_fruity,
                locationName.BTTICK4: self.can_kill_fruity,
            }

        if self.world.options.randomize_beans.value:
            self.beans_rules = {
                locationName.BEANCC1: self.bill_drill,
                locationName.BEANCC2: self.bill_drill
            }

    def has_green_relics(self, state: CollectionState, amt) -> bool:
        if self.world.options.randomize_green_relics.value:
            return state.has(itemName.GRRELIC, self.player, amt)
        else:
            return True

    def jiggy_targitzan(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.blue_eggs_item(state) or self.fire_eggs_item(state) or self.grenade_eggs_item(state)
        else:
            return (self.blue_eggs_item(state) or self.fire_eggs_item(state))\
                   or (self.ice_eggs_item(state) and self.beak_bayonet(state))\
                   or (self.grenade_eggs_item(state) and (self.ice_eggs_item(state) or self.beak_bayonet(state)))

    def jiggy_sschamber(self, state: CollectionState) -> bool:
        return self.has_green_relics(state, 10)

    def jiggy_mayahem_kickball(self, state: CollectionState) -> bool:
        return self.humbaMT(state)

    def jiggy_bovina(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.egg_aim(state) and (self.has_linear_egg(state))
        elif self.easy_tricks_logic(state):
            return self.egg_aim(state) or (self.MT_flight_pad(state) and self.airborne_egg_aiming(state))
        else:
            return (self.egg_aim(state) or (self.MT_flight_pad(state) and self.airborne_egg_aiming(state)))\
                   or (self.flap_flip(state) and self.beak_buster(state))\
                   or self.MT_flight_pad(state) and self.beak_bomb(state)

    def jiggy_treasure_chamber(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.egg_aim(state) and\
                (self.flap_flip(state) or self.slightly_elevated_ledge(state)) and\
                  ((self.grip_grab(state) and self.spring_pad(state) and self.flap_flip(state) and self.talon_trot(state)) or self.MT_flight_pad(state))
        else:
            return (self.flap_flip(state)
                       or self.tall_jump(state) and (self.grip_grab(state) or self.beak_buster(state))
                       or self.talon_trot(state) and self.flutter(state) and (self.grip_grab(state) or self.beak_buster(state))
                   )\
                   and ((self.grip_grab(state) and self.spring_pad(state) and self.flap_flip(state) and self.egg_aim(state) and self.talon_trot(state))
                       or (self.MT_flight_pad(state) and self.can_shoot_any_egg(state))
                       or state.can_reach_region(regionName.TL_HATCH, self.player))\
                   and (self.MT_flight_pad(state) and self.can_shoot_any_egg(state) or self.egg_aim(state))

    def jiggy_golden_goliath(self, state: CollectionState) -> bool:
        if self.glitches_logic(state):
            return state.has(itemName.MUMBOMT, self.player) or self.clockwork_eggs(state)
        else:
            return state.has(itemName.MUMBOMT, self.player)

    def jiggy_prison_quicksand(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.slightly_elevated_ledge(state)\
                  and self.stilt_stride(state) and self.prison_compound_as_banjo(state) and self.tall_jump(state)
        else:
            return self.slightly_elevated_ledge(state)\
                 and self.stilt_stride(state) and self.prison_compound_as_banjo(state)

    def jiggy_pillars(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.bill_drill(state) and (self.dive(state) or self.slightly_elevated_ledge(state) and self.tall_jump(state))\
                    and self.small_elevation(state) and self.prison_compound_as_banjo(state)
        elif self.easy_tricks_logic(state):
            return self.bill_drill(state) and self.small_elevation(state) and self.prison_compound_as_banjo(state)\
                    and (self.dive(state) or self.slightly_elevated_ledge(state) or self.beak_buster(state))
        else:
            return self.prison_compound_as_banjo(state) and \
               ((self.bill_drill(state) and self.small_elevation(state)) or self.extremelyLongJump(state) or self.clockwork_shot(state))\
                   and (self.dive(state) or self.slightly_elevated_ledge(state) or self.beak_buster(state))

    def jiggy_top(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.talon_trot(state) or self.MT_flight_pad(state)
        elif self.easy_tricks_logic(state):
            return self.talon_trot(state) or self.MT_flight_pad(state) or self.flap_flip(state)
        else:
            return True

    def jiggy_ssslumber(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.talon_trot(state) and self.grip_grab(state) and self.flap_flip(state)
        else:
            return self.talon_trot(state) and (self.grip_grab(state) or self.beak_buster(state))\
               and self.flap_flip(state)

    def jiggy_generator_cavern(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.fire_eggs(state) and self.egg_aim(state)\
                   and self.long_jump(state) and (self.flap_flip(state) or self.talon_trot(state))
        elif self.easy_tricks_logic(state):
            return (self.long_jump(state) and (self.flap_flip(state) or self.talon_trot(state)) and (self.has_fire(state) or self.bill_drill(state)))\
                or self.flap_flip(state) and self.beak_buster(state) and self.climb(state)\
                or self.ggm_boulders(state) and self.leg_spring(state) and self.fire_eggs(state)\
                or self.ggm_boulders(state) and self.tall_jump(state) and self.pack_whack(state) and self.climb(state)
        else:
            return self.long_jump(state) and (self.flap_flip(state) or self.talon_trot(state))\
                or self.flap_flip(state) and self.beak_buster(state)\
                or self.clockwork_shot(state)\
                or self.ggm_boulders(state) and self.tall_jump(state) and self.pack_whack(state) and self.climb(state)\
                or self.ggm_boulders(state) and self.leg_spring(state)\
                or self.beak_buster(state) and self.grip_grab(state)

    def jiggy_waterfall_cavern(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return (self.grip_grab(state) or self.small_elevation(state)) and self.reach_waterfall_cavern_gate(state)
        else:
            return self.reach_waterfall_cavern_gate(state)

    def jiggy_ordnance_storage(self, state: CollectionState) -> bool:
        return self.breegull_blaster(state) and self.beak_bayonet(state) and \
               self.ggm_boulders(state)

    def jiggy_crushing_shed(self, state: CollectionState) -> bool:
        return self.mumboGGM(state) and self.beak_barge(state)

    def jiggy_waterfall(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.springy_step_shoes(state)
        elif self.easy_tricks_logic(state):
            return self.springy_step_shoes(state) or \
                    (self.glide(state)
                    or self.wing_whack(state) and (self.tall_jump(state) or self.leg_spring(state))) and self.ggm_boulders(state)
        else:
            return self.springy_step_shoes(state) or \
                   (self.glide(state)
                   or self.wing_whack(state) and (self.tall_jump(state) or self.leg_spring(state))) and self.ggm_boulders(state)\
                   or self.clockwork_shot(state)

    def jiggy_power_hut(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.ggm_boulders(state) and self.split_up(state) and self.climb(state)
        elif self.easy_tricks_logic(state):
            return self.ggm_boulders(state) and\
                    ((self.split_up(state) and self.climb(state)) or self.has_fire(state) or self.bill_drill(state))
        else:
            return self.ggm_boulders(state)

    def jiggy_flooded_caves(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.humbaGGM(state) and self.dive(state) and (self.tall_jump(state) or self.grip_grab(state))
        elif self.easy_tricks_logic(state):
            return self.dive(state) and (self.tall_jump(state) or self.grip_grab(state) or self.beak_buster(state))\
                    and (self.humbaGGM(state)
                        or self.reach_waterfall_cavern_gate(state) and (
                            self.talon_trot(state) and (self.flutter(state) or self.air_rat_a_tat_rap(state))
                            or self.roll(state) and self.tall_jump(state) and (self.flutter(state) or self.air_rat_a_tat_rap(state))
                        )
                    )
        else:
            return self.dive(state) and (self.tall_jump(state) or self.grip_grab(state) or self.beak_buster(state) or self.clockwork_shot(state))\
                   and (self.humbaGGM(state)
                       or self.reach_waterfall_cavern_gate(state) and (
                           self.talon_trot(state) and (self.flutter(state) or self.air_rat_a_tat_rap(state))
                           or self.roll(state) and self.tall_jump(state) and (self.flutter(state) or self.air_rat_a_tat_rap(state))
                       )
                   )

    def reach_waterfall_cavern_gate(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.turbo_trainers(state)
        else:
            return self.ggm_trot(state)\
               or self.ggm_boulders(state) and self.split_up(state)\
               or state.has(itemName.WARPGM1, self.player) and state.has(itemName.WARPGM5, self.player)
    def jiggy_hoop_hurry(self, state: CollectionState) -> bool:
        # Solo Kazooie can get the jiggy with the spring pad.
        if self.intended_logic(state):
            return self.split_up(state) and self.has_explosives(state) and self.turbo_trainers(state)\
               and self.spring_pad(state) and (self.flap_flip(state) or self.leg_spring(state))
        else:
            return self.split_up(state) and self.has_explosives(state)\
               and (self.leg_spring(state) or self.tall_jump(state))\
               and (self.spring_pad(state) or self.flap_flip(state) or self.leg_spring(state))

    def jiggy_dodgem(self, state: CollectionState) -> bool:
        if self.glitches_logic(state):
            return self.mumboWW(state) and self.escape_inferno_as_mumbo(state)
        else:
            return self.mumboWW(state)

    # I assume nobody wants to do this from the ground.
    def jiggy_patches(self, state: CollectionState) -> bool:
        return self.airborne_egg_aiming(state) and self.egg_aim(state) and \
               self.grenade_eggs(state) and self.flight_pad(state)

    def jiggy_peril(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.humbaGGM(state) and \
                    self.mumboWW(state) and \
                    self.saucer_door_open(state) and \
                    self.can_reach_saucer(state) and\
                    state.can_reach_region(regionName.GM, self.player) and self.has_explosives(state)
        else:
            return self.humbaGGM(state) and \
                   self.mumboWW(state) and \
                   self.saucer_door_open(state) and state.can_reach_region(regionName.GM, self.player) and \
                   self.can_reach_saucer(state) and\
                   self.has_explosives(state)

    def jiggy_balloon_burst(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.split_up(state) and self.has_explosives(state) and self.airborne_egg_aiming(state)\
                and self.spring_pad(state) and (self.flap_flip(state) or self.leg_spring(state))
        else:
            return self.split_up(state) and self.has_explosives(state) and self.airborne_egg_aiming(state)\
               and (self.leg_spring(state) or self.tall_jump(state))\
               and (self.spring_pad(state) or self.flap_flip(state) or self.leg_spring(state))

    def jiggy_dive_of_death(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.grip_grab(state) and self.climb(state) and self.flap_flip(state)
        elif self.easy_tricks_logic(state):
            return self.climb(state) and (self.flap_flip(state) or self.talon_trot(state) or (
                self.tall_jump(state) and (self.beak_buster(state) or self.air_rat_a_tat_rap(state))))
        else:
            return self.climb(state) and (self.flap_flip(state) or self.talon_trot(state) or self.clockwork_shot(state) or (
               self.tall_jump(state) and (self.beak_buster(state) or self.air_rat_a_tat_rap(state))))

    def jiggy_mrs_boggy(self, state: CollectionState) -> bool:
        return self.moggy(state) and self.soggy(state) and self.groggy(state)

    def moggy(self, state: CollectionState) -> bool:
        if self.intended_logic(state) or self.easy_tricks_logic(state):
            return self.mumboWW(state) and \
               self.has_explosives(state)
        else:
            return self.mumboWW(state) and \
                ((self.split_up(state) and self.spring_pad(state)) or self.leg_spring(state) or self.glide(state) or self.has_explosives(state))

    def soggy(self, state: CollectionState) -> bool:
        return state.can_reach_region(regionName.WWI, self.player)

    def groggy(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return state.can_reach_region(regionName.WWI, self.player) and \
                   self.taxi_pack(state) and \
                   self.spring_pad(state)

        elif self.easy_tricks_logic(state):
            return state.can_reach_region(regionName.WWI, self.player) and \
                   self.taxi_pack(state) and \
                   (self.spring_pad(state) or self.leg_spring(state) or self.glide(state))
        else:
            return state.can_reach_region(regionName.WWI, self.player) and \
                   self.taxi_pack(state)\
                   and (self.spring_pad(state) or self.leg_spring(state) or self.glide(state))

    def jiggy_star_spinner(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.mumboWW(state) and self.talon_trot(state)
        elif self.easy_tricks_logic(state):
            return self.mumboWW(state) and (
                        self.talon_trot(state)
                        or self.leg_spring(state)
                        or self.turbo_trainers(state)
                    )
        else:
            return self.mumboWW(state)

    def jiggy_inferno(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.split_up(state) and self.tall_jump(state)
        elif self.easy_tricks_logic(state):
            return self.split_up(state) and (self.tall_jump(state) or self.leg_spring(state))\
                    or self.flap_flip(state) and (self.talon_trot(state) or self.turbo_trainers(state))
        else:
            return self.split_up(state)\
                   or self.flap_flip(state) and (self.talon_trot(state) or self.turbo_trainers(state))

    def jiggy_cactus(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.bill_drill(state) and self.grenade_eggs(state)\
                  and self.beak_buster(state) and self.climb(state)
        elif self.easy_tricks_logic(state):
            return self.bill_drill(state) and self.grenade_eggs(state)\
                  and self.beak_buster(state) and\
                    (self.climb(state) or self.leg_spring(state) and self.glide(state))
        else:
            return self.bill_drill(state) and self.grenade_eggs(state)\
                 and self.beak_buster(state) and\
                   (self.clockwork_shot(state) or self.climb(state) or self.leg_spring(state) and self.glide(state))

    def jiggy_sub_challenge(self, state: CollectionState) -> bool:
        return self.humbaJRL(state)

    def jiggy_tiptup(self, state: CollectionState) -> bool:
        return self.hatch(state) and self.has_explosives(state)

    # I assume nobody wants to do this with clockworks (is it even possible?) or talon torpedo
    def jiggy_bacon(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.sub_aqua_egg_aiming(state) and self.has_linear_egg(state) and state.has(itemName.MUMBOJR, self.player)
        elif self.easy_tricks_logic(state):
            return self.sub_aqua_egg_aiming(state) and self.has_linear_egg(state)\
                        and (state.has(itemName.MUMBOJR, self.player) or self.doubleAir(state))
        else:
            return (self.sub_aqua_egg_aiming(state) and self.has_linear_egg(state)) or \
               (self.humbaJRL(state) and self.egg_aim(state) and self.has_linear_egg(state))

    def jiggy_pig_pool(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.HFP_hot_water_cooled(state)\
                    and self.jrl_waste_disposal(state)\
                    and self.flap_flip(state)\
                    and (self.has_explosives(state) or self.beak_barge(state))
        elif self.easy_tricks_logic(state):
            return self.HFP_hot_water_cooled(state)\
                    and self.jrl_waste_disposal(state)\
                    and (self.flap_flip(state)
                        or self.tall_jump(state) and self.beak_buster(state)
                        or self.talon_trot(state) and self.flutter(state) and self.beak_buster(state)
                    )\
                    and (self.has_explosives(state)
                        or self.beak_barge(state)
                        or self.dragon_kazooie(state) and self.ground_rat_a_tat_rap(state)
                    )
        else:
            return self.HFP_hot_water_cooled(state)\
                   and self.jrl_waste_disposal(state)\
                   and ((self.flap_flip(state)
                       or self.tall_jump(state) and self.beak_buster(state)
                       or self.talon_trot(state) and self.flutter(state) and self.beak_buster(state)
                       or self.tall_jump(state) and self.flutter(state)
                       or self.extremelyLongJump(state)
                       ) and (
                           self.has_explosives(state)
                           or self.beak_barge(state)
                           or self.dragon_kazooie(state) and self.ground_rat_a_tat_rap(state)
                       )
                       or self.clockwork_shot(state)
                   )

    def jiggy_smuggler(self, state: CollectionState) -> bool:
        if self.intended_logic(state) or self.easy_tricks_logic(state):
            return self.has_explosives(state) and \
                    self.split_up(state) and self.glide(state)
        else:
            return self.has_explosives(state) and \
                     self.split_up(state) and self.glide(state)\
                     or self.clockwork_shot(state)

    def jiggy_merry_maggie(self, state: CollectionState) -> bool:
        if self.intended_logic(state) or self.easy_tricks_logic(state):
            return self.sub_aqua_egg_aiming(state) and self.has_linear_egg(state)
        else:
            return (self.sub_aqua_egg_aiming(state) or self.egg_aim(state)) and self.has_linear_egg(state)

    def jiggy_lord_woo(self, state: CollectionState) -> bool:
        if self.intended_logic(state) or self.easy_tricks_logic(state):
            return state.can_reach_region(regionName.JR, self.player) and (
                       self.sub_aqua_egg_aiming(state) and self.grenade_eggs(state)
                       and (self.humbaJRL(state) or state.has(itemName.MUMBOJR, self.player))
                   )
        else:
            return self.grenade_eggs(state) and self.sub_aqua_egg_aiming(state) and (
                        self.talon_torpedo(state) and self.doubleAir(state)
                        or state.can_reach_region(regionName.JR, self.player)
                        and (self.humbaJRL(state) or state.has(itemName.MUMBOJR, self.player))
                    )

    def jiggy_see_mee(self, state: CollectionState) -> bool:
        return self.talon_torpedo(state)

    def jiggy_pawno(self, state: CollectionState) -> bool:
        if self.intended_logic(state) or self.easy_tricks_logic(state):
            return state.has(itemName.DOUBLOON, self.player, 23) and self.small_elevation(state)
        else:
            return state.has(itemName.DOUBLOON, self.player, 23) and (self.small_elevation(state) or self.clockwork_shot(state))

    def jiggy_ufo(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return state.has(itemName.MUMBOJR, self.player) and self.talon_torpedo(state) and \
                    self.egg_aim(state) and self.ice_eggs(state)
        elif self.easy_tricks_logic(state):
            return self.talon_torpedo(state) and self.egg_aim(state) and \
                    self.ice_eggs(state)
        else:
            return self.talon_torpedo(state) and self.ice_eggs(state)\
                 and (self.talon_trot(state) or self.egg_aim(state))

    def jiggy_terry_nest(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.can_beat_terry(state) and (self.has_explosives(state) or
                    self.bill_drill(state))
        else:
            return (self.has_explosives(state) or self.bill_drill(state)) and self.can_beat_terry(state)

    def jiggy_dippy(self, state: CollectionState) -> bool:
        if self.intended_logic(state) or self.easy_tricks_logic(state):
            return self.talon_torpedo(state) and state.can_reach_region(regionName.CC, self.player) and self.dive(state)
        else:
            return self.talon_torpedo(state) and state.can_reach_region(regionName.CC, self.player)

    def scrit(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.mumboTDL(state) and self.bill_drill(state) and self.tall_jump(state)
        else:
            return self.mumboTDL(state) and self.bill_drill(state)

    def scrat(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.can_beat_king_coal(state) and state.has(itemName.TRAINSWIH, self.player) and state.has(itemName.TRAINSWTD, self.player)\
                    and self.taxi_pack(state) and state.has(itemName.MUMBOIH, self.player) and (self.tall_jump(state) or self.talon_trot(state))\
                    and self.train_raised(state)
        else:
            return self.can_beat_king_coal(state) and state.has(itemName.TRAINSWIH, self.player) and state.has(itemName.TRAINSWTD, self.player)\
                   and self.taxi_pack(state) and state.has(itemName.MUMBOIH, self.player) and self.train_raised(state)

    # You don't even need to go in the styrac cave for that one.
    def scrut(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.can_beat_king_coal(state) and state.has(itemName.TRAINSWTD, self.player) and state.has(itemName.TRAINSWWW, self.player)\
                    and self.train_raised(state) and self.grenade_eggs(state) and self.egg_aim(state)
        else:
            return self.can_beat_king_coal(state) and state.has(itemName.TRAINSWTD, self.player) and state.has(itemName.TRAINSWWW, self.player)\
                   and self.train_raised(state) and self.grenade_eggs(state)

    def jiggy_scrotty(self, state: CollectionState) -> bool:
        return self.scrit(state) and self.scrat(state) and self.scrut(state)

    def jiggy_oogle_boogle(self, state: CollectionState) -> bool:
        logic = True
        if self.intended_logic(state):
            logic = self.access_oogle_boogle(state) and self.fire_eggs(state) and \
                    self.smuggle_food(state) and self.grip_grab(state) and \
                    self.bill_drill(state) and self.spring_pad(state)
        elif self.easy_tricks_logic(state):
            logic = self.access_oogle_boogle(state) and self.has_fire(state) and \
                    self.smuggle_food(state) and self.grip_grab(state) and \
                    self.bill_drill(state) and self.spring_pad(state)
        elif self.hard_tricks_logic(state):
            logic = self.access_oogle_boogle(state) and self.has_fire(state) and \
                    self.grip_grab(state) and self.bill_drill(state) and self.smuggle_food(state)\
                    and self.spring_pad(state)
        elif self.glitches_logic(state):
            logic = (self.access_oogle_boogle(state) or self.clockwork_warp(state))\
                    and self.has_fire(state) and self.grip_grab(state) and self.bill_drill(state) and self.smuggle_food(state) and self.spring_pad(state)
        return logic

    def jiggy_chompa(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.breegull_blaster(state) and (
                (self.tall_jump(state) or self.grip_grab(state)) and self.flight_pad(state)
                 or (self.egg_aim(state) and self.has_explosives(state) and self.springy_step_shoes(state))
            )
        else:
            return self.breegull_blaster(state) and (
               (self.tall_jump(state) or self.grip_grab(state) or self.beak_buster(state)) and self.flight_pad(state)
                or (self.egg_aim(state) and self.has_explosives(state) and self.springy_step_shoes(state))
                or (self.springy_step_shoes(state) and self.very_long_jump(state))
            )

    def jiggy_terry_kids(self, state: CollectionState) -> bool:
        return self.can_beat_terry(state) and self.hatch(state) and \
               self.taxi_pack(state) and self.access_oogle_boogle(state)\
               and self.flight_pad(state) and self.climb(state) and self.spring_pad(state)

    def jiggy_stomping_plains(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.talon_trot(state)
        elif self.easy_tricks_logic(state):
            return self.talon_trot(state)\
                    or self.split_up(state) and self.snooze_pack(state) and self.tall_jump(state)
        else:
            return self.tall_jump(state) or self.talon_trot(state)\
                   or self.split_up(state) and self.snooze_pack(state) and self.tall_jump(state)

    def can_cross_bonfire_cavern(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.ice_eggs(state) and self.long_jump(state)
        elif self.easy_tricks_logic(state):
            return (self.ice_eggs(state)) and self.long_jump(state)
        else:
            return (self.long_jump(state) or self.talon_trot(state))

    def jiggy_rocknuts(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.egg_aim(state) and self.clockwork_eggs(state) and self.long_jump(state) and self.tall_jump(state)
        elif self.easy_tricks_logic(state):
            return self.egg_aim(state) and self.clockwork_eggs(state) and self.long_jump(state)
        else:
            return self.clockwork_eggs(state) and ((self.egg_aim(state) and self.long_jump(state)) or self.very_long_jump(state))

    def jiggy_roar_cage(self, state: CollectionState) -> bool:
        if self.glitches_logic(state):
            return self.humbaTDL(state) and self.roar(state)\
                    or self.clockwork_shot(state) and (self.springy_step_shoes(state) or self.long_jump(state) or self.split_up(state))
        else:
            return self.humbaTDL(state) and self.roar(state)

    def jiggy_skivvy(self, state: CollectionState) -> bool:
        return self.skivvy_worker_quarters(state) and self.skivvy_worker_quarters(state) \
               and self.skivvy_floor_1(state) and self.skivvy_floor_2(state) \
               and self.skivvy_floor_3(state) and self.skivvy_floor_5(state)

    def floor_2_skivvy_switch(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return state.can_reach_region(regionName.GI2, self.player) and self.claw_clamber_boots(state) and self.flap_flip(state) and self.grip_grab(state)
        else:
            return state.can_reach_region(regionName.GI2, self.player) and self.claw_clamber_boots(state)\
                       and ((self.flap_flip(state) and self.grip_grab(state))
                            or self.talon_trot(state) and (self.flutter(state) or self.air_rat_a_tat_rap(state)))\
                   or state.can_reach_region(regionName.GI2, self.player) and self.floor_2_split_up(state)\
                       and (self.leg_spring(state) or self.claw_clamber_boots(state) and (self.can_shoot_any_egg(state) or self.wing_whack(state)))\
                   or state.can_reach_region(regionName.GI3, self.player) and\
                       (self.climb(state) and (self.very_long_jump(state) or (self.flap_flip(state) or self.tall_jump(state)) and self.grip_grab(state))
                           or self.small_elevation(state) and self.split_up(state) and self.leg_spring(state))

    def skivvy_worker_quarters(self, state: CollectionState) -> bool:
        return self.humbaGI(state)

    def skivvy_outside(self, state: CollectionState) -> bool:
        return self.humbaGI(state)

    def skivvy_floor_1(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.humbaGI(state) and self.bill_drill(state)\
                    and state.can_reach_region(regionName.GIF, self.player) and (self.airborne_egg_aiming(state) or self.beak_bomb(state))
        else:
            return self.humbaGI(state) and self.bill_drill(state)\
                   and state.can_reach_region(regionName.GIF, self.player) and (self.airborne_egg_aiming(state) or self.beak_bomb(state)
                   or self.egg_aim(state))

    def skivvy_floor_2(self, state: CollectionState) -> bool:
        return self.humbaGI(state) and self.floor_2_skivvy_switch(state)

    def skivvy_floor_3(self, state: CollectionState) -> bool:
        return self.humbaGI(state)

    def skivvy_floor_5(self, state: CollectionState) -> bool:
        return self.humbaGI(state)

    def jiggy_floor5(self, state: CollectionState) -> bool:
        if self.intended_logic(state) or self.easy_tricks_logic(state):
            return self.split_up(state)
        else:
            return self.split_up(state) or self.clockwork_shot(state)

    def jiggy_quality_control(self, state: CollectionState) -> bool:
        logic = True
        if self.intended_logic(state):
            logic = self.grenade_eggs(state) and \
                    self.egg_aim(state) and \
                    self.can_use_battery(state) and self.humbaGI(state)\
                    and self.climb(state)
        elif self.easy_tricks_logic(state):
            logic = self.grenade_eggs(state) and \
                    (self.egg_aim(state) and self.humbaGI(state) or
                    self.leg_spring(state)) and self.can_use_battery(state) and self.climb(state)
        elif self.hard_tricks_logic(state):
            logic = self.grenade_eggs(state) and self.can_use_battery(state) and self.climb(state) and\
                    (self.tall_jump(state)
                        or self.leg_spring(state)
                        or self.humbaGI(state) and self.egg_aim(state)
                        or self.clockwork_shot(state))
        elif self.glitches_logic(state):
            logic = self.grenade_eggs(state) and self.can_use_battery(state) and self.climb(state) and\
                    (self.tall_jump(state)
                        or self.leg_spring(state)
                        or self.humbaGI(state) and self.egg_aim(state)
                        or self.clockwork_shot(state)
                        )\
                    or self.precise_clockwork_warp(state)
        return logic

    def jiggy_guarded(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.split_up(state) and self.claw_clamber_boots(state) and self.egg_aim(state) and\
                    (self.blue_eggs(state) or self.fire_eggs(state) or self.grenade_eggs(state))\
                    and (self.spring_pad(state) or self.wing_whack(state) or self.glide(state))\
                    and (self.tall_jump(state) or self.leg_spring(state))
        elif self.easy_tricks_logic(state):
            return self.split_up(state) and (self.tall_jump(state) or self.leg_spring(state)) and\
                    ((self.claw_clamber_boots(state) or state.can_reach_region(regionName.GI2, self.player)) and self.spring_pad(state)
                        or self.claw_clamber_boots(state) and (self.wing_whack(state) or self.glide(state)) and (self.egg_aim(state) or self.wing_whack(state))
                        or self.leg_spring(state) and self.glide(state) and (self.egg_aim(state) or self.wing_whack(state)))\
                    and (self.blue_eggs(state) or self.fire_eggs(state) or self.grenade_eggs(state))
        else:
            return self.split_up(state) and (self.tall_jump(state) or self.leg_spring(state)) and\
                   ((self.claw_clamber_boots(state) or state.can_reach_region(regionName.GI2, self.player)) and self.spring_pad(state)
                       or self.claw_clamber_boots(state) and (self.wing_whack(state) or self.glide(state)) and (self.egg_aim(state) or self.wing_whack(state))
                       or self.leg_spring(state) and self.glide(state) and (self.egg_aim(state) or self.wing_whack(state)))\
                   and (self.blue_eggs(state) or self.fire_eggs(state) or self.grenade_eggs(state))\
                   or (self.claw_clamber_boots(state) or state.can_reach_region(regionName.GI2, self.player)) and (self.spring_pad(state) or self.leg_spring(state)) and self.clockwork_shot(state)

    def jiggy_trash_compactor(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.snooze_pack(state)
        elif self.glitches_logic(state):
            return self.snooze_pack(state)\
                    or self.pack_whack(state) and self.tall_jump(state)\
                    or (self.egg_aim(state) and self.clockwork_eggs(state) and self.breegull_bash(state) and self.talon_trot(state))
        else:
            return self.snooze_pack(state) or self.pack_whack(state) and self.tall_jump(state)

    def jiggy_twinkly(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.can_use_battery(state) and self.grip_grab(state) and self.turbo_trainers(state)
        else:
            #Banjo to Boiler Plant
            #Solo Kazooie to boiler plant, otherwise turbo trainers to do the minigame as BK
            return self.can_use_battery(state) and (self.tall_jump(state) or self.grip_grab(state))\
                   and (self.leg_spring(state)
                       or (self.glide(state) or self.wing_whack(state)) and self.tall_jump(state)
                       or state.can_reach_region(regionName.GIF, self.player) and self.flight_to_boiler_plant(state)
                       or self.turbo_trainers(state))

    def jiggy_waste_disposal_box(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.sack_pack(state) and self.solo_banjo_waste_disposal(state)
        else:
            return self.solo_banjo_waste_disposal(state)

    def can_reach_hfp_ice_crater(self, state: CollectionState) -> bool:
        return self.claw_clamber_boots(state)

    def jiggy_dragons_bros(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.fire_eggs(state) and self.ice_eggs(state) and \
                   self.third_person_egg_shooting(state) and state.can_reach_region(regionName.HPIBOSS, self.player)\
                   and (self.tall_jump(state) or self.talon_trot(state))\
                   and self.climb(state)
        elif self.easy_tricks_logic(state):
            return self.fire_eggs(state) and self.ice_eggs(state) and \
                   state.can_reach_region(regionName.HPIBOSS, self.player) and self.third_person_egg_shooting(state)\
                   and (self.tall_jump(state) or self.talon_trot(state))\
                   and (self.climb(state)
                       or self.flap_flip(state)
                       or self.tall_jump(state) and self.grip_grab(state)
                       or self.talon_trot(state) and self.grip_grab(state))
        else:
            # In case people go for the damage boost for Chilly Willy then die before getting the jiggy, we also require Pack Whack to prevent softlocks.
            if self.world.options.randomize_boss_loading_zones.value:
                return self.fire_eggs(state) and self.ice_eggs(state) and state.can_reach_region(regionName.HPIBOSS, self.player) and \
                       self.third_person_egg_shooting(state)\
                       and (self.tall_jump(state) or self.talon_trot(state))\
                       and (self.climb(state)
                           or self.flap_flip(state)
                           or self.tall_jump(state) and self.grip_grab(state)
                           or self.talon_trot(state) and self.grip_grab(state)
                       )
            else:
                return self.fire_eggs(state) and self.ice_eggs(state) and self.flight_pad(state) and self.third_person_egg_shooting(state)\
                       and self.pack_whack(state)\
                       and (self.claw_clamber_boots(state)
                           or ((self.tall_jump(state) and self.roll(state) or self.talon_trot(state))
                               and (self.flutter(state) or self.air_rat_a_tat_rap(state))
                               and self.grip_grab(state)
                           )
                       )\
                       and (self.tall_jump(state) or self.talon_trot(state))\
                       and (self.climb(state)
                           or self.flap_flip(state)
                           or self.tall_jump(state) and self.grip_grab(state)
                           or self.talon_trot(state) and self.grip_grab(state)
                       )

    def jiggy_volcano(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.long_jump(state) and self.hfp_top(state)
        else:
            return self.hfp_top(state) and ((self.long_jump(state) or self.tall_jump(state)) or self.split_up(state))

    def jiggy_sabreman(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return state.has(itemName.MUMBOHP, self.player) and self.fire_eggs(state) and \
                    self.taxi_pack(state) and self.tall_jump(state) and self.hfp_top(state)
        else:
            return state.has(itemName.MUMBOHP, self.player) and self.has_fire(state) and \
                   self.taxi_pack(state) and self.tall_jump(state) and self.hfp_top(state)

    def jiggy_boggy(self, state: CollectionState) -> bool:
        if self.glitches_logic(state):
            return self.hfp_top(state) and \
                    (self.shack_pack(state)
                     or (self.clockwork_eggs(state) and self.third_person_egg_shooting(state) and (self.talon_trot(state) or self.flap_flip(state) or self.dive(state) and self.tall_jump(state)))
                     or self.leg_spring(state))
        else:
            return self.hfp_top(state) and self.shack_pack(state) and self.small_elevation(state)

    def jiggy_icy_side_station(self, state: CollectionState) -> bool:
        if self.hard_tricks_logic(state):
            return self.access_icy_side_train_station(state) and (self.climb(state) or self.clockwork_shot(state))
        elif self.glitches_logic(state):
            return self.access_icy_side_train_station(state) and (self.climb(state) or self.clockwork_shot(state))\
                    or (self.clockwork_shot(state) and self.small_elevation(state))
        else:
            return self.access_icy_side_train_station(state) and self.climb(state)

    def access_icy_side_train_station(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.can_beat_king_coal(state) and self.grenade_eggs(state) and \
                    state.has(itemName.TRAINSWHP1, self.player) and state.has(itemName.TRAINSWHP2, self.player) and \
                    self.egg_aim(state) and state.can_reach_region(regionName.WW, self.player)\
                    and self.beak_buster(state)\
                    and (self.claw_clamber_boots(state) or self.flight_pad(state))\
                    and self.train_raised(state) and state.can_reach_region(regionName.CHUFFY, self.player)
        else:
            return self.can_beat_king_coal(state) and self.grenade_eggs(state) and \
                   state.has(itemName.TRAINSWHP1, self.player) and state.has(itemName.TRAINSWHP2, self.player) and \
                   state.can_reach_region(regionName.WW, self.player) and self.beak_buster(state)\
                   and (self.claw_clamber_boots(state) or self.flight_pad(state))\
                   and self.train_raised(state) and state.can_reach_region(regionName.CHUFFY, self.player)

    def jiggy_oil_drill(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.humbaHFP(state) and \
                    self.shack_pack(state) and self.grip_grab(state)
        elif self.glitches_logic(state):
            return self.humbaHFP(state) and self.shack_pack(state) and \
                    (self.pack_whack(state) or self.grip_grab(state))
        else:
            return self.humbaHFP(state) and self.shack_pack(state) and \
                   (self.pack_whack(state) and self.tall_jump(state) or self.grip_grab(state))

    def jiggy_hfp_stomping(self, state: CollectionState) -> bool:
        if self.hard_tricks_logic(state):
            return self.tall_jump(state) and self.split_up(state)
        elif self.glitches_logic(state):
            return self.tall_jump(state) and self.split_up(state)\
                    or (state.can_reach_region(regionName.HP, self.player) and self.clockwork_shot(state)
                        and (self.talon_trot(state)
                            or self.split_up(state)
                            or self.leg_spring(state)
                            or self.flap_flip(state)))
        else:
            return self.snooze_pack(state) and self.tall_jump(state)

    def jiggy_hfp_kickball(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.humbaMT(state) and self.has_explosives(state)
        elif self.easy_tricks_logic(state):
            return self.humbaMT(state) and \
                    (self.has_explosives(state) or
                    state.has(itemName.MUMBOHP, self.player))
        else:
            return self.humbaMT(state) and \
                   (self.has_explosives(state) or state.has(itemName.MUMBOHP, self.player))

    def jiggy_aliens(self, state: CollectionState) -> bool:
        return self.alphette(state) and self.betette(state) and self.gamette(state)

    def alphette(self, state: CollectionState) -> bool:
        return state.can_reach_location(locationName.JIGGYJR10, self.player) and self.bill_drill(state) and state.has(itemName.MUMBOHP, self.player)

    def betette(self, state: CollectionState) -> bool:
        return state.can_reach_location(locationName.JIGGYJR10, self.player) and self.bill_drill(state) and state.has(itemName.MUMBOHP, self.player)

    def gamette(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return state.can_reach_location(locationName.JIGGYJR10, self.player) and self.hatch(state) and self.glide(state) and state.has(itemName.MUMBOHP, self.player)
        elif self.easy_tricks_logic(state):
            return state.can_reach_location(locationName.JIGGYJR10, self.player) and state.has(itemName.MUMBOHP, self.player) and \
                   self.hatch(state) and ((self.wing_whack(state) and self.tall_jump(state)) or self.glide(state))
        else:
            return state.can_reach_location(locationName.JIGGYJR10, self.player) and state.has(itemName.MUMBOHP, self.player) and \
                   self.hatch(state) and (self.wing_whack(state) or self.tall_jump(state) or self.glide(state))

    def jiggy_colosseum_split(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.split_up(state) and self.grip_grab(state) and self.climb(state)
        elif self.glitches_logic(state):
            return (self.split_up(state) and self.grip_grab(state)
                and (self.climb(state) or (self.pack_whack(state) and self.tall_jump(state))))\
                    or (self.clockwork_eggs(state) and self.split_up(state) and self.third_person_egg_shooting(state) and self.tall_jump(state))
        else:
            return self.split_up(state) and self.grip_grab(state)\
               and (self.climb(state) or (self.pack_whack(state) and self.tall_jump(state)))

    def jiggy_mingy(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return (self.can_shoot_linear_egg(state) or self.beak_barge(state) or self.air_rat_a_tat_rap(state) or self.wonderwing(state))\
                    and self.talon_trot(state)
        elif self.easy_tricks_logic(state):
            return self.can_shoot_linear_egg(state) or self.beak_barge(state) or self.air_rat_a_tat_rap(state) or self.wonderwing(state)
        else:
            return self.ground_attack(state)

    def jiggy_mr_fit(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.mr_fit_high_jump(state) and self.mr_fit_sack_race(state) and self.turbo_trainers(state)
        elif self.glitches_logic(state):
            return self.mr_fit_high_jump(state) and self.mr_fit_sack_race(state) and \
                    (self.turbo_trainers(state) or state.has(itemName.HUMBACC, self.player) or self.clockwork_eggs(state))
        else:
            return self.mr_fit_high_jump(state) and self.mr_fit_sack_race(state) and \
                   (self.turbo_trainers(state) or state.has(itemName.HUMBACC, self.player))

    def mr_fit_high_jump(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.springy_step_shoes(state) and self.bill_drill(state)
        elif self.easy_tricks_logic(state):
            return self.springy_step_shoes(state) and self.bill_drill(state) or state.has(itemName.HUMBACC, self.player)
        else:
            return (self.springy_step_shoes(state) and self.bill_drill(state))\
                   or self.flight_pad(state)\
                   or self.clockwork_shot(state)\
                   or state.has(itemName.HUMBACC, self.player)

    def mr_fit_sack_race(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.mr_fit_high_jump(state) and self.sack_pack(state) and \
                    self.grow_beanstalk(state) and self.can_use_floatus(state) and self.climb(state)
        elif self.easy_tricks_logic(state):
            return self.mr_fit_high_jump(state) and self.sack_pack(state) and self.grow_beanstalk(state) \
                    and self.can_use_floatus(state) and self.climb(state)
        else:
            return self.mr_fit_high_jump(state) and self.sack_pack(state) and \
                   self.grow_beanstalk(state) and (self.can_use_floatus(state) or self.pack_whack(state))\
                   and self.climb(state)

    def jiggy_pot_of_gold(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.blue_eggs(state) and self.fire_eggs(state) and self.grenade_eggs(state) and self.ice_eggs(state)\
                    and self.mumboCCL(state) and (self.flap_flip(state) or self.leg_spring(state))
        elif self.easy_tricks_logic(state):
            return self.blue_eggs(state) and self.fire_eggs(state) and self.grenade_eggs(state) and self.ice_eggs(state) and self.mumboCCL(state)\
                    and (self.flap_flip(state) or self.leg_spring(state) or self.flight_pad(state))
        else:
            return self.blue_eggs(state) and self.fire_eggs(state) and self.grenade_eggs(state) and self.ice_eggs(state)\
                       and (self.mumboCCL(state) and (self.flap_flip(state) or self.leg_spring(state) or self.flight_pad(state))
                   or (self.leg_spring(state) or (self.split_up(state) and self.tall_jump(state)))
                       and (self.flight_pad(state) and self.beak_bomb(state) or self.glide(state)))

    def jiggy_cheese(self, state: CollectionState) -> bool:
        if self.glitches_logic(state):
            return self.sack_pack(state) and self.grow_beanstalk(state) and \
                        self.can_use_floatus(state) and self.shack_pack(state)\
                    or (self.talon_trot(state) or self.clockwork_warp(state)) and self.flap_flip(state) and self.beak_buster(state) and self.flight_pad(state)\
                    or self.flight_pad(state) and (self.leg_spring(state) or (self.tall_jump(state) and self.wing_whack(state))) and self.clockwork_warp(state)
        else:
            return self.sack_pack(state) and self.grow_beanstalk(state) and \
                   self.can_use_floatus(state) and self.shack_pack(state)

    def jiggy_trash_can(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.wing_whack(state) and self.flight_pad(state)
        elif self.easy_tricks_logic(state):
            return self.split_up(state)\
                    and (self.flight_pad(state) or self.glide(state))\
                    and (self.wing_whack(state) or self.blue_eggs(state) or self.fire_eggs(state) or self.ice_eggs(state))
        else:
            return self.split_up(state)\
                   and (self.flight_pad(state) or self.glide(state) or ((self.tall_jump(state) or self.leg_spring(state)) and self.wing_whack(state)))\
                   and (self.wing_whack(state) or self.blue_eggs(state) or self.fire_eggs(state) or self.ice_eggs(state))

    def jiggy_superstash(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.clockwork_eggs(state) and self.grip_grab(state) and self.flight_pad(state) and self.flap_flip(state)
        elif self.glitches_logic(state):
            return self.clockwork_eggs(state)
        else:
            return self.clockwork_eggs(state) and self.flight_pad(state) and self.flap_flip(state)\
                    and (self.grip_grab(state) or self.very_long_jump(state) and self.climb(state))

    def honeycomb_mt_entrance(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.humbaMT(state)
        elif self.glitches_logic(state):
            return self.humbaMT(state)\
                    or self.clockwork_eggs(state)\
                    or self.breegull_bash(state)
        else:
            return self.humbaMT(state) or \
                   self.clockwork_eggs(state)

    def honeycomb_bovina(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.grip_grab(state) and self.flap_flip(state)
        elif self.easy_tricks_logic(state):
            return (self.flap_flip(state) and (self.grip_grab(state) or self.beak_buster(state)))\
                    or self.MT_flight_pad(state)
        else:
            return (self.flap_flip(state) and (self.grip_grab(state) or self.beak_buster(state)))\
                   or self.MT_flight_pad(state) or self.clockwork_shot(state)

    def honeycomb_treasure_chamber(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.can_shoot_any_egg(state) and self.egg_aim(state) and self.talon_trot(state)
        elif self.easy_tricks_logic(state):
            return (self.MT_flight_pad(state) and self.can_shoot_any_egg(state) and (self.grip_grab(state) or self.talon_trot(state)))\
                    or (self.can_shoot_any_egg(state) and self.egg_aim(state) and self.talon_trot(state))
        else:
            return (self.MT_flight_pad(state) and self.can_shoot_any_egg(state) and (self.grip_grab(state) or self.clockwork_shot(state) or self.talon_trot(state)))\
                   or (self.can_shoot_any_egg(state) and self.egg_aim(state) and (self.talon_trot(state) or self.clockwork_shot(state)))

    def honeycomb_prospector(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return (self.flap_flip(state) or self.ggm_trot(state) or self.slightly_elevated_ledge(state)) and self.bill_drill(state)\
                     or self.humbaGGM(state)
        elif self.glitches_logic(state):
            return self.bill_drill(state) or self.humbaGGM(state) or self.ground_rat_a_tat_rap(state) or self.egg_barge(state)
        else:
            return self.bill_drill(state) or self.humbaGGM(state)

    def honeycomb_gm_station(self, state: CollectionState) -> bool:
        return self.ground_attack(state) or self.humbaGGM(state)

    def honeycomb_space_zone(self, state: CollectionState) -> bool:
        logic = True
        if self.intended_logic(state):
            logic = self.grip_grab(state) and self.climb(state) and self.flap_flip(state)
        elif self.easy_tricks_logic(state):
            logic = self.grip_grab(state) and self.climb(state) and self.flap_flip(state)\
                    or self.leg_spring(state) and self.glide(state)
        elif self.hard_tricks_logic(state):
            logic = (self.grip_grab(state) or self.beak_buster(state)) and self.climb(state) and self.flap_flip(state)\
                    or self.leg_spring(state) and self.glide(state)\
                    or self.clockwork_shot(state) and (self.talon_trot(state) or self.split_up(state))
        elif self.glitches_logic(state):
            logic = (self.grip_grab(state) or self.beak_buster(state)) and self.climb(state) and self.flap_flip(state)\
                    or self.clockwork_shot(state) and state.can_reach_region(regionName.GMFD, self.player) and self.ggm_to_ww(state)\
                    or self.leg_spring(state) and self.glide(state)\
                    or self.clockwork_shot(state) and (self.talon_trot(state) or self.split_up(state))
        return logic

    def honeycomb_crazy_castle(self, state: CollectionState) -> bool:
        if self.hard_tricks_logic(state):
            return (self.has_explosives(state) and (self.small_elevation(state) or self.split_up(state) or self.grip_grab(state) or self.beak_buster(state))) or self.clockwork_shot(state)
        elif self.glitches_logic(state):
            return (self.has_explosives(state) and (self.small_elevation(state) or self.split_up(state) or self.grip_grab(state) or self.beak_buster(state)))\
                    or self.clockwork_shot(state)\
                    or self.pack_whack(state)
        else:
            return self.has_explosives(state) and (self.small_elevation(state) or self.split_up(state))

    def honeycomb_seemee(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return state.can_reach_region(regionName.JRLC, self.player) and self.talon_torpedo(state)
        else:
            return self.talon_torpedo(state)

    def honeycomb_jrl_pipes(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return (self.has_explosives(state) or  self.bill_drill(state)) and \
                    self.grip_grab(state) and self.spring_pad(state) and self.talon_trot(state)
        elif self.easy_tricks_logic(state):
            return ((self.has_explosives(state) or self.bill_drill(state))
                        and self.grip_grab(state) and self.spring_pad(state) and self.talon_trot(state))\
                    or (self.has_explosives(state) and self.spring_pad(state)
                        and (self.glide(state) or self.leg_spring(state)))
        else:
            return ((self.has_explosives(state) or self.bill_drill(state))
                       and self.grip_grab(state) and self.spring_pad(state) and self.talon_trot(state))\
                   or (self.has_explosives(state) and self.spring_pad(state)
                       and (self.glide(state) or self.leg_spring(state)))\
                   or self.clockwork_shot(state) and (self.very_long_jump(state) or self.has_explosives(state) and self.split_up(state))

    def honeycomb_lakeside(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.turbo_trainers(state)
        elif self.easy_tricks_logic(state):
            return self.turbo_trainers(state) or self.TDL_flight_pad(state)\
                or (self.tall_jump(state) and self.very_long_jump(state) and self.grip_grab(state))\
                or self.split_up(state)
        else:
            return self.turbo_trainers(state) or self.TDL_flight_pad(state) or self.clockwork_shot(state)\
               or (self.tall_jump(state) and self.very_long_jump(state) and self.grip_grab(state))\
               or self.split_up(state)

    def honeycomb_styracosaurus(self, state: CollectionState) -> bool:
        if self.intended_logic(state) or self.easy_tricks_logic(state):
            return self.bill_drill(state) and self.split_up(state) and self.spring_pad(state)
        else:
            return (self.bill_drill(state) and self.split_up(state) and self.spring_pad(state)) or \
                    (self.leg_spring(state) and self.wing_whack(state) and self.glide(state))\
                    or self.clockwork_shot(state)

    def honeycomb_river(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.talon_trot(state)
        elif self.easy_tricks_logic(state):
            return self.talon_trot(state) or self.split_up(state)
        else:
            return self.talon_trot(state) or self.clockwork_shot(state) or self.humbaTDL(state) or self.split_up(state)

    def honeycomb_floor3(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.flap_flip(state) and self.grip_grab(state) and self.spring_pad(state)\
                    or self.climb(state) and self.spring_pad(state) and (
                        self.tall_jump(state) and self.grip_grab(state)
                        or self.talon_trot(state) and self.flutter(state) and self.grip_grab(state)
                    )\
                    or self.floor_3_split_up(state) and self.leg_spring(state) and (
                        self.can_shoot_any_egg(state)
                        or self.wing_whack(state)
                    )
        elif self.easy_tricks_logic(state):
            return self.flap_flip(state) and (self.grip_grab(state) or self.beak_buster(state)) and self.spring_pad(state)\
                    or self.climb(state) and self.spring_pad(state) and (
                        self.tall_jump(state) and self.grip_grab(state)
                        or self.talon_trot(state) and self.flutter(state) and self.grip_grab(state)
                    )\
                    or self.floor_3_split_up(state) and self.leg_spring(state) and (
                        self.can_shoot_any_egg(state)
                        or self.wing_whack(state)
                    )
        else:
            return self.flap_flip(state) and (self.grip_grab(state) or self.beak_buster(state)) and self.spring_pad(state)\
                   or self.climb(state) and self.spring_pad(state) and (
                       self.tall_jump(state) and self.grip_grab(state)
                       or self.talon_trot(state) and self.flutter(state) and self.grip_grab(state)
                   )\
                   or self.floor_3_split_up(state) and (
                       self.leg_spring(state) and (
                           self.can_shoot_any_egg(state)
                           or self.wing_whack(state)
                       )
                       or self.tall_jump(state) and (
                               self.wing_whack(state)
                               or self.glide(state)
                           )
                           and (
                               self.can_shoot_any_egg(state)
                               or self.wing_whack(state)
                           )
                   )\
                   or self.clockwork_shot(state)

    def honeycomb_gi_station(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.grip_grab(state) and self.ground_attack(state) and self.spring_pad(state)
        elif self.easy_tricks_logic(state):
            return self.ground_attack(state) and self.spring_pad(state) and self.grip_grab(state)
        else:
            return (self.ground_attack(state) and self.spring_pad(state)) or self.clockwork_shot(state) or self.leg_spring(state)

    def honeycomb_volcano(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.hfp_top(state) and self.grenade_eggs(state) and self.egg_aim(state) and self.spring_pad(state) and (self.talon_trot(state) or self.split_up(state))
        elif self.easy_tricks_logic(state):
            return self.hfp_top(state) and (
                    self.split_up(state) and (self.tall_jump(state) or self.wing_whack(state) or self.glide(state) or self.leg_spring(state))
                    or self.grenade_eggs(state) and self.egg_aim(state) and self.spring_pad(state) and self.talon_trot(state))
        else:
            return self.hfp_top(state) and (
                   self.split_up(state) and (self.tall_jump(state) or self.wing_whack(state) or self.glide(state) or self.leg_spring(state))
                   or self.grenade_eggs(state) and self.egg_aim(state) and self.talon_trot(state)
                   or self.extremelyLongJump(state)
                   or self.clockwork_shot(state))

    def honeycomb_hfp_station(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.grip_grab(state) and\
                  (self.talon_trot(state) or self.tall_jump(state)) and\
                  (self.flutter(state) or self.air_rat_a_tat_rap(state))
        elif self.easy_tricks_logic(state):
            return (self.grip_grab(state) and
                  (self.talon_trot(state) or self.tall_jump(state)) and
                  (self.flutter(state) or self.air_rat_a_tat_rap(state)))\
                    or self.leg_spring(state)
        else:
            return (self.grip_grab(state) and
                 (self.talon_trot(state) or self.tall_jump(state)) and
                 (self.flutter(state) or self.air_rat_a_tat_rap(state)))\
                   or self.leg_spring(state)\
                    or self.clockwork_shot(state) and self.hfp_top(state)

    def honeycomb_lava_side(self, state: CollectionState) -> bool:
        logic = True
        if self.intended_logic(state):
            logic = self.grip_grab(state) and self.flap_flip(state)
        elif self.easy_tricks_logic(state):
            logic = self.grip_grab(state) and self.flap_flip(state) or self.flight_pad(state)\
                    or self.leg_spring(state) and (self.wing_whack(state) or self.glide(state))
        elif self.hard_tricks_logic(state):
            logic = self.grip_grab(state) and self.flap_flip(state)\
                    or self.flight_pad(state)\
                    or self.leg_spring(state) and (self.wing_whack(state) or self.glide(state))\
                    or self.hfp_top(state) and self.clockwork_shot(state)
        elif self.glitches_logic(state):
            logic = self.grip_grab(state) and self.flap_flip(state) or self.flight_pad(state)\
                    or self.leg_spring(state) and (self.wing_whack(state) or self.glide(state))\
                    or self.hfp_top(state) and self.clockwork_shot(state)
        return logic

    def honeycomb_trash(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.flight_pad(state) or state.has(itemName.HUMBACC, self.player)
        else:
            return self.flight_pad(state) or self.glide(state) or state.has(itemName.HUMBACC, self.player)

    def honeycomb_pot(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.flight_pad(state) or state.has(itemName.HUMBACC, self.player)
        else:
            return (self.flight_pad(state) or self.wing_whack(state) or self.glide(state)) or state.has(itemName.HUMBACC, self.player)

    def plateau_top(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.talon_trot(state) or self.split_up(state)
        elif self.easy_tricks_logic(state):
            return self.talon_trot(state) or self.split_up(state) or (state.can_reach_region(regionName.IOHCT, self.player) and self.claw_clamber_boots(state))
        else:
            return self.talon_trot(state) or self.split_up(state)\
                   or self.clockwork_shot(state)\
                   or (state.can_reach_region(regionName.IOHCT, self.player) and self.claw_clamber_boots(state))

    def cheato_snakehead(self, state: CollectionState) -> bool:
        logic = True
        if self.intended_logic(state):
            logic = self.egg_aim(state) and self.grip_grab(state) and self.spring_pad(state) and self.flap_flip(state) and self.talon_trot(state)\
                        or self.MT_flight_pad(state)
        elif self.easy_tricks_logic(state):
            logic = self.grip_grab(state) and self.spring_pad(state) and self.flap_flip(state) and self.can_shoot_any_egg(state) and self.egg_aim(state) and self.talon_trot(state)\
                        or self.MT_flight_pad(state)
        elif self.hard_tricks_logic(state):
            logic = (self.grip_grab(state) and self.spring_pad(state) and self.flap_flip(state) and self.can_shoot_any_egg(state) and self.egg_aim(state) and self.talon_trot(state))\
                        or self.MT_flight_pad(state)\
                        or self.clockwork_shot(state)
        elif self.glitches_logic(state):
            logic = ((self.grip_grab(state) and self.spring_pad(state) and self.flap_flip(state) and self.can_shoot_any_egg(state) and self.egg_aim(state) and self.talon_trot(state))
                        or (self.MT_flight_pad(state)))\
                        or self.clockwork_shot(state)
        return logic

    def cheato_prison(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.prison_compound_as_banjo(state) and self.slightly_elevated_ledge(state) and self.tall_jump(state)
        elif self.easy_tricks_logic(state):
            return self.prison_compound_as_banjo(state) and self.slightly_elevated_ledge(state)
        else:
            return self.prison_compound_as_banjo(state) and (self.slightly_elevated_ledge(state) or self.clockwork_shot(state))

    def cheato_jade_snake_grove(self, state: CollectionState) -> bool:
        if self.intended_logic(state) or self.easy_tricks_logic(state):
            return self.grip_grab(state)\
                       and self.talon_trot(state) and self.flap_flip(state)
        else:
            return self.talon_trot(state) and self.flap_flip(state) and self.grip_grab(state)\
                        or self.egg_aim(state) and self.clockwork_eggs(state)

    def cheato_gm_entrance(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.springy_step_shoes(state)
        elif self.easy_tricks_logic(state):
            return self.springy_step_shoes(state) or \
                    (self.climb(state) and (self.flutter(state) or (self.air_rat_a_tat_rap(state) and self.tall_jump(state))))\
                    or (self.ggm_boulders(state) and self.leg_spring(state))\
                    or (self.ggm_boulders(state) and self.glide(state) and self.tall_jump(state))
                    # or state.can_reach_region(regionName.IOHPL, self.player) and self.PL_to_GGM(state) and self.flutter(state) and (self.grip_grab(state) or self.beak_buster(state)) # Flutter right as you enter the level.
        else:
            return self.springy_step_shoes(state) or \
                   (self.climb(state) and (self.flutter(state) or self.air_rat_a_tat_rap(state)))\
                   or (self.clockwork_shot(state))\
                   or (self.ggm_boulders(state) and self.leg_spring(state))\
                   or (self.ggm_boulders(state) and self.glide(state) and self.tall_jump(state))\
                   or (self.ggm_boulders(state) and self.tall_jump(state) and self.turbo_trainers(state) and (self.wing_whack(state) or self.glide(state)))
                   # or state.can_reach_region(regionName.IOHPL, self.player) and self.PL_to_GGM(state) and self.flutter(state) and (self.grip_grab(state) or self.beak_buster(state))

    def cheato_water_storage(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.grip_grab(state) and self.flap_flip(state) and self.dive(state) and self.climb(state)
        elif self.glitches_logic(state):
            return (self.grip_grab(state) or self.beak_buster(state)) and self.flap_flip(state) and self.dive(state) and self.climb(state)\
                    or self.leg_spring(state) and self.glide(state) and self.ggm_boulders(state)\
                    or self.ggm_boulders(state) and self.pack_whack(state) and self.tall_jump(state) and self.dive(state) and self.climb(state) and self.grip_grab(state)
        else:
            return (self.grip_grab(state) or self.beak_buster(state)) and self.flap_flip(state) and self.dive(state) and self.climb(state)\
                   or self.ggm_boulders(state) and self.pack_whack(state) and self.tall_jump(state) and self.dive(state) and self.climb(state) and self.grip_grab(state)

    def cheato_haunted_cavern(self, state: CollectionState) -> bool:
        # You can damage boost from the torch at the end of the path to grip grab the ledge.
        if self.intended_logic(state):
            return self.slightly_elevated_ledge(state)
        elif self.easy_tricks_logic(state):
            return self.grip_grab(state) or (self.leg_spring(state) and
                   (self.wing_whack(state) or self.glide(state)))
        else:
            return self.grip_grab(state) or (self.leg_spring(state) and
                   (self.wing_whack(state) or self.glide(state)))\
                   or self.clockwork_shot(state)

    def cheato_inferno(self, state: CollectionState) -> bool:
        if self.glitches_logic(state):
            return self.humbaWW(state) or self.clockwork_eggs(state)
        else:
            return self.humbaWW(state)

    def cheato_saucer_of_peril(self, state: CollectionState) -> bool:
        return self.jiggy_peril(state)

    def cheato_pawno(self, state: CollectionState) -> bool:
        if self.intended_logic(state) or self.easy_tricks_logic(state):
            return state.has(itemName.DOUBLOON, self.player, 28) and self.small_elevation(state)
        else:
            return state.has(itemName.DOUBLOON, self.player, 28) and (self.small_elevation(state) or self.clockwork_shot(state))

    def cheato_seemee(self, state: CollectionState) -> bool:
        return self.talon_torpedo(state)

    def cheato_ancient_swimming_baths(self, state: CollectionState) -> bool:
        logic = True
        if self.intended_logic(state):
            logic = self.talon_torpedo(state) and \
                    self.glide(state) and self.tall_jump(state)
        elif self.easy_tricks_logic(state):
            logic = self.talon_torpedo(state) and \
                    ((self.glide(state) and self.tall_jump(state)) or self.leg_spring(state) or
                    (self.pack_whack(state) and self.grip_grab(state)))
        elif self.hard_tricks_logic(state):
            logic = self.talon_torpedo(state) and (
                        (self.glide(state) and self.tall_jump(state))
                        or self.leg_spring(state)
                        or self.wing_whack(state) and self.tall_jump(state)
                        or self.clockwork_shot(state)
                        or self.tall_jump(state) and self.pack_whack(state) and self.grip_grab(state)
                    )
        elif self.glitches_logic(state):
            logic = self.talon_torpedo(state) and (
                        (self.glide(state) and self.tall_jump(state))
                        or self.leg_spring(state)
                        or self.wing_whack(state) and self.tall_jump(state)
                        or self.clockwork_shot(state)
                        or self.tall_jump(state) and self.pack_whack(state) and self.grip_grab(state)
                        or self.sack_pack(state) and self.tall_jump(state)
                    )
        return logic

    def cheato_trex(self, state: CollectionState) -> bool:
        if self.glitches_logic(state):
            return self.humbaTDL(state) and self.roar(state) or self.clockwork_eggs(state)
        else:
            return self.humbaTDL(state) and self.roar(state)

    def cheato_dippy_pool(self, state: CollectionState) -> bool:
        return state.can_reach_region(regionName.CC, self.player) and self.jiggy_dippy(state) and self.dive(state)\
           and ((self.small_elevation(state) and self.springy_step_shoes(state)) or self.TDL_flight_pad(state))

    def cheato_tdlboulder(self, state: CollectionState) -> bool:
        logic = True
        if self.intended_logic(state):
            logic = self.bill_drill(state) and self.flap_flip(state) and self.grip_grab(state)
        elif self.easy_tricks_logic(state):
            logic = self.bill_drill(state)\
                        and (self.TDL_flight_pad(state)
                             or self.grip_grab(state) and (self.flap_flip(state) or (self.talon_trot(state) and self.flutter(state))))
        elif self.hard_tricks_logic(state):
            logic = self.bill_drill(state)\
                        and (self.TDL_flight_pad(state)
                             or self.grip_grab(state) and (self.flap_flip(state) or (self.talon_trot(state) and self.flutter(state)))
                             or state.can_reach_region(regionName.TLTOP, self.player) and self.talon_trot(state) and (self.flutter(state) or self.air_rat_a_tat_rap(state))
                        )
        elif self.glitches_logic(state):
            logic = (self.bill_drill(state) or self.egg_barge(state))\
                        and (self.TDL_flight_pad(state)
                             or self.grip_grab(state) and (self.flap_flip(state) or (self.talon_trot(state) and self.flutter(state)))
                             or state.can_reach_region(regionName.TLTOP, self.player) and self.talon_trot(state) and (self.flutter(state) or self.air_rat_a_tat_rap(state))
                        )
        return logic

    def cheato_loggo(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.has_explosives(state) and self.bill_drill(state)
        else:
            return self.has_explosives(state) and\
                       (self.grenade_eggs(state)
                        or self.bill_drill(state)
                        or self.breegull_bash(state)
                        or self.beak_barge(state)
                        or self.pack_whack(state))

    def cheato_window(self, state: CollectionState) -> bool:
        logic = True
        if self.intended_logic(state):
            logic = state.can_reach_region(regionName.GIF, self.player) and (self.egg_aim(state) or self.airborne_egg_aiming(state) or self.beak_bomb(state))
        elif self.easy_tricks_logic(state):
            logic = state.can_reach_region(regionName.GIF, self.player) and (self.egg_aim(state) or self.airborne_egg_aiming(state) or self.beak_bomb(state))\
                    or state.can_reach_region(regionName.GI1, self.player) and self.leg_spring(state) and self.claw_clamber_boots(state) and self.wing_whack(state)
        elif self.hard_tricks_logic(state):
            logic = state.can_reach_region(regionName.GIF, self.player) and (self.egg_aim(state) or self.airborne_egg_aiming(state) or self.beak_bomb(state))\
                    or state.can_reach_region(regionName.GI1, self.player) and self.leg_spring(state) and self.claw_clamber_boots(state) and self.wing_whack(state)\
                    or self.clockwork_shot(state)
        elif self.glitches_logic(state):
            logic = state.can_reach_region(regionName.GIF, self.player) and (self.egg_aim(state) or self.airborne_egg_aiming(state) or self.beak_bomb(state))\
                    or state.can_reach_region(regionName.GI1, self.player) and self.leg_spring(state) and self.claw_clamber_boots(state) and self.wing_whack(state)\
                    or state.can_reach_region(regionName.GI2, self.player) and self.clockwork_shot(state) and self.floor_2_split_up(state)\
                    or self.clockwork_shot(state)
        return logic

    def cheato_colosseum(self, state: CollectionState) -> bool:
        logic = True
        if self.intended_logic(state):
            logic = self.long_jump(state) and self.claw_clamber_boots(state) and (self.has_explosives(state) or self.dragon_kazooie(state))
        elif self.easy_tricks_logic(state):
            logic = self.long_jump(state) and  self.claw_clamber_boots(state) and (
                        self.has_explosives(state)
                        or state.has(itemName.MUMBOHP, self.player)
                        or self.dragon_kazooie(state)
                    )
        elif self.hard_tricks_logic(state):
            logic = self.claw_clamber_boots(state) and \
                    (self.has_explosives(state) or
                    state.has(itemName.MUMBOHP, self.player)
                    or self.dragon_kazooie(state))
        elif self.glitches_logic(state):
            logic = (self.claw_clamber_boots(state) and
                        (self.has_explosives(state) or
                        state.has(itemName.MUMBOHP, self.player)
                        or self.dragon_kazooie(state)))\
                    or self.hfp_top(state) and self.third_person_egg_shooting(state)
        return logic

    def cheato_icicle_grotto(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.hfp_top(state) and self.climb(state) and (self.clockwork_eggs(state) or self.shack_pack(state))
        elif self.glitches_logic(state):
            return self.hfp_top(state) and (
                    self.climb(state) and self.shack_pack(state)
                    or ((self.leg_spring(state) or self.climb(state)) and self.clockwork_eggs(state))
                    or ((self.talon_trot(state) or self.split_up(state)) and self.clockwork_shot(state)))
        else:
            return self.hfp_top(state) and (
                   self.climb(state) and self.shack_pack(state)
                   or ((self.leg_spring(state) or self.climb(state)) and self.clockwork_eggs(state)))

    def cheato_icy_pillar(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.hfp_top(state) and self.grenade_eggs(state) and self.egg_aim(state) and self.spring_pad(state) and self.split_up(state) and self.glide(state)\
                    or self.leg_spring(state)
        elif self.easy_tricks_logic(state):
            return self.split_up(state) and (self.tall_jump(state) or self.wing_whack(state) or self.glide(state))\
                    or self.leg_spring(state)
        else:
            return (self.split_up(state) and (self.tall_jump(state) or self.wing_whack(state) or self.glide(state)))\
                   or self.leg_spring(state)\
                   or (self.grenade_eggs(state) and self.clockwork_shot(state) and self.small_elevation(state) and self.spring_pad(state) and self.talon_trot(state))

    def cheato_potgold(self, state: CollectionState) -> bool:
        return self.jiggy_pot_of_gold(state)

    def cheato_spiral(self, state: CollectionState) -> bool:
        if self.intended_logic(state) or self.easy_tricks_logic(state):
            return self.spring_pad(state) or self.flight_pad(state)
        else:
            return True

    def glowbo_entrance_ggm(self, state: CollectionState) -> bool:
        if self.intended_logic(state) or self.easy_tricks_logic(state):
            return self.GGM_slope(state)
        else:
            return True

    def glowbo_wigwam(self, state: CollectionState) -> bool:
        logic = True
        if self.intended_logic(state):
            logic = self.flap_flip(state) and self.grip_grab(state)\
                    or self.warp_to_ww_wumba(state)
        elif self.easy_tricks_logic(state):
            logic = (self.flap_flip(state) and self.grip_grab(state)) \
                    or (self.climb(state) and self.very_long_jump(state) and self.flap_flip(state))\
                    or self.leg_spring(state)\
                    or self.warp_to_ww_wumba(state)
        elif self.hard_tricks_logic(state):
            logic = (self.flap_flip(state) and self.grip_grab(state)) \
                    or (self.climb(state) and self.very_long_jump(state) and self.flap_flip(state))\
                    or (self.clockwork_shot(state) and self.climb(state))\
                    or self.leg_spring(state)\
                    or self.warp_to_ww_wumba(state)
        elif self.glitches_logic(state):
            logic = (self.flap_flip(state) and self.grip_grab(state)) \
                    or (self.climb(state) and self.very_long_jump(state) and self.flap_flip(state))\
                    or (self.clockwork_shot(state) and self.climb(state)
                    or self.leg_spring(state))\
                    or self.warp_to_ww_wumba(state)
        return logic

    def glowbo_underwigwam(self, state: CollectionState) -> bool:
        return True

    def glowbo_tdl(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return (self.small_elevation(state) or self.TDL_flight_pad(state))
        elif self.easy_tricks_logic(state):
            return self.small_elevation(state)\
                    or self.TDL_flight_pad(state)\
                    or self.humbaTDL(state)\
                    or self.springy_step_shoes(state)\
                    or self.turbo_trainers(state)\
                    or self.beak_buster(state)
        else:
            return self.small_elevation(state)\
                   or self.TDL_flight_pad(state)\
                   or self.humbaTDL(state)\
                   or self.springy_step_shoes(state)\
                   or self.turbo_trainers(state)\
                   or self.clockwork_shot(state)\
                   or self.beak_buster(state)

    def glowbo_tdl_mumbo(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.stilt_stride(state)
        else:
            return True

    def glowbo_floor_3(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.flap_flip(state) and self.grip_grab(state)\
                    or self.climb(state) and (
                        self.tall_jump(state) and self.grip_grab(state)
                        or self.talon_trot(state) and self.flutter(state) and self.grip_grab(state)
                    )\
                    or self.floor_3_split_up(state) and self.leg_spring(state)
        elif self.easy_tricks_logic(state):
            return self.flap_flip(state) and (self.grip_grab(state) or self.beak_buster(state))\
                    or self.climb(state) and (
                        self.tall_jump(state) and self.grip_grab(state)
                        or self.talon_trot(state) and self.flutter(state) and self.grip_grab(state)
                    )\
                    or self.floor_3_split_up(state) and self.leg_spring(state)\
                    or self.pack_whack(state) and self.floor_3_split_up(state) and self.tall_jump(state)\
                    or state.can_reach_region(regionName.GI3B, self.player)
        else:
            return self.flap_flip(state) and (self.grip_grab(state) or self.beak_buster(state))\
                   or self.climb(state) and (
                       self.tall_jump(state) and self.grip_grab(state)
                       or self.talon_trot(state) and self.flutter(state) and self.grip_grab(state)
                   )\
                   or self.floor_3_split_up(state) and self.leg_spring(state)\
                   or self.pack_whack(state) and self.floor_3_split_up(state) and self.tall_jump(state)\
                   or state.can_reach_region(regionName.GI3B, self.player)\
                   or self.clockwork_shot(state)\
                   or self.sack_pack(state)\
                   or self.tall_jump(state) and (self.wing_whack(state) or self.glide(state))

    def pawno_shelves(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.small_elevation(state) or self.grip_grab(state)
        elif self.easy_tricks_logic(state):
            return self.small_elevation(state) or self.grip_grab(state)\
                    or self.has_explosives(state) and self.split_up(state)
        else:
            return self.small_elevation(state) or self.grip_grab(state) or self.clockwork_shot(state)\
                   or self.has_explosives(state) and self.split_up(state)

    def glowbo_cavern(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.small_elevation(state) and self.dive(state)
        elif self.easy_tricks_logic(state):
            return self.dive(state) or self.shack_pack(state) and self.tall_jump(state)
        else:
            return self.dive(state) or self.shack_pack(state)

    def glowbo_cliff(self, state: CollectionState) -> bool:
        if self.intended_logic(state) or self.easy_tricks_logic(state):
            return self.climb(state)
        else:
            return self.climb(state) or (self.clockwork_shot(state) and state.can_reach_region(regionName.IOHCT, self.player))

    def mega_glowbo(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.talon_torpedo(state) and state.has(itemName.IKEY, self.player)\
                   and self.dive(state) and self.tall_jump(state)
        elif self.easy_tricks_logic(state):
            return self.talon_torpedo(state) and state.has(itemName.IKEY, self.player)\
                   and self.dive(state) and\
                   (self.tall_jump(state) or self.beak_buster(state) or self.flutter(state) or self.air_rat_a_tat_rap(state))
        else:
            return self.talon_torpedo(state) and state.has(itemName.IKEY, self.player)\
                   and self.dive(state) and\
                   (self.tall_jump(state) or self.beak_buster(state) or self.clockwork_shot(state) or self.flutter(state) or self.air_rat_a_tat_rap(state))

    def ice_key(self, state: CollectionState) -> bool:
        if self.intended_logic(state) or self.easy_tricks_logic(state):
            return self.grip_grab(state) and self.flap_flip(state)
        else:
            return (self.grip_grab(state) and self.flap_flip(state)) or self.clockwork_shot(state)

    def pink_mystery_egg(self, state: CollectionState) -> bool:
        if self.hard_tricks_logic(state):
            return (self.grenade_eggs(state) or (self.airborne_egg_aiming(state) and self.grenade_eggs_item(state))) \
                    and self.flight_pad(state) \
                    or self.egg_aim(state) and self.grenade_eggs(state) and self.clockwork_shot(state)
        elif self.glitches_logic(state):
            return (self.has_explosives(state) or (self.airborne_egg_aiming(state) and self.grenade_eggs_item(state))) \
                    and self.flight_pad(state) \
                    or self.egg_aim(state) and self.grenade_eggs(state) and self.clockwork_shot(state)
        else:
            return (self.grenade_eggs(state) or (self.airborne_egg_aiming(state) and self.grenade_eggs_item(state))) \
                   and self.flight_pad(state)

    def blue_mystery_egg(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.grip_grab(state) and self.flap_flip(state) and self.flight_pad(state)\
                    and self.tall_jump(state)
        elif self.easy_tricks_logic(state):
            return self.grip_grab(state) and self.flap_flip(state) and self.flight_pad(state)\
                    and (self.tall_jump(state) or self.beak_buster(state))
        else:
            return ((self.grip_grab(state) and self.flap_flip(state) and (self.tall_jump(state) or self.beak_buster(state)))
                   or self.clockwork_shot(state)) and self.flight_pad(state)

    def jinjo_plateau(self, state: CollectionState) -> bool:
        if self.glitches_logic(state):
            return self.bill_drill(state) or self.egg_barge(state) or self.taxi_pack(state)
        else:
            return self.bill_drill(state)

    def jinjo_clifftop(self, state: CollectionState) -> bool:
        if self.intended_logic(state) or self.easy_tricks_logic(state):
            return self.claw_clamber_boots(state)
        else:
            return self.claw_clamber_boots(state) or self.clockwork_shot(state)

    def jinjo_wasteland(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.grip_grab(state) and self.flap_flip(state)
        elif self.easy_tricks_logic(state):
            return (self.grip_grab(state) or self.beak_buster(state)) and self.flap_flip(state)
        else:
            return ((self.grip_grab(state) or self.beak_buster(state)) and self.flap_flip(state))\
                       or self.clockwork_shot(state)

    def jinjo_jadesnakegrove(self, state: CollectionState) -> bool:
        logic = True
        if self.intended_logic(state):
            logic = self.grip_grab(state) and self.flap_flip(state)
        elif self.easy_tricks_logic(state):
            logic = self.flap_flip(state) and\
                    (self.beak_buster(state) or self.grip_grab(state))
        elif self.hard_tricks_logic(state):
            logic = (self.flap_flip(state) and (self.beak_buster(state) or self.grip_grab(state))) or\
                    self.clockwork_shot(state)
        elif self.glitches_logic(state):
            logic = (self.flap_flip(state) and (self.beak_buster(state) or self.grip_grab(state))) or\
                    self.clockwork_shot(state) or state.has(itemName.MUMBOMT, self.player)
        return logic

    def jinjo_stadium(self, state: CollectionState) -> bool:
        if self.intended_logic(state) or self.easy_tricks_logic(state):
            return self.MT_flight_pad(state)
        else:
            return self.MT_flight_pad(state) or self.clockwork_shot(state)

    def jinjo_pool(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.dive(state)\
                    or state.has(itemName.MUMBOMT, self.player)\
                    or self.humbaMT(state)
        else:
            return True

    def jinjo_jail(self, state: CollectionState) -> bool:
        if self.glitches_logic(state):
            return self.humbaGGM(state) or (self.bill_drill(state) and self.clockwork_shot(state))
        else:
            return self.humbaGGM(state)

    def jinjo_boulder(self, state: CollectionState) -> bool:
        if self.glitches_logic(state):
            return self.humbaGGM(state)\
                    or (self.ggm_trot(state) and (self.bill_drill(state) or self.egg_barge(state)))
        else:
            return self.humbaGGM(state) or (self.ggm_trot(state) and self.bill_drill(state))

    def jinjo_tent(self, state: CollectionState) -> bool:
        logic = True
        if self.intended_logic(state):
            logic = self.talon_trot(state)
        elif self.easy_tricks_logic(state):
            logic = self.talon_trot(state)\
                    or self.humbaWW(state)\
                    or self.split_up(state)\
                    or state.can_reach_region(regionName.WWI, self.player) and self.turbo_trainers(state)
        elif self.hard_tricks_logic(state):
            logic = self.talon_trot(state)\
                    or self.humbaWW(state)\
                    or self.clockwork_shot(state)\
                    or self.split_up(state)\
                    or state.can_reach_region(regionName.WWI, self.player) and self.turbo_trainers(state)
        elif self.glitches_logic(state):
            logic = self.talon_trot(state)\
                    or self.humbaWW(state)\
                    or self.clockwork_shot(state)\
                    or self.split_up(state)\
                    or (self.warp_to_inferno(state) or self.humbaWW(state)) and self.turbo_trainers(state)
        return logic

    def jinjo_cave_of_horrors(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.grenade_eggs(state) and self.egg_aim(state)
        else:
            return self.grenade_eggs(state)

    def jinjo_cactus(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.grip_grab(state) and self.flap_flip(state)
        elif self.easy_tricks_logic(state):
            return (self.grip_grab(state) and self.flap_flip(state))\
                    or (self.climb(state) and self.talon_trot(state) and self.flutter(state))\
                    or self.leg_spring(state)\
                    or self.pack_whack(state) and self.tall_jump(state) and self.grip_grab(state)
        else:
            return (self.grip_grab(state) and self.flap_flip(state))\
                   or (self.climb(state) and self.talon_trot(state) and (self.flutter(state) or self.air_rat_a_tat_rap(state)))\
                   or self.leg_spring(state)\
                   or self.clockwork_shot(state)\
                   or self.pack_whack(state) and self.tall_jump(state) and self.grip_grab(state)

    def jinjo_van_door(self, state: CollectionState) -> bool:
        if self.glitches_logic(state):
            return (self.has_explosives(state) and self.humbaWW(state)) or self.clockwork_eggs(state)
        else:
            return self.has_explosives(state) and \
                   self.humbaWW(state)

    def jinjo_dodgem(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.talon_trot(state) and self.climb(state)
        elif self.easy_tricks_logic(state):
            return self.talon_trot(state) and self.climb(state)\
                    or self.leg_spring(state) and self.glide(state)
        else:
            return (self.talon_trot(state) or self.clockwork_shot(state)) and self.climb(state)\
                   or self.leg_spring(state) and self.glide(state)

    def jinjo_alcove(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return state.has(itemName.DOUBLOON, self.player, 28) and self.turbo_trainers(state)
        elif self.easy_tricks_logic(state):
            return (state.has(itemName.DOUBLOON, self.player, 28) and self.turbo_trainers(state))\
                    or (self.has_explosives(state) and (
                            self.pack_whack(state) and self.tall_jump(state)
                            or self.sack_pack(state)
                            or (self.leg_spring(state) and self.glide(state))
                        )
                    )
        else:
            return (state.has(itemName.DOUBLOON, self.player, 28) and self.turbo_trainers(state))\
                   or (
                       self.has_explosives(state) and (
                           self.pack_whack(state)
                           or self.sack_pack(state)
                           or (self.leg_spring(state) and self.glide(state))
                       )
                   )\
                   or self.tall_jump(state) and (self.flutter(state) or self.air_rat_a_tat_rap(state))\
                   or self.clockwork_shot(state)

    def jinjo_blubber(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.spring_pad(state) or self.flap_flip(state)
        elif self.easy_tricks_logic(state):
            return self.spring_pad(state) or self.flap_flip(state) or (self.has_explosives(state) and self.leg_spring(state))
        else:
            return self.spring_pad(state) or self.flap_flip(state) or self.clockwork_shot(state) or (self.has_explosives(state) and self.leg_spring(state))

    def jinjo_big_fish(self, state: CollectionState) -> bool:
        return self.jiggy_merry_maggie(state)

    def jinjo_seaweed_sanctum(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.grip_grab(state) and self.flap_flip(state) and (
                self.can_climb_seaweed(state)
                or state.can_reach_region(regionName.JRBFC, self.player)
            )
        elif self.easy_tricks_logic(state):
            return (self.grip_grab(state) or self.beak_buster(state)) and self.flap_flip(state)\
                    and (
                        self.can_climb_seaweed(state)
                        or state.can_reach_region(regionName.JRBFC, self.player)
                    )
        else:
            return ((self.grip_grab(state) or self.beak_buster(state)) and self.flap_flip(state)
                       or self.clockwork_shot(state))\
                   and (
                       self.can_climb_seaweed(state)
                       or state.can_reach_region(regionName.JRBFC, self.player)
                   )

    def jinjo_sunken_ship(self, state: CollectionState) -> bool:
        return self.humbaJRL(state) or self.sub_aqua_egg_aiming(state) or \
                    self.talon_torpedo(state)

    def jinjo_tdl_entrance(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.TDL_flight_pad(state) and (self.beak_bomb(state) or self.grenade_eggs(state) and self.egg_aim(state))
        elif self.easy_tricks_logic(state):
            return self.TDL_flight_pad(state) and (self.beak_bomb(state) or self.grenade_eggs(state))
        else:
            return (self.TDL_flight_pad(state) and self.beak_bomb(state)) or (self.grenade_eggs(state)
                   and (self.egg_aim(state) or self.long_jump(state) or self.TDL_flight_pad(state) or self.turbo_trainers(state) or self.split_up(state)))

    def jinjo_big_t_rex(self, state: CollectionState) -> bool:
        if self.glitches_logic(state):
            return (self.mumboTDL(state) and self.humbaTDL(state)) or \
                    self.clockwork_eggs(state)
        else:
            return self.mumboTDL(state) and self.humbaTDL(state)

    def jinjo_stomping_plains(self, state: CollectionState) -> bool:
        if self.glitches_logic(state):
            return (self.split_up(state) and self.tall_jump(state)
                    or self.egg_barge(state) and (self.tall_jump(state) or self.talon_trot(state) or self.springy_step_shoes(state) or self.turbo_trainers(state)))
        else:
            return self.split_up(state) and self.tall_jump(state)

    def jinjo_legspring(self, state: CollectionState) -> bool:
        if self.intended_logic(state) or self.easy_tricks_logic(state):
            return self.leg_spring(state)
        else:
            return self.leg_spring(state) or self.clockwork_shot(state)

    def jinjo_gi_outside(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return state.can_reach_region(regionName.GI2, self.player) and self.floor_2_split_up(state)\
                   and self.pack_whack(state) and (self.wing_whack(state) or self.can_shoot_any_egg(state)) and self.claw_clamber_boots(state)
        elif self.glitches_logic(state):
            return state.can_reach_region(regionName.GI2, self.player) and self.floor_2_split_up(state)\
                       and self.pack_whack(state) and (self.wing_whack(state) or self.can_shoot_any_egg(state)) and self.claw_clamber_boots(state)\
                   or state.can_reach_region(regionName.GIR, self.player) and self.split_up(state) and (self.wing_whack(state) or self.can_shoot_any_egg(state))\
                   or state.can_reach_region(regionName.GIR, self.player) and self.taxi_pack(state)\
                   or (state.can_reach_region(regionName.GIOB, self.player) and self.claw_clamber_boots(state) or state.can_reach_region(regionName.GIR, self.player)) and self.egg_barge(state)
        else:
            return state.can_reach_region(regionName.GI2, self.player) and self.floor_2_split_up(state)\
                       and self.pack_whack(state) and (self.wing_whack(state) or self.can_shoot_any_egg(state)) and self.claw_clamber_boots(state)\
                   or state.can_reach_region(regionName.GIR, self.player) and self.split_up(state) and (self.wing_whack(state) or self.can_shoot_any_egg(state)) # Both characters drop from the roof, Banjo gets the jinjo.


    def jinjo_waste_disposal(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.talon_torpedo(state) and self.ice_eggs_item(state)\
                        and state.has(itemName.MUMBOJR, self.player) and self.sub_aqua_egg_aiming(state)
        elif self.easy_tricks_logic(state):
            return self.talon_torpedo(state) and self.ice_eggs_item(state)\
                        and (state.has(itemName.MUMBOJR, self.player) or self.doubleAir(state)) and self.sub_aqua_egg_aiming(state)
        else:
            return self.ice_eggs_item(state) and self.sub_aqua_egg_aiming(state) and \
                   self.talon_torpedo(state)

    def jinjo_boiler(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return state.can_reach_region(regionName.GIF, self.player) and self.flight_to_boiler_plant(state)
        elif self.easy_tricks_logic(state):
            return state.can_reach_region(regionName.GIF, self.player) and self.flight_to_boiler_plant(state)\
                    or state.can_reach_region(regionName.GI3, self.player) and self.small_elevation(state) and self.leg_spring(state) and self.glide(state)
        else:
            return state.can_reach_region(regionName.GIF, self.player) and self.flight_to_boiler_plant(state)\
                   or state.can_reach_region(regionName.GI3, self.player) and self.small_elevation(state) and self.leg_spring(state) and self.glide(state)\
                   or self.clockwork_shot(state)

    def jinjo_hot_pool(self, state: CollectionState) -> bool:
        if self.glitches_logic(state):
            return self.shack_pack(state) or self.dive(state) and self.tall_jump(state) and self.clockwork_eggs(state) and self.third_person_egg_shooting(state)
        else:
            return self.shack_pack(state)

    def jinjo_hot_waterfall(self, state: CollectionState) -> bool:
        if self.intended_logic(state) or self.easy_tricks_logic(state):
            return self.wonderwing(state) and self.flap_flip(state) and self.long_jump(state)
        else:
            return True

    def jinjo_wind_tunnel(self, state: CollectionState) -> bool:
        if self.intended_logic(state) or self.easy_tricks_logic(state):
            return self.humbaHFP(state)
        else:
            return self.humbaHFP(state) or self.clockwork_shot(state) and self.hfp_top(state)

    def jinjo_icicle_grotto(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.hfp_top(state) and self.glide(state) and self.grenade_eggs(state) and \
                    self.egg_aim(state) and self.tall_jump(state)
        elif self.easy_tricks_logic(state):
            return self.hfp_top(state) and (
                    self.glide(state) or (self.leg_spring(state) and self.wing_whack(state)))
        else:
            return self.hfp_top(state) and (
                   self.glide(state) or self.leg_spring(state)
                   or self.clockwork_shot(state) and ((self.tall_jump(state) and self.split_up(state)) or self.talon_trot(state)))

    def jinjo_mildred(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.hfp_top(state) and self.small_elevation(state) and (self.fire_eggs(state) or self.has_explosives(state) or
                    self.bill_drill(state) or self.dragon_kazooie(state))
        elif self.easy_tricks_logic(state):
            return self.hfp_top(state) and (
                (self.small_elevation(state) or self.beak_buster(state)) and (self.fire_eggs(state) or self.has_explosives(state) or self.bill_drill(state) or self.dragon_kazooie(state))
                or (state.has(itemName.MUMBOHP, self.player) and self.tall_jump(state))
                or self.split_up(state) and (self.tall_jump(state) and  self.leg_spring(state)) and (self.fire_eggs(state) or self.has_explosives(state)))
        else:
            return self.hfp_top(state) and (
               (self.small_elevation(state) or self.beak_buster(state)) and (self.fire_eggs(state) or self.has_explosives(state) or self.bill_drill(state) or self.dragon_kazooie(state))
               or (state.has(itemName.MUMBOHP, self.player) and self.tall_jump(state))
               or self.split_up(state) and (self.tall_jump(state) and self.leg_spring(state)) and (self.fire_eggs(state) or self.has_explosives(state))
               or self.clockwork_shot(state))

    def jinjo_trash_can(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.shack_pack(state) and self.climb(state) and self.tall_jump(state)
        elif self.easy_tricks_logic(state):
            return self.shack_pack(state) and self.climb(state) and (self.tall_jump(state) or self.pack_whack(state))\
                    or (self.flight_pad(state) or self.glide(state)) and self.leg_spring(state)
        else:
            return self.shack_pack(state) and self.climb(state) and (self.tall_jump(state) or self.pack_whack(state))\
                   or self.split_up(state)\
                       and (self.flight_pad(state) or self.glide(state) or ((self.tall_jump(state) or self.leg_spring(state)) and self.wing_whack(state)))\
                       and (self.leg_spring(state) or (self.glide(state) and self.tall_jump(state) or self.clockwork_shot(state)))

    def jinjo_cheese(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.flight_pad(state) and (self.sack_pack(state) and self.grow_beanstalk(state) and
                     self.can_use_floatus(state))
        elif self.easy_tricks_logic(state):
            return self.flight_pad(state) and ((self.sack_pack(state) and self.grow_beanstalk(state) and
                     self.can_use_floatus(state)) or self.leg_spring(state)
                     or (self.flap_flip(state) and self.beak_buster(state)))
        else:
            return self.flight_pad(state) and ((self.sack_pack(state) and self.grow_beanstalk(state) and
                    self.can_use_floatus(state)) or self.clockwork_shot(state) or self.leg_spring(state)
                    or (self.flap_flip(state) and self.beak_buster(state)))

    def jinjo_central(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.split_up(state) and self.spring_pad(state)\
                    or state.has(itemName.HUMBACC, self.player)
        elif self.easy_tricks_logic(state):
            return self.split_up(state) and (self.spring_pad(state) or self.flight_pad(state))\
                    or self.springy_step_shoes(state) and self.bill_drill(state) and (self.flutter(state) or self.air_rat_a_tat_rap(state) or self.split_up(state))\
                    or self.leg_spring(state)\
                    or state.has(itemName.HUMBACC, self.player)
        else:
            return self.split_up(state) and (self.spring_pad(state) or self.flight_pad(state))\
                   or self.clockwork_shot(state)\
                   or self.springy_step_shoes(state) and (self.flutter(state) or self.air_rat_a_tat_rap(state) or self.split_up(state))\
                       and (
                           self.bill_drill(state)
                           or not self.world.options.randomize_warp_pads.value
                           or state.has(itemName.WARPCC1, self.player) and state.has(itemName.WARPCC2, self.player)
                       )\
                   or self.leg_spring(state)\
                   or state.has(itemName.HUMBACC, self.player)

    def jinjo_humba_ccl(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.climb(state) or state.has(itemName.HUMBACC, self.player)
        elif self.easy_tricks_logic(state):
            return self.climb(state) or state.has(itemName.HUMBACC, self.player) or self.leg_spring(state)
        else:
            return self.climb(state) or state.has(itemName.HUMBACC, self.player) or self.leg_spring(state) or self.clockwork_shot(state)

    def treble_jv(self, state: CollectionState) -> bool:
        if self.intended_logic(state) or self.easy_tricks_logic(state):
            return self.grip_grab(state) and self.flap_flip(state)
        else:
            return ((self.grip_grab(state) or self.beak_buster(state)) and self.flap_flip(state))\
                    or self.clockwork_shot(state)

    def treble_gm(self, state: CollectionState) -> bool:
        if self.glitches_logic(state):
            return self.dive(state) or (self.ggm_boulders(state) and self.leg_spring(state))
        else:
            return self.dive(state)

    def treble_ww(self, state: CollectionState) -> bool:
        if self.glitches_logic(state):
            return self.humbaWW(state) or self.clockwork_eggs(state)
        else:
            return self.humbaWW(state)

    def treble_jrl(self, state: CollectionState) -> bool:
        return self.sub_aqua_egg_aiming(state) or self.talon_torpedo(state) or self.humbaJRL(state)

    def treble_tdl(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return ((self.flap_flip(state) and self.grip_grab(state)) or self.TDL_flight_pad(state)) and self.bill_drill(state)
        elif self.glitches_logic(state):
            return ((self.flap_flip(state) and (self.grip_grab(state) or self.beak_buster(state))) or self.TDL_flight_pad(state))\
                        and (self.bill_drill(state) or self.egg_barge(state) or self.ground_rat_a_tat_rap(state))\
                    or self.humbaTDL(state) and self.mumboTDL(state)
        else:
            return ((self.flap_flip(state) and (self.grip_grab(state) or self.beak_buster(state)))
                    or self.TDL_flight_pad(state)) and self.bill_drill(state)

    def treble_gi(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return state.can_reach_region(regionName.GI1, self.player) and self.split_up(state) and self.claw_clamber_boots(state)\
                    or state.can_reach_region(regionName.GIF, self.player)
        elif self.easy_tricks_logic(state):
            return state.can_reach_region(regionName.GI1, self.player) and (self.split_up(state) and self.claw_clamber_boots(state)
                    or self.leg_spring(state) and self.glide(state) and
                        (self.wing_whack(state) or self.egg_aim(state)))\
                    or state.can_reach_region(regionName.GIF, self.player)
        else:
            return state.can_reach_region(regionName.GI1, self.player) and (self.split_up(state) and self.claw_clamber_boots(state)
                       or self.leg_spring(state) and self.glide(state) and (self.wing_whack(state) or self.egg_aim(state)))\
                   or state.can_reach_region(regionName.GIF, self.player)\
                   or self.clockwork_shot(state)

    def treble_hfp(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.hfp_top(state) and self.grenade_eggs(state) and self.egg_aim(state) and self.spring_pad(state) and (self.talon_trot(state) or self.split_up(state))
        elif self.easy_tricks_logic(state):
            return (self.split_up(state) and self.ice_cube_kazooie(state) and (self.tall_jump(state) or self.wing_whack(state) or self.glide(state) or self.leg_spring(state)))\
                    or (self.hfp_top(state) and self.grenade_eggs(state) and self.egg_aim(state) and self.spring_pad(state) and (self.talon_trot(state) or self.split_up(state)))\
                    or self.claw_clamber_boots(state) and self.grenade_eggs(state) and self.egg_aim(state)
        else:
            return (self.split_up(state) and self.ice_cube_kazooie(state) and (self.tall_jump(state) or self.wing_whack(state) or self.glide(state) or self.leg_spring(state)))\
                   or (self.hfp_top(state) and (self.grenade_eggs(state) or self.clockwork_shot(state))
                       and self.egg_aim(state) and ((self.tall_jump(state) and self.split_up(state)) or self.talon_trot(state)))\
                   or (self.extremelyLongJump(state) and self.clockwork_shot(state))\
                   or self.claw_clamber_boots(state) and self.grenade_eggs(state) and self.egg_aim(state)

    def treble_ccl(self, state: CollectionState) -> bool:
        return self.notes_ccl_high(state)

    def solo_banjo_waste_disposal(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.grip_grab(state) and self.can_use_battery(state) and self.climb(state)
        else:
            return self.can_use_battery(state) and (self.grip_grab(state) and self.climb(state) or self.tall_jump(state))


    def silo_snooze(self, state: CollectionState) -> bool:
        return self.check_notes(state, locationName.SNPACK) and self.solo_banjo_waste_disposal(state)

    def tswitch_ww(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.grip_grab(state) and self.flap_flip(state)
        else:
            return self.grip_grab(state) and self.flap_flip(state)\
               or self.leg_spring(state)\
               or self.grip_grab(state) and self.pack_whack(state) and self.tall_jump(state)

    def tswitch_tdl(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.flap_flip(state)\
                    or self.very_long_jump(state)\
                    or self.TDL_flight_pad(state)\
                    or self.tall_jump(state) and self.grip_grab(state)
        else:
            return self.flap_flip(state)\
                   or self.very_long_jump(state)\
                   or self.TDL_flight_pad(state)\
                   or self.split_up(state)\
                   or self.springy_step_shoes(state)\
                   or self.tall_jump(state) and self.air_rat_a_tat_rap(state)\
                   or self.tall_jump(state) and self.grip_grab(state)

    def tswitch_gi(self, state: CollectionState) -> bool:
        if self.intended_logic(state) or self.easy_tricks_logic(state):
            return self.climb(state)
        else:
            return self.climb(state) or self.extremelyLongJump(state)

    def tswitch_lavaside(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.grip_grab(state)\
                    and (self.tall_jump(state) or self.talon_trot(state))\
                    and (self.flutter(state) or self.air_rat_a_tat_rap(state))
        elif self.easy_tricks_logic(state):
            return self.grip_grab(state)\
                        and (self.tall_jump(state) or self.talon_trot(state))\
                        and (self.flutter(state) or self.air_rat_a_tat_rap(state))\
                    or self.flight_pad(state)\
                    or self.leg_spring(state)\
                    or self.split_up(state) and self.tall_jump(state)
        else:
            return self.grip_grab(state)\
                       and (self.tall_jump(state) or self.talon_trot(state))\
                       and (self.flutter(state) or self.air_rat_a_tat_rap(state))\
                   or self.flight_pad(state)\
                   or self.leg_spring(state)\
                   or self.split_up(state) and self.tall_jump(state)\
                   or self.talon_trot(state) and self.flutter(state)

    def doubloon_ledge(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.split_up(state) and self.has_explosives(state)\
                    and self.spring_pad(state)
        elif self.easy_tricks_logic(state):
            return self.split_up(state) and self.has_explosives(state)\
                    and (self.spring_pad(state) or self.leg_spring(state))
        else:
            return self.split_up(state) and self.has_explosives(state)\
                       and (
                           self.spring_pad(state)
                           or self.leg_spring(state)
                           or self.pack_whack(state) and self.tall_jump(state) and self.grip_grab(state)
                           or self.glide(state) and self.tall_jump(state)
                           or self.wing_whack(state) and self.tall_jump(state)
                       )\
                   or self.clockwork_shot(state)

    def doubloon_dirtpatch(self, state: CollectionState) -> bool:
        return self.bill_drill(state) or self.has_explosives(state)

    def doubloon_water(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.dive(state)
        else:
            return self.dive(state) or self.shack_pack(state) and self.has_explosives(state)

    def notes_plateau_sign(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.grip_grab(state) and self.flap_flip(state)
        elif self.easy_tricks_logic(state):
            return (self.grip_grab(state) or self.beak_buster(state)) and self.flap_flip(state)\
                    or self.leg_spring(state)\
                    or self.split_up(state) and self.tall_jump(state)\
                    or self.glide(state)
        else:
            return ((self.grip_grab(state) or self.beak_buster(state)) and self.flap_flip(state))\
                   or self.clockwork_shot(state)\
                   or self.leg_spring(state)\
                   or self.split_up(state) and self.grip_grab(state)\
                   or self.split_up(state) and self.tall_jump(state)\
                   or self.glide(state)

    def can_reach_honey_b(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.talon_trot(state)
        else:
            return self.talon_trot(state)\
                   or state.can_reach_region(regionName.IOHCT, self.player) and self.claw_clamber_boots(state)

    def notes_ww_area51_right(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.has_explosives(state) and self.spring_pad(state)
        elif self.easy_tricks_logic(state):
            return self.has_explosives(state) and self.spring_pad(state)\
                    or self.leg_spring(state)\
                    or self.glide(state)
        else:
            return ((self.has_explosives(state) or self.split_up(state)) and self.spring_pad(state))\
                   or self.leg_spring(state)\
                   or self.clockwork_shot(state)\
                   or self.glide(state)

    def notes_ww_area51_left(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.has_explosives(state) and self.spring_pad(state) and self.long_jump(state)
        elif self.easy_tricks_logic(state):
            return self.has_explosives(state) and self.spring_pad(state) and self.long_jump(state)\
                    or self.leg_spring(state)\
                    or self.glide(state)
        else:
            return self.has_explosives(state) and self.spring_pad(state) and self.long_jump(state)\
                   or self.split_up(state) and self.spring_pad(state)\
                   or self.leg_spring(state)\
                   or self.clockwork_shot(state)\
                   or self.glide(state)

    def notes_dive_of_death(self, state: CollectionState) -> bool:
        logic = True
        if self.intended_logic(state):
            logic = ((self.grip_grab(state) and self.flap_flip(state)) or self.climb(state)) and self.dive(state)
        elif self.easy_tricks_logic(state):
            logic = ((self.grip_grab(state) or self.beak_buster(state)) and self.flap_flip(state) or self.climb(state))\
                        and (self.tall_jump(state) or self.dive(state))\
                    or (self.leg_spring(state) or self.glide(state)) and self.tall_jump(state)
        elif self.hard_tricks_logic(state):
            logic = (self.grip_grab(state) or self.beak_buster(state)) and self.flap_flip(state)\
                    or self.climb(state)\
                    or self.leg_spring(state)\
                    or self.glide(state)
        elif self.glitches_logic(state):
            logic = (self.grip_grab(state) or self.beak_buster(state)) and self.flap_flip(state)\
                    or self.climb(state)\
                    or self.ground_rat_a_tat_rap(state)\
                    or self.beak_barge(state)\
                    or self.leg_spring(state)\
                    or self.glide(state)\
                    or self.pack_whack(state)\
                    or self.taxi_pack(state)
        return logic

    def notes_bottom_clockwork(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.small_elevation(state)
        else:
            return True

    def notes_top_clockwork(self, state: CollectionState) -> bool:
        if self.hard_tricks_logic(state):
            return (self.flap_flip(state) or
                    (self.tall_jump(state) or (self.talon_trot(state) and self.flutter(state)))
                        and self.grip_grab(state))\
                    or self.clockwork_shot(state)
        elif self.glitches_logic(state):
            return (self.flap_flip(state) or
                        (self.tall_jump(state) or (self.talon_trot(state) and self.flutter(state)))
                        and self.grip_grab(state))\
                        or self.clockwork_shot(state)
        else:
            return self.flap_flip(state) or \
                   (self.tall_jump(state) or (self.talon_trot(state) and self.flutter(state)))\
                       and self.grip_grab(state)

    def notes_green_pile(self, state: CollectionState) -> bool:
        if self.intended_logic(state) or self.easy_tricks_logic(state):
            return self.GGM_slope(state)
        else:
            return self.GGM_slope(state) or self.clockwork_shot(state)

    def notes_prospector_easy(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.GGM_slope(state)\
                    or self.flap_flip(state)\
                    or (self.mt_jiggy(state) and self.dilberta_free(state))\
                    or self.tall_jump(state) and self.grip_grab(state)
        else:
            return True

    def notes_prospector_hard(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.GGM_slope(state) or self.flap_flip(state) or (self.mt_jiggy(state) and self.dilberta_free(state))
        else:
            return True

    def notes_gm_mumbo_easy(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.small_elevation(state) or self.warp_to_ggm_mumbo(state)
        elif self.easy_tricks_logic(state):
            return self.small_elevation(state) or self.grip_grab(state) or self.beak_buster(state) or self.ggm_trot(state) or self.warp_to_ggm_mumbo(state)
        else:
            return self.small_elevation(state) or self.grip_grab(state) or self.clockwork_shot(state) or self.beak_buster(state) or self.ggm_trot(state) or self.warp_to_ggm_mumbo(state)

    def notes_gm_mumbo_hard(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.small_elevation(state)
        elif self.easy_tricks_logic(state):
            return self.small_elevation(state) or self.grip_grab(state) or self.beak_buster(state) or self.ggm_trot(state)
        else:
            return self.small_elevation(state) or self.grip_grab(state) or self.clockwork_shot(state) or self.beak_buster(state) or self.ggm_trot(state)

    def notes_easy_fuel_depot(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.small_elevation(state)
        else:
            return True

    def notes_hard_fuel_depot(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.small_elevation(state)
        elif self.easy_tricks_logic(state):
            return self.small_elevation(state) or self.ggm_trot(state) or self.beak_buster(state)
        else:
            return self.small_elevation(state) or self.ggm_trot(state) or self.clockwork_shot(state) or self.beak_buster(state) or self.air_rat_a_tat_rap(state)

    def notes_jrl_blubs(self, state: CollectionState) -> bool:
        return self.sub_aqua_egg_aiming(state) or self.talon_torpedo(state) or self.humbaJRL(state)

    def notes_jrl_eels(self, state: CollectionState) -> bool:
        return True

    def notes_jolly(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.talon_trot(state) or (self.tall_jump(state) and self.grip_grab(state))\
                or self.flap_flip(state)
        elif self.easy_tricks_logic(state):
            return self.small_elevation(state) or self.long_jump(state) or self.roll(state)
        else:
            return self.small_elevation(state) or self.long_jump(state) or self.clockwork_shot(state) or self.roll(state)

    def notes_river_passage(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.dive(state)
        else:
            return self.dive(state) or self.humbaTDL(state) or self.shack_pack(state)

    def notes_tdl_station_right(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.small_elevation(state)\
                    or self.humbaTDL(state)
        elif self.easy_tricks_logic(state):
            return self.small_elevation(state)\
                    or self.humbaTDL(state)\
                    or self.split_up(state)\
                    or self.springy_step_shoes(state)\
                    or self.turbo_trainers(state)
        else:
            return self.small_elevation(state)\
                   or self.humbaTDL(state)\
                   or self.split_up(state)\
                   or self.springy_step_shoes(state)\
                   or self.turbo_trainers(state)\
                   or self.clockwork_shot(state)

    def notes_roar_cage(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.long_jump(state)\
                    or self.springy_step_shoes(state)\
                    or self.TDL_flight_pad(state)\
                    or self.humbaTDL(state) and self.roar(state)
        else:
            return self.long_jump(state)\
                   or self.springy_step_shoes(state)\
                   or self.TDL_flight_pad(state)\
                   or self.humbaTDL(state) and self.roar(state)\
                   or self.split_up(state)

    def notes_gi_floor1(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.grip_grab(state) and self.climb(state) and self.flap_flip(state)
        elif self.easy_tricks_logic(state):
            return self.F1_to_F2(state)\
                or (self.grip_grab(state) and self.climb(state) and self.flap_flip(state))
        else:
            return self.claw_clamber_boots(state)\
                   or (self.grip_grab(state) and self.climb(state) and self.flap_flip(state))\
                   or self.pack_whack(state) and self.tall_jump(state) and self.climb(state)\
                   or self.leg_spring(state)\
                   or self.clockwork_shot(state)

    def notes_gi_train_station_easy(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.small_elevation(state) or self.leg_spring(state) or self.grip_grab(state)
        elif self.easy_tricks_logic(state):
            return self.small_elevation(state) or self.leg_spring(state) or self.beak_buster(state) or self.grip_grab(state)
        else:
            return True

    def notes_gi_train_station_hard(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.small_elevation(state) or self.leg_spring(state)
        elif self.easy_tricks_logic(state):
            return self.small_elevation(state) or self.leg_spring(state) or self.beak_buster(state)
        else:
            return True

    def notes_aircon_hard(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.tall_jump(state) or self.split_up(state) or self.talon_trot(state)
        else:
            return True

    def notes_leg_spring(self, state: CollectionState) -> bool:
        if self.intended_logic(state) or self.easy_tricks_logic(state):
            return (self.climb(state) or (self.has_explosives(state) and self.small_elevation(state)))
        else:
            return (self.climb(state) or (self.has_explosives(state) and self.small_elevation(state)))\
                    or self.clockwork_shot(state)\
                    or self.claw_clamber_boots(state) and self.extremelyLongJump(state)

    def notes_short_stack(self, state: CollectionState) -> bool:
        if self.intended_logic(state) or self.easy_tricks_logic(state):
            return self.small_elevation(state)
        else:
            return True

    def notes_waste_disposal(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.can_use_battery(state) and (self.grip_grab(state) and self.climb(state))
        elif self.glitches_logic(state):
            return (self.can_use_battery(state) and (self.grip_grab(state) and self.climb(state) or self.tall_jump(state)))\
                    or self.clockwork_shot(state) and self.flap_flip(state)
        else:
            return self.can_use_battery(state) and (self.grip_grab(state) and self.climb(state) or self.tall_jump(state))

    def notes_floor_3(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.climb(state) and self.talon_trot(state) and self.flutter(state) and self.grip_grab(state)\
                    or self.floor_3_split_up(state) and self.leg_spring(state)\
                    or (self.grip_grab(state) and self.flap_flip(state) or self.split_up(state)) and self.spring_pad(state) and self.climb(state)
        elif self.easy_tricks_logic(state):
            return ((self.grip_grab(state) and self.flap_flip(state) or self.split_up(state)) and self.spring_pad(state) and self.climb(state))\
                    or (self.climb(state) or self.enter_floor_3_from_fire_exit(state)) and self.talon_trot(state) and self.flutter(state) and self.grip_grab(state)\
                    or self.floor_3_split_up(state) and self.leg_spring(state)
        else:
            return ((self.grip_grab(state) and self.flap_flip(state) or self.split_up(state)) and self.spring_pad(state) and self.climb(state))\
                   or (self.climb(state) or self.enter_floor_3_from_fire_exit(state))\
                       and self.talon_trot(state) and (
                           self.flutter(state) and self.grip_grab(state)
                           or self.flutter(state) and self.beak_buster(state)
                           or self.air_rat_a_tat_rap(state)
                       )\
                   or self.clockwork_shot(state)\
                   or self.small_elevation(state) and self.leg_spring(state)\
                   or self.floor_3_split_up(state) and self.tall_jump(state) and (self.wing_whack(state) or self.glide(state))\
                   or self.sack_pack(state) and self.floor_3_split_up(state)

    def notes_oil_drill(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return  self.hfp_top(state) and (self.flap_flip(state) or self.talon_trot(state)) and self.ice_cube_BK(state)\
                    or self.hfp_top(state) and self.split_up(state) and self.grip_grab(state) and self.pack_whack(state)\
                    or self.hfp_top(state) and self.split_up(state) and self.ice_cube_kazooie(state)
        elif self.easy_tricks_logic(state):
            return self.hfp_top(state) and (self.flap_flip(state) or self.talon_trot(state) or self.flight_pad(state)) and self.ice_cube_BK(state)\
                    or self.hfp_top(state) and self.split_up(state) and (self.grip_grab(state) or self.tall_jump(state)) and self.pack_whack(state)\
                    or self.hfp_top(state) and self.split_up(state) and self.ice_cube_kazooie(state)\
                    or self.humbaHFP(state)\
                    or self.hfp_top(state) and self.claw_clamber_boots(state)
        else:
            return self.hfp_top(state) and (self.flap_flip(state) or self.talon_trot(state) or self.flight_pad(state)) and self.ice_cube_BK(state)\
                   or self.hfp_top(state) and self.split_up(state) and (self.grip_grab(state) or self.tall_jump(state)) and self.pack_whack(state)\
                   or self.hfp_top(state) and self.split_up(state) and self.ice_cube_kazooie(state)\
                   or self.humbaHFP(state)\
                   or self.hfp_top(state) and self.clockwork_shot(state)\
                   or self.hfp_top(state) and self.claw_clamber_boots(state)

    def notes_ladder(self, state: CollectionState) -> bool:
        if self.intended_logic(state) or self.easy_tricks_logic(state):
            return self.hfp_top(state) or self.split_up(state)
        else:
            return self.hfp_top(state)

    def notes_ccl_silo(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.can_access_sack_pack_silo(state)
        else:
            return self.can_access_sack_pack_silo(state)\
                   or self.clockwork_eggs(state)

    def notes_cheese(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return (self.climb(state) and self.sack_pack(state))\
                    or self.notes_ccl_high(state)
        elif self.easy_tricks_logic(state):
            return (self.climb(state) and self.sack_pack(state))\
                    or self.notes_ccl_high(state)\
                    or self.springy_step_shoes(state) and self.split_up(state)\
                    or self.claw_clamber_boots(state) and self.glide(state)
        else:
            return self.climb(state)\
                   or (self.springy_step_shoes(state))\
                   or self.notes_ccl_high(state)\
                   or self.clockwork_shot(state)\
                   or self.springy_step_shoes(state) and self.split_up(state)\
                   or self.claw_clamber_boots(state) and self.glide(state)

    def notes_ccl_high(self, state: CollectionState) -> bool:
        return self.flight_pad(state) or state.has(itemName.HUMBACC, self.player)

    def notes_sack_race(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.flight_pad(state)\
                    or self.long_jump(state) and self.climb(state)\
                    or state.has(itemName.HUMBACC, self.player)
        elif self.easy_tricks_logic(state):
            return self.flight_pad(state)\
                    or self.climb(state) and (self.long_jump(state) or self.grip_grab(state) or self.pack_whack(state) or self.sack_pack(state))\
                    or state.has(itemName.HUMBACC, self.player)\
                    or self.claw_clamber_boots(state)
        else:
            return self.flight_pad(state)\
                   or self.climb(state) and (self.long_jump(state) or self.grip_grab(state) or self.pack_whack(state) or self.sack_pack(state))\
                   or self.leg_spring(state) and (self.glide(state) or self.wing_whack(state))\
                   or state.has(itemName.HUMBACC, self.player)\
                   or self.claw_clamber_boots(state)

    def glowbo_icy_side(self, state: CollectionState) -> bool:
        if self.intended_logic(state) or self.easy_tricks_logic(state):
            return self.hfp_top(state)\
                   and (self.long_jump(state)
                   or self.flap_flip(state) and self.grip_grab(state))
        else:
            return self.hfp_top(state)

    def ccl_glowbo_pool(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.dive(state)
        else:
            return True # Jumping in the pool outside and going through the loading zone gives dive for free.

    def notes_ccl_low(self, state: CollectionState) -> bool:
        return True

    def notes_dippy(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.dive(state)
        elif self.easy_tricks_logic(state):
            return self.dive(state) or self.shack_pack(state)
        else:
            return True

    def check_solo_moves(self, state: CollectionState, name) -> bool:
        for item_name in self.solo_moves:
            if name == item_name:
                return state.has(name, self.player) and self.split_up(state)
        return False

    def check_notes(self, state: CollectionState, silo: str) -> bool:
        amount = self.world.jamjars_siloname_costs[silo]
        count: int = 0
        count = state.count(itemName.TREBLE, self.player) * 20
        count += state.count(itemName.BASS, self.player) * 10
        count += state.count(itemName.NOTE, self.player) * 5
        return count >= amount

    def silo_bill_drill(self, state: CollectionState) -> bool:
        if self.intended_logic(state) or self.easy_tricks_logic(state):
            return self.check_notes(state, locationName.BDRILL)\
                   and (self.flap_flip(state)
                        or (self.tall_jump(state) or self.talon_trot(state) and self.flutter(state)) and self.grip_grab(state))
        else:
            return self.check_notes(state, locationName.BDRILL)\
                    and (self.flap_flip(state)
                        or (self.tall_jump(state) or self.talon_trot(state) and self.flutter(state)) and self.grip_grab(state)
                        or self.turbo_trainers(state))

    def silo_spring(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.flap_flip(state) and self.grip_grab(state)\
                    or self.TDL_flight_pad(state)
        else:
            return self.flap_flip(state) and (self.grip_grab(state) or self.beak_buster(state))\
                   or self.TDL_flight_pad(state)\
                   or self.very_long_jump(state)\
                   or self.turbo_trainers(state)\
                   or self.springy_step_shoes(state)

    def can_access_talon_torpedo_silo(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.grip_grab(state) and self.tall_jump(state)
        else:
            return (self.grip_grab(state) or self.beak_buster(state)) and self.tall_jump(state)

    def can_access_taxi_pack_silo(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.split_up(state) and (self.tall_jump(state) and (self.grip_grab(state) or self.sack_pack(state)))
        elif self.hard_tricks_logic(state):
            return self.split_up(state) and\
                        (self.tall_jump(state) and self.grip_grab(state)
                        or self.pack_whack(state) and self.tall_jump(state)
                        or self.pack_whack(state) and self.grip_grab(state)
                        or self.sack_pack(state))
        else:
            return self.split_up(state) and\
                       (self.tall_jump(state) and self.grip_grab(state) or
                       self.pack_whack(state) and self.tall_jump(state)
                       or self.pack_whack(state) and self.grip_grab(state)
                       or self.sack_pack(state))

    def can_access_glide_silo(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            # Through icicle grotto
            return self.hfp_top(state) and self.split_up(state) and self.grenade_eggs(state) and self.egg_aim(state) and self.spring_pad(state)
        else:
            return self.split_up(state) and (self.tall_jump(state) or self.wing_whack(state) or self.glide(state) or self.leg_spring(state))

    def can_access_sack_pack_silo(self, state: CollectionState) -> bool:
        return self.shack_pack(state) and (
                   state.has(itemName.WARPCC1, self.player) and state.has(itemName.WARPCC2, self.player)
                   or self.can_use_floatus(state)
               )

    def nest_lair_top(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.small_elevation(state)
        elif self.easy_tricks_logic(state):
            return self.small_elevation(state) or self.grip_grab(state) or self.beak_buster(state)
        else:
            return self.small_elevation(state)\
                   or self.grip_grab(state)\
                   or self.beak_buster(state)\
                   or self.air_rat_a_tat_rap(state)\
                   or self.flutter(state)\
                   or self.clockwork_shot(state)

    def SM_to_GL(self, state: CollectionState) -> bool:
        if self.intended_logic(state) or self.easy_tricks_logic(state):
            return self.flight_pad(state) or self.flap_flip(state) and self.climb(state)
        else:
            return self.flight_pad(state)\
                    or self.flap_flip(state) and self.climb(state)\
                    or (self.tall_jump(state) or self.talon_trot(state) and self.flutter(state)) and self.beak_buster(state) and self.climb(state)

    def nest_sm_waterfall_top(self, state: CollectionState) -> bool:
        return self.flight_pad(state)

    def nest_sm_waterfall_platform(self, state: CollectionState) -> bool:
        if self.intended_logic(state) or self.easy_tricks_logic(state):
            return self.flight_pad(state)\
                   or self.small_elevation(state)\
                   or self.air_rat_a_tat_rap(state)\
                   or self.flutter(state)\
                   or self.flap_flip(state)\
                   or self.grip_grab(state)
        else:
            return self.flight_pad(state)\
                    or self.small_elevation(state)\
                    or self.air_rat_a_tat_rap(state)\
                    or self.flutter(state)\
                    or self.flap_flip(state)\
                    or self.grip_grab(state)\
                    or self.clockwork_shot(state)

    def nest_bottles_house(self, state: CollectionState) -> bool:
        if self.intended_logic(state) or self.easy_tricks_logic(state):
            return self.small_elevation(state) or self.grip_grab(state)
        else:
            return self.small_elevation(state) or self.grip_grab(state) or self.clockwork_shot(state)

    def nest_pl_dirt_pile(self, state: CollectionState) -> bool:
        return self.plateau_top(state)

    def nest_cliff_top_hard(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.small_elevation(state) or self.grip_grab(state)
        elif self.easy_tricks_logic(state):
            return self.small_elevation(state)\
                    or self.grip_grab(state)\
                    or self.beak_buster(state)\
                    or self.claw_clamber_boots(state)\
                    or self.air_rat_a_tat_rap(state)
        else:
            return self.small_elevation(state)\
                   or self.grip_grab(state)\
                   or self.clockwork_shot(state)\
                   or self.beak_buster(state)\
                   or self.flutter(state)\
                   or self.claw_clamber_boots(state)\
                   or self.air_rat_a_tat_rap(state)

    def nest_another_digger_tunnel(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.dive(state)
        else:
            return self.dive(state) or self.beak_buster(state)

    def nest_quagmire_hard(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.small_elevation(state)
        elif self.easy_tricks_logic(state):
            return self.small_elevation(state) or self.beak_buster(state) or self.claw_clamber_boots(state)
        else:
            return self.small_elevation(state) or self.clockwork_shot(state) or self.beak_buster(state) or self.claw_clamber_boots(state)

    def nest_quagmire_easy(self, state: CollectionState) -> bool:
        return True

    def nest_quagmire_medium(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.small_elevation(state)
        elif self.easy_tricks_logic(state):
            return self.small_elevation(state) or self.air_rat_a_tat_rap(state) or self.beak_buster(state) or self.claw_clamber_boots(state)
        else:
            return self.small_elevation(state) or self.air_rat_a_tat_rap(state) or self.clockwork_shot(state) or self.beak_buster(state) or self.claw_clamber_boots(state)

    def nest_mt_stadium(self, state: CollectionState) -> bool:
        if self.intended_logic(state) or self.easy_tricks_logic(state):
            return self.MT_flight_pad(state)
        else:
            return self.MT_flight_pad(state) or self.clockwork_shot(state)

    def nest_pillars(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return (self.dive(state) or self.slightly_elevated_ledge(state) and self.tall_jump(state)) and self.prison_compound_as_banjo(state)\
                    or self.prison_compound_as_stony(state)
        elif self.easy_tricks_logic(state):
            return (self.dive(state) or self.slightly_elevated_ledge(state) or self.beak_buster(state)) and self.prison_compound_as_banjo(state)\
                    or self.prison_compound_as_stony(state)
        else:
            return (self.dive(state)
                   or self.slightly_elevated_ledge(state)
                   or self.beak_buster(state)
                   or self.clockwork_shot(state)) and self.prison_compound_as_banjo(state)\
                   or self.prison_compound_as_stony(state)

    def nest_mt_cell_left(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return (self.slightly_elevated_ledge(state) or self.flap_flip(state)) and self.tall_jump(state) and self.prison_compound_as_banjo(state)
        elif self.easy_tricks_logic(state):
            return (self.slightly_elevated_ledge(state) or self.flap_flip(state)) and self.prison_compound_as_banjo(state)
        else:
            return self.prison_compound_as_banjo(state) and (self.slightly_elevated_ledge(state) or self.flap_flip(state) or self.clockwork_shot(state) and self.tall_jump(state))

    def nest_mt_cell_right(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return (self.slightly_elevated_ledge(state) or self.flap_flip(state)) and self.tall_jump(state) and self.prison_compound_as_banjo(state)
        elif self.easy_tricks_logic(state):
            return (self.slightly_elevated_ledge(state) or self.flap_flip(state)) and self.prison_compound_as_banjo(state)
        else:
            return self.prison_compound_as_banjo(state) and (self.slightly_elevated_ledge(state) or self.flap_flip(state) or self.clockwork_shot(state))

    def nest_code_chamber(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.talon_trot(state)
        else:
            return True

    def nest_bill_drill(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.slightly_elevated_ledge(state) or self.flap_flip(state)
        elif self.easy_tricks_logic(state):
            return ((self.talon_trot(state) or self.springy_step_shoes(state) or self.turbo_trainers(state)) and (self.flutter(state) or self.air_rat_a_tat_rap(state)) or self.tall_jump(state)) and self.grip_grab(state)\
                    or self.flap_flip(state)\
                    or self.ggm_boulders(state) and self.split_up(state)\
                    or self.humbaGGM(state)
        else:
            return ((self.talon_trot(state) or self.springy_step_shoes(state)) and (self.flutter(state) or self.air_rat_a_tat_rap(state)) or self.tall_jump(state)) and self.grip_grab(state)\
                   or self.flap_flip(state)\
                   or self.turbo_trainers(state)\
                   or self.clockwork_shot(state)\
                   or self.ggm_boulders(state) and self.split_up(state)\
                   or self.humbaGGM(state)

    def nest_flooded_caves(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.humbaGGM(state) and self.dive(state)
        else:
            return self.dive(state)\
                   and (self.humbaGGM(state)
                       or self.talon_trot(state) and (self.flutter(state) or self.air_rat_a_tat_rap(state))
                       or self.roll(state) and self.tall_jump(state)
                           and (self.flutter(state) or self.air_rat_a_tat_rap(state)) and self.reach_waterfall_cavern_gate(state)
                   )

    def nest_outside_power_hut(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.ggm_boulders(state) and self.small_elevation(state)
        elif self.easy_tricks_logic(state):
            return self.ggm_boulders(state) and (
                        self.small_elevation(state)
                        or self.beak_buster(state)
                        or self.turbo_trainers(state)
                        or self.split_up(state))
        else:
            return self.ggm_boulders(state) and (
                       self.small_elevation(state)
                       or self.beak_buster(state)
                       or self.turbo_trainers(state)
                       or self.split_up(state)
                       or self.clockwork_shot(state)
                   )

    def nest_ggm_mumbo(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.small_elevation(state)
        elif self.easy_tricks_logic(state):
            return self.small_elevation(state) or self.grip_grab(state) or self.beak_buster(state)
        else:
            return self.small_elevation(state) or self.grip_grab(state) or self.clockwork_shot(state) or self.beak_buster(state)

    def nest_toxic_gas_cave(self, state: CollectionState) -> bool:
        if self.glitches_logic(state):
            return self.ggm_boulders(state) or self.ground_rat_a_tat_rap(state) or self.beak_barge(state) or self.egg_barge(state)
        else:
            return self.ggm_boulders(state)

    def nest_canary_low(self, state: CollectionState) -> bool:
        return self.humbaGGM(state)

    def nest_canary_high(self, state: CollectionState) -> bool:
        if self.intended_logic(state) or self.easy_tricks_logic(state):
            return self.humbaGGM(state) and (self.small_elevation(state) or self.grip_grab(state))
        else:
            return self.humbaGGM(state) and (self.small_elevation(state) or self.grip_grab(state) or self.clockwork_shot(state))

    def nest_pump_room(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return (self.flap_flip(state)
                        or self.leg_spring(state)
                        or self.split_up(state) and self.grip_grab(state)
                    ) and self.has_explosives(state)
        elif self.easy_tricks_logic(state):
            return (self.flap_flip(state)
                        or self.leg_spring(state)
                        or self.split_up(state) and self.grip_grab(state)
                        or self.pack_whack(state) and self.tall_jump(state)
                    ) and self.has_explosives(state)
        else:
            return (self.flap_flip(state)
                   or self.leg_spring(state)
                   or self.split_up(state) and self.grip_grab(state)
                   or self.pack_whack(state) and self.tall_jump(state)
                   or self.clockwork_shot(state) and (self.small_elevation(state) or self.grip_grab(state) or self.beak_buster(state))
                   ) and self.has_explosives(state)

    def has_enough_bigtop_tickets(self, state: CollectionState) -> bool:
        if self.world.options.randomize_tickets.value:
            return state.has(itemName.BTTICKET, self.player, 4)
        else:
            return self.can_kill_fruity(state)

    def can_enter_big_top(self, state: CollectionState) -> bool:
        return self.grenade_eggs_item(state) and self.airborne_egg_aiming(state) and self.has_enough_bigtop_tickets(state)

    def nest_jolly_gunpowder(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.dive(state) or self.grenade_eggs(state)
        else:
            return self.dive(state) or self.has_explosives(state)

    def nest_seaweed_bottom(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.flap_flip(state)
        elif self.easy_tricks_logic(state):
            return self.flap_flip(state)\
                    or self.tall_jump(state) and self.beak_buster(state)
        else:
            return self.flap_flip(state)\
                   or self.clockwork_shot(state)\
                   or self.tall_jump(state) and self.beak_buster(state)

    def nest_seaweed_others(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.can_climb_seaweed(state)
        elif self.easy_tricks_logic(state):
            return self.can_climb_seaweed(state)\
                    or state.can_reach_region(regionName.JRBFC, self.player) and (self.flutter(state) or self.air_rat_a_tat_rap(state))
        else:
            return self.can_climb_seaweed(state)\
                   or state.can_reach_region(regionName.JRBFC, self.player) and (
                       self.flutter(state) or self.air_rat_a_tat_rap(state)
                       or self.clockwork_shot(state)
                   )

    def nest_seaweed_top(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.grip_grab(state) and self.flap_flip(state) and (
                        self.can_climb_seaweed(state)
                        or state.can_reach_region(regionName.JRBFC, self.player)
                    )
        elif self.easy_tricks_logic(state):
            return (self.grip_grab(state) or self.beak_buster(state)) and self.flap_flip(state)\
                    and (
                        self.can_climb_seaweed(state)
                        or state.can_reach_region(regionName.JRBFC, self.player)
                    )
        else:
            return ((self.grip_grab(state) or self.beak_buster(state)) and self.flap_flip(state)
                       or self.clockwork_shot(state))\
                   and (
                       self.can_climb_seaweed(state)
                       or state.can_reach_region(regionName.JRBFC, self.player)
                   )

    def nest_big_fish_cavern(self, state: CollectionState) -> bool:
        return self.can_climb_seaweed(state) or state.can_reach_region(regionName.JRBFC, self.player)

    def nest_bacon(self, state: CollectionState) -> bool:
        return self.sub_aqua_egg_aiming(state) and self.has_linear_egg(state)\
               or self.humbaJRL(state)

    def nest_lord_woo(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return (state.has(itemName.MUMBOJR, self.player) or self.humbaJRL(state))\
                        and self.grenade_eggs_item(state) and self.sub_aqua_egg_aiming(state)
        elif self.easy_tricks_logic(state):
            return (state.has(itemName.MUMBOJR, self.player) or self.doubleAir(state) or self.humbaJRL(state))\
                        and self.grenade_eggs_item(state) and self.sub_aqua_egg_aiming(state)
        else:
            return self.grenade_eggs_item(state) and self.sub_aqua_egg_aiming(state)

    def nest_tdl_waterfall_alcove(self, state: CollectionState) -> bool:
        logic = True
        if self.intended_logic(state):
            logic = self.flap_flip(state) and self.grip_grab(state)
        elif self.easy_tricks_logic(state):
            logic = self.flap_flip(state) and self.grip_grab(state)\
                    or self.flutter(state)\
                    or self.air_rat_a_tat_rap(state)\
                    or self.split_up(state)\
                    or self.humbaTDL(state) and self.roar(state)
        elif self.hard_tricks_logic(state):
            logic = self.flap_flip(state) and self.grip_grab(state)\
                    or self.flutter(state)\
                    or self.air_rat_a_tat_rap(state)\
                    or self.split_up(state)\
                    or self.humbaTDL(state) and self.roar(state)\
                    or self.clockwork_shot(state)\
                    or self.talon_trot(state)\
                    or self.turbo_trainers(state)\
                    or state.can_reach_region(regionName.TLTOP, self.player)\
                    or self.springy_step_shoes(state)
        elif self.glitches_logic(state):
            logic = self.flap_flip(state) and self.grip_grab(state)\
                    or self.flutter(state)\
                    or self.air_rat_a_tat_rap(state)\
                    or self.split_up(state)\
                    or self.humbaTDL(state) and self.roar(state)\
                    or self.clockwork_shot(state)\
                    or self.talon_trot(state)\
                    or self.turbo_trainers(state)\
                    or self.springy_step_shoes(state)\
                    or state.can_reach_region(regionName.TLTOP, self.player)\
                    or self.humbaTDL(state) and self.mumboTDL(state)
        return logic

    def enter_tdl_train_station(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.small_elevation(state)\
                    or state.can_reach_region(regionName.CHUFFY, self.player) and state.has(itemName.TRAINSWTD, self.player) and self.can_beat_king_coal(state)
        elif self.easy_tricks_logic(state):
            return self.small_elevation(state)\
                    or self.turbo_trainers(state)\
                    or self.springy_step_shoes(state)\
                    or self.beak_buster(state)\
                    or state.can_reach_region(regionName.CHUFFY, self.player) and state.has(itemName.TRAINSWTD, self.player) and self.can_beat_king_coal(state)
        else:
            return True

    def nest_tdl_wall_with_holes(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.talon_trot(state) or self.tall_jump(state) and self.grip_grab(state)
        elif self.easy_tricks_logic(state):
            return self.talon_trot(state)\
                    or self.tall_jump(state) and self.grip_grab(state)\
                    or self.humbaTDL(state)\
                    or self.leg_spring(state)\
                    or self.glide(state)\
                    or self.pack_whack(state)\
                    or self.springy_step_shoes(state)\
                    or self.turbo_trainers(state)
        else:
            return self.talon_trot(state)\
                   or self.tall_jump(state) and self.grip_grab(state)\
                   or self.humbaTDL(state)\
                   or self.leg_spring(state)\
                   or self.glide(state)\
                   or self.pack_whack(state)\
                   or self.sack_pack(state)\
                   or self.springy_step_shoes(state)\
                   or self.turbo_trainers(state)\
                   or self.clockwork_shot(state)

    def nest_river_passage_entrance(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.tall_jump(state) or self.grip_grab(state)
        elif self.easy_tricks_logic(state):
            return self.tall_jump(state)\
                    or self.grip_grab(state)\
                    or self.pack_whack(state)\
                    or self.wing_whack(state)\
                    or self.glide(state)
        else:
            return self.tall_jump(state)\
                   or self.grip_grab(state)\
                   or self.pack_whack(state)\
                   or self.wing_whack(state)\
                   or self.glide(state)\
                   or self.clockwork_shot(state)

    def nest_mountain_flight_pad(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.tall_jump(state) or self.grip_grab(state)
        elif self.easy_tricks_logic(state):
            return self.tall_jump(state)\
                    or self.grip_grab(state)\
                    or self.beak_buster(state)\
                    or self.leg_spring(state) and self.glide(state)\
                    or state.can_reach_region(regionName.TLTOP, self.player) and self.split_up(state)
        else:
            return self.tall_jump(state)\
                   or self.grip_grab(state)\
                   or self.beak_buster(state)\
                   or self.leg_spring(state) and self.glide(state)\
                   or state.can_reach_region(regionName.TLTOP, self.player) and self.split_up(state)\
                   or self.clockwork_shot(state)

    def nest_mountain_underwater(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.dive(state)
        else:
            return self.dive(state) or self.humbaTDL(state) or self.shack_pack(state)

    def nest_river_passage(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.tall_jump(state) and self.grip_grab(state) and (self.flap_flip(state) or self.split_up(state))
        elif self.easy_tricks_logic(state):
            return self.tall_jump(state) and self.grip_grab(state) and (self.flap_flip(state) or self.split_up(state))\
                    or self.leg_spring(state) and self.glide(state)\
                    or self.pack_whack(state) and self.tall_jump(state)\
                    or self.pack_whack(state) and self.grip_grab(state)\
                    or self.sack_pack(state)\
                    or self.split_up(state) and self.tall_jump(state)
        else:
            return self.tall_jump(state) and self.grip_grab(state) and (self.flap_flip(state) or self.split_up(state))\
                   or self.leg_spring(state) and self.glide(state)\
                   or self.pack_whack(state) and self.tall_jump(state)\
                   or self.pack_whack(state) and self.grip_grab(state)\
                   or self.sack_pack(state)\
                   or self.clockwork_shot(state)\
                   or self.split_up(state) and self.tall_jump(state)

    def nest_unga_egg(self, state: CollectionState) -> bool:
        return state.can_reach_region(regionName.MT, self.player) and self.jiggy_treasure_chamber(state)\
               or self.small_elevation(state)

    def nest_gi_outside_right(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return state.can_reach_region(regionName.GIO, self.player) and self.outside_gi_to_outside_back(state)\
                    or state.can_reach_region(regionName.GIOB, self.player) and self.climb(state)
        elif self.easy_tricks_logic(state):
            return state.can_reach_region(regionName.GIO, self.player) and self.outside_gi_to_outside_back(state)\
                    or state.can_reach_region(regionName.GIOB, self.player) and self.climb(state)\
                    or state.can_reach_region(regionName.GI1, self.player) and (self.split_up(state) and self.tall_jump(state) or self.leg_spring(state))\
                    or state.can_reach_region(regionName.GI2, self.player) and (self.floor_2_split_up(state) and (self.tall_jump(state) or self.leg_spring(state)))\
                    or state.can_reach_region(regionName.GIF, self.player)
        else:
            return state.can_reach_region(regionName.GIO, self.player) and self.outside_gi_to_outside_back(state)\
                   or state.can_reach_region(regionName.GIOB, self.player) and self.climb(state)\
                   or state.can_reach_region(regionName.GI1, self.player) and (self.split_up(state) and self.tall_jump(state) or self.leg_spring(state))\
                   or state.can_reach_region(regionName.GI2, self.player) and (self.floor_2_split_up(state) and (self.tall_jump(state) or self.leg_spring(state)))\
                   or state.can_reach_region(regionName.GIF, self.player)\
                   or self.clockwork_shot(state)

    def nest_gi_outside_left(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.climb(state)
        elif self.easy_tricks_logic(state):
            return self.climb(state)\
                    or state.can_reach_region(regionName.GI1, self.player) and self.leg_spring(state)\
                    or state.can_reach_region(regionName.GI2, self.player) and self.floor_2_split_up(state) and self.leg_spring(state)\
                    or state.can_reach_region(regionName.GIF, self.player)
        else:
            return self.climb(state)\
                   or state.can_reach_region(regionName.GIOB, self.player) and self.claw_clamber_boots(state)\
                   or state.can_reach_region(regionName.GI1, self.player) and self.leg_spring(state)\
                   or state.can_reach_region(regionName.GI2, self.player) and self.floor_2_split_up(state) and self.leg_spring(state)\
                   or state.can_reach_region(regionName.GIF, self.player)\
                   or self.clockwork_shot(state)

    def nest_gi_floor1_top_pipe(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.split_up(state) and self.claw_clamber_boots(state) and (self.spring_pad(state) or self.wing_whack(state) or (self.egg_aim(state) and self.glide(state)))
        elif self.easy_tricks_logic(state):
            return self.split_up(state) and\
                    ((self.claw_clamber_boots(state) or state.can_reach_region(regionName.GI2, self.player)) and self.spring_pad(state)
                        or self.claw_clamber_boots(state) and (self.wing_whack(state) or self.glide(state)) and (self.egg_aim(state) or self.wing_whack(state)))
        else:
            return self.split_up(state) and\
                   (self.claw_clamber_boots(state) or state.can_reach_region(regionName.GI2, self.player) and self.floor_2_split_up(state))

    def nest_gi_floor1_high_pipe(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.claw_clamber_boots(state) and (self.leg_spring(state) or self.spring_pad(state))
        elif self.easy_tricks_logic(state):
            return self.claw_clamber_boots(state) and (self.leg_spring(state) or self.spring_pad(state))\
                    or state.can_reach_region(regionName.GI2, self.player) and (self.floor_2_split_up(state) and self.leg_spring(state) or self.F2_to_F1(state) and self.spring_pad(state))\
                    or self.claw_clamber_boots(state) and (self.wing_whack(state) or self.glide(state)) and (self.egg_aim(state) or self.wing_whack(state))
        else:
            return self.claw_clamber_boots(state)\
                   or state.can_reach_region(regionName.GI2, self.player) and (self.floor_2_split_up(state) and self.leg_spring(state) or self.F2_to_F1(state) and (self.spring_pad(state) or self.clockwork_shot(state)))\
                   or self.claw_clamber_boots(state) and (self.wing_whack(state) or self.glide(state)) and (self.egg_aim(state) or self.wing_whack(state))

    def nest_gi_outside_waste_disposal(self, state: CollectionState) -> bool:
        if self.intended_logic(state) or self.easy_tricks_logic(state):
            return self.slightly_elevated_ledge(state) or self.split_up(state) or self.flap_flip(state)
        else:
            return self.slightly_elevated_ledge(state) or self.split_up(state) or self.clockwork_shot(state) or self.flap_flip(state)

    def nest_outside_trash_compactor(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.snooze_pack(state)
        elif self.easy_tricks_logic(state):
            return True # You have to get crushed anyway in the intended strat. Is it fair that doing it without snooze pack is in easy tricks?
        else:
            return True

    def nest_gi_train_station_small_box(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.small_elevation(state)
        else:
            return True

    def nest_gi_train_station_medium_box(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.slightly_elevated_ledge(state)\
                    or self.flap_flip(state)\
                    or self.leg_spring(state)
        elif self.easy_tricks_logic(state):
            return self.slightly_elevated_ledge(state)\
                    or self.flap_flip(state)\
                    or self.split_up(state)\
                    or self.flutter(state)\
                    or self.air_rat_a_tat_rap(state)
        else:
            return self.slightly_elevated_ledge(state)\
                   or self.flap_flip(state)\
                   or self.split_up(state)\
                   or self.flutter(state)\
                   or self.air_rat_a_tat_rap(state)\
                   or self.clockwork_shot(state)

    def nest_trash_compactor(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.snooze_pack(state)
        elif self.easy_tricks_logic(state):
            return self.snooze_pack(state)\
                    or self.talon_trot(state)\
                    or self.split_up(state) and self.tall_jump(state)\
                    or self.wing_whack(state)\
                    or self.glide(state)\
                    or self.leg_spring(state)\
                    or self.flap_flip(state)\
                    or self.clockwork_eggs(state)
        else:
            return self.snooze_pack(state)\
                   or self.talon_trot(state)\
                   or self.split_up(state) and self.tall_jump(state)\
                   or self.wing_whack(state)\
                   or self.glide(state)\
                   or self.leg_spring(state)\
                   or self.clockwork_eggs(state)\
                   or self.flap_flip(state)

    def nest_elevator_shaft_floor2(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.climb(state)\
                    or state.can_reach_region(regionName.GI2EM, self.player) and self.floor_2_em_room_to_elevator_shaft(state)
        elif self.easy_tricks_logic(state):
            return self.climb(state)\
                    or state.can_reach_region(regionName.GI2EM, self.player) and self.floor_2_em_room_to_elevator_shaft(state)\
                    or state.can_reach_region(regionName.GI3B, self.player) and self.boiler_plant_to_elevator_shaft(state) and self.beak_buster(state)\
                    or state.can_reach_region(regionName.GI4B, self.player) and self.floor_4_back_to_elevator_shaft(state) and self.beak_buster(state)
        else:
            return self.climb(state)\
                   or state.can_reach_region(regionName.GI2EM, self.player) and self.floor_2_em_room_to_elevator_shaft(state)\
                   or state.can_reach_region(regionName.GI3B, self.player) and self.boiler_plant_to_elevator_shaft(state)\
                   or state.can_reach_region(regionName.GI4B, self.player) and (self.health_upgrades(state, 2) or self.beak_buster(state)) and self.floor_4_back_to_elevator_shaft(state)

    def nest_elevator_shaft_floor3(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.climb(state)\
                    or state.can_reach_region(regionName.GI3B, self.player) and self.boiler_plant_to_elevator_shaft(state)
        elif self.easy_tricks_logic(state):
            return self.climb(state)\
                    or state.can_reach_region(regionName.GI3B, self.player) and self.boiler_plant_to_elevator_shaft(state)\
                    or state.can_reach_region(regionName.GI4B, self.player) and self.floor_4_back_to_elevator_shaft(state) and self.beak_buster(state)
        else:
            return self.climb(state)\
                   or state.can_reach_region(regionName.GI3B, self.player) and self.boiler_plant_to_elevator_shaft(state)\
                   or state.can_reach_region(regionName.GI4B, self.player) and self.floor_4_back_to_elevator_shaft(state)

    def nest_elevator_shaft_floor4(self, state: CollectionState) -> bool:
        return self.climb(state)\
               or state.can_reach_region(regionName.GI4B, self.player) and self.floor_4_back_to_elevator_shaft(state)

    def nest_funny_platform(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return state.can_reach_region(regionName.GI2, self.player) and self.claw_clamber_boots(state) and self.flap_flip(state) and self.grip_grab(state)
        elif self.easy_tricks_logic(state):
            return state.can_reach_region(regionName.GI2, self.player) and self.claw_clamber_boots(state) and (self.flap_flip(state) and self.grip_grab(state))\
                    or state.can_reach_region(regionName.GI2, self.player) and self.floor_2_split_up(state)\
                        and (self.leg_spring(state) or self.claw_clamber_boots(state) and (self.can_shoot_any_egg(state) or self.wing_whack(state)))\
                        and self.glide(state)\
                    or state.can_reach_region(regionName.GI3, self.player) and\
                        self.climb(state) and (self.very_long_jump(state) or self.flap_flip(state) or self.tall_jump(state)) and self.grip_grab(state)\
                    or state.can_reach_region(regionName.GI3, self.player) and self.small_elevation(state)\
                        and self.split_up(state) and self.leg_spring(state) and self.glide(state)
        else:
            return state.can_reach_region(regionName.GI2, self.player) and self.claw_clamber_boots(state)\
                       and ((self.flap_flip(state) and self.grip_grab(state))
                            or self.talon_trot(state) and (self.flutter(state) or self.air_rat_a_tat_rap(state)))\
                   or state.can_reach_region(regionName.GI2, self.player) and self.floor_2_split_up(state)\
                       and (self.leg_spring(state) or self.claw_clamber_boots(state) and (self.can_shoot_any_egg(state) or self.wing_whack(state)))\
                       and self.glide(state)\
                   or state.can_reach_region(regionName.GI3, self.player) and\
                       self.climb(state) and (self.very_long_jump(state) or self.flap_flip(state) or self.tall_jump(state)) and self.grip_grab(state)\
                   or state.can_reach_region(regionName.GI3, self.player) and self.small_elevation(state)\
                       and self.split_up(state) and self.leg_spring(state) and self.glide(state)\
                   or self.clockwork_shot(state)

    def nest_magnet(self, state: CollectionState) -> bool:
        if self.intended_logic(state) or self.easy_tricks_logic(state):
            return self.tall_jump(state)\
                   or self.talon_trot(state)\
                   or self.flutter(state)\
                   or self.air_rat_a_tat_rap(state)\
                   or state.can_reach_region(regionName.GI2, self.player) and self.floor_2_to_em_room(state)
        else:
            return self.tall_jump(state)\
                    or self.talon_trot(state)\
                    or self.flutter(state)\
                    or self.air_rat_a_tat_rap(state)\
                    or state.can_reach_region(regionName.GI2, self.player) and self.floor_2_to_em_room(state)\
                    or self.clockwork_shot(state)

    def nest_floor3_under_notes_boxes(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.climb(state)\
                    or self.floor_3_split_up(state) and self.leg_spring(state)\
                    or self.flap_flip(state)\
                    or self.slightly_elevated_ledge(state)
        elif self.easy_tricks_logic(state):
            return self.climb(state)\
                    or self.enter_floor_3_from_fire_exit(state)\
                    or self.flap_flip(state)\
                    or self.slightly_elevated_ledge(state)\
                    or self.floor_3_split_up(state) and self.leg_spring(state)\
                    or self.floor_3_split_up(state) and self.pack_whack(state)
        else:
            return self.climb(state)\
                   or self.enter_floor_3_from_fire_exit(state)\
                   or self.flap_flip(state)\
                   or self.slightly_elevated_ledge(state)\
                   or self.floor_3_split_up(state) and self.leg_spring(state)\
                   or self.floor_3_split_up(state) and self.pack_whack(state)\
                   or self.floor_3_split_up(state) and self.sack_pack(state)\
                   or self.floor_3_split_up(state) and self.tall_jump(state) and (self.wing_whack(state) or self.glide(state))\
                   or self.clockwork_shot(state)

    def nest_floor3_corner_box(self, state: CollectionState) -> bool:
        if self.intended_logic(state) or self.easy_tricks_logic(state):
            return self.floor_3_split_up(state)\
                   or self.small_elevation(state)
        else:
            return self.floor_3_split_up(state)\
                    or self.small_elevation(state)\
                    or self.clockwork_shot(state)

    def nest_floor3_feather(self, state: CollectionState) -> bool:
        return self.glowbo_floor_3(state)

    def nest_floor3_high_box(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.flap_flip(state) and self.grip_grab(state)\
                    or self.climb(state) and (
                        self.tall_jump(state) and self.grip_grab(state)
                        or self.talon_trot(state) and self.flutter(state) and self.grip_grab(state)
                    )\
                    or self.floor_3_split_up(state) and self.leg_spring(state)
        elif self.easy_tricks_logic(state):
            return self.flap_flip(state) and (self.grip_grab(state) or self.beak_buster(state))\
                    or self.climb(state) and (
                        self.tall_jump(state) and self.grip_grab(state)
                        or self.talon_trot(state) and self.flutter(state) and self.grip_grab(state)
                    )\
                    or self.pack_whack(state) and self.floor_3_split_up(state) and self.tall_jump(state)\
                    or self.floor_3_split_up(state) and self.leg_spring(state)
        else:
            return self.flap_flip(state) and (self.grip_grab(state) or self.beak_buster(state))\
                   or self.climb(state) and (
                       self.tall_jump(state) and self.grip_grab(state)
                       or self.talon_trot(state) and self.flutter(state) and self.grip_grab(state)
                   )\
                   or self.pack_whack(state) and self.floor_3_split_up(state) and self.tall_jump(state)\
                   or self.floor_3_split_up(state) and self.leg_spring(state)\
                   or self.floor_3_split_up(state) and self.tall_jump(state) and (self.wing_whack(state) or self.glide(state))\
                   or self.clockwork_shot(state)

    def nest_floor3_shortcut(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.floor_3_split_up(state)\
                    or self.small_elevation(state)
        elif self.easy_tricks_logic(state):
            return self.floor_3_split_up(state)\
                    or self.small_elevation(state)\
                    or self.beak_buster(state)
        else:
            return self.floor_3_split_up(state)\
                   or self.small_elevation(state)\
                   or self.beak_buster(state)\
                   or self.clockwork_shot(state)

    def nest_floor4_front(self, state: CollectionState) -> bool:
        if self.intended_logic(state) or self.easy_tricks_logic(state):
            return self.small_elevation(state)
        else:
            return self.small_elevation(state) or self.clockwork_shot(state)

    def nest_outside_QC(self, state: CollectionState) -> bool:
        if self.hard_tricks_logic(state):
            return self.climb(state)\
                    or self.pack_whack(state) and self.tall_jump(state)\
                    or self.split_up(state) and (self.leg_spring(state) or self.spring_pad(state))
        elif self.glitches_logic(state):
            return self.climb(state)\
                    or self.pack_whack(state) and self.tall_jump(state)\
                    or self.split_up(state) and (self.leg_spring(state) or self.spring_pad(state))\
                    or self.precise_clockwork_warp(state) and (self.spring_pad(state) or self.flap_flip(state))\
                    or state.can_reach_region(regionName.GIES, self.player) and self.elevator_shaft_to_floor_4(state)
        else:
            return self.climb(state)

    def nest_quality_control(self, state: CollectionState) -> bool:
        if self.glitches_logic(state):
            return self.can_use_battery(state) and self.climb(state)\
                    or self.precise_clockwork_warp(state) and (self.spring_pad(state) or self.flap_flip(state))
        else:
            return self.can_use_battery(state) and self.climb(state)

    def nest_floor5_small_stack(self, state: CollectionState) -> bool:
        if self.intended_logic(state) or self.easy_tricks_logic(state):
            return self.small_elevation(state)\
                   or self.split_up(state)
        else:
            return self.small_elevation(state)\
                    or self.split_up(state)\
                    or self.clockwork_shot(state)

    def nest_egg_fan_easy(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return (self.tall_jump(state) or self.flutter(state) or self.air_rat_a_tat_rap(state)) and self.climb(state)
        elif self.easy_tricks_logic(state):
            return self.climb(state)
        else:
            return self.climb(state)\
                   or self.leg_spring(state) and (self.wing_whack(state) or self.glide(state))

    # This one is a lot harder than the other ones!
    def nest_egg_fan_hard(self, state: CollectionState) -> bool:
        if self.intended_logic(state) or self.easy_tricks_logic(state):
            return self.can_beat_weldar(state) and self.climb(state)
        else:
            return self.can_beat_weldar(state) and (
                        self.climb(state)
                        or self.leg_spring(state) and (self.wing_whack(state) or self.glide(state))
                    )\
                    or self.climb(state) and self.clockwork_shot(state)

    def nest_outside_repair_depot(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.flap_flip(state) and self.climb(state) and self.grip_grab(state)
        elif self.easy_tricks_logic(state):
            return self.flap_flip(state) and self.climb(state) and (self.grip_grab(state)
                        or (self.tall_jump(state) and (self.flutter(state) or self.air_rat_a_tat_rap(state))))
        else:
            return self.flap_flip(state) and self.climb(state) and (self.grip_grab(state)
                       or (self.tall_jump(state) and (self.flutter(state) or self.air_rat_a_tat_rap(state))))\
                   or self.leg_spring(state) and (self.glide(state) or self.wing_whack(state))\
                   or self.clockwork_shot(state)

    def nest_waste_disposal_water_pump(self, state: CollectionState) -> bool:
        if self.intended_logic(state) or self.easy_tricks_logic(state):
            return self.jrl_waste_disposal(state) and self.flap_flip(state) and self.climb(state)
        else:
            #If someone finds a setup for a clockwork shot for these nests, I'll add it to the logic.
            return self.jrl_waste_disposal(state) and self.climb(state)\
                        and (self.flap_flip(state)
                           or self.tall_jump(state) and self.flutter(state)
                           or self.extremelyLongJump(state)
                           or self.tall_jump(state) and self.beak_buster(state)
                           or self.talon_trot(state) and self.flutter(state) and self.beak_buster(state)
                       )

    def jrl_waste_disposal(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return (self.has_explosives(state) or self.bill_drill(state))\
                        and (self.talon_trot(state)
                             or self.tall_jump(state) and (self.flutter(state) or self.air_rat_a_tat_rap(state))
                        )
        else:
            return (self.has_explosives(state) or self.bill_drill(state))\
                   and (self.talon_trot(state)
                       or self.tall_jump(state) and (self.flutter(state) or self.air_rat_a_tat_rap(state))
                       or state.has(itemName.DOUBLOON, self.player, 28) and self.turbo_trainers(state)
                   )

    def nest_clinkers_lobby(self, state: CollectionState) -> bool:
        if self.glitches_logic(state):
            return self.claw_clamber_boots(state)\
                    and (self.clockwork_warp(state) and (self.spring_pad(state) or self.flap_flip(state))
                        or state.can_reach_region(regionName.GIES, self.player) and self.elevator_shaft_to_floor_4(state)
                        or self.climb(state))
        else:
            return self.claw_clamber_boots(state) and self.climb(state)

    def nest_hfp_entrance_shelter(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.flight_pad(state) or self.leg_spring(state)
        elif self.easy_tricks_logic(state):
            return self.flight_pad(state)\
                    or self.leg_spring(state)\
                    or self.glide(state)\
                    or self.tall_jump(state) and self.wing_whack(state)\
                    or self.flap_flip(state) and (self.grip_grab(state) or self.beak_buster(state))
        else:
            return self.flight_pad(state)\
                   or self.leg_spring(state)\
                   or self.glide(state)\
                   or self.clockwork_shot(state)\
                   or self.tall_jump(state) and self.wing_whack(state)\
                   or self.flap_flip(state) and (self.grip_grab(state) or self.beak_buster(state))

    def nest_ice_cube(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.ice_cube_BK(state) and self.hfp_top(state)
        else:
            return self.hfp_top(state)\
                       and (self.ice_cube_BK(state)
                            or self.split_up(state) and self.ice_cube_kazooie(state)
                            or state.has(itemName.MUMBOHP, self.player)
                            or self.pack_whack(state)
                            or self.humbaHFP(state)
                            )

    def nest_icy_side_train_station_easy(self, state: CollectionState) -> bool:
        return self.jiggy_icy_side_station(state)

    def nest_icy_side_train_station_hard(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.access_icy_side_train_station(state) and self.dive(state)
        elif self.easy_tricks_logic(state):
            return self.access_icy_side_train_station(state) and (self.beak_buster(state) or self.dive(state))
        else:
            return self.access_icy_side_train_station(state)

    def nest_hfp_spring_pad(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.hfp_top(state) and self.spring_pad(state) and self.talon_trot(state) and self.ice_cube_BK(state)\
                    or self.hfp_top(state) and self.spring_pad(state) and self.split_up(state) and self.ice_cube_kazooie(state)\
                    or self.warp_to_icicle_grotto(state) and (
                        self.ice_cube_BK(state)
                        or self.split_up(state) and self.ice_cube_kazooie(state)
                    )
        elif self.easy_tricks_logic(state):
            return (self.split_up(state) and self.ice_cube_kazooie(state) and (self.tall_jump(state) or self.wing_whack(state) or self.glide(state) or self.leg_spring(state)))\
                    or (self.hfp_top(state) and self.spring_pad(state) and self.talon_trot(state) and self.ice_cube_BK(state))\
                    or self.warp_to_icicle_grotto(state) and (
                        self.ice_cube_BK(state)
                        or self.split_up(state) and self.ice_cube_kazooie(state)
                    )
        else:
            return (self.split_up(state) and self.ice_cube_kazooie(state) and (self.tall_jump(state) or self.wing_whack(state) or self.glide(state) or self.leg_spring(state)))\
                   or (self.hfp_top(state) and (self.ice_cube_BK(state) or self.clockwork_shot(state)) and (self.talon_trot(state) or self.claw_clamber_boots(state)))\
                   or (self.extremelyLongJump(state) and self.clockwork_shot(state))\
                   or self.warp_to_icicle_grotto(state) and (
                       self.ice_cube_BK(state)
                       or self.split_up(state) and self.ice_cube_kazooie(state)
                   )

    def nest_icicle_grotto_top(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.hfp_top(state) and self.grenade_eggs(state) and self.egg_aim(state) and self.spring_pad(state) and (self.talon_trot(state) or self.split_up(state))
        elif self.easy_tricks_logic(state):
            return (self.split_up(state) and self.ice_cube_kazooie(state) and (self.tall_jump(state) or self.wing_whack(state) or self.glide(state) or self.leg_spring(state)))\
                    or (self.hfp_top(state) and self.grenade_eggs(state) and self.egg_aim(state) and self.spring_pad(state) and (self.talon_trot(state) or self.split_up(state)))\
                    or self.claw_clamber_boots(state) and self.grenade_eggs(state) and self.egg_aim(state)
        else:
            return (self.split_up(state) and self.ice_cube_kazooie(state) and (self.tall_jump(state) or self.wing_whack(state) or self.glide(state) or self.leg_spring(state)))\
                   or (self.hfp_top(state) and (self.grenade_eggs(state) or self.clockwork_shot(state))
                       and self.egg_aim(state) and ((self.tall_jump(state) and self.split_up(state)) or self.talon_trot(state)))\
                   or (self.extremelyLongJump(state) and self.clockwork_shot(state))\
                   or self.claw_clamber_boots(state) and self.ice_cube_BK(state)

    def nest_ccl_flight(self, state: CollectionState) -> bool:
        return self.flight_pad(state) or state.has(itemName.HUMBACC, self.player)

    def nest_jelly_castle(self, state: CollectionState) -> bool:
        return self.nest_ccl_flight(state)\
                or self.climb(state) and (self.small_elevation(state) or self.split_up(state))

    def nest_ccl_dippy(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.nest_ccl_flight(state) or self.dive(state) and self.talon_torpedo(state) and self.flap_flip(state)
        elif self.easy_tricks_logic(state):
            return True # Slide from pot of gold token pile
        else:
            return True

    def nest_outside_trash_can(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.climb(state) and self.tall_jump(state) or self.nest_ccl_flight(state)
        elif self.easy_tricks_logic(state):
            return self.climb(state) and (self.tall_jump(state) or self.pack_whack(state))\
                    or (self.flight_pad(state) or self.glide(state))\
                    or self.nest_ccl_flight(state)
        else:
            return self.climb(state) and (self.tall_jump(state) or self.pack_whack(state))\
                   or (self.flight_pad(state) or self.glide(state) or ((self.tall_jump(state) or self.leg_spring(state)) and self.wing_whack(state)))\
                   or self.nest_ccl_flight(state)

    def nest_inside_trash_can(self, state: CollectionState) -> bool:
        logic = True
        if self.intended_logic(state):
            logic = self.flight_pad(state) and self.leg_spring(state)
        elif self.easy_tricks_logic(state):
            logic = self.climb(state) and self.shack_pack(state) and self.pack_whack(state)\
                    or self.split_up(state)\
                        and (self.flight_pad(state) or self.glide(state) or (self.leg_spring(state) and self.wing_whack(state)))\
                        and self.leg_spring(state)

        elif self.hard_tricks_logic(state):
            logic = self.climb(state) and self.shack_pack(state) and (self.pack_whack(state) or self.tall_jump(state) and self.grip_grab(state))\
                    or self.split_up(state)\
                        and (self.flight_pad(state) or self.glide(state) or (self.leg_spring(state) and self.wing_whack(state)))\
                        and (self.leg_spring(state) or (self.glide(state) and self.tall_jump(state) or self.clockwork_shot(state)))

        elif self.glitches_logic(state):
            logic = self.climb(state) and self.shack_pack(state) and (self.pack_whack(state) or self.tall_jump(state) and self.grip_grab(state))\
                    or self.split_up(state)\
                        and (self.flight_pad(state) or self.glide(state) or (self.leg_spring(state) and self.wing_whack(state)))\
                        and (self.leg_spring(state) or (self.glide(state) and self.tall_jump(state) or self.clockwork_shot(state)))\
                    or self.flight_pad(state) and self.clockwork_warp(state) and self.climb(state)
        return logic

    def nest_near_superstash(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.grip_grab(state) and self.flap_flip(state) or state.has(itemName.HUMBACC, self.player)
        elif self.easy_tricks_logic(state):
            return self.flap_flip(state) and self.grip_grab(state) or self.very_long_jump(state) and (self.climb(state) or self.flight_pad(state))\
                    or state.has(itemName.HUMBACC, self.player)
        else:
            return self.flap_flip(state) and self.grip_grab(state) or self.very_long_jump(state) and (self.climb(state) or self.flight_pad(state))\
                   or self.clockwork_shot(state)\
                   or state.has(itemName.HUMBACC, self.player)

    def nest_pot_of_gold(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.mumboCCL(state) and (self.flap_flip(state) or self.leg_spring(state))
        elif self.easy_tricks_logic(state):
            return self.mumboCCL(state) and (self.flap_flip(state) or self.leg_spring(state) or self.flight_pad(state))
        else:
            return (self.mumboCCL(state) and (self.flap_flip(state) or self.leg_spring(state) or self.flight_pad(state))
                    or (self.leg_spring(state) or (self.split_up(state) and self.tall_jump(state))) and self.flight_pad(state) and self.beak_bomb(state))

    def nest_chilly_willy(self, state: CollectionState) -> bool:
        if self.intended_logic(state) or self.easy_tricks_logic(state):
            return self.fire_eggs(state) and self.claw_clamber_boots(state)
        else:
            # In case people go for the damage boost for Chilly Willy then die before getting the jiggy, we also require Pack Whack to prevent softlocks.
            return self.claw_clamber_boots(state)\
                     or (self.pack_whack(state) and self.tall_jump(state) and self.flutter(state) and
                         (self.talon_trot(state) or self.flap_flip(state)))

    def nest_hfp_kickball_egg(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.long_jump(state) and self.small_elevation(state) and self.has_explosives(state)
        elif self.easy_tricks_logic(state):
            return self.long_jump(state) and self.small_elevation(state) and self.has_explosives(state)\
                    or state.has(itemName.MUMBOHP, self.player) and self.tall_jump(state)\
                    or self.long_jump(state) and self.dragon_kazooie(state)
        else:
            return self.has_explosives(state) or state.has(itemName.MUMBOHP, self.player)\
                   or self.dragon_kazooie(state)

    def nest_hfp_kickball_feather(self, state: CollectionState) -> bool:
        if self.intended_logic(state) or self.easy_tricks_logic(state):
            return self.long_jump(state)
        else:
            return True

    def nest_stomping_plains_footprint(self, state: CollectionState) -> bool:
        if self.intended_logic(state) or self.easy_tricks_logic(state):
            return self.tall_jump(state) and self.split_up(state)\
                   or self.snooze_pack(state)\
                   or self.talon_trot(state)
        else:
            return self.tall_jump(state)\
                    or self.snooze_pack(state)\
                    or self.talon_trot(state)

    def signpost_jiggywiggy_back(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.small_elevation(state)
        else:
            return self.small_elevation(state)\
                   or self.flutter(state)\
                   or self.air_rat_a_tat_rap(state)\
                   or self.beak_buster(state)

    def signpost_code_chamber(self, state: CollectionState) -> bool:
        return self.grip_grab(state)\
               and self.talon_trot(state) and self.flap_flip(state)

    def signpost_pillars(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return (self.dive(state) or self.slightly_elevated_ledge(state) and self.tall_jump(state)) and self.prison_compound_as_banjo(state)\
                    or self.prison_compound_as_stony(state)
        elif self.easy_tricks_logic(state):
            return (self.dive(state) or self.slightly_elevated_ledge(state) or self.beak_buster(state)) and self.prison_compound_as_banjo(state)\
                    or self.prison_compound_as_stony(state)
        else:
            return (self.dive(state)
                   or self.slightly_elevated_ledge(state)
                   or self.beak_buster(state)) and self.prison_compound_as_banjo(state)\
                   or self.prison_compound_as_stony(state)

    def signpost_gloomy_cavern(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.ggm_boulders(state) and (self.small_elevation(state) or self.split_up(state))
        else:
            return self.ggm_boulders(state)

    def signpost_chuffy(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return state.can_reach_region(regionName.GM, self.player) and self.flap_flip(state)\
                    or state.can_reach_region(regionName.WW, self.player) and state.has(itemName.TRAINSWWW, self.player) and state.has(itemName.CHUFFY, self.player)\
                    or state.can_reach_region(regionName.TL, self.player) and state.has(itemName.TRAINSWTD, self.player) and state.has(itemName.CHUFFY, self.player)\
                    or state.can_reach_region(regionName.GI1, self.player) and state.has(itemName.TRAINSWGI, self.player) and state.has(itemName.CHUFFY, self.player)\
                    or state.can_reach_region(regionName.IOHCT, self.player) and state.has(itemName.TRAINSWIH, self.player) and state.has(itemName.CHUFFY, self.player)
        else:
            return state.can_reach_region(regionName.GM, self.player) and (self.small_elevation(state) or self.beak_buster(state) or self.humbaGGM(state) or self.ggm_trot(state))\
                   or state.can_reach_region(regionName.WW, self.player) and state.has(itemName.TRAINSWWW, self.player) and state.has(itemName.CHUFFY, self.player)\
                   or state.can_reach_region(regionName.TL, self.player) and state.has(itemName.TRAINSWTD, self.player) and state.has(itemName.CHUFFY, self.player)\
                   or state.can_reach_region(regionName.GI1, self.player) and state.has(itemName.TRAINSWGI, self.player) and state.has(itemName.CHUFFY, self.player)\
                   or state.can_reach_region(regionName.IOHCT, self.player) and state.has(itemName.TRAINSWIH, self.player) and state.has(itemName.CHUFFY, self.player)\
                   or state.can_reach_region(regionName.HP, self.player) and state.has(itemName.TRAINSWHP1, self.player) and self.hfp_top(state)\
                       and (self.leg_spring(state)
                           or self.tall_jump(state) and self.pack_whack(state)
                           or self.flap_flip(state)
                           or self.claw_clamber_boots(state)
                           or self.flight_pad(state))

    def signpost_pump_master(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return (self.flap_flip(state)
                        or self.leg_spring(state)
                        or self.split_up(state) and self.grip_grab(state)
                    ) and self.has_explosives(state)
        else:
            return (self.flap_flip(state)
                       or self.leg_spring(state)
                       or self.split_up(state) and self.grip_grab(state)
                       or self.pack_whack(state) and self.tall_jump(state)
                   ) and self.has_explosives(state)

    def signpost_gobi(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.grenade_eggs(state) and self.egg_aim(state)
        else:
            return self.grenade_eggs(state)

    def signpost_smugglers(self, state: CollectionState) -> bool:
        return self.has_explosives(state) or self.dive(state)

    def signpost_jrl_pipes(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return (self.has_explosives(state) or self.bill_drill(state)) and \
                    self.grip_grab(state) and self.spring_pad(state) and self.talon_trot(state)
        else:
            return (self.has_explosives(state) or self.bill_drill(state))\
                       and self.grip_grab(state) and self.spring_pad(state) and self.talon_trot(state)\
                   or self.has_explosives(state) and (
                       self.split_up(state) and self.spring_pad(state)
                       or self.leg_spring(state)
                       or self.glide(state)
                   )

    def signpost_trex(self, state: CollectionState) -> bool:
        if self.glitches_logic(state):
            return self.humbaTDL(state) and self.roar(state) or self.clockwork_warp(state)
        else:
            return self.humbaTDL(state) and self.roar(state)

    def signpost_mountain_top(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return (self.tall_jump(state) or self.grip_grab(state)) and self.flight_pad(state)\
                    or state.can_reach_region(regionName.TLTOP, self.player)
        else:
            return self.flight_pad(state) and (
                       self.tall_jump(state)
                       or self.grip_grab(state)
                       or self.beak_buster(state)
                       or self.leg_spring(state) and self.glide(state)
                       or state.can_reach_region(regionName.TLTOP, self.player) and self.split_up(state)
                   )\
                   or state.can_reach_region(regionName.TLTOP, self.player)

    def signpost_river_passage(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.tall_jump(state) and self.grip_grab(state)
        elif self.easy_tricks_logic(state):
            return self.tall_jump(state) and self.grip_grab(state)\
                    or self.leg_spring(state) and self.glide(state)\
                    or self.pack_whack(state) and self.grip_grab(state)
        else:
            return self.tall_jump(state) and self.grip_grab(state)\
                   or self.leg_spring(state) and self.glide(state)\
                   or self.pack_whack(state) and self.grip_grab(state)\
                   or self.sack_pack(state) and self.tall_jump(state)

    def signpost_gi_outside(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return state.can_reach_region(regionName.GIO, self.player) and self.outside_gi_to_outside_back(state)\
                    or state.can_reach_region(regionName.GIOB, self.player) and self.climb(state)
        else:
            return state.can_reach_region(regionName.GIO, self.player) and self.outside_gi_to_outside_back(state)\
                   or state.can_reach_region(regionName.GIOB, self.player) and self.climb(state)\
                   or state.can_reach_region(regionName.GI1, self.player) and (self.split_up(state) and self.tall_jump(state) or self.leg_spring(state))\
                   or state.can_reach_region(regionName.GI2, self.player) and (self.floor_2_split_up(state) and (self.tall_jump(state) or self.leg_spring(state)))\
                   or state.can_reach_region(regionName.GIF, self.player)

    def signpost_elevator_shaft(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.climb(state) and self.tall_jump(state) and (self.flutter(state) or self.air_rat_a_tat_rap(state))
        else:
            return self.climb(state) and (
                       self.flutter(state)
                       or self.air_rat_a_tat_rap(state)
                       or self.tall_jump(state) and self.beak_buster(state)
                   )

    def signpost_ccl_underwater(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.dive(state)
        else:
            return self.dive(state) or self.shack_pack(state)

    def signpost_pool_rim(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.flap_flip(state) and self.grip_grab(state)
        else:
            return True

    def warp_pad_ggm_mumbo(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.small_elevation(state) or self.warp_to_ggm_mumbo(state)
        elif self.easy_tricks_logic(state):
            return self.small_elevation(state)\
                    or self.grip_grab(state)\
                    or self.beak_buster(state)\
                    or self.ggm_trot(state)\
                    or self.warp_to_ggm_mumbo(state)
        else:
            return self.small_elevation(state)\
                   or self.grip_grab(state)\
                   or self.beak_buster(state)\
                   or self.ggm_trot(state)\
                   or self.warp_to_ggm_mumbo(state)\
                   or self.clockwork_shot(state)

    def warp_pad_ggm_wumba(self, state: CollectionState) -> bool:
        if self.intended_logic(state) or self.easy_tricks_logic(state):
            return self.ggm_trot(state) or self.warp_to_ggm_wumba(state)
        else:
            return self.ggm_trot(state) or self.clockwork_shot(state) or self.warp_to_ggm_wumba(state)

    def warp_pad_ww_wumba(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.flap_flip(state) and self.grip_grab(state)\
                    or self.warp_to_ww_wumba(state)
        elif self.easy_tricks_logic(state):
            return self.flap_flip(state)\
                        and ((self.flap_flip(state) and self.grip_grab(state))
                            or (self.climb(state) and self.very_long_jump(state)))\
                    or self.warp_to_ww_wumba(state)\
                    or self.leg_spring(state)
        else:
            return self.flap_flip(state) and self.grip_grab(state) \
                   or self.climb(state) and self.very_long_jump(state) and self.flap_flip(state)\
                   or self.clockwork_shot(state) and self.climb(state)\
                   or self.leg_spring(state)\
                   or self.warp_to_ww_wumba(state)

    def warp_to_ww_wumba(self, state: CollectionState) -> bool:
        return state.has(itemName.WARPWW4, self.player) and (
                    state.has(itemName.WARPWW1, self.player)
                    or state.has(itemName.WARPWW2, self.player)
                    or state.has(itemName.WARPWW3, self.player)
                    or state.has(itemName.WARPWW5, self.player) and state.can_reach_region(regionName.WWI, self.player)
                )

    def warp_to_inferno(self, state: CollectionState) -> bool:
        can_reach_humba_warp_pad = True
        if self.intended_logic(state):
            can_reach_humba_warp_pad = self.flap_flip(state) and self.grip_grab(state)
        else:
            can_reach_humba_warp_pad = self.flap_flip(state) and self.grip_grab(state)\
                                        or self.climb(state) and self.very_long_jump(state) and self.flap_flip(state)

        return state.has(itemName.WARPWW5, self.player) and (
                    state.has(itemName.WARPWW1, self.player)
                    or state.has(itemName.WARPWW2, self.player)
                    or state.has(itemName.WARPWW3, self.player)
                    or state.has(itemName.WARPWW4, self.player) and can_reach_humba_warp_pad
                )

    # The Wumba warp pad is always as hard or harder to reach, so warping from Wumba to Mumbo is not considered to avoid infinite loops.
    def warp_to_ggm_mumbo(self, state: CollectionState) -> bool:
        return state.has(itemName.WARPGM2, self.player) and (
                    state.has(itemName.WARPGM1, self.player)
                    or state.has(itemName.WARPGM4, self.player)
                    or state.has(itemName.WARPGM5, self.player)
                )

    def warp_to_ggm_wumba(self, state: CollectionState) -> bool:
        return state.has(itemName.WARPGM3, self.player) and (
                    state.has(itemName.WARPGM1, self.player)
                    or state.has(itemName.WARPGM2, self.player) and (
                        self.small_elevation(state)
                            or self.grip_grab(state)
                            or self.beak_buster(state)
                            or self.ggm_trot(state)
                            or self.warp_to_ggm_mumbo(state)
                        if not self.intended_logic(state)
                        else self.small_elevation(state)
                    )
                    or state.has(itemName.WARPGM4, self.player)
                    or state.has(itemName.WARPGM5, self.player)
                )

    def warp_pad_tdl_mumbo(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.stilt_stride(state)\
                    or self.warp_to_tdl_mumbo(state)
        else:
            return True

    def warp_to_tdl_mumbo(self, state: CollectionState) -> bool:
        return state.has(itemName.WARPTL3, self.player) and (
            state.has(itemName.WARPTL1, self.player)
            or state.has(itemName.WARPTL2, self.player) and state.can_reach_region(regionName.TLSP, self.player)
            or state.has(itemName.WARPTL4, self.player) and self.small_elevation(state)
            or state.has(itemName.WARPTL5, self.player) and state.can_reach_region(regionName.TLTOP, self.player)
        )

    def warp_pad_tdl_wumba(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.small_elevation(state) or self.warp_to_tdl_wumba(state)
        else:
            return True

    def tdl_to_warp_pads(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return state.has(itemName.WARPTL1, self.player)\
                    or state.has(itemName.WARPTL3, self.player) and self.stilt_stride(state)\
                    or state.has(itemName.WARPTL4, self.player) and self.small_elevation(state)
        else:
            return state.has(itemName.WARPTL1, self.player)\
                   or state.has(itemName.WARPTL3, self.player)\
                   or state.has(itemName.WARPTL4, self.player)

    def warp_to_tdl_wumba(self, state: CollectionState) -> bool:
        reach_mumbo_warp_pad = not self.intended_logic(state) or self.stilt_stride(state)
        return state.has(itemName.WARPTL4, self.player) and (
            state.has(itemName.WARPTL1, self.player)
            or state.has(itemName.WARPTL2, self.player) and state.can_reach_region(regionName.TLSP, self.player)
            or state.has(itemName.WARPTL3, self.player) and reach_mumbo_warp_pad
            or state.has(itemName.WARPTL5, self.player) and state.can_reach_region(regionName.TLTOP, self.player)
        )

    # TODO: readd leg spring + glide in the big rewrite
    def tdl_to_tdl_top(self, state: CollectionState) -> bool:
        if self.intended_logic(state) or self.easy_tricks_logic(state):
            return self.springy_step_shoes(state)\
                       and (self.tall_jump(state) and (self.flutter(state) or self.air_rat_a_tat_rap(state))
                           or self.talon_trot(state))\
                   or self.TDL_flight_pad(state)
        else:
            return self.springy_step_shoes(state)\
                    or self.TDL_flight_pad(state)

    def solo_banjo_to_terry(self, state: CollectionState) -> bool:
        return self.split_up(state) and state.has(itemName.WARPTL5, self.player) and (
                    state.has(itemName.WARPTL1, self.player) and state.can_reach_region(regionName.TL, self.player)
                    or state.has(itemName.WARPTL2, self.player) and state.can_reach_region(regionName.TLSP, self.player)
                    or state.has(itemName.WARPTL3, self.player) and not self.intended_logic(state)
                        and state.can_reach_region(regionName.TL, self.player)
                    or state.has(itemName.WARPTL4, self.player) and state.can_reach_region(regionName.TL, self.player)
                )

    def inside_the_mountain_to_top(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.flight_pad(state)\
                    and (self.tall_jump(state) or self.grip_grab(state))
        else:
            return self.flight_pad(state)\
                   and (self.tall_jump(state) or self.beak_buster(state) or self.grip_grab(state))

    def inside_the_mountain_to_terry(self, state: CollectionState) -> bool:
        logic = True
        if self.intended_logic(state):
            logic = state.can_reach_region(regionName.TLBOSS, self.player)
        elif self.easy_tricks_logic(state):
            logic =  state.can_reach_region(regionName.TLBOSS, self.player) or self.solo_banjo_to_terry(state)
        elif self.hard_tricks_logic(state):
            logic = state.can_reach_region(regionName.TLBOSS, self.player) or self.solo_banjo_to_terry(state)
        elif self.glitches_logic(state):
            logic = state.can_reach_region(regionName.TLBOSS, self.player)\
                    or self.solo_banjo_to_terry(state)\
                    or self.clockwork_warp(state)\
                    or (
                        self.flight_pad(state) and self.beak_bomb(state)
                        and (self.tall_jump(state) or self.beak_buster(state) or self.grip_grab(state))
                    )
        return logic

    def warp_pad_floor_1(self, state: CollectionState) -> bool:
        if self.glitches_logic(state):
            return self.split_up(state)\
                    or state.can_reach_region(regionName.GIWARP, self.player) and state.has(itemName.WARPGI1, self.player)\
                    or state.can_reach_region(regionName.GIO, self.player) and self.clockwork_shot(state)\
                    or self.world.options.open_gi_frontdoor.value
        else:
            return self.split_up(state)\
                   or state.can_reach_region(regionName.GIWARP, self.player) and state.has(itemName.WARPGI1, self.player)\
                   or self.world.options.open_gi_frontdoor.value

    def warp_pad_floor_4(self, state: CollectionState) -> bool:
        if self.intended_logic(state) or self.easy_tricks_logic(state):
            return self.small_elevation(state)\
                   or state.can_reach_region(regionName.GIWARP, self.player) and state.has(itemName.WARPGI4, self.player)
        else:
            return True

    def warp_to_hfp_top(self, state: CollectionState) -> bool:
        return state.has(itemName.WARPHP1, self.player) and (
                    state.has(itemName.WARPHP2, self.player)
                    or state.has(itemName.WARPHP3, self.player)
                    or state.has(itemName.WARPHP4, self.player)
                    or state.has(itemName.WARPHP5, self.player)
                )

    def warp_pad_icicle_grotto(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.hfp_top(state) and self.spring_pad(state) and self.talon_trot(state)\
                    or self.hfp_top(state) and self.spring_pad(state) and self.split_up(state)\
                    or self.warp_to_icicle_grotto(state)
        elif self.easy_tricks_logic(state):
            return self.split_up(state) and (self.tall_jump(state) or self.wing_whack(state) or self.glide(state) or self.leg_spring(state))\
                    or self.hfp_top(state) and self.spring_pad(state) and self.talon_trot(state)\
                    or self.warp_to_icicle_grotto(state)
        else:
            return self.split_up(state) and (self.tall_jump(state) or self.wing_whack(state) or self.glide(state) or self.leg_spring(state))\
                   or self.hfp_top(state) and (self.talon_trot(state) or self.claw_clamber_boots(state))\
                   or (self.extremelyLongJump(state) and self.clockwork_shot(state))\
                   or self.warp_to_icicle_grotto(state)

    def warp_to_icicle_grotto(self, state: CollectionState) -> bool:
        return state.has(itemName.WARPHP5, self.player) and (
                    state.has(itemName.WARPHP1, self.player)
                    or state.has(itemName.WARPHP2, self.player) and self.hfp_top(state)
                    or state.has(itemName.WARPHP3, self.player) and self.hfp_top(state)
                    or state.has(itemName.WARPHP4, self.player) and self.hfp_top(state)
                )

    def warp_pad_ck_top(self, state: CollectionState) -> bool:
        return self.pack_whack(state)\
               or self.sack_pack(state)\
               or self.shack_pack(state)\
               or state.has(itemName.WARPCK1, self.player) and state.has(itemName.WARPCK2, self.player)

    def has_fire(self, state: CollectionState) -> bool:
        return self.fire_eggs(state) or self.dragon_kazooie(state)

    def dragon_kazooie(self, state: CollectionState) -> bool:
        return state.has(itemName.HUMBAIH, self.player) and state.can_reach_region(regionName.IOHPG, self.player) and self.ground_rat_a_tat_rap(state)

    def has_explosives(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.grenade_eggs(state)
        else:
            return self.grenade_eggs(state) or self.clockwork_eggs(state)

    def can_pass_octopi(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.ice_eggs_item(state) and state.has(itemName.MUMBOJR, self.player) and self.sub_aqua_egg_aiming(state)\
                    or self.humbaJRL(state)
        elif self.easy_tricks_logic(state):
            return self.ice_eggs_item(state) and (self.doubleAir(state) or state.has(itemName.MUMBOJR, self.player)) and self.sub_aqua_egg_aiming(state)\
                    or self.humbaJRL(state)
        else:
            return True

    def big_fish_cave_to_locker_cavern(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.ice_eggs_item(state) and state.has(itemName.MUMBOJR, self.player) and self.sub_aqua_egg_aiming(state)\
                    or self.humbaJRL(state)
        elif self.easy_tricks_logic(state):
            return self.ice_eggs_item(state) and state.has(itemName.MUMBOJR, self.player) and self.sub_aqua_egg_aiming(state)\
                    or self.ice_eggs_item(state) and self.doubleAir(state) and self.sub_aqua_egg_aiming(state)\
                        and (
                            state.has(itemName.WARPJR1, self.player) and state.has(itemName.WARPJR4, self.player)
                            or self.dive(state)
                        )\
                    or self.humbaJRL(state)
        else:
            return state.has(itemName.MUMBOJR, self.player)\
                   or state.has(itemName.WARPJR1, self.player) and state.has(itemName.WARPJR4, self.player)\
                   or self.dive(state)\
                   or self.humbaJRL(state)

    def can_escape_locker_cavern(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.ice_eggs_item(state) and state.has(itemName.MUMBOJR, self.player) and self.sub_aqua_egg_aiming(state)\
                    or self.humbaJRL(state)
        elif self.easy_tricks_logic(state):
            return self.ice_eggs_item(state) and state.has(itemName.MUMBOJR, self.player) and self.sub_aqua_egg_aiming(state)\
                    or self.ice_eggs_item(state) and self.doubleAir(state) and self.sub_aqua_egg_aiming(state)\
                        and self.air_pit_from_jrl_warp_pads(state) and state.has(itemName.WARPJR5, self.player)\
                    or self.humbaJRL(state)
        else:
            return state.has(itemName.MUMBOJR, self.player)\
                   or self.air_pit_from_jrl_warp_pads(state) and state.has(itemName.WARPJR5, self.player)\
                   or self.humbaJRL(state)

    def can_escape_sunken_ship(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.ice_eggs_item(state) and state.has(itemName.MUMBOJR, self.player) and self.sub_aqua_egg_aiming(state)\
                    or self.humbaJRL(state)
        elif self.easy_tricks_logic(state):
            return self.ice_eggs_item(state) and state.has(itemName.MUMBOJR, self.player) and self.sub_aqua_egg_aiming(state)\
                    or self.ice_eggs_item(state) and self.doubleAir(state) and self.sub_aqua_egg_aiming(state)\
                        and self.air_pit_from_jrl_warp_pads(state) and state.has(itemName.WARPJR3, self.player)\
                    or self.humbaJRL(state)
        else:
            return state.has(itemName.MUMBOJR, self.player)\
                   or self.air_pit_from_jrl_warp_pads(state) and state.has(itemName.WARPJR3, self.player)\
                   or self.humbaJRL(state)

    def locker_cavern_to_sunken_ship(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.ice_eggs_item(state) and state.has(itemName.MUMBOJR, self.player) and self.sub_aqua_egg_aiming(state)\
                    or self.humbaJRL(state)
        elif self.easy_tricks_logic(state):
            return self.ice_eggs_item(state) and state.has(itemName.MUMBOJR, self.player) and self.sub_aqua_egg_aiming(state)\
                    or self.ice_eggs_item(state) and self.doubleAir(state) and self.sub_aqua_egg_aiming(state)\
                        and self.air_pit_from_jrl_warp_pads(state) and state.has(itemName.WARPJR5, self.player)\
                    or self.humbaJRL(state)
        else:
            return state.has(itemName.MUMBOJR, self.player)\
                   or self.air_pit_from_jrl_warp_pads(state) and state.has(itemName.WARPJR5, self.player)\
                   or self.humbaJRL(state)

    def locker_cavern_to_big_fish_cavern(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.ice_eggs_item(state) and state.has(itemName.MUMBOJR, self.player) and self.sub_aqua_egg_aiming(state)\
                    or self.humbaJRL(state)
        elif self.easy_tricks_logic(state):
            return self.ice_eggs_item(state) and state.has(itemName.MUMBOJR, self.player) and self.sub_aqua_egg_aiming(state)\
                    or self.ice_eggs_item(state) and self.doubleAir(state) and self.sub_aqua_egg_aiming(state)\
                        and state.has(itemName.WARPJR1, self.player) and state.has(itemName.WARPJR5, self.player)\
                    or self.humbaJRL(state)
        else:
            return state.has(itemName.MUMBOJR, self.player)\
                   or state.has(itemName.WARPJR1, self.player) and state.has(itemName.WARPJR5, self.player)\
                   or self.humbaJRL(state)

    def sunken_ship_to_ggm(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.ice_eggs_item(state) and state.has(itemName.MUMBOJR, self.player)\
                    and self.sub_aqua_egg_aiming(state) and self.talon_torpedo(state)
        elif self.easy_tricks_logic(state):
            return self.ice_eggs_item(state) and state.has(itemName.MUMBOJR, self.player)\
                        and self.sub_aqua_egg_aiming(state) and self.talon_torpedo(state)\
                    or self.ice_eggs_item(state) and self.doubleAir(state) and self.sub_aqua_egg_aiming(state)\
                        and self.air_pit_from_jrl_warp_pads(state) and state.has(itemName.WARPJR4, self.player) and self.talon_torpedo(state)
        else:
            return self.ice_eggs_item(state) and state.has(itemName.MUMBOJR, self.player)\
                       and self.sub_aqua_egg_aiming(state) and self.talon_torpedo(state)\
                   or self.ice_eggs_item(state) and self.sub_aqua_egg_aiming(state)\
                       and self.air_pit_from_jrl_warp_pads(state) and state.has(itemName.WARPJR4, self.player) and self.talon_torpedo(state)

    def seaweed_to_bfc(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.tall_jump(state) and self.grip_grab(state) and self.flap_flip(state) and self.dive(state)
        else:
            return self.dive(state)\
                   and self.flap_flip(state)\
                   and self.tall_jump(state)\
                   and (self.beak_buster(state) or self.grip_grab(state))

    def can_climb_seaweed(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.tall_jump(state) and self.grip_grab(state) and self.flap_flip(state)
        else:
            return self.flap_flip(state)\
                   and self.tall_jump(state)\
                   and (self.beak_buster(state) or self.grip_grab(state))

    def MT_flight_pad(self, state: CollectionState) -> bool:
        return self.flight_pad(state) and\
                (state.has(itemName.MUMBOMT, self.player)
                    or (self.bill_drill(state) and (self.small_elevation(state) or self.flutter(state))))

    def prison_compound_open(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.has_explosives(state) or state.has(itemName.MUMBOMT, self.player)
        else:
            return self.has_explosives(state)\
                   or state.has(itemName.MUMBOMT, self.player)\
                   or self.MT_flight_pad(state) and self.airborne_egg_aiming(state) and (
                       self.grenade_eggs_item(state) or self.clockwork_eggs_item(state)
                   )

    # Due to the fact that the stony can warp to the prison compound from the kickball stadium,
    # we gotta make sure that BK can get there for the majority of the checks.
    def prison_compound_as_banjo(self, state: CollectionState) -> bool:
        return self.prison_compound_open(state)\
                or state.can_reach_region(regionName.HP, self.player) and self.HFP_to_MT(state)\
                    and state.has(itemName.WARPMT3, self.player) and state.has(itemName.WARPMT5, self.player)\
                or state.can_reach_region(regionName.MTJSG, self.player) and state.has(itemName.WARPMT4, self.player)\
                    and state.has(itemName.WARPMT3, self.player)\
                or state.has(itemName.WARPMT3, self.player)\
                    and (state.has(itemName.WARPMT1, self.player) or state.has(itemName.WARPMT2, self.player))

    def prison_compound_as_stony(self, state: CollectionState) -> bool:
        return self.humbaMT(state) and (
                    self.prison_compound_open(state)
                    or state.has(itemName.WARPMT3, self.player)
                        and (state.has(itemName.WARPMT1, self.player) or state.has(itemName.WARPMT2, self.player)
                             or state.has(itemName.WARPMT4, self.player) or state.has(itemName.WARPMT5, self.player))
                )

    def kickball_stadium_as_banjo(self, state: CollectionState) -> bool:
        return state.can_reach_region(regionName.HP, self.player) and self.HFP_to_MT(state)\
                or state.has(itemName.WARPMT5, self.player) and (
                    state.has(itemName.WARPMT1, self.player)
                    or state.has(itemName.WARPMT2, self.player)
                    or state.has(itemName.WARPMT3, self.player) and self.prison_compound_as_banjo(state)
                    or state.has(itemName.WARPMT4, self.player) and state.can_reach_region(regionName.MTJSG, self.player)
                )

    def dilberta_free(self, state: CollectionState) -> bool:
        return self.prison_compound_as_banjo(state) and self.bill_drill(state)

    def ggm_boulders(self, state: CollectionState) -> bool:
        return self.bill_drill(state) or self.humbaGGM(state)

    def canary_mary_free(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.humbaGGM(state)
        else:
            return self.humbaGGM(state) or self.clockwork_eggs(state)

    def can_beat_king_coal(self, state: CollectionState) -> bool:
        hasAttack = False
        if self.intended_logic(state):
            hasAttack = self.blue_eggs(state) or self.grenade_eggs(state) or self.ice_eggs(state)
        elif self.easy_tricks_logic(state):
            hasAttack = self.blue_eggs(state) or self.grenade_eggs(state) or self.ice_eggs(state) or self.beak_barge(state) or self.roll(state) or self.air_rat_a_tat_rap(state)
        else:
            hasAttack = self.blue_eggs(state) or self.grenade_eggs(state) or self.ice_eggs(state) or self.beak_barge(state) or self.roll(state)\
            or self.air_rat_a_tat_rap(state) or self.ground_rat_a_tat_rap(state) or self.breegull_bash(state)

        return state.can_reach_region(regionName.GMBOSS, self.player) and hasAttack

    def can_kill_fruity(self, state: CollectionState) -> bool:
        return state.can_reach_region(regionName.WW, self.player) and (
                    self.has_explosives(state)
                    or self.humbaWW(state)
                    or self.bill_drill(state)
                    or self.mumboWW(state) and self.escape_inferno_as_mumbo(state)
                    or self.ice_eggs(state) and ( # Freezing these enemies severely weakens them.
                        self.beak_barge(state)
                        or self.air_rat_a_tat_rap(state)
                        or self.ground_rat_a_tat_rap(state)
                        or self.beak_buster(state)
                        or self.wing_whack(state)
                    )
               )

    def saucer_door_open(self, state: CollectionState) -> bool:
        logic = True
        if self.intended_logic(state):
            logic = self.longJumpToGripGrab(state) and self.flap_flip(state) and self.climb(state)\
                  and (self.has_explosives(state) or self.beak_barge(state)) or\
                  self.backdoors_enabled(state)
        elif self.easy_tricks_logic(state):
            logic = (self.longJumpToGripGrab(state) and self.flap_flip(state) and self.climb(state) and (self.has_explosives(state) or self.beak_barge(state)))\
                or (self.egg_aim(state) and self.grenade_eggs(state) and self.amaze_o_gaze(state) and self.climb(state))\
                or (self.has_explosives(state) and self.leg_spring(state) and self.glide(state))\
                or self.backdoors_enabled(state)
        elif self.hard_tricks_logic(state):
            logic = (self.longJumpToGripGrab(state) and self.flap_flip(state) and self.climb(state) and (self.has_explosives(state) or self.beak_barge(state)))\
                or (self.egg_aim(state) and self.grenade_eggs(state) and self.amaze_o_gaze(state))\
                or (self.has_explosives(state) and self.leg_spring(state) and self.glide(state))\
                or self.backdoors_enabled(state)\
                or self.clockwork_shot(state)
        elif self.glitches_logic(state):
            logic = (self.longJumpToGripGrab(state) and self.flap_flip(state) and self.climb(state) and (self.has_explosives(state) or self.beak_barge(state)))\
                or (self.egg_aim(state) and self.grenade_eggs(state) and self.amaze_o_gaze(state))\
                or (self.has_explosives(state) and self.leg_spring(state) and self.glide(state))\
                or self.backdoors_enabled(state)\
                or self.clockwork_shot(state)\
                or (state.can_reach_region(regionName.GM, self.player) and self.humbaGGM(state) and self.small_elevation(state) and self.clockwork_eggs(state)) # You can shoot a clockwork through the door from GGM.
        return logic


    def can_reach_saucer(self, state: CollectionState) -> bool:
        return (self.longJumpToGripGrab(state) and self.flap_flip(state) and self.climb(state)) or (state.can_reach_region(regionName.GM, self.player) and self.small_elevation(state))


    def longJumpToGripGrab(self, state: CollectionState) -> bool:
        return self.grip_grab(state) and (self.air_rat_a_tat_rap(state) or self.flutter(state))

    def can_beat_terry(self, state: CollectionState) -> bool:
        logic = True
        # I assume nobody wants to do this fight with clockwork eggs.
        if self.intended_logic(state):
            logic = self.egg_aim(state) and self.can_shoot_linear_egg(state)\
                    and state.can_reach_region(regionName.TLBOSS, self.player)
        elif self.easy_tricks_logic(state):
            logic = self.egg_aim(state)  and self.can_shoot_linear_egg(state)\
                    and state.can_reach_region(regionName.TLBOSS, self.player)
        elif self.hard_tricks_logic(state):
            logic = self.can_shoot_linear_egg(state) and (self.flap_flip(state) or self.egg_aim(state))\
                    and state.can_reach_region(regionName.TLBOSS, self.player)
        elif self.glitches_logic(state):
            logic = self.can_shoot_linear_egg(state) and (self.flap_flip(state) or self.egg_aim(state))\
                    and state.can_reach_region(regionName.TLBOSS, self.player)
        return logic

    def smuggle_food(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.claw_clamber_boots(state) and self.talon_trot(state) and self.has_explosives(state)
        elif self.easy_tricks_logic(state):
            return self.claw_clamber_boots(state) and self.has_explosives(state)\
                    and (
                        self.talon_trot(state)
                        or state.can_reach_region(regionName.WWI, self.player) and self.turbo_trainers(state)
                    )
        else:
            return self.has_explosives(state) or self.spring_pad(state)

    def oogle_boogles_open(self, state: CollectionState) -> bool:
        return self.humbaTDL(state) and self.mumboTDL(state)

    def access_oogle_boogle(self, state: CollectionState) -> bool:
        if self.glitches_logic(state):
            return self.oogle_boogles_open(state)\
                    or state.can_reach_region(regionName.WW, self.player) and self.ww_tdl_backdoor(state)\
                    or self.clockwork_warp(state)
        else:
            return self.oogle_boogles_open(state) or state.can_reach_region(regionName.WW, self.player) and self.ww_tdl_backdoor(state)

    def can_enter_gi_repair_depot(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.can_use_battery(state) and self.mumboGI(state) and \
               self.humbaGI(state) and self.bill_drill(state) and self.climb(state) \
                and self.flap_flip(state) and self.grip_grab(state) \
                and (
                    state.has(itemName.WARPGI2, self.player) and state.has(itemName.WARPGI3, self.player)
                    if self.world.options.randomize_warp_pads.value
                    else state.can_reach_region(regionName.GI2, self.player) and state.can_reach_region(regionName.GI3, self.player)
                )
        elif self.easy_tricks_logic(state):
            return self.can_use_battery(state) and self.mumboGI(state) and \
               self.humbaGI(state) and self.bill_drill(state) and self.climb(state) and self.flap_flip(state) and \
               (self.grip_grab(state) or (self.tall_jump(state) and (self.flutter(state) or self.air_rat_a_tat_rap(state))))\
               and (
                    state.has(itemName.WARPGI2, self.player) and state.has(itemName.WARPGI3, self.player)
                    if self.world.options.randomize_warp_pads.value
                    else state.can_reach_region(regionName.GI2, self.player) and state.can_reach_region(regionName.GI3, self.player)
                )
        else:
            return self.can_use_battery(state) and self.mumboGI(state) and \
              self.humbaGI(state) and self.bill_drill(state) and self.climb(state) and self.flap_flip(state) and\
              ((self.grip_grab(state) or (self.tall_jump(state) and (self.flutter(state) or self.air_rat_a_tat_rap(state))))
                   or self.extremelyLongJump(state))\
               and (
                   state.has(itemName.WARPGI2, self.player) and state.has(itemName.WARPGI3, self.player)
                   if self.world.options.randomize_warp_pads.value
                   else state.can_reach_region(regionName.GI2, self.player) and state.can_reach_region(regionName.GI3, self.player)
               )

    def can_beat_weldar(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.grenade_eggs(state) and \
                    (self.tall_jump(state) and (self.flutter(state) or self.air_rat_a_tat_rap(state)))\
                    and state.can_reach_region(regionName.GIBOSS, self.player)
        elif self.easy_tricks_logic(state):
            return self.grenade_eggs(state) and \
                    (self.tall_jump(state) or self.talon_trot(state))\
                    and state.can_reach_region(regionName.GIBOSS, self.player)
        else:
            return self.grenade_eggs(state)\
                   and state.can_reach_region(regionName.GIBOSS, self.player)

    def jiggy_weldar(self, state: CollectionState) -> bool:
        logic = True
        if self.intended_logic(state):
            logic = self.flap_flip(state) and self.climb(state) and self.grip_grab(state) and self.can_beat_weldar(state)
        elif self.easy_tricks_logic(state):
            logic = self.can_beat_weldar(state) and (
                        self.flap_flip(state) and self.climb(state) and (self.grip_grab(state)
                            or (self.tall_jump(state) and (self.flutter(state) or self.air_rat_a_tat_rap(state))))
                    )

        elif self.hard_tricks_logic(state):
            logic = self.can_beat_weldar(state) and (
                        self.flap_flip(state) and self.climb(state) and (self.grip_grab(state)
                            or (self.tall_jump(state) and (self.flutter(state) or self.air_rat_a_tat_rap(state))))
                        or self.leg_spring(state) and (self.glide(state) or self.wing_whack(state))
                    )
        elif self.glitches_logic(state):
            logic = self.can_beat_weldar(state) and (
                        self.flap_flip(state) and self.climb(state) and (self.grip_grab(state)
                            or (self.tall_jump(state) and (self.flutter(state) or self.air_rat_a_tat_rap(state))))
                        or self.leg_spring(state) and (self.glide(state) or self.wing_whack(state))
                    )\
                    or self.clockwork_shot(state)
        return logic

    def jiggy_underwater_waste_disposal(self, state: CollectionState) -> bool:
        if self.glitches_logic(state):
            # Getting the jiggy from waste disposal through the wall.
            return (self.can_beat_weldar(state) and (self.shack_pack(state) and self.climb(state) or self.leg_spring(state)))\
                   or self.can_use_battery(state) and (
                       (self.climb(state) and self.flap_flip(state) and self.talon_torpedo(state)
                        and self.dive(state) and self.wonderwing(state))
                        or (self.shack_pack(state) and self.climb(state) and self.grip_grab(state)))
        else:
            return self.can_beat_weldar(state) and self.shack_pack(state) and self.climb(state)

    def jiggy_clinkers(self, state: CollectionState) -> bool:
        if self.glitches_logic(state):
            return self.claw_clamber_boots(state) and self.breegull_blaster(state)\
                    and (self.precise_clockwork_warp(state) and (self.spring_pad(state) or self.flap_flip(state))
                        or state.can_reach_region(regionName.GIES, self.player) and self.elevator_shaft_to_floor_4(state)
                        or self.climb(state))
        else:
            return self.claw_clamber_boots(state) and self.breegull_blaster(state) and self.climb(state)

    def can_use_battery(self, state: CollectionState) -> bool:
        return self.pack_whack(state) and self.taxi_pack(state)

    def MT_to_JSG(self, state: CollectionState) -> bool:
        if self.glitches_logic(state):
            return self.MT_flight_pad(state) and self.beak_bomb(state) or state.has(itemName.MUMBOMT, self.player)
        else:
            return state.has(itemName.MUMBOMT, self.player)

    def MT_to_KS(self, state: CollectionState) -> bool:
        if self.glitches_logic(state):
            return self.MT_flight_pad(state) and self.beak_bomb(state) or self.humbaMT(state)
        else:
            return self.humbaMT(state)

    def glitchedInfernoAccess(self, state: CollectionState) -> bool:
        return self.humbaWW(state) or self.clockwork_eggs(state) and self.tall_jump(state)

    def HFP_to_MT(self, state: CollectionState) -> bool:
        logic = True
        if self.intended_logic(state):
            logic = self.has_explosives(state)\
                    or self.dragon_kazooie(state)
        elif self.easy_tricks_logic(state):
            logic = self.has_explosives(state) or \
                    state.has(itemName.MUMBOHP, self.player)\
                    or self.dragon_kazooie(state)
        elif self.hard_tricks_logic(state):
            logic = self.has_explosives(state) or \
                    state.has(itemName.MUMBOHP, self.player)\
                    or self.dragon_kazooie(state)
        elif self.glitches_logic(state):
            logic = self.has_explosives(state) or \
                    state.has(itemName.MUMBOHP, self.player)\
                    or self.dragon_kazooie(state)
        return logic



    def HFP_to_JRL(self, state: CollectionState) -> bool:
        if self.glitches_logic(state):
            return self.HFP_hot_water_cooled(state)\
                    or (self.grip_grab(state) and (self.flutter(state) or self.air_rat_a_tat_rap(state)) and self.ground_rat_a_tat_rap(state) and self.tall_jump(state))
        else:
            return self.HFP_hot_water_cooled(state)

    def set_world_requirement(self, state: CollectionState, locationId: int) -> bool: #1
        world = ""
        for worldLoc, locationno in self.world.world_order.items():
            if locationno == locationId:
                world = worldLoc
                break
        if world == "":
            raise KeyError(
                "Something got messed up when generating the world order.",
                "Please report this to the Banjo-Tooie AP dev team."
            )
        amt = self.world.world_requirements[world]
        return state.has(itemName.JIGGY, self.player, amt)


    def mt_jiggy(self, state: CollectionState) -> bool: #1
        if self.world.options.randomize_worlds.value:
            return state.has(itemName.MTA, self.player)
        else:
            amt = self.world.world_requirements[regionName.MT]
            return state.has(itemName.JIGGY, self.player, amt)

    def MT_to_WH(self, state: CollectionState) -> bool: #1
        if self.intended_logic(state):
            return self.mt_jiggy(state)
        else:
            return True

    def WH_to_PL(self, state: CollectionState) -> bool:
        if self.intended_logic(state) or self.easy_tricks_logic(state):
            return self.slightly_elevated_ledge(state)
        else:
            return self.slightly_elevated_ledge(state) or (self.flap_flip(state) and self.beak_buster(state))

    def GGM_to_PL(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.gm_jiggy(state) and self.climb(state)
        else:
            return self.climb(state)

    def escape_ggm_loading_zone(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.gm_jiggy(state) and self.climb(state)
        else:
            return self.climb(state) or self.beak_buster(state) or self.flutter(state) or self.air_rat_a_tat_rap(state)

    def PG_to_PL(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return False
        else:
            return True

    def CT_to_PL(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return False
        else:
            return True

    def gm_jiggy(self, state: CollectionState) -> bool: #4
        if self.world.options.randomize_worlds.value:
            return state.has(itemName.GGA, self.player)
        else:
            amt = self.world.world_requirements[regionName.GM]
            return state.has(itemName.JIGGY, self.player, amt)


    def can_access_water_storage_jinjo_from_GGM(self, state: CollectionState) -> bool:
        if self.intended_logic(state) or self.easy_tricks_logic(state):
            return False
        else:
            return (self.wing_whack(state) and self.leg_spring(state) and
                        self.glide(state) and self.ggm_boulders(state))\
                    or self.clockwork_shot(state)

    # If you warp to a warp pad in JRL, this checks to see if you have enough air to get the checks in the region that you warp to.
    def air_pit_from_jrl_warp_pads(self, state: CollectionState) -> bool:
        return state.has(itemName.WARPJR1, self.player)\
                or state.has(itemName.WARPJR2, self.player) and self.dive(state)\
                or state.has(itemName.WARPJR4, self.player) and self.dive(state)

    def PL_to_PG(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.fire_eggs(state) and self.egg_aim(state)
        else:
            return self.fire_eggs(state) and self.egg_aim(state)\
                   or self.talon_trot(state) and self.fire_eggs(state)\
                   or self.split_up(state) and self.fire_eggs(state)

    def PL_to_GGM(self, state: CollectionState) -> bool:
        if self.glitches_logic(state):
            return self.gm_jiggy(state)\
                    or (self.beak_buster(state) and (self.flap_flip(state) or self.tall_jump(state) or (self.talon_trot(state) and self.flutter(state))))
        else:
            return self.gm_jiggy(state)

    def hatch_to_TDL(self, state: CollectionState) -> bool:
        if self.glitches_logic(state):
            return (self.clockwork_eggs(state) and self.egg_aim(state)) or self.backdoors_enabled(state)
        else:
            return self.backdoors_enabled(state)

    def ww_jiggy(self, state: CollectionState) -> bool: #8
        if self.world.options.randomize_worlds.value:
            return state.has(itemName.WWA, self.player)
        else:
            amt = self.world.world_requirements[regionName.WW]
            return state.has(itemName.JIGGY, self.player, amt)

    def jrl_jiggy(self, state: CollectionState) -> bool: #14
        if self.world.options.randomize_worlds.value:
            return state.has(itemName.JRA, self.player)
        else:
            amt = self.world.world_requirements[regionName.JR]
            return state.has(itemName.JIGGY, self.player, amt)

    def tdl_jiggy(self, state: CollectionState) -> bool: #20
        if self.world.options.randomize_worlds.value:
            return state.has(itemName.TDA, self.player)
        else:
            amt = self.world.world_requirements[regionName.TL]
            return state.has(itemName.JIGGY, self.player, amt)


    def gi_jiggy(self, state: CollectionState) -> bool: #28
        if self.world.options.randomize_worlds.value:
            return state.has(itemName.GIA, self.player)
        else:
            amt = self.world.world_requirements[regionName.GIO]
            return state.has(itemName.JIGGY, self.player, amt)

    def ck_jiggy(self, state: CollectionState) -> bool: #55
        if self.world.options.randomize_worlds.value:
            return state.has(itemName.CKA, self.player)
        else:
            amt = self.world.world_requirements[regionName.CK]
            return state.has(itemName.JIGGY, self.player, amt)

    def quag_to_CK(self, state: CollectionState) -> bool:
        if self.glitches_logic(state):
            return (self.clockwork_warp(state) and self.talon_trot(state) and self.climb(state) and self.beak_buster(state) or self.claw_clamber_boots(state))\
                    and (self.ck_jiggy(state) or (self.climb(state) and self.tall_jump(state) and self.beak_buster(state) and (self.flutter(state) or self.air_rat_a_tat_rap(state))))
        else:
            return self.claw_clamber_boots(state) and self.ck_jiggy(state)

    def mt_tdl_backdoor(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.egg_aim(state) and\
                (self.grip_grab(state) and self.spring_pad(state) and self.flap_flip(state) and self.talon_trot(state) or self.MT_flight_pad(state)) and\
                   self.backdoors_enabled(state)
        else:
            return (self.grip_grab(state) and self.spring_pad(state) and self.flap_flip(state) and self.egg_aim(state) and self.talon_trot(state)
                   or self.MT_flight_pad(state) and self.can_shoot_any_egg(state)) and\
                  self.backdoors_enabled(state)

    def mt_to_hatch_region(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.egg_aim(state) and\
                (self.flap_flip(state) or self.slightly_elevated_ledge(state)) and\
                  ((self.grip_grab(state) and self.spring_pad(state) and self.flap_flip(state) and self.talon_trot(state)) or self.MT_flight_pad(state))
        else:
            return (self.flap_flip(state) or self.slightly_elevated_ledge(state))\
                   and ((self.grip_grab(state) and self.spring_pad(state) and self.flap_flip(state) and self.egg_aim(state) and self.talon_trot(state))
                       or (self.MT_flight_pad(state) and self.can_shoot_any_egg(state))
                       or state.can_reach_region(regionName.TL_HATCH, self.player))\
                   and (self.MT_flight_pad(state) and self.can_shoot_any_egg(state) or self.egg_aim(state))

    def mt_hfp_backdoor(self, state: CollectionState) -> bool:
        return self.backdoors_enabled(state) and self.kickball_stadium_as_banjo(state)


    def ww_tdl_backdoor(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.has_explosives(state) and self.claw_clamber_boots(state) and\
                   self.talon_trot(state) and self.backdoors_enabled(state)
        elif self.glitches_logic(state):
            return self.has_explosives(state) and self.claw_clamber_boots(state) and self.backdoors_enabled(state) and (
                       self.talon_trot(state)
                       or (self.warp_to_inferno(state) or self.humbaWW(state)) and self.turbo_trainers(state)
                   )
        else:
            return self.has_explosives(state) and self.claw_clamber_boots(state) and self.backdoors_enabled(state) and (
                       self.talon_trot(state)
                       or state.can_reach_region(regionName.WWI, self.player) and self.turbo_trainers(state)
                   )


    def ggm_to_fuel_depot(self, state: CollectionState) -> bool:
        return self.humbaGGM(state) and self.small_elevation(state)


    def ggm_to_ww(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.backdoors_enabled(state) and self.small_elevation(state) and self.humbaGGM(state)
        elif self.glitches_logic(state):
            return (self.clockwork_eggs(state) or self.backdoors_enabled(state)) and (self.small_elevation(state) or self.ggm_trot(state)) and self.humbaGGM(state)
        else:
            return self.backdoors_enabled(state) and (self.small_elevation(state) or self.ggm_trot(state)) and self.humbaGGM(state)

    def ggm_to_fuel_depot_nests(self, state: CollectionState) -> bool:
        if self.glitches_logic(state):
            return self.humbaGGM(state)\
                    or self.clockwork_shot(state) and (
                        self.small_elevation(state)
                        or self.ggm_trot(state)
                        or self.beak_buster(state)
                    )
        else:
            return self.humbaGGM(state)

    def ww_to_fuel_depot(self, state: CollectionState) -> bool:
        if self.intended_logic(state) or self.easy_tricks_logic(state):
            return self.climb(state) and self.flap_flip(state) and self.grip_grab(state) and self.longJumpToGripGrab(state) and self.saucer_door_open(state)
        else:
            return self.climb(state) and self.flap_flip(state) and (self.grip_grab(state) or self.beak_buster(state)) and self.longJumpToGripGrab(state) and self.saucer_door_open(state)

    def a51_nests_from_WW(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.has_explosives(state)
        elif self.easy_tricks_logic(state):
            return self.has_explosives(state) or self.glide(state) or self.leg_spring(state)
        else:
            return self.has_explosives(state)\
                   or self.glide(state)\
                   or self.leg_spring(state)\
                   or self.split_up(state) and self.spring_pad(state)

    def ww_to_inferno(self, state: CollectionState) -> bool:
        if self.glitches_logic(state):
            return self.glitchedInfernoAccess(state) or self.warp_to_inferno(state)
        else:
            return self.humbaWW(state) or self.warp_to_inferno(state)

    def a51_nests_from_TDL(self, state: CollectionState) -> bool:
        if self.glitches_logic(state):
            return self.oogle_boogles_open(state) or self.clockwork_warp(state)
        else:
            return self.oogle_boogles_open(state)

    def backdoors_enabled(self, state: CollectionState) -> bool:
        return self.world.options.backdoors.value

    def train_raised(self, state: CollectionState) -> bool:
        return state.has(itemName.CHUFFY, self.player)\
                if self.world.options.randomize_chuffy.value\
                else self.mumboGGM(state)

    def ggm_to_chuffy(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.train_raised(state) and (
                        self.climb(state) and self.small_elevation(state)
                    )
        elif self.easy_tricks_logic(state):
            return self.train_raised(state) and (
                        self.small_elevation(state)
                        or self.climb(state)
                    )
        else:
            return self.train_raised(state) and (
                       self.small_elevation(state)
                       or self.climb(state)
                       or self.beak_buster(state)
                   )

    def can_call_train(self, state: CollectionState) -> bool:
        return state.has(itemName.CHUFFY, self.player)\
            if self.world.options.randomize_chuffy.value\
            else self.can_beat_king_coal(state) and self.mumboGGM(state)

    def ww_to_chuffy(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return state.has(itemName.TRAINSWWW, self.player) and (self.climb(state) and self.small_elevation(state))\
                    and self.can_call_train(state)
        else:
            return state.has(itemName.TRAINSWWW, self.player) and (self.small_elevation(state) or self.climb(state))\
                   and self.can_call_train(state)

    def ioh_to_chuffy(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return state.has(itemName.TRAINSWIH, self.player) and (self.climb(state) and self.small_elevation(state))\
                    and self.can_call_train(state)
        elif self.easy_tricks_logic(state):
            return state.has(itemName.TRAINSWIH, self.player) and (self.small_elevation(state) or self.climb(state))\
                    and self.can_call_train(state)
        else:
            return state.has(itemName.TRAINSWIH, self.player) and (self.small_elevation(state) or self.climb(state) or self.beak_buster(state))\
                   and self.can_call_train(state)

    # For this one, the ladder is farther off the ground.
    def tdl_to_chuffy(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return state.has(itemName.TRAINSWTD, self.player)\
                    and (self.climb(state) and self.small_elevation(state))\
                    and self.can_call_train(state)
        elif self.easy_tricks_logic(state):
            return state.has(itemName.TRAINSWTD, self.player)\
                    and ((self.small_elevation(state) or self.beak_buster(state)) and self.climb(state)
                        or self.flap_flip(state) and self.beak_buster(state))\
                    and self.can_call_train(state)
        else:
            return state.has(itemName.TRAINSWTD, self.player)\
                   and (
                       ((self.small_elevation(state) or self.beak_buster(state)) and self.climb(state))
                       or self.extremelyLongJump(state)
                       or self.flap_flip(state) and self.beak_buster(state)
                       or self.tall_jump(state) and self.beak_buster(state)
                   )\
                   and self.can_call_train(state)


    #The train door is at ground level.
    def gi_to_chuffy(self, state: CollectionState) -> bool:
        return state.has(itemName.TRAINSWGI, self.player)\
               and self.can_call_train(state)

    #This one is pixels higher than WW or IoH, you can't just short jump to the ladder.
    def hfp_to_chuffy(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return state.has(itemName.TRAINSWHP1, self.player) and self.climb(state) and self.small_elevation(state)\
                    and self.can_call_train(state)
        elif self.easy_tricks_logic(state):
            return state.has(itemName.TRAINSWHP1, self.player) and (
                        self.climb(state) and (self.small_elevation(state) or self.beak_buster(state))
                        or self.talon_trot(state)
                    )\
                    and self.can_call_train(state)
        else:
            return state.has(itemName.TRAINSWHP1, self.player) and (
                       self.climb(state) and (self.small_elevation(state) or self.beak_buster(state))
                       or self.talon_trot(state)
                       or self.tall_jump(state) and self.beak_buster(state)
                   )\
                   and self.can_call_train(state)

    def PGU_to_PG(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.grip_grab(state) or self.tall_jump(state)
        elif self.easy_tricks_logic(state):
            return self.grip_grab(state) or self.tall_jump(state) or (self.beak_buster(state) and (self.flutter(state) or self.air_rat_a_tat_rap(state)))
        else:
            return self.grip_grab(state) or self.tall_jump(state) or self.beak_buster(state)

    def QM_to_WL(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.grip_grab(state) and self.flap_flip(state)
        else:
            return (self.grip_grab(state) or self.beak_buster(state)) and self.flap_flip(state)

    def outside_gi_to_floor1(self, state: CollectionState) -> bool:
        if self.glitches_logic(state):
            return self.clockwork_shot(state) or self.world.options.open_gi_frontdoor.value
        else:
            return self.world.options.open_gi_frontdoor.value

    def outside_gi_to_outside_back(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.climb(state) and self.flap_flip(state) and self.long_jump(state) and self.grip_grab(state) # The intended way to not take damage!
        elif self.easy_tricks_logic(state):
            return self.climb(state)
        else:
            return self.climb(state) or self.extremelyLongJump(state)

    def outside_gi_back_to_floor2(self, state: CollectionState) -> bool:
        if self.glitches_logic(state):
            return self.clockwork_eggs(state) and (self.climb(state) or self.extremelyLongJump(state))
        else:
            return False

    def outside_gi_to_flight(self, state: CollectionState) -> bool:
        return self.outside_gi_to_outside_back(state) and self.flight_pad(state) and self.gi_flight_pad_switch(state)

    def outside_gi_back_to_flight(self, state: CollectionState) -> bool:
        return self.climb(state) and self.flight_pad(state) and self.gi_flight_pad_switch(state)

    def outside_gi_back_to_floor_4(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return False
        elif self.easy_tricks_logic(state):
            return self.claw_clamber_boots(state) and (self.flutter(state) or self.air_rat_a_tat_rap(state)) and self.small_elevation(state)
        else:
            return self.claw_clamber_boots(state) and (self.flutter(state) or self.air_rat_a_tat_rap(state))

    def outside_gi_back_to_floor_3(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return False
        else:
            return self.claw_clamber_boots(state) and (self.flutter(state) or self.air_rat_a_tat_rap(state))

    def em_chamber_to_elevator_shaft(self, state: CollectionState) -> bool:
        return self.elevator_door(state)

    def boiler_plant_to_elevator_shaft(self, state: CollectionState) -> bool:
        return self.elevator_door(state)

    def floor_4_back_to_elevator_shaft(self, state: CollectionState) -> bool:
        if self.glitches_logic(state):
            return self.climb(state) and self.elevator_door(state)\
                    or state.can_reach_region(regionName.GI4, self.player) and self.clockwork_warp(state) and (self.spring_pad(state) or self.flap_flip(state))
        else:
            return self.climb(state) and self.elevator_door(state)

    # If you can fly, then you can enter floor 1 from the window.
    def flight_to_floor_1(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return (self.beak_bomb(state) or self.egg_aim(state) or self.airborne_egg_aiming(state))\
                    and (self.flutter(state) or self.air_rat_a_tat_rap(state))
        elif self.easy_tricks_logic(state):
            return (self.beak_bomb(state)
                        or self.egg_aim(state)
                        or self.airborne_egg_aiming(state)
                        or self.has_explosives(state))\
                    and (self.flutter(state) or self.air_rat_a_tat_rap(state))
        else:
            return (self.beak_bomb(state)
                   or self.egg_aim(state)
                   or self.airborne_egg_aiming(state)
                   or self.has_explosives(state))

    def flight_to_boiler_plant(self, state: CollectionState) -> bool:
        return self.flight_pad(state) and (self.beak_bomb(state) or self.has_explosives(state) and (self.egg_aim(state) or self.airborne_egg_aiming(state)))

    def roof_to_upper_floors(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return False
        elif self.easy_tricks_logic(state):
            return self.beak_buster(state) or self.flutter(state) or self.air_rat_a_tat_rap(state)
        else:
            return True

    def roof_to_ground_level(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return False
        else:
            return self.beak_buster(state)

    # This is disgusting, but will get rewritten later.
    def roof_to_floor5(self, state: CollectionState) -> bool:
        return self.leg_spring(state) or self.spring_pad(state)

    def elevator_shaft_to_floor_1(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.climb(state)
        elif self.easy_tricks_logic(state):
            return self.climb(state) or self.beak_buster(state)
        else:
            return self.climb(state) or self.beak_buster(state)\
                   or state.can_reach_region(regionName.GI2EM, self.player) and self.em_chamber_to_elevator_shaft(state)\
                   or state.can_reach_region(regionName.GI3B, self.player) and self.health_upgrades(state, 2) and self.boiler_plant_to_elevator_shaft(state)\
                   or state.can_reach_region(regionName.GI4B, self.player) and self.health_upgrades(state, 5) and self.floor_4_back_to_elevator_shaft(state)

    def elevator_shaft_to_em(self, state: CollectionState) -> bool:
        if self.glitches_logic(state):
            return (self.climb(state)
                        or state.can_reach_region(regionName.GI3B, self.player) and self.boiler_plant_to_elevator_shaft(state)
                        or state.can_reach_region(regionName.GI4B, self.player) and (self.health_upgrades(state, 2) or self.beak_buster(state)) and self.floor_4_back_to_elevator_shaft(state))\
                    and self.breegull_bash(state)
        else:
            return False

    def elevator_shaft_to_boiler_plant(self, state: CollectionState) -> bool:
        if self.glitches_logic(state):
            return (self.climb(state)
                        or state.can_reach_region(regionName.GI4B, self.player) and self.floor_4_back_to_elevator_shaft(state))\
                    and self.breegull_bash(state)
        else:
            return False

    def elevator_shaft_to_floor_4(self, state: CollectionState) -> bool:
        if self.glitches_logic(state):
            return self.climb(state) and (self.breegull_bash(state) or self.grenade_eggs(state) and self.egg_aim(state))
        else:
            return False


    def health_upgrades(self, state: CollectionState, amt) -> bool:
        if self.world.options.honeyb_rewards.value:
            return state.has(itemName.HEALTHUP, self.player, amt)
        else:
            if amt == 1:
                return state.can_reach_region(regionName.IOHPL, self.player) and state.has(itemName.HONEY, self.player, 1) and self.talon_trot(state)
            if amt == 2:
                return state.can_reach_region(regionName.IOHPL, self.player) and state.has(itemName.HONEY, self.player, 4) and self.talon_trot(state)
            if amt == 3:
                return state.can_reach_region(regionName.IOHPL, self.player) and state.has(itemName.HONEY, self.player, 9) and self.talon_trot(state)
            if amt == 4:
                return state.can_reach_region(regionName.IOHPL, self.player) and state.has(itemName.HONEY, self.player, 16) and self.talon_trot(state)
            if amt == 5:
                return state.can_reach_region(regionName.IOHPL, self.player) and state.has(itemName.HONEY, self.player, 25) and self.talon_trot(state)
        return False #Should never hit here.

    def elevator_door(self, state: CollectionState) -> bool:
        return self.beak_barge(state)\
                or self.grenade_eggs(state)\
                or self.ground_rat_a_tat_rap(state)\
                or self.air_rat_a_tat_rap(state)

    def gi_low_flight_pad_solo_kazooie(self, state: CollectionState) -> bool:
        return self.split_up(state) and self.flight_pad(state) and self.gi_flight_pad_switch(state)\
                and ((self.tall_jump(state) or self.leg_spring(state)) and state.can_reach_region(regionName.GI1, self.player)
                    or self.leg_spring(state) and state.can_reach_region(regionName.GI2, self.player))

    def F1_to_F2(self, state: CollectionState) -> bool:
        return self.claw_clamber_boots(state) and (self.spring_pad(state) or self.leg_spring(state))

    def F1_to_F5(self, state: CollectionState) -> bool:
        if self.intended_logic(state) or self.easy_tricks_logic(state):
            return self.gi_low_flight_pad_solo_kazooie(state)
        else:
            return self.gi_low_flight_pad_solo_kazooie(state)\
                    or self.split_up(state) and self.claw_clamber_boots(state) and self.leg_spring(state) and (self.wing_whack(state) or self.egg_aim(state)) and self.flight_pad(state)

    def F2_to_F1(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.grip_grab(state) and self.flap_flip(state)
        else:
            return (self.grip_grab(state) or self.beak_buster(state)) and self.flap_flip(state)

    def F2_to_F3(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return (self.flap_flip(state) and self.grip_grab(state) and self.claw_clamber_boots(state) and self.climb(state))
        elif self.glitches_logic(state):
            return ((self.flap_flip(state) and self.grip_grab(state) or self.very_long_jump(state))
                        and self.claw_clamber_boots(state)
                        and (self.climb(state) or (self.grenade_eggs(state) and self.third_person_egg_shooting(state) and self.flap_flip(state) and self.beak_buster(state))))\
                    # or self.leg_spring(state) and self.floor_2_split_up(state)
        else:
            return ((self.flap_flip(state) and self.grip_grab(state) or self.very_long_jump(state)) and self.claw_clamber_boots(state) and self.climb(state))\
                   # or self.leg_spring(state) and self.floor_2_split_up(state)

    def floor_2_to_em_room(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.floor_2_split_up(state) and self.grip_grab(state) and self.can_use_battery(state)
        else:
            return self.floor_2_split_up(state) and self.can_use_battery(state)

    def floor_2_em_room_to_elevator_shaft(self, state: CollectionState) -> bool:
        return self.elevator_door(state)

    def floor_2_split_up(self, state: CollectionState) -> bool:
        if self.intended_logic(state) or self.easy_tricks_logic(state):
            return self.split_up(state) and\
                   (self.climb(state) or self.has_explosives(state))
        else:
            return self.split_up(state) and\
                    (self.climb(state) or self.has_explosives(state) or self.claw_clamber_boots(state) and self.extremelyLongJump(state))

    def F3_to_F2(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.climb(state)
        elif self.easy_tricks_logic(state):
            return self.climb(state) or (self.flap_flip(state) and self.beak_buster(state) and self.very_long_jump(state))
        else:
            return self.climb(state)\
                   or self.flap_flip(state) and self.very_long_jump(state)\
                   or self.tall_jump(state) and (self.flutter(state) or self.air_rat_a_tat_rap(state))

    def F3_to_F4(self, state: CollectionState) -> bool:
        return (self.climb(state) or self.leg_spring(state)) and self.small_elevation(state)

    def drop_down_from_higher_floors_outside(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return False
        elif self.easy_tricks_logic(state):
            return self.beak_buster(state) or self.flutter(state) or self.air_rat_a_tat_rap(state)
        else:
            return True

    def escape_floor_4_bk(self, state: CollectionState) -> bool:
        if self.intended_logic(state) or self.easy_tricks_logic(state):
            return self.springy_step_shoes(state)
        else:
            return self.springy_step_shoes(state) or self.flap_flip(state) and self.grip_grab(state)

    def floor_4_to_outside_back(self, state: CollectionState) -> bool:
        return self.escape_floor_4_bk(state) and self.drop_down_from_higher_floors_outside(state)

    def floor_3_to_outside_back(self, state: CollectionState) -> bool:
        return self.climb(state) and self.drop_down_from_higher_floors_outside(state)

    def floor_3_split_up(self, state: CollectionState) -> bool:
        if self.intended_logic(state) or self.easy_tricks_logic(state):
            return self.split_up(state) and self.small_elevation(state)
        else:
            return self.split_up(state)

    def floor_4_to_floor_3(self, state: CollectionState) -> bool:
        #Small elevation to reach the floor 4 split up pad
        return self.escape_floor_4_bk(state) or self.leg_spring(state) and self.small_elevation(state)

    def floor_4_to_floor_4_back(self, state: CollectionState) -> bool:
        if self.glitches_logic(state):
            return self.mumboGI(state) and self.tall_jump(state) and (
                        state.has(itemName.WARPGI3, self.player) and state.has(itemName.WARPGI4, self.player)
                        if self.world.options.randomize_warp_pads.value
                        else state.can_reach_region(regionName.GI3, self.player) and state.can_reach_region(regionName.GI4, self.player)
                    )\
                    or self.tall_jump(state) and self.pack_whack(state)\
                    or self.precise_clockwork_warp(state) and (self.spring_pad(state) or self.flap_flip(state))
        else:
            return self.mumboGI(state) and self.tall_jump(state)\
                   and (
                       state.has(itemName.WARPGI3, self.player) and state.has(itemName.WARPGI4, self.player)
                       if self.world.options.randomize_warp_pads.value
                       else state.can_reach_region(regionName.GI3, self.player) and state.can_reach_region(regionName.GI4, self.player)
                   )


    # Unused due to warp pads
    def floor_4_to_floor_5(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return False
        else:
            return self.leg_spring(state) and self.flight_pad(state) and self.small_elevation(state)


    # Unused due to warp pads
    def floor_3_to_floor_5(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return False
        else:
            return self.leg_spring(state) and self.flight_pad(state) and self.floor_3_split_up(state) and self.gi_flight_pad_switch(state)

    def enter_floor_3_from_fire_exit(self, state: CollectionState) -> bool:
        return state.can_reach_region(regionName.GIOB, self.player) and self.outside_gi_back_to_floor_3(state)\
                or state.can_reach_region(regionName.GI4, self.player) and self.floor_4_to_floor_3(state)\
                or state.can_reach_region(regionName.GIR, self.player) and self.roof_to_upper_floors(state)

    def floor_3_to_boiler_plant(self, state: CollectionState) -> bool:
        return self.flap_flip(state) and self.grip_grab(state)\
               or self.climb(state) and self.slightly_elevated_ledge(state)

    def WL_to_PGU(self, state: CollectionState) -> bool:
        # Going through the loading zone gives you dive for free, which is a thing beginners would not know.
        # If nestsanity is turned on, players are forced to go through the digger tunnel
        if self.intended_logic(state):
            return self.talon_torpedo(state) and self.dive(state)
        elif self.glitches_logic(state):
            return (not self.world.options.nestsanity.value or self.dive(state) or self.beak_buster(state))
        else:
            return self.talon_torpedo(state)\
                   and (not self.world.options.nestsanity.value or self.dive(state) or self.beak_buster(state))

    def tdl_to_hatch(self, state: CollectionState) -> bool:
        logic = True
        if self.intended_logic(state):
            logic = self.long_jump(state)\
                    or self.springy_step_shoes(state)
        elif self.easy_tricks_logic(state):
            logic = self.long_jump(state)\
                    or self.springy_step_shoes(state)\
                    or self.split_up(state)
        elif self.hard_tricks_logic(state):
            logic = self.long_jump(state)\
                    or self.springy_step_shoes(state)\
                    or state.can_reach_region(regionName.TLTOP, self.player)\
                    or self.split_up(state)
        elif self.glitches_logic(state):
            logic = self.long_jump(state)\
                    or self.springy_step_shoes(state)\
                    or self.TDL_flight_pad(state)\
                    or self.split_up(state)\
                    or state.can_reach_region(regionName.TLTOP, self.player)
        return logic

    def can_dive_in_jrl(self, state: CollectionState) -> bool:
        return self.dive(state)

    def JRL_to_CT(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.jrl_jiggy(state)
        else:
            return True

    def HFP_to_CTHFP(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.hfp_jiggy(state)
        else:
            return True

    def CCL_to_WL(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.ccl_jiggy(state)
        else:
            return True

    def CK_to_Quag(self, state: CollectionState) -> bool:
        if self.intended_logic(state) or self.easy_tricks_logic(state):
            return self.ck_jiggy(state)
        else:
            return True

    def TDL_to_IOHWL(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.tdl_jiggy(state)
        else:
            return True

    def TDL_to_WW(self, state: CollectionState) -> bool:
        if self.glitches_logic(state):
            return (self.spring_pad(state) or self.has_explosives(state)) and (self.oogle_boogles_open(state) or
                self.clockwork_warp(state))
        else:
            return self.oogle_boogles_open(state) and (self.spring_pad(state) or self.has_explosives(state))

    def hfp_jiggy(self, state: CollectionState) -> bool: # 36
        if self.world.options.randomize_worlds.value:
            return state.has(itemName.HFA, self.player)
        else:
            amt = self.world.world_requirements[regionName.HP]
            return state.has(itemName.JIGGY, self.player, amt)

    def ccl_jiggy(self, state: CollectionState) -> bool: # 45
        if self.world.options.randomize_worlds.value:
            return state.has(itemName.CCA, self.player)
        else:
            amt = self.world.world_requirements[regionName.CC]
            return state.has(itemName.JIGGY, self.player, amt)

    def HFP_hot_water_cooled(self, state: CollectionState) -> bool:
        if self.world.options.backdoors.value:
            return state.can_reach_region(regionName.HP, self.player) and\
               self.split_up(state) and\
               (self.dive(state) or self.shack_pack(state))
        else:
            return state.can_reach_region(regionName.HP, self.player) and\
               self.boop_george(state) and \
               self.split_up(state) and\
               self.ground_attack(state) and\
               (self.dive(state) or self.shack_pack(state))

    def boop_george(self, state: CollectionState) -> bool:
        return state.can_reach_region(regionName.CC, self.player) and (
            self.beak_barge(state)
            or self.roll(state)
            or self.air_rat_a_tat_rap(state)
            or self.ground_rat_a_tat_rap(state)
            or self.grip_grab(state)
            or self.pack_whack(state)
            or self.wing_whack(state)
        )

    def can_use_floatus(self, state: CollectionState) -> bool:
        return self.taxi_pack(state) and self.hatch(state)

    def has_enough_beans(self, state: CollectionState) -> bool:
        if self.world.options.randomize_beans.value:
            return state.has(itemName.BEANS, self.player, 2)
        else:
            return self.bill_drill(state)

    def grow_beanstalk(self, state: CollectionState) -> bool:
        return self.has_enough_beans(state) and self.mumboCCL(state) and self.flight_pad(state) and self.climb(state)

    def check_hag1_options(self, state: CollectionState) -> bool:
        door_open = False
        if self.world.options.victory_condition.value == VictoryCondition.option_hag1:
            door_open = self.world.options.open_hag1.value == 1 or state.has(itemName.JIGGY, self.player, 70)
        elif self.world.options.victory_condition.value == VictoryCondition.option_wonderwing_challenge:
            door_open = state.has(itemName.MUMBOTOKEN, self.player, 32)
        elif self.world.options.victory_condition.value == VictoryCondition.option_boss_hunt_and_hag1:
            door_open = state.has(itemName.MUMBOTOKEN, self.player, self.world.options.boss_hunt_length.value)

        if self.intended_logic(state):
            return door_open and \
                self.warp_pad_ck_top(state) and \
                self.breegull_blaster(state) and \
                self.clockwork_eggs(state)\
                and self.can_shoot_linear_egg(state)\
                and (self.talon_trot(state) and self.tall_jump(state))
        elif self.easy_tricks_logic(state):
            return door_open and \
                self.warp_pad_ck_top(state) and \
                self.breegull_blaster(state) and \
                self.clockwork_eggs(state)\
                and self.can_shoot_linear_egg(state)\
                and (self.talon_trot(state) or self.tall_jump(state))
        else:
            return door_open and \
                self.warp_pad_ck_top(state) and \
                self.breegull_blaster(state) and \
                self.clockwork_eggs(state) and \
                self.can_shoot_linear_egg(state)

    def reach_cheato(self, state: CollectionState, page_amt: int) -> bool:
        return state.has(itemName.PAGES, self.player, page_amt)

    def has_BK_move(self, state: CollectionState, move) -> bool:
        if move == itemName.BEGGS:
            raise ValueError("Use self.blueEgg(state) instead!")
        if move not in [itemName.DIVE, itemName.FPAD, itemName.GRAT, itemName.ROLL, itemName.ARAT, itemName.BBARGE,
                        itemName.TJUMP, itemName.FLUTTER, itemName.FFLIP, itemName.CLIMB, itemName.TTROT, itemName.BBUST,
                        itemName.WWING, itemName.SSTRIDE, itemName.TTRAIN, itemName.BBOMB, itemName.EGGAIM, itemName.EGGSHOOT]:
            raise ValueError(f"Not a BK move! {move}")
        if self.world.options.randomize_bk_moves.value == RandomizeBKMoveList.option_none:
            return True
        if self.world.options.randomize_bk_moves.value == RandomizeBKMoveList.option_mcjiggy_special and move in [itemName.TTROT, itemName.TJUMP]:
            return True
        return state.has(move, self.player)

    # You need tall jump to let the charging animation finish.
    def spring_pad(self, state: CollectionState) -> bool:
        return self.tall_jump(state)

    def small_elevation(self, state: CollectionState) -> bool:
        return self.flap_flip(state) or self.tall_jump(state) or self.talon_trot(state)

    def slightly_elevated_ledge(self, state: CollectionState) -> bool:
        return (self.flap_flip(state) or self.tall_jump(state) or (self.talon_trot(state) and self.flutter(state))) and self.grip_grab(state)

    def ground_attack(self, state: CollectionState) -> bool:
        return self.can_shoot_any_egg(state) or self.beak_barge(state) or self.roll(state)\
            or self.air_rat_a_tat_rap(state) or self.ground_rat_a_tat_rap(state) or self.beak_buster(state) or self.breegull_bash(state) or self.wonderwing(state)

    def repeatable_ground_attack(self, state: CollectionState) -> bool:
        return self.blue_eggs(state) or self.fire_eggs(state) or self.grenade_eggs(state) or self.ice_eggs(state) or self.beak_barge(state) or self.roll(state)\
            or self.air_rat_a_tat_rap(state) or self.ground_rat_a_tat_rap(state) or self.beak_buster(state) or self.breegull_bash(state)

    def mobile_attack(self, state: CollectionState) -> bool:
        return self.can_shoot_any_egg(state) or self.beak_barge(state) or self.roll(state) or self.air_rat_a_tat_rap(state) or self.wonderwing(state)

    def repeatable_mobile_attack(self, state: CollectionState) -> bool:
        return self.blue_eggs(state) or self.fire_eggs(state) or self.grenade_eggs(state) or self.ice_eggs(state)\
               or self.beak_barge(state) or self.roll(state) or self.air_rat_a_tat_rap(state)

    def can_shoot_any_egg(self, state: CollectionState) -> bool:
        return self.egg_aim(state) or self.third_person_egg_shooting(state)

    # The regular variant of the function check to see if you can shoot the eggs, the "item" variant only checks if you have the egg item
    def blue_eggs(self, state: CollectionState) -> bool:
        if not self.can_shoot_any_egg(state):
            return False
        return self.blue_eggs_item(state)

    def blue_eggs_item(self, state: CollectionState) -> bool:
        if self.world.options.egg_behaviour.value == EggsBehaviour.option_random_starting_egg or \
            self.world.options.egg_behaviour.value == EggsBehaviour.option_simple_random_starting_egg:
            return state.has(itemName.BEGGS, self.player)
        return True

    def fire_eggs(self, state: CollectionState) -> bool:
        if not self.can_shoot_any_egg(state):
            return False
        return self.fire_eggs_item(state)

    def fire_eggs_item(self, state: CollectionState) -> bool:
        if self.world.options.egg_behaviour.value == EggsBehaviour.option_progressive_eggs:
            return state.has(itemName.PEGGS, self.player, 1)
        return state.has(itemName.FEGGS, self.player)

    def grenade_eggs(self, state: CollectionState) -> bool:
        if not self.can_shoot_any_egg(state):
            return False
        return self.grenade_eggs_item(state)

    def grenade_eggs_item(self, state: CollectionState) -> bool:
        if self.world.options.egg_behaviour.value == EggsBehaviour.option_progressive_eggs:
            return state.has(itemName.PEGGS, self.player, 2)
        return state.has(itemName.GEGGS, self.player)

    def ice_eggs(self, state: CollectionState) -> bool:
        if not self.can_shoot_any_egg(state):
            return False
        return self.ice_eggs_item(state)

    def ice_eggs_item(self, state: CollectionState) -> bool:
        if self.world.options.egg_behaviour.value == EggsBehaviour.option_progressive_eggs:
            return state.has(itemName.PEGGS, self.player, 3)
        return state.has(itemName.IEGGS, self.player)

    def clockwork_eggs(self, state: CollectionState) -> bool:
        if not self.can_shoot_any_egg(state):
            return False
        return self.clockwork_eggs_item(state)

    def clockwork_eggs_item(self, state: CollectionState) -> bool:
        if self.world.options.egg_behaviour.value == EggsBehaviour.option_progressive_eggs:
            return state.has(itemName.PEGGS, self.player, 4)
        return state.has(itemName.CEGGS, self.player)

    def can_shoot_linear_egg(self, state: CollectionState) -> bool:
        return self.has_linear_egg(state) and (self.egg_aim(state) or self.third_person_egg_shooting(state))

    def has_linear_egg(self, state: CollectionState) -> bool:
        return self.blue_eggs(state) or\
                self.fire_eggs(state) or\
                self.grenade_eggs(state) or\
                self.ice_eggs(state)

    def canGetPassedKlungo(self, state: CollectionState) -> bool:
        if self.world.options.skip_klungo.value == 1:
            return True
        if self.intended_logic(state) or self.easy_tricks_logic(state):
            return self.mobile_attack(state)
        else:
            return self.ground_attack(state)

    def clockwork_warp(self, state: CollectionState) -> bool:
        return self.clockwork_eggs(state) and self.grenade_eggs(state) and self.egg_aim(state) and self.third_person_egg_shooting(state)

    # Sometimes, it's nice to have talon trot to do a precise 180 turn during a clockwork warp
    def precise_clockwork_warp(self, state: CollectionState) -> bool:
        return self.clockwork_warp(state) and self.talon_trot(state)

    def grip_grab(self, state: CollectionState) -> bool:
        return state.has(itemName.GGRAB, self.player)

    def breegull_blaster(self, state: CollectionState) -> bool:
        return state.has(itemName.BBLASTER, self.player) or state.has(itemName.PAEGGAIM, self.player, 4)

    def egg_aim(self, state: CollectionState) -> bool:
        return state.has(itemName.EGGAIM, self.player) or state.has(itemName.PEGGAIM, self.player, 2) \
        or state.has(itemName.PAEGGAIM, self.player, 3)

    #You cannot use bill drill without beak buster. Pressing Z in the air does nothing.
    def bill_drill(self, state: CollectionState) -> bool:
        return (self.has_BK_move(state, itemName.BBUST) and state.has(itemName.BDRILL, self.player))\
            or state.has(itemName.PBBUST, self.player, 2)

    def beak_bayonet(self, state: CollectionState) -> bool:
        return state.has(itemName.BBAYONET, self.player)

    def split_up(self, state: CollectionState) -> bool:
        return state.has(itemName.SPLITUP, self.player)

    def pack_whack(self, state: CollectionState) -> bool:
        return self.check_solo_moves(state, itemName.PACKWH)

    def airborne_egg_aiming(self, state: CollectionState) -> bool:
        return state.has(itemName.AIREAIM, self.player) or state.has(itemName.PFLIGHT, self.player, 3)

    def wing_whack(self, state: CollectionState) -> bool:
        return self.check_solo_moves(state, itemName.WWHACK)

    def sub_aqua_egg_aiming(self, state: CollectionState) -> bool:
        return state.has(itemName.AUQAIM, self.player) or state.has(itemName.PASWIM, self.player, 2)

    def talon_torpedo(self, state: CollectionState) -> bool:
        return state.has(itemName.TTORP, self.player) or state.has(itemName.PASWIM, self.player, 3)

    def springy_step_shoes(self, state: CollectionState) -> bool:
        return state.has(itemName.SPRINGB, self.player) or state.has(itemName.PSHOES, self.player, 3)

    def taxi_pack(self, state: CollectionState) -> bool:
        return self.check_solo_moves(state, itemName.TAXPACK)

    def hatch(self, state: CollectionState) -> bool:
        return self.check_solo_moves(state, itemName.HATCH)

    def claw_clamber_boots(self, state: CollectionState) -> bool:
        return state.has(itemName.CLAWBTS, self.player) or state.has(itemName.PSHOES, self.player, 4)

    def snooze_pack(self, state: CollectionState) -> bool:
        return self.check_solo_moves(state, itemName.SNPACK)

    def leg_spring(self, state: CollectionState) -> bool:
        return self.check_solo_moves(state, itemName.LSPRING)

    def shack_pack(self, state: CollectionState) -> bool:
        return self.check_solo_moves(state, itemName.SHPACK)

    def glide(self, state: CollectionState) -> bool:
        return self.check_solo_moves(state, itemName.GLIDE)

    def sack_pack(self, state: CollectionState) -> bool:
        return self.check_solo_moves(state, itemName.SAPACK)

    #You cannot use breegull bash without the ground ratatat rat, pressing B does nothing.
    def breegull_bash(self, state: CollectionState) -> bool:
        return (self.has_BK_move(state, itemName.GRAT) and state.has(itemName.BBASH, self.player))\
            or state.has(itemName.PBASH, self.player, 2)

    def amaze_o_gaze(self, state: CollectionState) -> bool:
        return state.has(itemName.AMAZEOGAZE, self.player) or state.has(itemName.PAEGGAIM, self.player, 2)

    def doubleAir(self, state: CollectionState) -> bool:
        return state.has(itemName.DAIR, self.player) or state.has(itemName.PSWIM, self.player, 2) \
        or state.has(itemName.PASWIM, self.player, 4)

    def dive(self, state: CollectionState) -> bool:
        return self.has_BK_move(state, itemName.DIVE) or state.has(itemName.PSWIM, self.player, 1) \
        or state.has(itemName.PASWIM, self.player, 1)

    def tall_jump(self, state: CollectionState) -> bool:
        return self.has_BK_move(state, itemName.TJUMP)

    def flutter(self, state: CollectionState) -> bool:
        return self.has_BK_move(state, itemName.FLUTTER)

    def flap_flip(self, state: CollectionState) -> bool:
        return self.has_BK_move(state, itemName.FFLIP)

    def climb(self, state: CollectionState) -> bool:
        return self.has_BK_move(state, itemName.CLIMB)

    def ground_rat_a_tat_rap(self, state: CollectionState) -> bool:
        return self.has_BK_move(state, itemName.GRAT) or state.has(itemName.PBASH, self.player)

    def roll(self, state: CollectionState) -> bool:
        return self.has_BK_move(state, itemName.ROLL)

    def air_rat_a_tat_rap(self, state: CollectionState) -> bool:
        return self.has_BK_move(state, itemName.ARAT)

    def beak_barge(self, state: CollectionState) -> bool:
        return self.has_BK_move(state, itemName.BBARGE)

    def third_person_egg_shooting(self, state: CollectionState) -> bool:
        return self.has_BK_move(state, itemName.EGGSHOOT) or state.has(itemName.PEGGAIM, self.player, 1) \
        or state.has(itemName.PAEGGAIM, self.player, 1)

    def talon_trot(self, state: CollectionState) -> bool:
        return self.has_BK_move(state, itemName.TTROT)

    def beak_buster(self, state: CollectionState) -> bool:
        return self.has_BK_move(state, itemName.BBUST) or state.has(itemName.PBBUST, self.player)

    def flight_pad(self, state: CollectionState) -> bool:
        return self.has_BK_move(state, itemName.FPAD) or state.has(itemName.PFLIGHT, self.player, 1)

    def wonderwing(self, state: CollectionState) -> bool:
        return self.has_BK_move(state, itemName.WWING)

    def stilt_stride(self, state: CollectionState) -> bool:
        return self.has_BK_move(state, itemName.SSTRIDE) or state.has(itemName.PSHOES, self.player, 1)

    def beak_bomb(self, state: CollectionState) -> bool:
        return self.has_BK_move(state, itemName.BBOMB) or state.has(itemName.PFLIGHT, self.player, 2)

    def turbo_trainers(self, state: CollectionState) -> bool:
        return self.has_BK_move(state, itemName.TTRAIN) or state.has(itemName.PSHOES, self.player, 2)

    def intended_logic(self, state: CollectionState) -> bool:
        return self.world.options.logic_type.value == LogicType.option_intended and not state.has(itemName.UT_GLITCHED, self.player)

    def easy_tricks_logic(self, state: CollectionState) -> bool:
        return self.world.options.logic_type.value == LogicType.option_easy_tricks and not state.has(itemName.UT_GLITCHED, self.player)

    def hard_tricks_logic(self, state: CollectionState) -> bool:
        return self.world.options.logic_type.value == LogicType.option_hard_tricks and not state.has(itemName.UT_GLITCHED, self.player)

    def glitches_logic(self, state: CollectionState) -> bool:
        return self.world.options.logic_type.value == LogicType.option_glitches or state.has(itemName.UT_GLITCHED, self.player)


    def long_jump(self, state: CollectionState) -> bool:
        return self.talon_trot(state) or self.flutter(state) or self.air_rat_a_tat_rap(state)

    def very_long_jump(self, state: CollectionState) -> bool:
        return self.talon_trot(state) and (self.flutter(state) or self.air_rat_a_tat_rap(state)) or\
                (self.tall_jump(state) and self.roll(state) and self.flutter(state))

    def extremelyLongJump(self, state: CollectionState) -> bool:
        if self.intended_logic(state) or self.easy_tricks_logic(state):
            return False
        else:
            return self.talon_trot(state) and (self.flutter(state) or self.air_rat_a_tat_rap(state)) and self.beak_buster(state)

    def humbaMT(self, state: CollectionState) -> bool:
        return state.can_reach_region(regionName.MTJSG, self.player) and state.has(itemName.HUMBAMT, self.player)

    def humbaGGM(self, state: CollectionState) -> bool:
        return state.has(itemName.HUMBAGM, self.player) and (self.ggm_trot(state) or self.warp_to_ggm_wumba(state))

    def mumboGGM(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.small_elevation(state) and state.has(itemName.MUMBOGM, self.player)\
                    and state.can_reach_region(regionName.GM, self.player)
        else:
            return self.ggm_trot(state) and state.has(itemName.MUMBOGM, self.player)\
                   and state.can_reach_region(regionName.GM, self.player)

    def ggm_trot(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.talon_trot(state)
        else:
            return self.talon_trot(state) or self.turbo_trainers(state) or self.springy_step_shoes(state)

    def humbaWW(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return state.has(itemName.HUMBAWW, self.player) and (
                        self.flap_flip(state) and self.grip_grab(state)
                        or self.warp_to_ww_wumba(state)
                    )
        else:
            return state.has(itemName.HUMBAWW, self.player) and (
                       self.flap_flip(state) and self.grip_grab(state)
                       or self.climb(state) and self.very_long_jump(state) and self.flap_flip(state)
                       or self.warp_to_ww_wumba(state)
                   )

    def mumboWW(self, state: CollectionState) -> bool:
        if self.glitches_logic(state):
            return state.can_reach_region(regionName.WWI, self.player) and state.has(itemName.MUMBOWW, self.player)\
                    and self.escape_inferno_as_mumbo(state)
        else:
            return state.can_reach_region(regionName.WWI, self.player) and state.has(itemName.MUMBOWW, self.player)

    def escape_inferno_as_mumbo(self, state: CollectionState) -> bool:
        return self.humbaWW(state)\
                or state.has(itemName.WARPWW5, self.player) and (
                    state.has(itemName.WARPWW1, self.player)
                    or state.has(itemName.WARPWW2, self.player)
                    or state.has(itemName.WARPWW3, self.player)
                    or state.has(itemName.WARPWW4, self.player)
                )

    def mumboTDL(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.stilt_stride(state) and state.has(itemName.MUMBOTD, self.player)
        else:
            return state.has(itemName.MUMBOTD, self.player)

    def mumboGI(self, state: CollectionState) -> bool:
        if self.intended_logic(state) or self.easy_tricks_logic(state):
            return self.small_elevation(state) and state.has(itemName.MUMBOGI, self.player) and state.can_reach_region(regionName.GI3, self.player)
        else:
            return state.has(itemName.MUMBOGI, self.player) and state.can_reach_region(regionName.GI3, self.player) and \
                    self.small_elevation(state)


    def humbaGI(self, state: CollectionState) -> bool:
        return state.has(itemName.HUMBAGI, self.player) and state.can_reach_region(regionName.GI2, self.player)

    def humbaHFP(self, state: CollectionState) -> bool:
        return self.hfp_top(state) and state.has(itemName.HUMBAHP, self.player)

    def mumboCCL(self, state: CollectionState) -> bool:
        return self.tall_jump(state) and state.has(itemName.MUMBOCC, self.player)

    def humbaJRL(self, state: CollectionState) -> bool:
        return state.can_reach_region(regionName.JRAT, self.player) and state.has(itemName.HUMBAJR, self.player)

    def humbaTDL(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.small_elevation(state) and state.has(itemName.HUMBATD, self.player)
        else:
            return state.has(itemName.HUMBATD, self.player)

    def bargasaurus_roar(self, state: CollectionState) -> bool:
        return self.humbaTDL(state)

    def roar(self, state: CollectionState) -> bool:
        return state.has(itemName.ROAR, self.player) or not self.world.options.randomize_dino_roar.value

    def TDL_flight_pad(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.can_beat_terry(state) and self.springy_step_shoes(state) and self.flight_pad(state)
        else:
            return self.can_beat_terry(state) and self.flight_pad(state)\
                   and (self.springy_step_shoes(state) or (self.talon_trot(state) and self.flutter(state)))

    def GGM_slope(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.ggm_trot(state)
        else:
            return self.ggm_trot(state) or (self.ggm_boulders(state) and self.split_up(state))

    def clockwork_shot(self, state: CollectionState) -> bool:
        return self.clockwork_eggs(state) and self.egg_aim(state)

    def egg_barge(self, state: CollectionState) -> bool:
        return (self.blue_eggs(state) or self.fire_eggs(state) or self.ice_eggs(state)) and self.third_person_egg_shooting(state) and self.beak_barge(state)

    def can_dive_in_JRL(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.dive(state) and state.has(itemName.MUMBOJR, self.player)
        else:
            return self.dive(state)

    def hfp_top(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.small_elevation(state)\
                    or self.flight_pad(state)\
                    or (state.can_reach_region(regionName.CHUFFY, self.player) and state.has(itemName.TRAINSWHP1, self.player))\
                    or self.has_explosives(state)\
                    or self.warp_to_hfp_top(state)
        elif self.easy_tricks_logic(state):
            return self.small_elevation(state)\
                    or self.flight_pad(state)\
                    or state.can_reach_region(regionName.CHUFFY, self.player) and state.has(itemName.TRAINSWHP1, self.player)\
                    or self.has_explosives(state)\
                    or state.has(itemName.MUMBOHP, self.player)\
                    or self.dragon_kazooie(state)\
                    or self.warp_to_hfp_top(state)
        else:
            return self.small_elevation(state)\
                   or self.flight_pad(state)\
                   or self.split_up(state)\
                   or state.can_reach_region(regionName.CHUFFY, self.player) and state.has(itemName.TRAINSWHP1, self.player)\
                   or self.has_explosives(state)\
                   or state.has(itemName.MUMBOHP, self.player)\
                   or self.dragon_kazooie(state)\
                   or self.warp_to_hfp_top(state)

    def notes_boggy(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.ice_cube_BK(state) and self.hfp_top(state) and self.small_elevation(state)
        elif self.easy_tricks_logic(state):
            return self.hfp_top(state)\
                        and (self.ice_cube_BK(state) and (self.small_elevation(state) or self.beak_buster(state))
                             or self.split_up(state) and (self.leg_spring(state) or self.tall_jump(state)) and self.ice_cube_kazooie(state)
                             or self.tall_jump(state) and state.has(itemName.MUMBOHP, self.player)
                             or self.pack_whack(state)
                             or self.humbaHFP(state)
                             )
        else:
            return self.hfp_top(state)\
                       and (self.ice_cube_BK(state) and (self.small_elevation(state) or self.beak_buster(state))
                            or self.split_up(state) and (self.leg_spring(state) or self.tall_jump(state)) and self.ice_cube_kazooie(state)
                            or self.tall_jump(state) and state.has(itemName.MUMBOHP, self.player)
                            or self.pack_whack(state)
                            or self.clockwork_shot(state)
                            or self.humbaHFP(state)
                            )

    def notes_lower_icy_side(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.ice_cube_BK(state) and self.hfp_top(state)
        else:
            return self.hfp_top(state)\
                       and (self.ice_cube_BK(state)
                            or self.split_up(state) and self.ice_cube_kazooie(state)
                            or state.has(itemName.MUMBOHP, self.player)
                            or self.pack_whack(state)
                            or self.humbaHFP(state)
                            )

    def notes_upper_icy_side(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.ice_cube_BK(state) and self.hfp_top(state)
        else:
            return self.hfp_top(state)\
                       and (self.ice_cube_BK(state)
                            or self.split_up(state) and self.ice_cube_kazooie(state)
                            or state.has(itemName.MUMBOHP, self.player)
                            or self.pack_whack(state)
                            or self.humbaHFP(state)
                            )

    def ice_cube_BK(self, state: CollectionState) -> bool:
        return self.blue_eggs(state) or self.fire_eggs(state) or self.has_explosives(state) or self.beak_barge(state) or self.roll(state)\
            or self.air_rat_a_tat_rap(state) or self.ground_rat_a_tat_rap(state) or self.beak_buster(state) or self.breegull_bash(state) or self.wonderwing(state)

    def ice_cube_kazooie(self, state: CollectionState) -> bool:
        return self.split_up(state) and (self.has_explosives(state) or self.fire_eggs(state) or self.blue_eggs(state) or self.wing_whack(state))

    def gi_flight_pad_switch(self, state: CollectionState) -> bool:
        return state.can_reach_region(regionName.GI4, self.player)\
               or self.humbaGI(state)

    def big_al_burgers(self, state: CollectionState) -> bool:
        if self.intended_logic(state):
            return self.tall_jump(state)
        else:
            return self.tall_jump(state) or self.leg_spring(state) or self.glide(state)

    def world_1_unlocked(self, state: CollectionState) -> bool:
        return self.set_world_requirement(state, 1230944)

    def world_2_unlocked(self, state: CollectionState) -> bool:
        return self.set_world_requirement(state, 1230945)

    def world_3_unlocked(self, state: CollectionState) -> bool:
        return self.set_world_requirement(state, 1230946)

    def world_4_unlocked(self, state: CollectionState) -> bool:
        return self.set_world_requirement(state, 1230947)

    def world_5_unlocked(self, state: CollectionState) -> bool:
        return self.set_world_requirement(state, 1230948)

    def world_6_unlocked(self, state: CollectionState) -> bool:
        return self.set_world_requirement(state, 1230949)

    def world_7_unlocked(self, state: CollectionState) -> bool:
        return self.set_world_requirement(state, 1230950)

    def world_8_unlocked(self, state: CollectionState) -> bool:
        return self.set_world_requirement(state, 1230951)

    def world_9_unlocked(self, state: CollectionState) -> bool:
        return self.set_world_requirement(state, 1230952)

    def cheato_reward_1(self, state: CollectionState) -> bool:
        return self.reach_cheato(state, 5)

    def cheato_reward_2(self, state: CollectionState) -> bool:
        return self.reach_cheato(state, 10)

    def cheato_reward_3(self, state: CollectionState) -> bool:
        return self.reach_cheato(state, 15)

    def cheato_reward_4(self, state: CollectionState) -> bool:
        return self.reach_cheato(state, 20)

    def cheato_reward_5(self, state: CollectionState) -> bool:
        return self.reach_cheato(state, 25)

    def silo_egg_aim(self, state: CollectionState) -> bool:
        return self.check_notes(state, locationName.EGGAIM)

    def silo_breegull_blaster(self, state: CollectionState) -> bool:
        return self.check_notes(state, locationName.BBLASTER)

    def silo_grip_grab(self, state: CollectionState) -> bool:
        return self.check_notes(state, locationName.GGRAB)

    def silo_airborne_egg_aiming(self, state: CollectionState) -> bool:
        return self.check_notes(state, locationName.AIREAIM)

    def silo_split_up(self, state: CollectionState) -> bool:
        return self.check_notes(state, locationName.SPLITUP)

    def silo_claw_clamber_boots(self, state: CollectionState) -> bool:
        return self.check_notes(state, locationName.CLAWBTS)

    def silo_fire_eggs(self, state: CollectionState) -> bool:
        return self.check_notes(state, locationName.FEGGS)

    def silo_grenade_eggs(self, state: CollectionState) -> bool:
        return self.check_notes(state, locationName.GEGGS)

    def silo_ice_eggs(self, state: CollectionState) -> bool:
        return self.check_notes(state, locationName.IEGGS)

    def silo_clockwork_eggs(self, state: CollectionState) -> bool:
        return self.check_notes(state, locationName.CEGGS)

    def jiggy_zubbas(self, state: CollectionState) -> bool:
        return state.has(itemName.HUMBACC, self.player)

    def jiggy_jiggium_plant(self, state: CollectionState) -> bool:
        return state.has(itemName.HUMBACC, self.player)

    def cheato_zubbas(self, state: CollectionState) -> bool:
        return self.jiggy_zubbas(state)

    def jiggy_white_jinjo_family(self, state: CollectionState) -> bool:
        return state.has(itemName.WJINJO, self.player, 1)

    def jiggy_orange_jinjo_family(self, state: CollectionState) -> bool:
        return state.has(itemName.OJINJO, self.player, 2)

    def jiggy_yellow_jinjo_family(self, state: CollectionState) -> bool:
        return state.has(itemName.YJINJO, self.player, 3)

    def jiggy_brown_jinjo_family(self, state: CollectionState) -> bool:
        return state.has(itemName.BRJINJO, self.player, 4)

    def jiggy_green_jinjo_family(self, state: CollectionState) -> bool:
        return state.has(itemName.GJINJO, self.player, 5)

    def jiggy_red_jinjo_family(self, state: CollectionState) -> bool:
        return state.has(itemName.RJINJO, self.player, 6)

    def jiggy_blue_jinjo_family(self, state: CollectionState) -> bool:
        return state.has(itemName.BLJINJO, self.player, 7)

    def jiggy_purple_jinjo_family(self, state: CollectionState) -> bool:
        return state.has(itemName.PJINJO, self.player, 8)

    def jiggy_black_jinjo_family(self, state: CollectionState) -> bool:
        return state.has(itemName.BKJINJO, self.player, 9)

    def jiggy_cc_canary_mary(self, state: CollectionState) -> bool:
        return self.canary_mary_free(state) and state.can_reach_region(regionName.GM, self.player)

    def cheato_canary_mary(self, state: CollectionState) -> bool:
        return self.jiggy_cc_canary_mary(state)

    def honey_b_reward_1(self, state: CollectionState) -> bool:
        return state.has(itemName.HONEY, self.player, 1) and self.can_reach_honey_b(state)

    def honey_b_reward_2(self, state: CollectionState) -> bool:
        return state.has(itemName.HONEY, self.player, 4) and self.can_reach_honey_b(state)

    def honey_b_reward_3(self, state: CollectionState) -> bool:
        return state.has(itemName.HONEY, self.player, 9) and self.can_reach_honey_b(state)

    def honey_b_reward_4(self, state: CollectionState) -> bool:
        return state.has(itemName.HONEY, self.player, 16) and self.can_reach_honey_b(state)

    def honey_b_reward_5(self, state: CollectionState) -> bool:
        return state.has(itemName.HONEY, self.player, 25) and self.can_reach_honey_b(state)

    def train_switch_ioh(self, state: CollectionState) -> bool:
        return self.grip_grab(state) and self.flap_flip(state)

    def jiggy_jelly_castle(self, state: CollectionState) -> bool:
        return self.shack_pack(state) and self.climb(state)

    def silo_beak_bayonet(self, state: CollectionState) -> bool:
        return self.ggm_boulders(state) and self.check_notes(state, locationName.BBAYONET)

    def silo_pack_whack(self, state: CollectionState) -> bool:
        return self.split_up(state) and self.check_notes(state, locationName.PACKWH)

    def silo_springy_step_shoes(self, state: CollectionState) -> bool:
        return self.check_notes(state, locationName.SPRINGB) and self.silo_spring(state)

    def silo_taxi_pack(self, state: CollectionState) -> bool:
        return self.can_access_taxi_pack_silo(state) and self.check_notes(state, locationName.TAXPACK)

    def silo_hatch(self, state: CollectionState) -> bool:
        return self.split_up(state) and self.check_notes(state, locationName.HATCH)

    def silo_leg_spring(self, state: CollectionState) -> bool:
        return self.check_notes(state, locationName.LSPRING) and self.split_up(state)

    def silo_shack_pack(self, state: CollectionState) -> bool:
        return self.split_up(state) and self.check_notes(state, locationName.SHPACK)

    def silo_glide(self, state: CollectionState) -> bool:
        return self.can_access_glide_silo(state) and self.check_notes(state, locationName.GLIDE)

    def silo_sack_pack(self, state: CollectionState) -> bool:
        return self.can_access_sack_pack_silo(state) and self.check_notes(state, locationName.SAPACK)

    def jinjo_spiral_mountain(self, state: CollectionState) -> bool:
        return self.talon_torpedo(state) and self.dive(state)

    def jinjo_talon_torpedo(self, state: CollectionState) -> bool:
        return self.talon_torpedo(state) and self.dive(state)

    def silo_sub_aqua_egg_aiming(self, state: CollectionState) -> bool:
        return (self.has_explosives(state) or state.has(itemName.DOUBLOON, self.player, 28)) and self.check_notes(state, locationName.AUQAIM)

    def silo_talon_torpedo(self, state: CollectionState) -> bool:
        return self.can_access_talon_torpedo_silo(state) and self.check_notes(state, locationName.TTORP)

    def silo_wing_whack(self, state: CollectionState) -> bool:
        return (self.has_explosives(state)) and self.split_up(state) and self.check_notes(state, locationName.WWHACK)

    def pink_egg_hatched(self, state: CollectionState) -> bool:
        return state.has(itemName.PMEGG, self.player)

    def blue_egg_hatched(self, state: CollectionState) -> bool:
        return state.has(itemName.BMEGG, self.player)

    def yellow_egg_hatched(self, state: CollectionState) -> bool:
        return (self.has_explosives(state) or self.bill_drill(state)) and self.hatch(state)

    def nest_jr_sub_aqua_1(self, state: CollectionState) -> bool:
        return self.has_explosives(state) or state.has(itemName.DOUBLOON, self.player, 28)

    def nest_jr_sub_aqua_2(self, state: CollectionState) -> bool:
        return self.has_explosives(state) or state.has(itemName.DOUBLOON, self.player, 28)

    def nest_gi_unscrewable_platform(self, state: CollectionState) -> bool:
        return self.egg_aim(state) or self.airborne_egg_aiming(state) or self.beak_bomb(state)

    def nest_chilli_billi_crater(self, state: CollectionState) -> bool:
        return self.flight_pad(state) and self.ice_eggs_item(state)

    def victory_minigame_hunt(self, state: CollectionState) -> bool:
        return state.has(itemName.MUMBOTOKEN, self.player, self.world.options.minigame_hunt_length.value)

    def victory_boss_hunt(self, state: CollectionState) -> bool:
        return state.has(itemName.MUMBOTOKEN, self.player, self.world.options.boss_hunt_length.value)

    def victory_jinjo_rescue(self, state: CollectionState) -> bool:
        return state.has(itemName.MUMBOTOKEN, self.player, self.world.options.jinjo_family_rescue_length.value)

    def victory_wonderwing(self, state: CollectionState) -> bool:
        return state.has(itemName.MUMBOTOKEN, self.player, 32) and self.check_hag1_options(state)

    def victory_token_hunt(self, state: CollectionState) -> bool:
        return state.has(itemName.MUMBOTOKEN, self.player, self.world.options.token_hunt_length.value)

    def victory_hag1(self, state: CollectionState) -> bool:
        return state.has("Kick Around", self.player)

    def set_rules(self) -> None:
        for location, rules in self.jiggy_rules.items():
            jiggy = self.world.multiworld.get_location(location, self.player)
            set_rule(jiggy, rules)

        for location, rules in self.honey_rules.items():
            honeycomb = self.world.multiworld.get_location(location, self.player)
            set_rule(honeycomb, rules)

        for location, rules in self.cheato_rules.items():
            cheato = self.world.multiworld.get_location(location, self.player)
            set_rule(cheato, rules)

        for location, rules in self.glowbo_rules.items():
            glowbo = self.world.multiworld.get_location(location, self.player)
            set_rule(glowbo, rules)

        for location, rules in self.silo_rules.items():
            silo = self.world.multiworld.get_location(location, self.player)
            set_rule(silo, rules)

        for location, rules in self.doubloon_rules.items():
            doubloon = self.world.multiworld.get_location(location, self.player)
            set_rule(doubloon, rules)

        for location, rules in self.treble_clef_rules.items():
            treble = self.world.multiworld.get_location(location, self.player)
            set_rule(treble, rules)

        for location, rules in self.train_rules.items():
            train = self.world.multiworld.get_location(location, self.player)
            set_rule(train, rules)

        for location, rules in self.jiggy_chunks_rules.items():
            jiggy_chunks = self.world.multiworld.get_location(location, self.player)
            set_rule(jiggy_chunks, rules)

        for location, rules in self.jinjo_rules.items():
            jinjo = self.world.multiworld.get_location(location, self.player)
            set_rule(jinjo, rules)

        for location, rules in self.notes_rules.items():
            notes = self.world.multiworld.get_location(location, self.player)
            set_rule(notes, rules)

        for location, rules in self.stopnswap_rules.items():
            stop = self.world.multiworld.get_location(location, self.player)
            set_rule(stop, rules)

        if self.world.options.nestsanity.value:
            for location, rules in self.nest_rules.items():
                nest = self.world.multiworld.get_location(location, self.player)
                set_rule(nest, rules)

        if self.world.options.randomize_signposts.value:
            for location, rules in self.signpost_rules.items():
                sign = self.world.multiworld.get_location(location, self.player)
                set_rule(sign, rules)

        if self.world.options.skip_puzzles.value:
            for location, rules in self.access_rules.items():
                access = self.world.multiworld.get_location(location, self.player)
                set_rule(access, rules)

        set_rule(self.world.multiworld.get_location(locationName.ROARDINO, self.player), self.bargasaurus_roar)


        if self.world.options.cheato_rewards.value:
            for location, rules in self.cheato_rewards_rules.items():
                cheato = self.world.multiworld.get_location(location, self.player)
                set_rule(cheato, rules)

        if self.world.options.honeyb_rewards.value:
            for location, rules in self.honeyb_rewards_rules.items():
                honeyb = self.world.multiworld.get_location(location, self.player)
                set_rule(honeyb, rules)

        if self.world.options.randomize_tickets.value:
            for location, rules in self.big_top_tickets_rules.items():
                tickets = self.world.multiworld.get_location(location, self.player)
                set_rule(tickets, rules)

        if self.world.options.randomize_beans.value:
            for location, rules in self.beans_rules.items():
                beans = self.world.multiworld.get_location(location, self.player)
                set_rule(beans, rules)

        for location, rules in self.scrit_scrat_scrut_rules.items():
            dinos = self.world.multiworld.get_location(location, self.player)
            set_rule(dinos, rules)

        for location, rules in self.boggy_kids_rules.items():
            kids = self.world.multiworld.get_location(location, self.player)
            set_rule(kids, rules)

        for location, rules in self.alien_kids_rules.items():
            kids = self.world.multiworld.get_location(location, self.player)
            set_rule(kids, rules)

        for location, rules in self.skivvy_rules.items():
            skivvy = self.world.multiworld.get_location(location, self.player)
            set_rule(skivvy, rules)

        for location, rules in self.mr_fit_rules.items():
            fit = self.world.multiworld.get_location(location, self.player)
            set_rule(fit, rules)

        if self.world.options.randomize_warp_pads.value:
            for location, rules in self.warp_pad_rules.items():
                warp_pads = self.world.multiworld.get_location(location, self.player)
                set_rule(warp_pads, rules)

        if self.world.options.victory_condition.value == VictoryCondition.option_minigame_hunt:
            for location, rules in self.gametoken_rules.items():
                tokens = self.world.multiworld.get_location(location, self.player)
                set_rule(tokens, rules)
            self.world.multiworld.completion_condition[self.player] = self.victory_minigame_hunt
        elif self.world.options.victory_condition.value == VictoryCondition.option_boss_hunt:
            for location, rules in self.bosstoken_rules.items():
                tokens = self.world.multiworld.get_location(location, self.player)
                set_rule(tokens, rules)
            self.world.multiworld.completion_condition[self.player] = self.victory_boss_hunt
        elif self.world.options.victory_condition.value == VictoryCondition.option_jinjo_family_rescue:
            for location, rules in self.jinjotoken_rules.items():
                tokens = self.world.multiworld.get_location(location, self.player)
                set_rule(tokens, rules)
            self.world.multiworld.completion_condition[self.player] = self.victory_jinjo_rescue
        elif self.world.options.victory_condition.value == VictoryCondition.option_wonderwing_challenge:
            for location, rules in self.bosstoken_rules.items():
                tokens = self.world.multiworld.get_location(location, self.player)
                set_rule(tokens, rules)
            for location, rules in self.gametoken_rules.items():
                tokens = self.world.multiworld.get_location(location, self.player)
                set_rule(tokens, rules)
            for location, rules in self.jinjotoken_rules.items():
                tokens = self.world.multiworld.get_location(location, self.player)
                set_rule(tokens, rules)
            self.world.multiworld.completion_condition[self.player] = self.victory_wonderwing
        elif self.world.options.victory_condition.value == VictoryCondition.option_token_hunt:
            self.world.multiworld.completion_condition[self.player] = self.victory_token_hunt
        elif self.world.options.victory_condition.value == VictoryCondition.option_boss_hunt_and_hag1:
            for location, rules in self.bosstoken_rules.items():
                tokens = self.world.multiworld.get_location(location, self.player)
                set_rule(tokens, rules)
            self.world.multiworld.completion_condition[self.player] = self.victory_hag1
        else:
            self.world.multiworld.completion_condition[self.player] = self.victory_hag1
