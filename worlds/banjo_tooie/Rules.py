from BaseClasses import CollectionState
from typing import TYPE_CHECKING

from .Options import EggsBehaviour, LogicType, RandomizeBKMoveList, VictoryCondition
from .Names import regionName, itemName, locationName
from worlds.generic.Rules import add_rule, set_rule, forbid_item, add_item_rule

# I don't know what is going on here, but it works.
if TYPE_CHECKING:
    from . import BanjoTooieWorld

# Shamelessly Stolen from KH2 :D

class BanjoTooieRules:
    player: int
    world: "BanjoTooieWorld"
    region_rules = {}
    #can_transform = {}
    mumbo_magic = []
    humba_magic = []
    solo_moves = []
    jinjo_forbid = []
    moves_forbid = []
    magic_forbid = []
    # banjo_moves = []
    # kazooie_moves = []
    jiggy_rules = {}

    def __init__(self, world: "BanjoTooieWorld") -> None:
        self.player = world.player
        self.world = world

        self.mumbo_magic = [
            itemName.MUMBOMT,
            itemName.MUMBOGM,
            itemName.MUMBOWW,
            itemName.MUMBOIH,
            itemName.MUMBOJR,
            itemName.MUMBOTD,
            itemName.MUMBOGI,
            itemName.MUMBOHP,
            itemName.MUMBOCC
        ]

        self.humba_magic = [
            itemName.HUMBAMT,
            itemName.HUMBAGM,
            itemName.HUMBAWW,
            itemName.HUMBAIH,
            itemName.HUMBAJR,
            itemName.HUMBATD,
            itemName.HUMBAGI,
            itemName.HUMBAHP,
            itemName.HUMBACC
        ]

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

        self.moves_forbid = [
            itemName.GGRAB,
            itemName.BBLASTER,
            itemName.EGGAIM,
            itemName.FEGGS,
            itemName.BDRILL,
            itemName.BBAYONET,
            itemName.GEGGS,
            itemName.AIREAIM,
            itemName.SPLITUP,
            itemName.PACKWH,
            itemName.IEGGS,
            itemName.WWHACK,
            itemName.TTORP,
            itemName.AUQAIM,
            itemName.CEGGS,
            itemName.SPRINGB,
            itemName.TAXPACK,
            itemName.HATCH,
            itemName.SNPACK,
            itemName.LSPRING,
            itemName.CLAWBTS,
            itemName.SHPACK,
            itemName.GLIDE,
            itemName.SAPACK,
        ]

        self.magic_forbid = {
            itemName.MUMBOMT,
            itemName.MUMBOGM,
            itemName.MUMBOWW,
            itemName.MUMBOJR,
            itemName.MUMBOTD,
            itemName.MUMBOGI,
            itemName.MUMBOHP,
            itemName.MUMBOCC,
            itemName.MUMBOIH,

            itemName.HUMBAMT,
            itemName.HUMBAGM,
            itemName.HUMBAWW,
            itemName.HUMBAJR,
            itemName.HUMBATD,
            itemName.HUMBAGI,
            itemName.HUMBAHP,
            itemName.HUMBACC,
            itemName.HUMBAIH,
        }

        self.jinjo_forbid = [
            itemName.WJINJO,
            itemName.OJINJO,
            itemName.YJINJO,
            itemName.BRJINJO,
            itemName.GJINJO,
            itemName.RJINJO,
            itemName.BLJINJO,
            itemName.PJINJO,
            itemName.BKJINJO,
        ]


        if self.world.options.skip_puzzles:
            self.access_rules = {
                locationName.W1: lambda state: self.WorldUnlocks_req(state, 1230944),
                locationName.W2: lambda state: self.WorldUnlocks_req(state, 1230945),
                locationName.W3: lambda state: self.WorldUnlocks_req(state, 1230946),
                locationName.W4: lambda state: self.WorldUnlocks_req(state, 1230947),
                locationName.W5: lambda state: self.WorldUnlocks_req(state, 1230948),
                locationName.W6: lambda state: self.WorldUnlocks_req(state, 1230949),
                locationName.W7: lambda state: self.WorldUnlocks_req(state, 1230950),
                locationName.W8: lambda state: self.WorldUnlocks_req(state, 1230951),
                locationName.W9: lambda state: self.WorldUnlocks_req(state, 1230952)
            }

        if self.world.options.victory_condition == VictoryCondition.option_minigame_hunt\
            or self.world.options.victory_condition == VictoryCondition.option_wonderwing_challenge:

            self.gametoken_rules = {
                locationName.MUMBOTKNGAME1: lambda state: self.jiggy_mayahem_kickball(state),
                locationName.MUMBOTKNGAME2: lambda state: self.jiggy_ordnance_storage(state),
                locationName.MUMBOTKNGAME3: lambda state: self.jiggy_hoop_hurry(state),
                locationName.MUMBOTKNGAME4: lambda state: self.jiggy_dodgem(state),
                locationName.MUMBOTKNGAME5: lambda state: self.jiggy_peril(state),
                locationName.MUMBOTKNGAME6: lambda state: self.jiggy_balloon_burst(state),
                locationName.MUMBOTKNGAME7: lambda state: self.jiggy_sub_challenge(state),
                locationName.MUMBOTKNGAME8: lambda state: self.jiggy_chompa(state),
                locationName.MUMBOTKNGAME9: lambda state: self.jiggy_clinkers(state),
                locationName.MUMBOTKNGAME10: lambda state: self.jiggy_twinkly(state),
                locationName.MUMBOTKNGAME11: lambda state: self.jiggy_hfp_kickball(state),
                locationName.MUMBOTKNGAME12: lambda state: self.jiggy_pot_of_gold(state),
                locationName.MUMBOTKNGAME13: lambda state: self.check_humba_magic(state, itemName.HUMBACC),
                locationName.MUMBOTKNGAME14: lambda state: self.jiggy_trash_can(state),
                locationName.MUMBOTKNGAME15: lambda state: self.canary_mary_free(state) and state.can_reach_region(regionName.GM, self.player),

            }

        if self.world.options.victory_condition == VictoryCondition.option_boss_hunt\
            or self.world.options.victory_condition == VictoryCondition.option_wonderwing_challenge\
            or self.world.options.victory_condition == VictoryCondition.option_boss_hunt_and_hag1:
            self.bosstoken_rules = {
                locationName.MUMBOTKNBOSS1: lambda state: self.jiggy_targitzan(state),
                locationName.MUMBOTKNBOSS2: lambda state: self.can_beat_king_coal(state),
                locationName.MUMBOTKNBOSS3: lambda state: self.jiggy_patches(state),
                locationName.MUMBOTKNBOSS4: lambda state: self.jiggy_lord_woo(state),
                locationName.MUMBOTKNBOSS5: lambda state: self.can_beat_terry(state),
                locationName.MUMBOTKNBOSS6: lambda state: self.can_beat_weldar(state),
                locationName.MUMBOTKNBOSS7: lambda state: self.jiggy_dragons_bros(state),
                locationName.MUMBOTKNBOSS8: lambda state: self.jiggy_mingy(state),
            }

        if self.world.options.victory_condition == VictoryCondition.option_jinjo_family_rescue\
            or self.world.options.victory_condition == VictoryCondition.option_wonderwing_challenge:
            self.jinjotoken_rules = {
                locationName.MUMBOTKNJINJO1: lambda state: state.has(itemName.WJINJO, self.player, 1),
                locationName.MUMBOTKNJINJO2: lambda state: state.has(itemName.OJINJO, self.player, 2),
                locationName.MUMBOTKNJINJO3: lambda state: state.has(itemName.YJINJO, self.player, 3),
                locationName.MUMBOTKNJINJO4: lambda state: state.has(itemName.BRJINJO, self.player, 4),
                locationName.MUMBOTKNJINJO5: lambda state: state.has(itemName.GJINJO, self.player, 5),
                locationName.MUMBOTKNJINJO6: lambda state: state.has(itemName.RJINJO, self.player, 6),
                locationName.MUMBOTKNJINJO7: lambda state: state.has(itemName.BLJINJO, self.player, 7),
                locationName.MUMBOTKNJINJO8: lambda state: state.has(itemName.PJINJO, self.player, 8),
                locationName.MUMBOTKNJINJO9: lambda state: state.has(itemName.BKJINJO, self.player, 9),
            }

        if self.world.options.cheato_rewards:
            self.cheato_rewards_rules = {
                locationName.CHEATOR1: lambda state: self.reach_cheato(state, 5),
                locationName.CHEATOR2: lambda state: self.reach_cheato(state, 10),
                locationName.CHEATOR3: lambda state: self.reach_cheato(state, 15),
                locationName.CHEATOR4: lambda state: self.reach_cheato(state, 20),
                locationName.CHEATOR5: lambda state: self.reach_cheato(state, 25),
            }

        if self.world.options.honeyb_rewards:
            self.honeyb_rewards_rules = {
                locationName.HONEYBR1: lambda state: state.has(itemName.HONEY, self.player, 1) and self.can_reach_honey_b(state),
                locationName.HONEYBR2: lambda state: state.has(itemName.HONEY, self.player, 4) and self.can_reach_honey_b(state),
                locationName.HONEYBR3: lambda state: state.has(itemName.HONEY, self.player, 9) and self.can_reach_honey_b(state),
                locationName.HONEYBR4: lambda state: state.has(itemName.HONEY, self.player, 16) and self.can_reach_honey_b(state),
                locationName.HONEYBR5: lambda state: state.has(itemName.HONEY, self.player, 25) and self.can_reach_honey_b(state),
            }



        self.train_rules = {
            locationName.CHUFFY: lambda state: self.can_beat_king_coal(state),
            locationName.TRAINSWIH: lambda state: self.grip_grab(state) and self.flap_flip(state),
            locationName.TRAINSWHP2: lambda state: self.humbaHFP(state),
            locationName.TRAINSWHP1: lambda state: self.tswitch_lavaside(state),
            locationName.TRAINSWWW: lambda state: self.tswitch_ww(state),
            locationName.TRAINSWTD: lambda state: self.tswitch_tdl(state),
            #locationName.TRAINSWGI: lambda state: self.tswitch_gi(state),
        }

        self.jiggy_chunks_rules = {
            locationName.CHUNK1: lambda state: self.jiggy_crushing_shed(state),
            locationName.CHUNK2: lambda state: self.jiggy_crushing_shed(state),
            locationName.CHUNK3: lambda state: self.jiggy_crushing_shed(state),
        }

        self.scrit_scrat_scrut_rules = {
            locationName.SCRUT: lambda state: self.scrut(state),
            locationName.SCRAT: lambda state: self.scrat(state),
            locationName.SCRIT: lambda state: self.scrit(state)
        }

        self.jiggy_rules = {
            #Mayahem Temple Jiggies
            locationName.JIGGYMT1:  lambda state: self.jiggy_targitzan(state),
            locationName.JIGGYMT2:  lambda state: self.jiggy_sschamber(state),
            locationName.JIGGYMT3:  lambda state: self.jiggy_mayahem_kickball(state),
            locationName.JIGGYMT4:  lambda state: self.jiggy_bovina(state),
            locationName.JIGGYMT5:  lambda state: self.jiggy_treasure_chamber(state),
            locationName.JIGGYMT6:  lambda state: self.jiggy_golden_goliath(state),
            locationName.JIGGYMT7:  lambda state: self.jiggy_prison_quicksand(state),
            locationName.JIGGYMT8:  lambda state: self.jiggy_pillars(state),
            locationName.JIGGYMT9:  lambda state: self.jiggy_top(state),
            locationName.JIGGYMT10: lambda state: self.jiggy_ssslumber(state),

            #Glitter Gulch Mine Jiggies
            locationName.JIGGYGM1: lambda state: self.can_beat_king_coal(state),
            locationName.JIGGYGM2: lambda state: self.canary_mary_free(state),
            locationName.JIGGYGM3: lambda state: self.jiggy_generator_cavern(state),
            locationName.JIGGYGM4: lambda state: self.jiggy_waterfall_cavern(state),
            locationName.JIGGYGM5: lambda state: self.jiggy_ordnance_storage(state),
            locationName.JIGGYGM6: lambda state: self.dilberta_free(state),
            locationName.JIGGYGM7: lambda state: self.jiggy_crushing_shed(state),
            locationName.JIGGYGM8: lambda state: self.jiggy_waterfall(state),
            locationName.JIGGYGM9: lambda state: self.jiggy_power_hut(state),
            locationName.JIGGYGM10: lambda state: self.jiggy_flooded_caves(state),

            #Witchyworld Jiggies
            locationName.JIGGYWW1:  lambda state: self.jiggy_hoop_hurry(state),
            locationName.JIGGYWW2:  lambda state: self.jiggy_dodgem(state),
            locationName.JIGGYWW3:  lambda state: self.jiggy_patches(state),
            locationName.JIGGYWW4:  lambda state: self.jiggy_peril(state),
            locationName.JIGGYWW5:  lambda state: self.jiggy_balloon_burst(state),
            locationName.JIGGYWW6:  lambda state: self.jiggy_dive_of_death(state),
            locationName.JIGGYWW7:  lambda state: self.jiggy_mrs_boggy(state),
            locationName.JIGGYWW8:  lambda state: self.jiggy_star_spinner(state),
            locationName.JIGGYWW9:  lambda state: self.jiggy_inferno(state),
            locationName.JIGGYWW10: lambda state: self.jiggy_cactus(state),

            #Jolly Joger's Lagoon Jiggies
            locationName.JIGGYJR1:  lambda state: self.jiggy_sub_challenge(state),
            locationName.JIGGYJR2:  lambda state: self.jiggy_tiptup(state),
            locationName.JIGGYJR3:  lambda state: self.jiggy_bacon(state),
            locationName.JIGGYJR4:  lambda state: self.jiggy_pig_pool(state),
            locationName.JIGGYJR5:  lambda state: self.jiggy_smuggler(state),
            locationName.JIGGYJR6:  lambda state: self.jiggy_merry_maggie(state),
            locationName.JIGGYJR7:  lambda state: self.jiggy_lord_woo(state),
            locationName.JIGGYJR8:  lambda state: self.jiggy_see_mee(state),
            locationName.JIGGYJR9:  lambda state: self.jiggy_pawno(state),
            locationName.JIGGYJR10: lambda state: self.jiggy_ufo(state),

            #Terrydactyland Jiggies
            locationName.JIGGYTD1:  lambda state: self.jiggy_terry_nest(state),
            locationName.JIGGYTD2:  lambda state: self.jiggy_dippy(state),
            locationName.JIGGYTD3:  lambda state: self.jiggy_scrotty(state),
            locationName.JIGGYTD4:  lambda state: self.can_beat_terry(state),
            locationName.JIGGYTD5:  lambda state: self.jiggy_oogle_boogle(state),
            locationName.JIGGYTD6:  lambda state: self.jiggy_chompa(state),
            locationName.JIGGYTD7:  lambda state: self.jiggy_terry_kids(state),
            locationName.JIGGYTD8:  lambda state: self.jiggy_stomping_plains(state),
            locationName.JIGGYTD9:  lambda state: self.jiggy_rocknuts(state),
            locationName.JIGGYTD10: lambda state: self.jiggy_roar_cage(state),

            #Grunty Industries Jiggies
            locationName.JIGGYGI1: lambda state: self.jiggy_underwater_waste_disposal(state),
            locationName.JIGGYGI2: lambda state: self.can_beat_weldar(state),
            locationName.JIGGYGI3: lambda state: self.jiggy_clinkers(state),
            locationName.JIGGYGI4: lambda state: self.jiggy_skivvy(state),
            locationName.JIGGYGI5: lambda state: self.jiggy_floor5(state),
            locationName.JIGGYGI6: lambda state: self.jiggy_quality_control(state),
            locationName.JIGGYGI7: lambda state: self.jiggy_guarded(state),
            locationName.JIGGYGI8: lambda state: self.jiggy_trash_compactor(state),
            locationName.JIGGYGI9: lambda state: self.jiggy_twinkly(state),
            locationName.JIGGYGI10: lambda state: self.jiggy_waste_disposal_box(state),

            #Hailfire Peaks Jiggies
            locationName.JIGGYHP1:  lambda state: self.jiggy_dragons_bros(state),
            locationName.JIGGYHP2:  lambda state: self.jiggy_volcano(state),
            locationName.JIGGYHP3:  lambda state: self.jiggy_sabreman(state),
            locationName.JIGGYHP4:  lambda state: self.jiggy_boggy(state),
            locationName.JIGGYHP5:  lambda state: self.jiggy_ice_station(state),
            locationName.JIGGYHP6:  lambda state: self.jiggy_oil_drill(state),
            locationName.JIGGYHP7:  lambda state: self.jiggy_hfp_stomping(state),
            locationName.JIGGYHP8:  lambda state: self.jiggy_hfp_kickball(state),
            locationName.JIGGYHP9:  lambda state: self.jiggy_aliens(state),
            locationName.JIGGYHP10: lambda state: self.jiggy_colosseum_split(state),

            #Cloud Cuckooland Jiggies
            locationName.JIGGYCC1: lambda state: self.jiggy_mingy(state),
            locationName.JIGGYCC2: lambda state: self.jiggy_mr_fit(state),
            locationName.JIGGYCC3: lambda state: self.jiggy_pot_of_gold(state),
            locationName.JIGGYCC4: lambda state: self.canary_mary_free(state) and state.can_reach_region(regionName.GM, self.player),
            locationName.JIGGYCC5: lambda state: self.check_humba_magic(state, itemName.HUMBACC),
            locationName.JIGGYCC6: lambda state: self.check_humba_magic(state, itemName.HUMBACC),
            locationName.JIGGYCC7: lambda state: self.jiggy_cheese(state),
            locationName.JIGGYCC8: lambda state: self.jiggy_trash_can(state),
            locationName.JIGGYCC9: lambda state: self.jiggy_superstash(state),
            locationName.JIGGYCC10: lambda state: self.shack_pack(state) and self.climb(state),

            #Jinjo Family Jiggies
            locationName.JIGGYIH1: lambda state: state.has(itemName.WJINJO, self.player, 1),
            locationName.JIGGYIH2: lambda state: state.has(itemName.OJINJO, self.player, 2),
            locationName.JIGGYIH3: lambda state: state.has(itemName.YJINJO, self.player, 3),
            locationName.JIGGYIH4: lambda state: state.has(itemName.BRJINJO, self.player, 4),
            locationName.JIGGYIH5: lambda state: state.has(itemName.GJINJO, self.player, 5),
            locationName.JIGGYIH6: lambda state: state.has(itemName.RJINJO, self.player, 6),
            locationName.JIGGYIH7: lambda state: state.has(itemName.BLJINJO, self.player, 7),
            locationName.JIGGYIH8: lambda state: state.has(itemName.PJINJO, self.player, 8),
            locationName.JIGGYIH9: lambda state: state.has(itemName.BKJINJO, self.player, 9),

        }
        self.cheato_rules = {
            locationName.CHEATOMT1: lambda state: self.cheato_snakehead(state),
            locationName.CHEATOMT2: lambda state: self.cheato_prison(state),
            locationName.CHEATOMT3: lambda state: self.cheato_jade_snake_grove(state),

            locationName.CHEATOGM1: lambda state: self.canary_mary_free(state),
            locationName.CHEATOGM2: lambda state: self.cheato_gm_entrance(state),
            locationName.CHEATOGM3: lambda state: self.cheato_water_storage(state),

            locationName.CHEATOWW1: lambda state: self.cheato_haunted_cavern(state),
            locationName.CHEATOWW2: lambda state: self.cheato_inferno(state),
            locationName.CHEATOWW3: lambda state: self.cheato_saucer_of_peril(state),

            locationName.CHEATOJR1: lambda state: self.cheato_pawno(state),
            locationName.CHEATOJR2: lambda state: self.cheato_seemee(state),
            locationName.CHEATOJR3: lambda state: self.cheato_ancient_swimming_baths(state),

            locationName.CHEATOTL1: lambda state: self.cheato_dippy_pool(state),
            locationName.CHEATOTL2: lambda state: self.cheato_trex(state),
            locationName.CHEATOTL3: lambda state: self.cheato_tdlboulder(state),

            locationName.CHEATOGI1: lambda state: self.cheato_loggo(state),
            locationName.CHEATOGI2: lambda state: self.cheato_window(state),
            locationName.CHEATOGI3: lambda state: self.can_beat_weldar(state),

            locationName.CHEATOHP1: lambda state: self.cheato_colosseum(state),
            locationName.CHEATOHP2: lambda state: self.cheato_icicle_grotto(state),
            locationName.CHEATOHP3: lambda state: self.cheato_icy_pillar(state),

            locationName.CHEATOCC1: lambda state: self.canary_mary_free(state) and state.can_reach_region(regionName.GM, self.player),
            locationName.CHEATOCC2: lambda state: self.cheato_potgold(state),
            locationName.CHEATOCC3: lambda state: self.check_humba_magic(state, itemName.HUMBACC),

            locationName.CHEATOSM1: lambda state: self.cheato_spiral(state)
        }
        self.honey_rules = {
            locationName.HONEYCMT1: lambda state: self.honeycomb_mt_entrance(state),
            locationName.HONEYCMT2: lambda state: self.honeycomb_bovina(state),
            locationName.HONEYCMT3: lambda state: self.honeycomb_treasure_chamber(state),

            locationName.HONEYCGM1: lambda state: self.GM_boulders(state),
            locationName.HONEYCGM2: lambda state: self.honeycomb_prospector(state),
            locationName.HONEYCGM3: lambda state: self.honeycomb_gm_station(state),

            locationName.HONEYCWW1: lambda state: self.honeycomb_space_zone(state),
            locationName.HONEYCWW2: lambda state: self.honeycomb_inferno(state),
            locationName.HONEYCWW3: lambda state: self.honeycomb_crazy_castle(state),

            locationName.HONEYCJR1: lambda state: self.honeycomb_seemee(state),
            locationName.HONEYCJR2: lambda state: self.honeycomb_atlantis(state),
            locationName.HONEYCJR3: lambda state: self.honeycomb_jrl_pipes(state),

            locationName.HONEYCTL1: lambda state: self.honeycomb_lakeside(state),
            locationName.HONEYCTL2: lambda state: self.honeycomb_styracosaurus(state),
            locationName.HONEYCTL3: lambda state: self.honeycomb_river(state),

            locationName.HONEYCGI1: lambda state: self.honeycomb_floor3(state),
            locationName.HONEYCGI2: lambda state: self.honeycomb_gi_station(state),

            locationName.HONEYCHP1: lambda state: self.honeycomb_volcano(state),
            locationName.HONEYCHP2: lambda state: self.honeycomb_hfp_station(state),
            locationName.HONEYCHP3: lambda state: self.honeycomb_lava_side(state),

            locationName.HONEYCCC1: lambda state: self.bill_drill(state),
            locationName.HONEYCCC2: lambda state: self.honeycomb_trash(state),
            locationName.HONEYCCC3: lambda state: self.honeycomb_pot(state),

            locationName.HONEYCIH1: lambda state: self.plateau_top(state)

        }
        self.glowbo_rules = {
            locationName.GLOWBOGM1: lambda state: self.glowbo_entrance_ggm(state),

            locationName.GLOWBOWW1: lambda state: self.glowbo_inferno(state),
            locationName.GLOWBOWW2: lambda state: self.glowbo_wigwam(state),

            locationName.GLOWBOJR1: lambda state: self.pawno_shelves(state),
            locationName.GLOWBOJR2: lambda state: self.glowbo_underwigwam(state),

            locationName.GLOWBOTL1: lambda state: self.glowbo_tdl(state),
            locationName.GLOWBOTL2: lambda state: self.glowbo_tdl_mumbo(state),

            locationName.GLOWBOGI2: lambda state: self.glowbo_floor_3(state),

            locationName.GLOWBOHP2: lambda state: self.hfp_top(state),

            locationName.GLOWBOCC1: lambda state: self.ccl_glowbo_pool(state),
            locationName.GLOWBOCC2: lambda state: self.glowbo_cavern(state),

            locationName.GLOWBOIH1: lambda state: self.glowbo_cliff(state),
            locationName.GLOWBOMEG: lambda state: self.mega_glowbo(state)

        }
        self.doubloon_rules = {
            #Alcove
            locationName.JRLDB22:   lambda state: self.doubloon_ledge(state),
            locationName.JRLDB23:   lambda state: self.doubloon_ledge(state),
            locationName.JRLDB24:   lambda state: self.doubloon_ledge(state),
            #Underground
            locationName.JRLDB19:   lambda state: self.doubloon_dirtpatch(state),
            locationName.JRLDB20:   lambda state: self.doubloon_dirtpatch(state),
            locationName.JRLDB21:   lambda state: self.doubloon_dirtpatch(state),
            #Underwater
            locationName.JRLDB11:   lambda state: self.doubloon_water(state),
            locationName.JRLDB12:   lambda state: self.doubloon_water(state),
            locationName.JRLDB13:   lambda state: self.doubloon_water(state),
            locationName.JRLDB14:   lambda state: self.doubloon_water(state),
            locationName.JRLDB27:   lambda state: self.doubloon_water(state),
            locationName.JRLDB28:   lambda state: self.doubloon_water(state),
            locationName.JRLDB29:   lambda state: self.doubloon_water(state),
            locationName.JRLDB30:   lambda state: self.doubloon_water(state),

        }
        self.treble_clef_rules = {
            locationName.TREBLEJV:  lambda state: self.treble_jv(state),
            locationName.TREBLEGM:  lambda state: self.treble_gm(state),
            locationName.TREBLEWW:  lambda state: self.treble_ww(state),
            locationName.TREBLEJR:  lambda state: self.treble_jrl(state),
            locationName.TREBLETL:  lambda state: self.treble_tdl(state),
            locationName.TREBLEGI:  lambda state: self.treble_gi(state),
            locationName.TREBLEHP:  lambda state: self.treble_hfp(state),
            locationName.TREBLECC:  lambda state: self.treble_ccl(state),
        }

        self.silo_rules = {
            ## Faster swimming and double air rules are here ##
            locationName.ROYSTEN1: lambda state: self.bill_drill(state),
            locationName.ROYSTEN2: lambda state: self.bill_drill(state),

            locationName.EGGAIM: lambda state: self.check_notes(state, locationName.EGGAIM),
            locationName.BBLASTER: lambda state: self.check_notes(state, locationName.BBLASTER),
            locationName.GGRAB: lambda state: self.check_notes(state, locationName.GGRAB),

            locationName.BDRILL: lambda state: self.silo_bill_drill(state),
            locationName.BBAYONET: lambda state: self.GM_boulders(state) and self.check_notes(state, locationName.BBAYONET),

            locationName.AIREAIM: lambda state: self.check_notes(state, locationName.AIREAIM),
            locationName.SPLITUP: lambda state: self.check_notes(state, locationName.SPLITUP),
            locationName.PACKWH: lambda state: self.split_up(state) and self.check_notes(state, locationName.PACKWH),

            locationName.AUQAIM: lambda state: (self.has_explosives(state) or state.has(itemName.DOUBLOON, self.player, 28)) and
                                               self.check_notes(state, locationName.AUQAIM),
            locationName.TTORP: lambda state:  self.can_access_talon_torpedo_silo(state) and
                                               self.check_notes(state, locationName.TTORP),
            locationName.WWHACK: lambda state: (self.has_explosives(state)) and self.split_up(state) and
                                               self.check_notes(state, locationName.WWHACK),

            locationName.SPRINGB: lambda state: self.check_notes(state, locationName.SPRINGB) and self.silo_spring(state),
            locationName.TAXPACK: lambda state: self.can_access_taxi_pack_silo(state) and self.check_notes(state, locationName.TAXPACK),
            locationName.HATCH: lambda state:   self.split_up(state) and self.check_notes(state, locationName.HATCH),

            locationName.SNPACK: lambda state:  self.silo_snooze(state),
            locationName.LSPRING: lambda state: self.check_notes(state, locationName.LSPRING) and self.split_up(state),
            locationName.CLAWBTS: lambda state: self.check_notes(state, locationName.CLAWBTS),

            locationName.SHPACK: lambda state: self.split_up(state) and self.check_notes(state, locationName.SHPACK),
            locationName.GLIDE: lambda state: self.can_access_glide_silo(state) and self.check_notes(state, locationName.GLIDE),

            locationName.SAPACK: lambda state: self.can_access_sack_pack_silo(state) and self.check_notes(state, locationName.SAPACK),

            locationName.FEGGS: lambda state: self.check_notes(state, locationName.FEGGS),
            locationName.GEGGS: lambda state: self.check_notes(state, locationName.GEGGS),
            locationName.IEGGS: lambda state: self.check_notes(state, locationName.IEGGS),
            locationName.CEGGS: lambda state: self.check_notes(state, locationName.CEGGS)
        }

        self.jinjo_rules = {
            locationName.JINJOIH5: lambda state: self.talon_torpedo(state) and self.dive(state),
            locationName.JINJOIH4: lambda state: self.jinjo_plateau(state),
            locationName.JINJOIH3: lambda state: self.jinjo_clifftop(state),
            locationName.JINJOIH2: lambda state: self.jinjo_wasteland(state),

            locationName.JINJOMT1: lambda state: self.jinjo_jadesnakegrove(state),
            locationName.JINJOMT2: lambda state: self.jinjo_stadium(state),
            locationName.JINJOMT3: lambda state: self.breegull_blaster(state),
            locationName.JINJOMT4: lambda state: self.jinjo_pool(state),

            #Water Storage Jinjo always true because it's in the GMWSJT area
            locationName.JINJOGM2: lambda state: self.jinjo_jail(state),
            locationName.JINJOGM4: lambda state: self.jinjo_boulder(state),

            locationName.JINJOWW1: lambda state: self.jinjo_tent(state),
            locationName.JINJOWW2: lambda state: self.jinjo_cave_of_horrors(state),
            locationName.JINJOWW3: lambda state: self.jinjo_van_door(state),
            locationName.JINJOWW4: lambda state: self.jinjo_dodgem(state),
            locationName.JINJOWW5: lambda state: self.jinjo_cactus(state),

            locationName.JINJOJR1: lambda state: self.jinjo_alcove(state),
            locationName.JINJOJR2: lambda state: self.jinjo_blubber(state),
            locationName.JINJOJR3: lambda state: self.jinjo_big_fish(state),
            locationName.JINJOJR4: lambda state: self.jinjo_seaweed_sanctum(state),
            locationName.JINJOJR5: lambda state: self.jinjo_sunken_ship(state),

            locationName.JINJOTL2: lambda state: self.jinjo_tdl_entrance(state),
            locationName.JINJOTL1: lambda state: self.talon_torpedo(state) and self.dive(state),
            locationName.JINJOTL3: lambda state: self.clockwork_eggs(state),
            locationName.JINJOTL4: lambda state: self.jinjo_big_t_rex(state),
            locationName.JINJOTL5: lambda state: self.jinjo_stomping_plains(state),

            locationName.JINJOGI2: lambda state: self.jinjo_legspring(state),
            locationName.JINJOGI3: lambda state: self.jinjo_waste_disposal(state),
            locationName.JINJOGI4: lambda state: self.jinjo_boiler(state),
            locationName.JINJOGI5: lambda state: self.jinjo_gi_outside(state),

            locationName.JINJOHP1: lambda state: self.jinjo_hot_waterfall(state),
            locationName.JINJOHP2: lambda state: self.jinjo_hot_pool(state),
            locationName.JINJOHP3: lambda state: self.jinjo_wind_tunnel(state),
            locationName.JINJOHP4: lambda state: self.jinjo_icicle_grotto(state),
            locationName.JINJOHP5: lambda state: self.jinjo_mildred(state),

            locationName.JINJOCC1: lambda state: self.jinjo_trash_can(state),
            locationName.JINJOCC2: lambda state: self.jinjo_cheese(state),
            locationName.JINJOCC3: lambda state: self.jinjo_central(state),
            locationName.JINJOCC5: lambda state: self.jinjo_humba_ccl(state),
        }

        self.notes_rules = {
            locationName.NOTEIH1:  lambda state: self.notes_plateau_sign(state),
            locationName.NOTEIH2:  lambda state: self.notes_plateau_sign(state),
            locationName.NOTEIH3:  lambda state: self.plateau_top(state),
            locationName.NOTEIH4:  lambda state: self.plateau_top(state),
            locationName.NOTEIH13:  lambda state: self.notes_bottom_clockwork(state),
            locationName.NOTEIH14:  lambda state: self.notes_top_clockwork(state),

            locationName.NOTEGGM1:  lambda state: self.notes_green_pile(state),
            locationName.NOTEGGM2:  lambda state: self.notes_green_pile(state),
            locationName.NOTEGGM3:  lambda state: self.notes_green_pile(state),
            locationName.NOTEGGM4:  lambda state: self.notes_green_pile(state),
            locationName.NOTEGGM5: lambda state: self.notes_prospector_easy(state),
            locationName.NOTEGGM6: lambda state: self.notes_prospector_easy(state),
            locationName.NOTEGGM7: lambda state: self.notes_prospector_hard(state),
            locationName.NOTEGGM8: lambda state: self.notes_prospector_easy(state),
            locationName.NOTEGGM9: lambda state: self.notes_prospector_easy(state),
            locationName.NOTEGGM10: lambda state: self.notes_gm_mumbo(state),
            locationName.NOTEGGM11: lambda state: self.notes_gm_mumbo(state),
            locationName.NOTEGGM12: lambda state: self.notes_gm_mumbo(state),
            locationName.NOTEGGM13: lambda state: self.notes_easy_fuel_depot(state),
            locationName.NOTEGGM14: lambda state: self.notes_hard_fuel_depot(state),
            locationName.NOTEGGM15: lambda state: self.notes_easy_fuel_depot(state),
            locationName.NOTEGGM16: lambda state: self.notes_easy_fuel_depot(state),


            locationName.NOTEWW9:   lambda state: self.notes_ww_area51_left(state),
            locationName.NOTEWW10:  lambda state: self.notes_ww_area51_right(state),
            locationName.NOTEWW13:  lambda state: self.notes_dive_of_death(state),
            locationName.NOTEWW14:  lambda state: self.notes_dive_of_death(state),

            locationName.NOTEJRL4:  lambda state: self.notes_jrl_blubs(state),
            locationName.NOTEJRL5:  lambda state: self.notes_jrl_blubs(state),
            locationName.NOTEJRL6:  lambda state: self.notes_jrl_eels(state),
            locationName.NOTEJRL7:  lambda state: self.notes_jrl_eels(state),
            locationName.NOTEJRL11:  lambda state: self.pawno_shelves(state),
            locationName.NOTEJRL12:  lambda state: self.pawno_shelves(state),
            locationName.NOTEJRL13:  lambda state: self.pawno_shelves(state),
            locationName.NOTEJRL14:  lambda state: self.notes_jolly(state),
            locationName.NOTEJRL15:  lambda state: self.notes_jolly(state),
            locationName.NOTEJRL16:  lambda state: self.notes_jolly(state),

            locationName.NOTETDL1:  lambda state: self.notes_tdl_station_right(state),
            locationName.NOTETDL10:  lambda state: self.notes_roar_cage(state),
            locationName.NOTETDL11:  lambda state: self.notes_roar_cage(state),
            locationName.NOTETDL12:  lambda state: self.notes_roar_cage(state),
            locationName.NOTETDL13:  lambda state: self.notes_river_passage(state),
            locationName.NOTETDL14:  lambda state: self.notes_river_passage(state),
            locationName.NOTETDL15:  lambda state: self.notes_river_passage(state),
            locationName.NOTETDL16:  lambda state: self.notes_river_passage(state),

            locationName.NOTEGI1:   lambda state: self.notes_gi_train_station_hard(state),
            locationName.NOTEGI2:   lambda state: self.notes_gi_train_station_easy(state),
            locationName.NOTEGI3:   lambda state: self.notes_gi_train_station_easy(state),
            locationName.NOTEGI4:   lambda state: self.notes_gi_floor1(state),
            locationName.NOTEGI5:   lambda state: self.notes_gi_floor1(state),
            locationName.NOTEGI6:   lambda state: self.notes_leg_spring(state),
            locationName.NOTEGI7:   lambda state: self.notes_leg_spring(state),
            locationName.NOTEGI8:   lambda state: self.notes_leg_spring(state),
            locationName.NOTEGI9:   lambda state: self.notes_short_stack(state),
            locationName.NOTEGI11:  lambda state: self.notes_waste_disposal(state),
            locationName.NOTEGI12:  lambda state: self.notes_waste_disposal(state),
            locationName.NOTEGI13:  lambda state: self.notes_aircon_hard(state),
            locationName.NOTEGI15:  lambda state: self.notes_floor_3(state),
            locationName.NOTEGI16:  lambda state: self.notes_floor_3(state),

            locationName.NOTEHFP1:  lambda state: self.hfp_top(state),
            locationName.NOTEHFP2:  lambda state: self.hfp_top(state),
            locationName.NOTEHFP5:  lambda state: self.hfp_top(state),
            locationName.NOTEHFP6:  lambda state: self.hfp_top(state),
            locationName.NOTEHFP7:  lambda state: self.notes_ladder(state),
            locationName.NOTEHFP8:  lambda state: self.notes_ladder(state),
            locationName.NOTEHFP9:  lambda state: self.notes_oil_drill(state),
            locationName.NOTEHFP10:  lambda state: self.notes_oil_drill(state),
            locationName.NOTEHFP11:  lambda state: self.notes_upper_icy_side(state),
            locationName.NOTEHFP12:  lambda state: self.notes_upper_icy_side(state),
            locationName.NOTEHFP13:  lambda state: self.notes_boggy(state),
            locationName.NOTEHFP14:  lambda state: self.notes_boggy(state),
            locationName.NOTEHFP15:  lambda state: self.notes_lower_icy_side(state),
            locationName.NOTEHFP16:  lambda state: self.notes_lower_icy_side(state),

            locationName.NOTECCL2: lambda state: self.notes_ccl_low(state),
            locationName.NOTECCL3: lambda state: self.notes_ccl_silo(state),
            locationName.NOTECCL4: lambda state: self.notes_ccl_silo(state),
            locationName.NOTECCL5: lambda state: self.notes_cheese(state),
            locationName.NOTECCL6: lambda state: self.notes_ccl_low(state),
            locationName.NOTECCL7: lambda state: self.notes_dippy(state),
            locationName.NOTECCL8: lambda state: self.notes_ccl_low(state),
            locationName.NOTECCL9: lambda state: self.notes_ccl_low(state),
            locationName.NOTECCL10: lambda state: self.notes_sack_race(state),
            locationName.NOTECCL11: lambda state: self.notes_ccl_high(state),
            locationName.NOTECCL12: lambda state: self.notes_ccl_high(state),
            locationName.NOTECCL13: lambda state: self.ccl_glowbo_pool(state),
            locationName.NOTECCL14: lambda state: self.notes_ccl_low(state),
            locationName.NOTECCL15: lambda state: self.notes_ccl_low(state),
            locationName.NOTECCL16: lambda state: self.notes_ccl_low(state),
        }

        self.stopnswap_rules = {
            locationName.IKEY:      lambda state: self.ice_key(state),
            locationName.PMEGG:     lambda state: self.pink_mystery_egg(state),
            locationName.PMEGGH:    lambda state: state.has(itemName.PMEGG, self.player),
            locationName.BMEGG:     lambda state: self.blue_mystery_egg(state),
            locationName.BMEGGH:    lambda state: state.has(itemName.BMEGG, self.player),
            locationName.YMEGGH:    lambda state: (self.has_explosives(state) or self.bill_drill(state)) and self.hatch(state)
        }

        self.nest_rules = {
            locationName.NESTSM4:    lambda state: self.nest_lair_top(state),
            locationName.NESTSM5:    lambda state: self.nest_lair_top(state),
            locationName.NESTSM6:    lambda state: self.nest_lair_top(state),

            locationName.NESTSM22:    lambda state: self.nest_sm_waterfall_top(state),
            locationName.NESTSM23:    lambda state: self.nest_sm_waterfall_platform(state),
            locationName.NESTSM24:    lambda state: self.nest_sm_waterfall_platform(state),


            locationName.NESTIH16:    lambda state: self.nest_bottles_house(state),
            locationName.NESTIH17:    lambda state: self.nest_bottles_house(state),

            locationName.NESTIH32:    lambda state: self.nest_pl_dirt_pile(state),
            locationName.NESTIH33:    lambda state: self.nest_pl_dirt_pile(state),

            locationName.NESTIH43:    lambda state: self.nest_cliff_top_hard(state),

            locationName.NESTIH56:    lambda state: self.nest_another_digger_tunnel(state),
            locationName.NESTIH57:    lambda state: self.nest_another_digger_tunnel(state),

            locationName.NESTIH58:    lambda state: self.nest_quagmire_medium(state),
            locationName.NESTIH59:    lambda state: self.nest_quagmire_easy(state),
            locationName.NESTIH60:    lambda state: self.nest_quagmire_hard(state),

            locationName.NESTMT11:    lambda state: self.nest_mt_stadium(state),
            locationName.NESTMT12:    lambda state: self.nest_mt_stadium(state),

            locationName.NESTMT15:    lambda state: self.nest_pillars(state),
            locationName.NESTMT16:    lambda state: self.nest_pillars(state),
            locationName.NESTMT17:    lambda state: self.nest_pillars(state),
            locationName.NESTMT18:    lambda state: self.nest_mt_cell_right(state),
            locationName.NESTMT21:    lambda state: self.nest_mt_cell_left(state),

            locationName.NESTMT25:    lambda state: self.breegull_blaster(state),
            locationName.NESTMT26:    lambda state: self.breegull_blaster(state),
            locationName.NESTMT27:    lambda state: self.breegull_blaster(state),
            locationName.NESTMT28:    lambda state: self.breegull_blaster(state),
            locationName.NESTMT29:    lambda state: self.breegull_blaster(state),
            locationName.NESTMT30:    lambda state: self.breegull_blaster(state),
            locationName.NESTMT31:    lambda state: self.breegull_blaster(state),
            locationName.NESTMT32:    lambda state: self.breegull_blaster(state),
            locationName.NESTMT33:    lambda state: self.breegull_blaster(state),
            locationName.NESTMT34:    lambda state: self.breegull_blaster(state),
            locationName.NESTMT35:    lambda state: self.breegull_blaster(state),



            locationName.NESTGM3:    lambda state: self.nest_bill_drill(state),
            locationName.NESTGM4:    lambda state: self.nest_bill_drill(state),

            locationName.NESTGM13:    lambda state: self.nest_flooded_caves(state),
            locationName.NESTGM14:    lambda state: self.nest_flooded_caves(state),

            locationName.NESTGM16:    lambda state: self.nest_outside_power_hut(state),
            locationName.NESTGM17:    lambda state: self.nest_outside_power_hut(state),
            locationName.NESTGM18:    lambda state: self.GM_boulders(state),
            locationName.NESTGM19:    lambda state: self.GM_boulders(state),

            locationName.NESTGM21:    lambda state: self.GM_boulders(state),

            locationName.NESTGM26:    lambda state: self.notes_prospector_hard(state),

            locationName.NESTGM27:    lambda state: self.nest_ggm_mumbo(state),
            locationName.NESTGM28:    lambda state: self.nest_ggm_mumbo(state),
            locationName.NESTGM29:    lambda state: self.nest_ggm_mumbo(state),

            locationName.NESTGM30:    lambda state: self.nest_toxic_gas_cave(state),
            locationName.NESTGM31:    lambda state: self.nest_toxic_gas_cave(state),

            locationName.NESTGM32:    lambda state: self.nest_canary_high(state),
            locationName.NESTGM33:    lambda state: self.nest_canary_low(state),
            locationName.NESTGM34:    lambda state: self.nest_canary_low(state),
            locationName.NESTGM35:    lambda state: self.nest_canary_low(state),

            locationName.NESTGM36:    lambda state: self.GM_boulders(state),
            locationName.NESTGM37:    lambda state: self.GM_boulders(state),
            locationName.NESTGM38:    lambda state: self.GM_boulders(state),


            locationName.NESTWW15:    lambda state: self.nest_pump_room(state),
            locationName.NESTWW16:    lambda state: self.nest_pump_room(state),

            locationName.NESTWW27:    lambda state: self.nest_big_top(state),
            locationName.NESTWW28:    lambda state: self.nest_big_top(state),
            locationName.NESTWW29:    lambda state: self.nest_big_top(state),
            locationName.NESTWW30:    lambda state: self.nest_big_top(state),
            locationName.NESTWW31:    lambda state: self.nest_big_top(state),
            locationName.NESTWW32:    lambda state: self.nest_big_top(state),
            locationName.NESTWW33:    lambda state: self.nest_big_top(state),
            locationName.NESTWW34:    lambda state: self.nest_big_top(state),
            locationName.NESTWW35:    lambda state: self.nest_big_top(state),
            locationName.NESTWW36:    lambda state: self.nest_big_top(state),
            locationName.NESTWW37:    lambda state: self.nest_big_top(state),
            locationName.NESTWW38:    lambda state: self.nest_big_top(state),
            locationName.NESTWW39:    lambda state: self.nest_big_top(state),
            locationName.NESTWW40:    lambda state: self.nest_big_top(state),
            locationName.NESTWW41:    lambda state: self.nest_big_top(state),
            locationName.NESTWW42:    lambda state: self.nest_big_top(state),


            locationName.NESTJR3:    lambda state: self.has_explosives(state) or state.has(itemName.DOUBLOON, self.player, 28),
            locationName.NESTJR4:    lambda state: self.has_explosives(state) or state.has(itemName.DOUBLOON, self.player, 28),
            locationName.NESTJR5:    lambda state: self.nest_jolly_gunpowder(state),
            locationName.NESTJR6:    lambda state: self.nest_jolly_gunpowder(state),

            locationName.NESTJR10:    lambda state: self.nest_seaweed_bottom(state),
            locationName.NESTJR11:    lambda state: self.nest_seaweed_others(state),
            locationName.NESTJR12:    lambda state: self.nest_seaweed_top(state),
            locationName.NESTJR13:    lambda state: self.nest_seaweed_others(state),

            locationName.NESTJR14:    lambda state: self.jiggy_merry_maggie(state),
            locationName.NESTJR15:    lambda state: self.jiggy_merry_maggie(state),

            locationName.NESTJR16:    lambda state: self.nest_bacon(state),
            locationName.NESTJR17:    lambda state: self.nest_bacon(state),
            locationName.NESTJR18:    lambda state: self.nest_bacon(state),
            locationName.NESTJR19:    lambda state: self.nest_bacon(state),

            locationName.NESTJR20:    lambda state: self.nest_lord_woo(state),
            locationName.NESTJR21:    lambda state: self.nest_lord_woo(state),
            locationName.NESTJR22:    lambda state: self.nest_lord_woo(state),
            locationName.NESTJR23:    lambda state: self.nest_lord_woo(state),

            locationName.NESTJR27:    lambda state: self.notes_jrl_blubs(state),

            locationName.NESTJR33:    lambda state: self.talon_torpedo(state),

            locationName.NESTJR39:    lambda state: self.talon_torpedo(state),
            locationName.NESTJR40:    lambda state: self.talon_torpedo(state),


            locationName.NESTTL4:    lambda state: self.nest_tdl_waterfall_alcove(state),
            locationName.NESTTL5:    lambda state: self.nest_tdl_waterfall_alcove(state),

            locationName.NESTTL12:    lambda state: self.nest_tdl_wall_with_holes(state),
            locationName.NESTTL13:    lambda state: self.nest_tdl_wall_with_holes(state),
            locationName.NESTTL14:    lambda state: self.nest_tdl_wall_with_holes(state),
            locationName.NESTTL15:    lambda state: self.nest_tdl_wall_with_holes(state),
            locationName.NESTTL18:    lambda state: self.nest_river_passage_entrance(state),

            locationName.NESTTL23:    lambda state: self.enter_tdl_train_station(state),
            locationName.NESTTL24:    lambda state: self.enter_tdl_train_station(state),
            locationName.NESTTL25:    lambda state: self.enter_tdl_train_station(state),
            locationName.NESTTL26:    lambda state: self.enter_tdl_train_station(state),

            locationName.NESTTL27:    lambda state: self.access_oogle_boogle(state),
            locationName.NESTTL28:    lambda state: self.access_oogle_boogle(state),
            locationName.NESTTL29:    lambda state: self.access_oogle_boogle(state),
            locationName.NESTTL30:    lambda state: self.access_oogle_boogle(state),

            locationName.NESTTL31:    lambda state: self.nest_mountain_flight_pad(state),
            locationName.NESTTL32:    lambda state: self.nest_mountain_flight_pad(state),
            locationName.NESTTL33:    lambda state: self.nest_mountain_underwater(state),
            locationName.NESTTL34:    lambda state: self.nest_mountain_underwater(state),

            locationName.NESTTL35:    lambda state: self.nest_river_passage(state),

            locationName.NESTTL42:    lambda state: self.nest_unga_egg(state),
            locationName.NESTTL43:    lambda state: self.nest_unga_egg(state),
            locationName.NESTTL44:    lambda state: self.nest_unga_egg(state),


            locationName.NESTTL45:    lambda state: self.nest_stomping_plains_footprint(state),
            locationName.NESTTL47:    lambda state: self.nest_stomping_plains_footprint(state),
            locationName.NESTTL48:    lambda state: self.nest_stomping_plains_footprint(state),
            locationName.NESTTL49:    lambda state: self.nest_stomping_plains_footprint(state),
            locationName.NESTTL50:    lambda state: self.nest_stomping_plains_footprint(state),
            locationName.NESTTL51:    lambda state: self.nest_stomping_plains_footprint(state),


            locationName.NESTGI4:    lambda state: self.nest_gi_outside_right(state),
            locationName.NESTGI5:    lambda state: self.nest_gi_outside_left(state),

            locationName.NESTGI6:    lambda state: self.nest_gi_floor1_top_pipe(state),
            locationName.NESTGI7:    lambda state: self.nest_gi_floor1_high_pipe(state),
            locationName.NESTGI8:    lambda state: self.nest_gi_outside_waste_disposal(state),
            locationName.NESTGI9:    lambda state: self.nest_gi_outside_waste_disposal(state),
            locationName.NESTGI10:    lambda state: self.nest_gi_floor1_high_pipe(state),
            locationName.NESTGI11:    lambda state: self.nest_outside_trash_compactor(state),

            locationName.NESTGI13:    lambda state: self.nest_gi_train_station_small_box(state),
            locationName.NESTGI14:    lambda state: self.nest_gi_train_station_medium_box(state),

            locationName.NESTGI17:    lambda state: self.nest_trash_compactor(state),
            locationName.NESTGI18:    lambda state: self.nest_trash_compactor(state),

            locationName.NESTGI19:    lambda state: self.nest_elevator_shaft_floor2(state),
            locationName.NESTGI20:    lambda state: self.nest_elevator_shaft_floor3(state),
            locationName.NESTGI21:    lambda state: self.nest_elevator_shaft_floor4(state),

            locationName.NESTGI23:    lambda state: self.nest_funny_platform(state),
            locationName.NESTGI26:    lambda state: self.egg_aim(state) or self.airborne_egg_aiming(state) or self.beak_bomb(state),
            locationName.NESTGI27:    lambda state: self.nest_funny_platform(state),
            locationName.NESTGI28:    lambda state: self.nest_funny_platform(state),
            locationName.NESTGI29:    lambda state: self.nest_funny_platform(state),
            locationName.NESTGI30:    lambda state: self.nest_funny_platform(state),
            locationName.NESTGI31:    lambda state: self.egg_aim(state) or self.airborne_egg_aiming(state) or self.beak_bomb(state),

            locationName.NESTGI33:    lambda state: self.nest_magnet(state),
            locationName.NESTGI34:    lambda state: self.nest_magnet(state),

            locationName.NESTGI35:    lambda state: self.nest_floor3_boxes(state),
            locationName.NESTGI36:    lambda state: self.nest_floor3_boxes(state),
            locationName.NESTGI37:    lambda state: self.nest_floor3_shortcut(state),
            locationName.NESTGI38:    lambda state: self.nest_floor3_boxes(state),
            locationName.NESTGI39:    lambda state: self.nest_floor3_boxes(state),
            locationName.NESTGI40:    lambda state: self.nest_floor3_boxes(state),

            locationName.NESTGI43:    lambda state: self.nest_floor4_front(state),
            locationName.NESTGI44:    lambda state: self.nest_floor4_front(state),
            locationName.NESTGI45:    lambda state: self.nest_floor4_front(state),
            locationName.NESTGI46:    lambda state: self.nest_floor4_front(state),
            locationName.NESTGI49:    lambda state: self.nest_outside_QC(state),

            locationName.NESTGI50:    lambda state: self.nest_quality_control(state),
            locationName.NESTGI51:    lambda state: self.nest_quality_control(state),
            locationName.NESTGI52:    lambda state: self.nest_quality_control(state),

            locationName.NESTGI53:    lambda state: self.nest_floor5_small_stack(state),

            locationName.NESTGI56:    lambda state: self.nest_outside_repair_depot(state),
            locationName.NESTGI57:    lambda state: self.nest_egg_fan_easy(state),
            locationName.NESTGI58:    lambda state: self.nest_egg_fan_easy(state),
            locationName.NESTGI59:    lambda state: self.nest_egg_fan_hard(state),
            locationName.NESTGI60:    lambda state: self.nest_outside_repair_depot(state),

            locationName.NESTGI61:    lambda state: self.can_beat_weldar(state),
            locationName.NESTGI62:    lambda state: self.can_beat_weldar(state),

            locationName.NESTGI63:    lambda state: self.nest_waste_disposal_water_pump(state),
            locationName.NESTGI64:    lambda state: self.jinjo_waste_disposal(state),
            locationName.NESTGI65:    lambda state: self.jinjo_waste_disposal(state),
            locationName.NESTGI66:    lambda state: self.nest_waste_disposal_water_pump(state),

            locationName.NESTGI67:    lambda state: self.jiggy_clinkers(state),
            locationName.NESTGI68:    lambda state: self.jiggy_clinkers(state),
            locationName.NESTGI69:    lambda state: self.jiggy_clinkers(state),
            locationName.NESTGI70:    lambda state: self.jiggy_clinkers(state),
            locationName.NESTGI71:    lambda state: self.jiggy_clinkers(state),
            locationName.NESTGI72:    lambda state: self.jiggy_clinkers(state),
            locationName.NESTGI73:    lambda state: self.jiggy_clinkers(state),
            locationName.NESTGI74:    lambda state: self.jiggy_clinkers(state),

            locationName.NESTGI75:    lambda state: self.nest_clinkers_lobby(state),
            locationName.NESTGI76:    lambda state: self.nest_clinkers_lobby(state),
            locationName.NESTGI77:    lambda state: self.nest_clinkers_lobby(state),
            locationName.NESTGI78:    lambda state: self.nest_clinkers_lobby(state),


            locationName.NESTHP1:    lambda state: self.tswitch_lavaside(state),
            locationName.NESTHP9:    lambda state: self.nest_hfp_entrance_shelter(state),
            locationName.NESTHP10:    lambda state: self.hfp_top(state),
            locationName.NESTHP11:    lambda state: self.hfp_top(state),

            locationName.NESTHP12:    lambda state: self.nest_ice_cube(state),
            locationName.NESTHP13:    lambda state: self.nest_ice_cube(state),
            locationName.NESTHP14:    lambda state: self.nest_ice_cube(state),
            locationName.NESTHP15:    lambda state: self.nest_ice_cube(state),
            locationName.NESTHP16:    lambda state: self.nest_ice_cube(state),
            locationName.NESTHP17:    lambda state: self.nest_ice_cube(state),
            locationName.NESTHP18:    lambda state: self.nest_ice_cube(state),

            locationName.NESTHP19:    lambda state: self.hfp_top(state),
            locationName.NESTHP20:    lambda state: self.hfp_top(state),

            locationName.NESTHP21:    lambda state: self.nest_icy_side_train_station_easy(state),
            locationName.NESTHP22:    lambda state: self.nest_icy_side_train_station_hard(state),

            locationName.NESTHP23:    lambda state: self.flight_pad(state) and self.ice_eggs_item(state),

            locationName.NESTHP24:    lambda state: self.nest_chilly_willy(state),

            locationName.NESTHP25:    lambda state: self.nest_hfp_kickball_egg(state),
            locationName.NESTHP26:    lambda state: self.nest_hfp_kickball_egg(state),
            locationName.NESTHP27:    lambda state: self.nest_hfp_kickball_egg(state),
            locationName.NESTHP28:    lambda state: self.nest_hfp_kickball_egg(state),
            locationName.NESTHP29:    lambda state: self.nest_hfp_kickball_feather(state),
            locationName.NESTHP30:    lambda state: self.nest_hfp_kickball_feather(state),

            locationName.NESTHP31:    lambda state: self.nest_ice_cube(state),
            locationName.NESTHP32:    lambda state: self.nest_ice_cube(state),
            locationName.NESTHP33:    lambda state: self.nest_ice_cube(state),
            locationName.NESTHP34:    lambda state: self.nest_hfp_spring_pad(state),
            locationName.NESTHP35:    lambda state: self.treble_hfp(state),
            locationName.NESTHP36:    lambda state: self.treble_hfp(state),

            locationName.NESTHP39:    lambda state: self.hfp_top(state),
            locationName.NESTHP40:    lambda state: self.hfp_top(state),



            locationName.NESTCC1:    lambda state: self.nest_ccl_flight(state),
            locationName.NESTCC2:    lambda state: self.nest_ccl_flight(state),
            locationName.NESTCC3:    lambda state: self.nest_ccl_flight(state),
            locationName.NESTCC4:    lambda state: self.nest_ccl_flight(state),
            locationName.NESTCC8:    lambda state: self.nest_jelly_castle(state),
            locationName.NESTCC9:    lambda state: self.nest_jelly_castle(state),
            locationName.NESTCC10:    lambda state: self.nest_jelly_castle(state),
            locationName.NESTCC11:    lambda state: self.nest_jelly_castle(state),
            locationName.NESTCC12:    lambda state: self.nest_ccl_dippy(state),
            locationName.NESTCC13:    lambda state: self.nest_ccl_dippy(state),
            locationName.NESTCC14:    lambda state: self.nest_ccl_dippy(state),
            locationName.NESTCC15:    lambda state: self.nest_ccl_dippy(state),
            locationName.NESTCC16:    lambda state: self.nest_ccl_flight(state),
            locationName.NESTCC17:    lambda state: self.nest_ccl_flight(state),
            locationName.NESTCC18:    lambda state: self.nest_ccl_flight(state),
            locationName.NESTCC19:    lambda state: self.nest_ccl_flight(state),

            locationName.NESTCC25:    lambda state: self.nest_outside_trash_can(state),
            locationName.NESTCC26:    lambda state: self.nest_outside_trash_can(state),
            locationName.NESTCC27:    lambda state: self.nest_outside_trash_can(state),
            locationName.NESTCC28:    lambda state: self.nest_outside_trash_can(state),

            locationName.NESTCC34:    lambda state: self.bill_drill(state),
            locationName.NESTCC35:    lambda state: self.bill_drill(state),

            locationName.NESTCC36:    lambda state: self.nest_inside_trash_can(state),
            locationName.NESTCC37:    lambda state: self.nest_inside_trash_can(state),

            locationName.NESTCC38:    lambda state: self.flight_pad(state),
            locationName.NESTCC39:    lambda state: self.flight_pad(state),

            locationName.NESTCC42:    lambda state: self.nest_ccl_flight(state),
            locationName.NESTCC43:    lambda state: self.nest_ccl_flight(state),
            locationName.NESTCC44:    lambda state: self.nest_near_superstash(state),
            locationName.NESTCC45:    lambda state: self.nest_near_superstash(state),

            locationName.NESTCC47:    lambda state: self.nest_pot_of_gold(state),
            locationName.NESTCC48:    lambda state: self.nest_pot_of_gold(state),
        }

        self.signpost_rules = {
            locationName.SIGNIH3: lambda state: self.signpost_jiggywiggy_back(state),
            locationName.SIGNIH4: lambda state: self.signpost_jiggywiggy_back(state),
            locationName.SIGNIH5: lambda state: self.signpost_jiggywiggy_back(state),

            locationName.SIGNMT3: lambda state: self.nest_pillars(state),

            locationName.SIGNMT7: lambda state: self.signpost_code_chamber(state),
            locationName.SIGNMT8: lambda state: self.breegull_blaster(state),
            locationName.SIGNMT9: lambda state: self.breegull_blaster(state),

            locationName.SIGNGM1: lambda state: self.signpost_gloomy_cavern(state),
            locationName.SIGNGM4: lambda state: self.signpost_chuffy(state),

            locationName.SIGNWW6: lambda state: self.signpost_pump_master(state),
            locationName.SIGNWW7: lambda state: self.signpost_gobi(state),

            locationName.SIGNJR3: lambda state: self.signpost_smugglers(state),
            locationName.SIGNJR4: lambda state: self.signpost_jrl_pipes(state),

            locationName.SIGNTL1: lambda state: self.notes_roar_cage(state),
            locationName.SIGNTL2: lambda state: self.signpost_trex(state),
            locationName.SIGNTL3: lambda state: self.signpost_mountain_top(state),
            locationName.SIGNTL4: lambda state: self.signpost_river_passage(state),

            locationName.SIGNGI1: lambda state: self.signpost_gi_outside(state),
            locationName.SIGNGI3: lambda state: self.signpost_elevator_shaft(state),
            locationName.SIGNGI4: lambda state: self.signpost_elevator_shaft(state),

            locationName.SIGNHP2: lambda state: self.hfp_top(state),
            locationName.SIGNHP3: lambda state: self.jiggy_volcano(state),
            locationName.SIGNHP4: lambda state: self.jiggy_volcano(state),
            locationName.SIGNHP5: lambda state: self.jiggy_volcano(state),

            locationName.SIGNCC1: lambda state: self.signpost_ccl_underwater(state),
            locationName.SIGNCC2: lambda state: self.can_access_sack_pack_silo(state),
            locationName.SIGNCC3: lambda state: self.signpost_pool_rim(state),
        }

        self.warp_pad_rules = {
            locationName.WARPGM2: lambda state: self.warp_pad_ggm_mumbo(state),
            locationName.WARPGM3: lambda state: self.warp_pad_ggm_wumba(state),
            locationName.WARPWW4: lambda state: self.warp_pad_ww_wumba(state),
            locationName.WARPTL3: lambda state: self.warp_pad_tdl_mumbo(state),
            locationName.WARPTL4: lambda state: self.warp_pad_tdl_wumba(state),
            locationName.WARPGI1: lambda state: self.warp_pad_floor_1(state),
            locationName.WARPGI4: lambda state: self.warp_pad_floor_4(state),
            locationName.WARPHP2: lambda state: self.hfp_top(state),
            locationName.WARPHP3: lambda state: self.hfp_top(state),
            locationName.WARPHP4: lambda state: self.hfp_top(state),
            locationName.WARPHP5: lambda state: self.warp_pad_icicle_grotto(state),
            locationName.WARPCK2: lambda state: self.warp_pad_ck_top(state),
        }

    def jiggy_targitzan(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
          logic = self.jiggy_sschamber(state) and (self.blue_eggs_item(state) or self.fire_eggs_item(state) or self.grenade_eggs_item(state))
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
          logic = self.jiggy_sschamber(state)\
                         and ((self.blue_eggs_item(state) or self.fire_eggs_item(state) or self.grenade_eggs_item(state))\
                              or self.ice_eggs_item(state) and self.beak_bayonet(state))
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
          logic = self.jiggy_sschamber(state)\
                         and ((self.blue_eggs_item(state) or self.fire_eggs_item(state) or self.grenade_eggs_item(state))\
                              or self.ice_eggs_item(state) and self.beak_bayonet(state))
        elif self.world.options.logic_type == LogicType.option_glitches:
          logic = self.jiggy_sschamber(state)\
                         and ((self.blue_eggs_item(state) or self.fire_eggs_item(state) or self.grenade_eggs_item(state))\
                              or self.ice_eggs_item(state) and self.beak_bayonet(state))
        return logic

    def jiggy_sschamber(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.breegull_blaster(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.breegull_blaster(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.breegull_blaster(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.breegull_blaster(state)
        return logic

    def jiggy_mayahem_kickball(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.humbaMT(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.humbaMT(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.humbaMT(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.humbaMT(state)
        return logic

    def jiggy_bovina(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
          logic = self.egg_aim(state) and (self.has_linear_egg(state))
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
          logic = self.egg_aim(state) or (self.MT_flight_pad(state) and self.airborne_egg_aiming(state))
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = (self.egg_aim(state) or (self.MT_flight_pad(state) and self.airborne_egg_aiming(state)))\
                    or (self.flap_flip(state) and self.beak_buster(state))\
                    or self.MT_flight_pad(state) and self.beak_bomb(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = (self.egg_aim(state) or (self.MT_flight_pad(state) and self.airborne_egg_aiming(state)))\
                    or (self.flap_flip(state) and self.beak_buster(state))\
                    or self.MT_flight_pad(state) and self.beak_bomb(state)
        return logic

    def jiggy_treasure_chamber(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.egg_aim(state) and\
                (self.flap_flip(state) or self.slightly_elevated_ledge(state)) and\
                  ((self.grip_grab(state) and self.spring_pad(state) and self.flap_flip(state) and self.talon_trot(state)) or self.MT_flight_pad(state))
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = (self.flap_flip(state) or self.slightly_elevated_ledge(state))\
                    and ((self.grip_grab(state) and self.spring_pad(state) and self.flap_flip(state) and self.egg_aim(state) and self.talon_trot(state))\
                        or (self.MT_flight_pad(state) and self.can_shoot_any_egg(state))\
                        or state.can_reach_region(regionName.TL_HATCH, self.player))\
                    and (self.MT_flight_pad(state) and self.can_shoot_any_egg(state) or self.egg_aim(state))
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = (self.flap_flip(state) or self.slightly_elevated_ledge(state))\
                    and ((self.grip_grab(state) and self.spring_pad(state) and self.flap_flip(state) and self.egg_aim(state) and self.talon_trot(state))\
                        or (self.MT_flight_pad(state) and self.can_shoot_any_egg(state))\
                        or state.can_reach_region(regionName.TL_HATCH, self.player))\
                    and (self.MT_flight_pad(state) and self.can_shoot_any_egg(state) or self.egg_aim(state))
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = (self.flap_flip(state) or self.slightly_elevated_ledge(state))\
                    and ((self.grip_grab(state) and self.spring_pad(state) and self.flap_flip(state) and self.egg_aim(state) and self.talon_trot(state))\
                        or (self.MT_flight_pad(state) and self.can_shoot_any_egg(state))\
                        or state.can_reach_region(regionName.TL_HATCH, self.player))\
                    and (self.MT_flight_pad(state) and self.can_shoot_any_egg(state) or self.egg_aim(state))
        return logic



    def jiggy_golden_goliath(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.check_mumbo_magic(state, itemName.MUMBOMT)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.check_mumbo_magic(state, itemName.MUMBOMT)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.check_mumbo_magic(state, itemName.MUMBOMT)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.check_mumbo_magic(state, itemName.MUMBOMT) or self.clockwork_eggs(state)
        return logic

    def jiggy_prison_quicksand(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.slightly_elevated_ledge(state)\
                  and self.stilt_stride(state) and self.prison_compound_as_banjo(state) and self.tall_jump(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.slightly_elevated_ledge(state)\
                  and self.stilt_stride(state) and self.prison_compound_as_banjo(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.slightly_elevated_ledge(state)\
                  and self.stilt_stride(state) and self.prison_compound_as_banjo(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.slightly_elevated_ledge(state)\
                  and self.stilt_stride(state) and self.prison_compound_as_banjo(state)
        return logic

    def jiggy_pillars(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.bill_drill(state) and (self.dive(state) or self.slightly_elevated_ledge(state) and self.tall_jump(state))\
                    and self.small_elevation(state) and self.prison_compound_as_banjo(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.bill_drill(state) and self.small_elevation(state) and self.prison_compound_as_banjo(state)\
                    and (self.dive(state) or self.slightly_elevated_ledge(state) or self.beak_buster(state))
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.prison_compound_as_banjo(state) and \
                ((self.bill_drill(state) and self.small_elevation(state)) or self.extremelyLongJump(state) or self.clockwork_shot(state))\
                    and (self.dive(state) or self.slightly_elevated_ledge(state) or self.beak_buster(state))
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.prison_compound_as_banjo(state) and \
                ((self.bill_drill(state) and self.small_elevation(state)) or self.extremelyLongJump(state) or self.clockwork_shot(state))\
                    and (self.dive(state) or self.slightly_elevated_ledge(state) or self.beak_buster(state))
        return logic

    def jiggy_top(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.talon_trot(state) or self.MT_flight_pad(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.talon_trot(state) or self.MT_flight_pad(state) or self.flap_flip(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = True
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = True
        return logic

    def jiggy_ssslumber(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.talon_trot(state) and self.grip_grab(state) and self.flap_flip(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.talon_trot(state) and (self.grip_grab(state) or self.beak_buster(state))\
                and self.flap_flip(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.talon_trot(state) and (self.grip_grab(state) or self.beak_buster(state))\
                and self.flap_flip(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.talon_trot(state) and (self.grip_grab(state) or self.beak_buster(state))\
                and self.flap_flip(state)
        return logic

    def jiggy_generator_cavern(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
          logic = self.fire_eggs(state) and self.egg_aim(state)\
                     and self.long_jump(state) and (self.flap_flip(state) or self.talon_trot(state))
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
          logic = (self.long_jump(state) and (self.flap_flip(state) or self.talon_trot(state)) and (self.has_fire(state) or self.bill_drill(state)))\
                or self.flap_flip(state) and self.beak_buster(state) and self.climb(state)\
                or self.GM_boulders(state) and self.leg_spring(state) and self.fire_eggs(state)\
                or self.GM_boulders(state) and self.tall_jump(state) and self.pack_whack(state) and self.climb(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.long_jump(state) and (self.flap_flip(state) or self.talon_trot(state))\
                or self.flap_flip(state) and self.beak_buster(state)\
                or self.clockwork_shot(state)\
                or self.GM_boulders(state) and self.tall_jump(state) and self.pack_whack(state) and self.climb(state)\
                or self.GM_boulders(state) and self.leg_spring(state)\
                or self.beak_buster(state) and self.grip_grab(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = (self.long_jump(state) and (self.flap_flip(state) or self.talon_trot(state)))\
                or self.flap_flip(state) and self.beak_buster(state)\
                or self.clockwork_shot(state)\
                or self.GM_boulders(state) and self.tall_jump(state) and self.pack_whack(state) and self.climb(state)\
                or self.GM_boulders(state) and self.leg_spring(state)\
                or self.beak_buster(state) and self.grip_grab(state)
        return logic

    def jiggy_waterfall_cavern(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
          logic = (self.grip_grab(state) or self.small_elevation(state)) and self.reach_waterfall_cavern_gate(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
          logic = self.reach_waterfall_cavern_gate(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.reach_waterfall_cavern_gate(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.reach_waterfall_cavern_gate(state)
        return logic

    def jiggy_ordnance_storage(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.breegull_blaster(state) and self.beak_bayonet(state) and \
                    self.GM_boulders(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.breegull_blaster(state) and self.beak_bayonet(state) and \
                    self.GM_boulders(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.breegull_blaster(state) and self.beak_bayonet(state) and \
                    self.GM_boulders(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.breegull_blaster(state) and self.beak_bayonet(state) and \
                    self.GM_boulders(state)
        return logic

    def jiggy_crushing_shed(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.mumboGGM(state) and self.beak_barge(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.mumboGGM(state) and self.beak_barge(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.mumboGGM(state) and self.beak_barge(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.mumboGGM(state) and self.beak_barge(state)
        return logic

    def jiggy_waterfall(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.springy_step_shoes(state)

        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.springy_step_shoes(state) or \
                    (self.glide(state)\
                    or self.wing_whack(state) and (self.tall_jump(state) or self.leg_spring(state))) and self.GM_boulders(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.springy_step_shoes(state) or \
                    (self.glide(state)\
                    or self.wing_whack(state) and (self.tall_jump(state) or self.leg_spring(state))) and self.GM_boulders(state)\
                    or self.clockwork_shot(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.springy_step_shoes(state) or \
                    (self.glide(state)\
                    or self.wing_whack(state) and (self.tall_jump(state) or self.leg_spring(state))) and self.GM_boulders(state)\
                    or self.clockwork_shot(state)
        return logic

    def jiggy_power_hut(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.GM_boulders(state) and self.split_up(state) and self.climb(state)

        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.GM_boulders(state) and\
                    ((self.split_up(state) and self.climb(state)) or self.has_fire(state) or self.bill_drill(state))

        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.GM_boulders(state)

        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.GM_boulders(state)
        return logic

    def jiggy_flooded_caves(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.humbaGGM(state) and self.dive(state) and (self.tall_jump(state) or self.grip_grab(state))

        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.dive(state) and (self.tall_jump(state) or self.grip_grab(state) or self.beak_buster(state))\
                    and (self.humbaGGM(state)\
                        or self.reach_waterfall_cavern_gate(state) and (
                            self.talon_trot(state) and (self.flutter(state) or self.air_rat_a_tat_rap(state))\
                            or self.roll(state) and self.tall_jump(state) and (self.flutter(state) or self.air_rat_a_tat_rap(state))
                        )
                    )

        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.dive(state) and (self.tall_jump(state) or self.grip_grab(state) or self.beak_buster(state) or self.clockwork_shot(state))\
                    and (self.humbaGGM(state)\
                        or self.reach_waterfall_cavern_gate(state) and (
                            self.talon_trot(state) and (self.flutter(state) or self.air_rat_a_tat_rap(state))\
                            or self.roll(state) and self.tall_jump(state) and (self.flutter(state) or self.air_rat_a_tat_rap(state))
                        )
                    )

        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.dive(state) and (self.tall_jump(state) or self.grip_grab(state) or self.beak_buster(state) or self.clockwork_shot(state))\
                    and (self.humbaGGM(state)\
                        or self.reach_waterfall_cavern_gate(state) and (
                            self.talon_trot(state) and (self.flutter(state) or self.air_rat_a_tat_rap(state))\
                            or self.roll(state) and self.tall_jump(state) and (self.flutter(state) or self.air_rat_a_tat_rap(state))
                        )
                    )
        return logic

    def reach_waterfall_cavern_gate(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
          logic = self.turbo_trainers(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
          logic = self.ggm_trot(state)\
                or self.GM_boulders(state) and self.split_up(state)\
                or state.has(itemName.WARPGM1, self.player) and state.has(itemName.WARPGM5, self.player)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.ggm_trot(state)\
                or self.GM_boulders(state) and self.split_up(state)\
                or state.has(itemName.WARPGM1, self.player) and state.has(itemName.WARPGM5, self.player)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.ggm_trot(state)\
                or self.GM_boulders(state) and self.split_up(state)\
                or state.has(itemName.WARPGM1, self.player) and state.has(itemName.WARPGM5, self.player)
        return logic
    def jiggy_hoop_hurry(self, state: CollectionState) -> bool:
        # Solo Kazooie can get the jiggy with the spring pad.
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.split_up(state) and self.has_explosives(state) and self.turbo_trainers(state)\
                and self.spring_pad(state) and (self.flap_flip(state) or self.leg_spring(state))
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.split_up(state) and self.has_explosives(state)\
                and (self.leg_spring(state) or self.tall_jump(state))\
                and (self.spring_pad(state) or self.flap_flip(state) or self.leg_spring(state))
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.split_up(state) and self.has_explosives(state)\
                and (self.leg_spring(state) or self.tall_jump(state))\
                and (self.spring_pad(state) or self.flap_flip(state) or self.leg_spring(state))
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.split_up(state) and self.has_explosives(state)\
                and (self.leg_spring(state) or self.tall_jump(state))\
                and (self.spring_pad(state) or self.flap_flip(state) or self.leg_spring(state))
        return logic

    def jiggy_dodgem(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.humbaWW(state) and self.mumboWW(state) and \
                    self.grip_grab(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.humbaWW(state) and self.mumboWW(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.humbaWW(state) and self.mumboWW(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            if self.world.options.speed_up_minigames:
                # No van required if you can clockwork warp into dodgems, since the door is already opened!
                logic = (self.humbaWW(state) and self.mumboWW(state))\
                    or (self.precise_clockwork_warp(state))
            else:
                logic = self.humbaWW(state) and self.mumboWW(state)
        return logic

    # I assume nobody wants to do this from the ground.
    def jiggy_patches(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.airborne_egg_aiming(state) and self.egg_aim(state) and \
                    self.grenade_eggs(state) and self.flight_pad(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.airborne_egg_aiming(state) and self.egg_aim(state) and \
                    self.grenade_eggs(state) and self.flight_pad(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.airborne_egg_aiming(state) and self.egg_aim(state) and \
                    self.grenade_eggs(state) and self.flight_pad(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.airborne_egg_aiming(state) and self.egg_aim(state) and \
                    self.grenade_eggs(state) and self.flight_pad(state)
        return logic

    def jiggy_peril(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.humbaGGM(state) and \
                    self.mumboWW(state) and \
                    self.saucer_door_open(state) and \
                    self.can_reach_saucer(state) and\
                    state.can_reach_region(regionName.GM, self.player) and self.has_explosives(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.humbaGGM(state) and \
                    self.mumboWW(state) and \
                    self.saucer_door_open(state) and state.can_reach_region(regionName.GM, self.player) and \
                    self.can_reach_saucer(state) and\
                    self.has_explosives(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.humbaGGM(state) and \
                    self.mumboWW(state) and \
                    self.saucer_door_open(state) and state.can_reach_region(regionName.GM, self.player) and \
                    self.can_reach_saucer(state) and\
                    self.has_explosives(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.humbaGGM(state) and \
                    self.mumboWW(state) and \
                    self.saucer_door_open(state) and state.can_reach_region(regionName.GM, self.player) and \
                    self.can_reach_saucer(state) and\
                    self.has_explosives(state)
        return logic

    def jiggy_balloon_burst(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.split_up(state) and self.has_explosives(state) and self.airborne_egg_aiming(state)\
                and self.spring_pad(state) and (self.flap_flip(state) or self.leg_spring(state))
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.split_up(state) and self.has_explosives(state) and self.airborne_egg_aiming(state)\
                and (self.leg_spring(state) or self.tall_jump(state))\
                and (self.spring_pad(state) or self.flap_flip(state) or self.leg_spring(state))
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.split_up(state) and self.has_explosives(state) and self.airborne_egg_aiming(state)\
                and (self.leg_spring(state) or self.tall_jump(state))\
                and (self.spring_pad(state) or self.flap_flip(state) or self.leg_spring(state))
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.split_up(state) and self.has_explosives(state) and self.airborne_egg_aiming(state)\
                and (self.leg_spring(state) or self.tall_jump(state))\
                and (self.spring_pad(state) or self.flap_flip(state) or self.leg_spring(state))
        return logic

    def jiggy_dive_of_death(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.grip_grab(state) and self.climb(state) and self.flap_flip(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.climb(state) and (self.flap_flip(state) or self.talon_trot(state) or (\
                self.tall_jump(state) and (self.beak_buster(state) or self.air_rat_a_tat_rap(state))))
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.climb(state) and (self.flap_flip(state) or self.talon_trot(state) or self.clockwork_shot(state) or (\
                self.tall_jump(state) and (self.beak_buster(state) or self.air_rat_a_tat_rap(state))))
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.climb(state) and (self.flap_flip(state) or self.talon_trot(state) or self.clockwork_shot(state) or (\
                self.tall_jump(state) and (self.beak_buster(state) or self.air_rat_a_tat_rap(state))))
        return logic

    def jiggy_mrs_boggy(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.mumboWW(state) and \
                self.taxi_pack(state) and \
                self.has_explosives(state)\
                and self.spring_pad(state)

        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.mumboWW(state) and \
                self.taxi_pack(state) and \
                self.has_explosives(state)\
                and (self.spring_pad(state) or self.leg_spring(state) or self.glide(state))

        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.humbaWW(state) and \
                self.mumboWW(state) and \
                self.taxi_pack(state)\
                and (self.spring_pad(state) or self.leg_spring(state) or self.glide(state))

        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.glitchedInfernoAccess(state) and\
                    (self.mumboWW(state) or self.clockwork_eggs(state)) and \
                    self.taxi_pack(state)\
                    and (self.spring_pad(state) or self.leg_spring(state) or self.glide(state))
        return logic

    def jiggy_star_spinner(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.mumboWW(state) and self.talon_trot(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.mumboWW(state) and self.talon_trot(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.mumboWW(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.mumboWW(state)
        return logic

    def jiggy_inferno(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.humbaWW(state) and self.split_up(state) and self.tall_jump(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.humbaWW(state) and (self.split_up(state) and (self.tall_jump(state) or self.leg_spring(state)) or self.flap_flip(state) and (self.talon_trot(state) or self.turbo_trainers(state)))
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.humbaWW(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.humbaWW(state) or (self.glitchedInfernoAccess(state) and (self.split_up(state) and (self.tall_jump(state) or self.leg_spring(state)) or self.flap_flip(state) and (self.talon_trot(state) or self.turbo_trainers(state))))
        return logic

    def jiggy_cactus(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.bill_drill(state) and self.grenade_eggs(state)\
                  and self.beak_buster(state) and self.climb(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.bill_drill(state) and self.grenade_eggs(state)\
                  and self.beak_buster(state) and\
                    (self.climb(state) or self.leg_spring(state) and self.glide(state))
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.bill_drill(state) and self.grenade_eggs(state)\
                  and self.beak_buster(state) and\
                    (self.clockwork_shot(state) or self.climb(state) or self.leg_spring(state) and self.glide(state))
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.bill_drill(state) and self.grenade_eggs(state)\
                  and self.beak_buster(state) and\
                    (self.clockwork_shot(state) or self.climb(state) or self.leg_spring(state) and self.glide(state))
        return logic

    def jiggy_sub_challenge(self, state: CollectionState) -> bool:
        return self.humbaJRL(state)

    def jiggy_tiptup(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.hatch(state) and self.has_explosives(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.hatch(state) and self.has_explosives(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.hatch(state) and self.has_explosives(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.hatch(state) and self.has_explosives(state)
        return logic


    # I assume nobody wants to do this with clockworks (is it even possible?) or talon torpedo
    def jiggy_bacon(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.sub_aqua_egg_aiming(state) and self.has_linear_egg(state) and state.has(itemName.MUMBOJR, self.player)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.sub_aqua_egg_aiming(state) and self.has_linear_egg(state)\
                        and (state.has(itemName.MUMBOJR, self.player) or self.doubleAir(state))
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = (self.sub_aqua_egg_aiming(state) and self.has_linear_egg(state)) or \
                (self.humbaJRL(state) and self.egg_aim(state) and self.has_linear_egg(state))
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = (self.sub_aqua_egg_aiming(state) and self.has_linear_egg(state)) or \
                (self.humbaJRL(state) and self.egg_aim(state) and self.has_linear_egg(state))
        return logic

    def jiggy_pig_pool(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.HFP_hot_water_cooled(state)\
                    and self.jrl_waste_disposal(state)\
                    and self.flap_flip(state)\
                    and (self.has_explosives(state) or self.beak_barge(state))
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.HFP_hot_water_cooled(state)\
                    and self.jrl_waste_disposal(state)\
                    and (self.flap_flip(state)\
                        or self.tall_jump(state) and self.beak_buster(state)\
                        or self.talon_trot(state) and self.flutter(state) and self.beak_buster(state)
                    )\
                    and (self.has_explosives(state)\
                        or self.beak_barge(state)\
                        or self.dragon_kazooie(state) and self.ground_rat_a_tat_rap(state)\
                    )
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.HFP_hot_water_cooled(state)\
                    and self.jrl_waste_disposal(state)\
                    and ((self.flap_flip(state)\
                        or self.tall_jump(state) and self.beak_buster(state)\
                        or self.talon_trot(state) and self.flutter(state) and self.beak_buster(state)\
                        or self.tall_jump(state) and self.flutter(state)\
                        or self.extremelyLongJump(state)\
                        ) and (
                            self.has_explosives(state)\
                            or self.beak_barge(state)\
                            or self.dragon_kazooie(state) and self.ground_rat_a_tat_rap(state)\
                        )\
                        or self.clockwork_shot(state)
                    )
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.HFP_hot_water_cooled(state)\
                    and self.jrl_waste_disposal(state)\
                    and ((self.flap_flip(state)\
                        or self.tall_jump(state) and self.beak_buster(state)\
                        or self.talon_trot(state) and self.flutter(state) and self.beak_buster(state)
                        ) and (
                            self.has_explosives(state)\
                            or self.beak_barge(state)\
                            or self.dragon_kazooie(state) and self.ground_rat_a_tat_rap(state)\
                        )\
                        or self.clockwork_shot(state)
                    )
        return logic

    def jiggy_smuggler(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.has_explosives(state) and \
                     self.split_up(state) and self.glide(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.has_explosives(state) and \
                     self.split_up(state) and self.glide(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.has_explosives(state) and \
                     self.split_up(state) and self.glide(state)\
                     or self.clockwork_shot(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.has_explosives(state) and \
                     self.split_up(state) and self.glide(state)\
                     or self.clockwork_shot(state)
        return logic

    def jiggy_merry_maggie(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.sub_aqua_egg_aiming(state) and self.has_linear_egg(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.sub_aqua_egg_aiming(state) and self.has_linear_egg(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = (self.sub_aqua_egg_aiming(state) or self.egg_aim(state)) and self.has_linear_egg(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = (self.sub_aqua_egg_aiming(state) or self.egg_aim(state)) and self.has_linear_egg(state)
        return logic

    def jiggy_lord_woo(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.sub_aqua_egg_aiming(state) and self.grenade_eggs(state)\
                        and (self.humbaJRL(state) or self.check_mumbo_magic(state, itemName.MUMBOJR))
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.sub_aqua_egg_aiming(state) and self.grenade_eggs(state)\
                        and (self.humbaJRL(state) or self.check_mumbo_magic(state, itemName.MUMBOJR))
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.grenade_eggs(state) and self.sub_aqua_egg_aiming(state) and (
                        self.talon_torpedo(state) and self.doubleAir(state)\
                        or self.check_mumbo_magic(state, itemName.MUMBOJR)\
                        or self.humbaJRL(state)
                    )
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.grenade_eggs(state) and self.sub_aqua_egg_aiming(state) and (
                        self.talon_torpedo(state) and self.doubleAir(state)\
                        or self.check_mumbo_magic(state, itemName.MUMBOJR)\
                        or self.humbaJRL(state)
                    )
        return logic

    def jiggy_see_mee(self, state: CollectionState) -> bool:
        return self.talon_torpedo(state)

    def jiggy_pawno(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = state.has(itemName.DOUBLOON, self.player, 23) and self.small_elevation(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = state.has(itemName.DOUBLOON, self.player, 23) and self.small_elevation(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = state.has(itemName.DOUBLOON, self.player, 23) and (self.small_elevation(state) or self.clockwork_shot(state))
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = state.has(itemName.DOUBLOON, self.player, 23) and (self.small_elevation(state) or self.clockwork_shot(state))
        return logic

    def jiggy_ufo(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.check_mumbo_magic(state, itemName.MUMBOJR) and self.talon_torpedo(state) and \
                    self.egg_aim(state) and self.ice_eggs(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.talon_torpedo(state) and self.egg_aim(state) and \
                    self.ice_eggs(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.talon_torpedo(state) and self.ice_eggs(state)\
                  and (self.talon_trot(state) or self.egg_aim(state))
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.talon_torpedo(state) and self.ice_eggs(state)\
                  and (self.talon_trot(state) or self.egg_aim(state))
        return logic

    def jiggy_terry_nest(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.can_beat_terry(state) and (self.has_explosives(state) or \
                    self.bill_drill(state))
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = (self.has_explosives(state) or self.bill_drill(state)) and self.can_beat_terry(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = (self.has_explosives(state) or self.bill_drill(state)) and self.can_beat_terry(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = (self.has_explosives(state) or self.bill_drill(state)) and self.can_beat_terry(state)
        return logic

    def jiggy_dippy(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.talon_torpedo(state) and state.can_reach_region(regionName.CC, self.player) and self.dive(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.talon_torpedo(state) and state.can_reach_region(regionName.CC, self.player) and (self.dive(state) or self.beak_buster(state))
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.talon_torpedo(state) and state.can_reach_region(regionName.CC, self.player)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.talon_torpedo(state) and state.can_reach_region(regionName.CC, self.player)
        return logic

    def scrit(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.mumboTDL(state) and self.bill_drill(state) and self.tall_jump(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.mumboTDL(state) and self.bill_drill(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.mumboTDL(state) and self.bill_drill(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.mumboTDL(state) and self.bill_drill(state)
        return logic

    def scrat(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.can_beat_king_coal(state) and state.has(itemName.TRAINSWIH, self.player) and state.has(itemName.TRAINSWTD, self.player) and self.taxi_pack(state) and self.check_mumbo_magic(state, itemName.MUMBOIH) and (self.tall_jump(state) or self.talon_trot(state))
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.can_beat_king_coal(state) and state.has(itemName.TRAINSWIH, self.player) and state.has(itemName.TRAINSWTD, self.player) and self.taxi_pack(state) and self.check_mumbo_magic(state, itemName.MUMBOIH)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.can_beat_king_coal(state) and state.has(itemName.TRAINSWIH, self.player) and state.has(itemName.TRAINSWTD, self.player) and self.taxi_pack(state) and self.check_mumbo_magic(state, itemName.MUMBOIH)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.can_beat_king_coal(state) and state.has(itemName.TRAINSWIH, self.player) and state.has(itemName.TRAINSWTD, self.player) and self.taxi_pack(state) and self.check_mumbo_magic(state, itemName.MUMBOIH)
        return logic

    # You don't even need to go in the styrac cave for that one.
    def scrut(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.can_beat_king_coal(state) and state.has(itemName.TRAINSWTD, self.player) and state.has(itemName.TRAINSWWW, self.player) and self.grenade_eggs(state) and self.egg_aim(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.can_beat_king_coal(state) and state.has(itemName.TRAINSWTD, self.player) and state.has(itemName.TRAINSWWW, self.player) and self.grenade_eggs(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.can_beat_king_coal(state) and state.has(itemName.TRAINSWTD, self.player) and state.has(itemName.TRAINSWWW, self.player) and self.grenade_eggs(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.can_beat_king_coal(state) and state.has(itemName.TRAINSWTD, self.player) and state.has(itemName.TRAINSWWW, self.player) and self.grenade_eggs(state)
        return logic

    def jiggy_scrotty(self, state: CollectionState) -> bool:
        return self.scrit(state) and self.scrat(state) and self.scrut(state)

    def jiggy_oogle_boogle(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.access_oogle_boogle(state) and self.fire_eggs(state) and \
                    self.smuggle_food(state) and self.grip_grab(state) and \
                    self.bill_drill(state) and self.spring_pad(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.access_oogle_boogle(state) and self.has_fire(state) and \
                    self.smuggle_food(state) and self.grip_grab(state) and \
                    self.bill_drill(state) and self.spring_pad(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.access_oogle_boogle(state) and self.has_fire(state) and \
                    self.grip_grab(state) and self.bill_drill(state) and self.smuggle_food(state)\
                    and self.spring_pad(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = (self.access_oogle_boogle(state) or self.clockwork_warp(state))\
                    and self.has_fire(state) and self.grip_grab(state) and self.bill_drill(state) and self.smuggle_food(state) and self.spring_pad(state)
        return logic

    def jiggy_chompa(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.breegull_blaster(state) and (
                ((self.tall_jump(state) or self.grip_grab(state)) and self.flight_pad(state)
                 or (self.egg_aim(state) and self.has_explosives(state) and self.springy_step_shoes(state)))
            )
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.breegull_blaster(state) and (
                ((self.tall_jump(state) or self.grip_grab(state)) and self.flight_pad(state)
                 or (self.egg_aim(state) and self.has_explosives(state) and self.springy_step_shoes(state))
                 or (self.springy_step_shoes(state) and self.veryLongJump(state)))
            )
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.breegull_blaster(state) and (
                ((self.tall_jump(state) or self.grip_grab(state) or self.beak_buster(state)) and self.flight_pad(state)
                 or (self.egg_aim(state) and self.has_explosives(state) and self.springy_step_shoes(state))
                 or (self.springy_step_shoes(state) and self.veryLongJump(state)))
            )
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.breegull_blaster(state) and (
                ((self.tall_jump(state) or self.grip_grab(state) or self.beak_buster(state)) and self.flight_pad(state)
                 or (self.egg_aim(state) and self.has_explosives(state) and self.springy_step_shoes(state))
                 or (self.springy_step_shoes(state) and self.veryLongJump(state)))
            )
        return logic

    def jiggy_terry_kids(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.can_beat_terry(state) and self.hatch(state) and \
                    self.taxi_pack(state) and self.access_oogle_boogle(state)\
                    and self.flight_pad(state) and self.climb(state) and self.spring_pad(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.can_beat_terry(state) and self.hatch(state) and \
                    self.taxi_pack(state) and self.access_oogle_boogle(state)\
                    and self.flight_pad(state) and self.climb(state) and self.spring_pad(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.can_beat_terry(state) and self.hatch(state) and \
                    self.taxi_pack(state) and self.access_oogle_boogle(state)\
                    and self.flight_pad(state) and self.climb(state) and self.spring_pad(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.can_beat_terry(state) and self.hatch(state) and \
                    self.taxi_pack(state) and self.access_oogle_boogle(state)\
                    and self.flight_pad(state) and self.climb(state) and self.spring_pad(state)
        return logic

    def jiggy_stomping_plains(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.talon_trot(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.talon_trot(state) or self.springy_step_shoes(state) or self.turbo_trainers(state)\
                    or self.split_up(state) and self.snooze_pack(state) and self.tall_jump(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.tall_jump(state) or self.talon_trot(state) or self.springy_step_shoes(state) or self.turbo_trainers(state)\
                    or self.split_up(state) and self.snooze_pack(state) and self.tall_jump(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.tall_jump(state) or self.talon_trot(state) or self.springy_step_shoes(state) or self.turbo_trainers(state)\
                    or self.split_up(state) and self.snooze_pack(state) and self.tall_jump(state)
        return logic

    # TDL top to stomping plains
    def can_reach_stomping_plains(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.ice_eggs(state) and self.tdl_top(state) and self.long_jump(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.tdl_top(state) and \
            (self.wing_whack(state) or self.glide(state) or self.ice_eggs(state)) and self.long_jump(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.tdl_top(state) and (self.long_jump(state) or self.talon_trot(state) or self.split_up(state))
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.tdl_top(state) and (self.long_jump(state) or self.talon_trot(state))
        return logic

    def can_cross_bonfire_cavern(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.ice_eggs(state) and self.long_jump(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = (self.ice_eggs(state)) and self.long_jump(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = (self.long_jump(state) or self.talon_trot(state))
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = (self.long_jump(state) or self.talon_trot(state))
        return logic

    def jiggy_rocknuts(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.egg_aim(state) and self.clockwork_eggs(state) and self.long_jump(state) and self.tall_jump(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.egg_aim(state) and self.clockwork_eggs(state) and self.long_jump(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.clockwork_eggs(state) and ((self.egg_aim(state) and self.long_jump(state)) or self.veryLongJump(state))
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.clockwork_eggs(state) and ((self.egg_aim(state) and self.long_jump(state)) or self.veryLongJump(state))
        return logic

    def jiggy_roar_cage(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.humbaTDL(state) and self.roar(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.humbaTDL(state) and self.roar(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.humbaTDL(state) and self.roar(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.humbaTDL(state) and self.roar(state)\
                    or self.clockwork_shot(state) and (self.springy_step_shoes(state) or self.long_jump(state) or self.split_up(state))
        return logic

    def jiggy_skivvy(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.humbaGI(state) and self.bill_drill(state)\
                    and state.can_reach_region(regionName.GIF, self.player) and (self.airborne_egg_aiming(state) or self.beak_bomb(state))\
                    and self.floor_2_skivvy_switch(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.humbaGI(state) and self.bill_drill(state)\
                    and state.can_reach_region(regionName.GIF, self.player) and (self.airborne_egg_aiming(state) or self.beak_bomb(state))\
                    and self.floor_2_skivvy_switch(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.humbaGI(state) and self.bill_drill(state)\
                    and state.can_reach_region(regionName.GIF, self.player) and (self.airborne_egg_aiming(state) or self.beak_bomb(state))\
                    and self.floor_2_skivvy_switch(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.humbaGI(state) and self.bill_drill(state)\
                    and state.can_reach_region(regionName.GIF, self.player) and (self.airborne_egg_aiming(state) or self.beak_bomb(state))\
                    and self.floor_2_skivvy_switch(state)
        return logic

    def floor_2_skivvy_switch(self, state: CollectionState) -> bool:
        if self.world.options.logic_type == LogicType.option_intended:
            logic = state.can_reach_region(regionName.GI2, self.player) and self.claw_clamber_boots(state) and self.flap_flip(state) and self.grip_grab(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = state.can_reach_region(regionName.GI2, self.player) and self.claw_clamber_boots(state)\
                        and ((self.flap_flip(state) and self.grip_grab(state))\
                             or self.talon_trot(state) and (self.flutter(state) or self.air_rat_a_tat_rap(state)))\
                    or state.can_reach_region(regionName.GI2, self.player) and self.solo_kazooie_gi(state)\
                        and (self.leg_spring(state) or self.claw_clamber_boots(state) and (self.can_shoot_any_egg(state) or self.wing_whack(state)))\
                    or state.can_reach_region(regionName.GI3, self.player) and\
                        (self.climb(state) and (self.veryLongJump(state) or (self.flap_flip(state) or self.tall_jump(state)) and self.grip_grab(state))\
                            or self.small_elevation(state) and self.split_up(state) and self.leg_spring(state))
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = state.can_reach_region(regionName.GI2, self.player) and self.claw_clamber_boots(state)\
                        and ((self.flap_flip(state) and self.grip_grab(state))\
                             or self.talon_trot(state) and (self.flutter(state) or self.air_rat_a_tat_rap(state)))\
                    or state.can_reach_region(regionName.GI2, self.player) and self.solo_kazooie_gi(state)\
                        and (self.leg_spring(state) or self.claw_clamber_boots(state) and (self.can_shoot_any_egg(state) or self.wing_whack(state)))\
                    or state.can_reach_region(regionName.GI3, self.player) and\
                        (self.climb(state) and (self.veryLongJump(state) or (self.flap_flip(state) or self.tall_jump(state)) and self.grip_grab(state))\
                            or self.small_elevation(state) and self.split_up(state) and self.leg_spring(state))
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = state.can_reach_region(regionName.GI2, self.player) and self.claw_clamber_boots(state)\
                        and ((self.flap_flip(state) and self.grip_grab(state))\
                             or self.talon_trot(state) and (self.flutter(state) or self.air_rat_a_tat_rap(state)))\
                    or state.can_reach_region(regionName.GI2, self.player) and self.solo_kazooie_gi(state)\
                        and (self.leg_spring(state) or self.claw_clamber_boots(state) and (self.can_shoot_any_egg(state) or self.wing_whack(state)))\
                    or state.can_reach_region(regionName.GI3, self.player) and\
                        (self.climb(state) and (self.veryLongJump(state) or (self.flap_flip(state) or self.tall_jump(state)) and self.grip_grab(state))\
                            or self.small_elevation(state) and self.split_up(state) and self.leg_spring(state))
        return logic

    def jiggy_floor5(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.split_up(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.split_up(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.split_up(state) or self.clockwork_shot(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.split_up(state) or self.clockwork_shot(state)
        return logic

    def jiggy_quality_control(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.grenade_eggs(state) and \
                    self.egg_aim(state) and \
                    self.can_use_battery(state) and self.humbaGI(state)\
                    and self.climb(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.grenade_eggs(state) and \
                    ((self.egg_aim(state) and self.humbaGI(state) or \
                    self.leg_spring(state))) and self.can_use_battery(state) and self.climb(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.grenade_eggs(state) and self.can_use_battery(state) and self.climb(state) and\
                    (self.tall_jump(state)\
                        or self.leg_spring(state)\
                        or self.humbaGI(state) and self.egg_aim(state)\
                        or self.clockwork_shot(state))
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.grenade_eggs(state) and self.can_use_battery(state) and self.climb(state) and\
                    (self.tall_jump(state)\
                        or self.leg_spring(state)\
                        or self.humbaGI(state) and self.egg_aim(state)\
                        or self.clockwork_shot(state)\
                        )\
                    or self.precise_clockwork_warp(state)
        return logic

    def jiggy_guarded(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.split_up(state) and self.claw_clamber_boots(state) and self.egg_aim(state) and\
                    (self.blue_eggs(state) or self.fire_eggs(state) or self.grenade_eggs(state))\
                    and (self.spring_pad(state) or self.wing_whack(state) or self.glide(state))
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.split_up(state) and\
                    ((self.claw_clamber_boots(state) or state.can_reach_region(regionName.GI2, self.player)) and self.spring_pad(state)\
                        or self.claw_clamber_boots(state) and (self.wing_whack(state) or self.glide(state)) and (self.egg_aim(state) or self.wing_whack(state))\
                        or self.leg_spring(state) and self.glide(state) and (self.egg_aim(state) or self.wing_whack(state)))\
                    and (self.blue_eggs(state) or self.fire_eggs(state) or self.grenade_eggs(state))
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.split_up(state) and\
                    ((self.claw_clamber_boots(state) or state.can_reach_region(regionName.GI2, self.player)) and self.spring_pad(state)\
                        or self.claw_clamber_boots(state) and (self.wing_whack(state) or self.glide(state)) and (self.egg_aim(state) or self.wing_whack(state))\
                        or self.leg_spring(state) and self.glide(state) and (self.egg_aim(state) or self.wing_whack(state)))\
                    and (self.blue_eggs(state) or self.fire_eggs(state) or self.grenade_eggs(state))\
                    or (self.claw_clamber_boots(state) or state.can_reach_region(regionName.GI2, self.player)) and (self.spring_pad(state) or self.leg_spring(state)) and self.clockwork_shot(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.split_up(state) and\
                    ((self.claw_clamber_boots(state) or state.can_reach_region(regionName.GI2, self.player)) and self.spring_pad(state)\
                        or self.claw_clamber_boots(state) and (self.wing_whack(state) or self.glide(state)) and (self.egg_aim(state) or self.wing_whack(state))\
                        or self.leg_spring(state) and self.glide(state) and (self.egg_aim(state) or self.wing_whack(state)))\
                    and (self.blue_eggs(state) or self.fire_eggs(state) or self.grenade_eggs(state))\
                    or (self.claw_clamber_boots(state) or state.can_reach_region(regionName.GI2, self.player)) and (self.spring_pad(state) or self.leg_spring(state)) and self.clockwork_shot(state)
        return logic

    def jiggy_trash_compactor(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.snooze_pack(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.snooze_pack(state) or self.pack_whack(state) and self.tall_jump(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.snooze_pack(state) or self.pack_whack(state) and self.tall_jump(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.snooze_pack(state)\
                    or self.pack_whack(state) and self.tall_jump(state)\
                    or (self.egg_aim(state) and self.clockwork_eggs(state) and self.breegull_bash(state) and self.talon_trot(state))
        return logic

    def jiggy_twinkly(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.can_use_battery(state) and self.grip_grab(state) and self.turbo_trainers(state)\
                    or self.can_use_battery(state) and self.elevator_door(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            #Banjo to Boiler Plant
            #Solo Kazooie to boiler plant, otherwise turbo trainers to do the minigame as BK
            logic = self.can_use_battery(state) and (self.tall_jump(state) or self.grip_grab(state))\
                    and (self.leg_spring(state)\
                        or (self.glide(state) or self.wing_whack(state)) and self.tall_jump(state)
                        or state.can_reach_region(regionName.GIF, self.player) and self.flight_to_boiler_plant(state)
                        or self.turbo_trainers(state))
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = logic = self.can_use_battery(state) and (self.tall_jump(state) or self.grip_grab(state))\
                    and (self.leg_spring(state)\
                        or (self.glide(state) or self.wing_whack(state)) and self.tall_jump(state)
                        or state.can_reach_region(regionName.GIF, self.player) and self.flight_to_boiler_plant(state)
                        or self.turbo_trainers(state))
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = logic = self.can_use_battery(state) and (self.tall_jump(state) or self.grip_grab(state))\
                    and (self.leg_spring(state)\
                        or (self.glide(state) or self.wing_whack(state)) and self.tall_jump(state)
                        or state.can_reach_region(regionName.GIF, self.player) and self.flight_to_boiler_plant(state)
                        or self.turbo_trainers(state))
        return logic

    def jiggy_waste_disposal_box(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.sack_pack(state) and self.solo_banjo_waste_disposal(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.solo_banjo_waste_disposal(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.solo_banjo_waste_disposal(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.solo_banjo_waste_disposal(state)
        return logic

    def jiggy_dragons_bros(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.fire_eggs(state) and self.ice_eggs(state) and \
                    self.claw_clamber_boots(state) and self.flight_pad(state) and self.third_person_egg_shooting(state)\
                    and (self.tall_jump(state) or self.talon_trot(state))\
                    and self.climb(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.fire_eggs(state) and self.ice_eggs(state) and \
                    self.claw_clamber_boots(state) and self.flight_pad(state) and self.third_person_egg_shooting(state)\
                    and (self.tall_jump(state) or self.talon_trot(state))\
                    and (self.climb(state)\
                        or self.flap_flip(state)\
                        or self.tall_jump(state) and self.grip_grab(state)\
                        or self.talon_trot(state) and self.grip_grab(state))
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            # In case people go for the damage boost for Chilly Willy then die before getting the jiggy, we also require Pack Whack to prevent softlocks.
            logic = self.fire_eggs(state) and self.ice_eggs(state) and self.flight_pad(state) and self.third_person_egg_shooting(state)\
                    and self.pack_whack(state)\
                    and (self.claw_clamber_boots(state)\
                        or ((self.tall_jump(state) and self.roll(state) or self.talon_trot(state))\
                            and (self.flutter(state) or self.air_rat_a_tat_rap(state))\
                            and self.grip_grab(state)
                        )
                    )\
                    and (self.tall_jump(state) or self.talon_trot(state))\
                    and (self.climb(state)\
                        or self.flap_flip(state)\
                        or self.tall_jump(state) and self.grip_grab(state)\
                        or self.talon_trot(state) and self.grip_grab(state)
                    )
        elif self.world.options.logic_type == LogicType.option_glitches:
            # In case people go for the damage boost for Chilly Willy then die before getting the jiggy, we also require Pack Whack to prevent softlocks.
            logic = self.fire_eggs(state) and self.ice_eggs(state) and self.flight_pad(state) and self.third_person_egg_shooting(state)\
                    and self.pack_whack(state)\
                    and (self.claw_clamber_boots(state)\
                        or ((self.tall_jump(state) and self.roll(state) or self.talon_trot(state))\
                            and (self.flutter(state) or self.air_rat_a_tat_rap(state))\
                            and self.grip_grab(state)
                        )
                    )\
                    and (self.tall_jump(state) or self.talon_trot(state))\
                    and (self.climb(state)\
                        or self.flap_flip(state)\
                        or self.tall_jump(state) and self.grip_grab(state)\
                        or self.talon_trot(state) and self.grip_grab(state)
                    )
        return logic

    def jiggy_volcano(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.long_jump(state) and self.hfp_top(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.long_jump(state) and self.hfp_top(state) or self.split_up(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.long_jump(state) and self.hfp_top(state) or self.split_up(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.long_jump(state) and self.hfp_top(state) or self.split_up(state)
        return logic

    def jiggy_sabreman(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.check_mumbo_magic(state, itemName.MUMBOHP) and self.fire_eggs(state) and \
                    self.taxi_pack(state) and self.tall_jump(state) and self.hfp_top(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.check_mumbo_magic(state, itemName.MUMBOHP) and self.has_fire(state) and \
                    self.taxi_pack(state) and self.tall_jump(state) and self.hfp_top(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.check_mumbo_magic(state, itemName.MUMBOHP) and self.has_fire(state) and \
                    self.taxi_pack(state) and self.tall_jump(state) and self.hfp_top(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.check_mumbo_magic(state, itemName.MUMBOHP) and self.has_fire(state) and \
                    self.taxi_pack(state) and self.tall_jump(state) and self.hfp_top(state)
        return logic

    def jiggy_boggy(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.hfp_top(state) and self.shack_pack(state) and self.small_elevation(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.hfp_top(state) and self.shack_pack(state) and self.small_elevation(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.hfp_top(state) and self.shack_pack(state) and self.small_elevation(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.hfp_top(state) and \
                    (self.shack_pack(state)\
                     or (self.clockwork_eggs(state) and self.third_person_egg_shooting(state) and (self.talon_trot(state) or self.flap_flip(state) or self.dive(state) and self.tall_jump(state)))\
                     or self.leg_spring(state))
        return logic

    def jiggy_ice_station(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.can_beat_king_coal(state) and self.grenade_eggs(state) and \
                    state.has(itemName.TRAINSWHP1, self.player) and state.has(itemName.TRAINSWHP2, self.player) and \
                    self.egg_aim(state) and state.can_reach_region(regionName.WW, self.player)\
                    and self.flight_pad(state) and self.climb(state) and self.beak_buster(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.can_beat_king_coal(state) and self.grenade_eggs(state) and \
                    state.has(itemName.TRAINSWHP1, self.player) and state.has(itemName.TRAINSWHP2, self.player) and \
                    state.can_reach_region(regionName.WW, self.player)\
                    and self.flight_pad(state) and self.climb(state) and self.beak_buster(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.can_beat_king_coal(state) and self.grenade_eggs(state) and \
                        state.has(itemName.TRAINSWHP1, self.player) and state.has(itemName.TRAINSWHP2, self.player) and state.can_reach_region(regionName.WW, self.player)\
                        and self.flight_pad(state) and self.beak_buster(state)\
                        and (self.climb(state) or self.clockwork_shot(state))
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.can_beat_king_coal(state) and self.grenade_eggs(state) and \
                        state.has(itemName.TRAINSWHP1, self.player) and state.has(itemName.TRAINSWHP2, self.player) and state.can_reach_region(regionName.WW, self.player)\
                        and self.flight_pad(state) and self.beak_buster(state)\
                        and (self.climb(state) or self.clockwork_shot(state))\
                    or (self.clockwork_shot(state) and self.small_elevation(state))
        return logic

    def jiggy_oil_drill(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.humbaHFP(state) and \
                    self.shack_pack(state) and self.grip_grab(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.humbaHFP(state) and self.shack_pack(state) and \
                    (self.pack_whack(state) and self.tall_jump(state) or self.grip_grab(state))
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.humbaHFP(state) and self.shack_pack(state) and \
                    (self.pack_whack(state) and self.tall_jump(state) or self.grip_grab(state))
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.humbaHFP(state) and self.shack_pack(state) and \
                    (self.pack_whack(state) or self.grip_grab(state))
        return logic

    def jiggy_hfp_stomping(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.snooze_pack(state) and self.tall_jump(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.snooze_pack(state) and self.tall_jump(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.tall_jump(state) and self.split_up(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.tall_jump(state) and self.split_up(state)\
                    or (state.can_reach_region(regionName.HP, self.player) and self.clockwork_shot(state)\
                        and (self.talon_trot(state)\
                            or self.split_up(state)\
                            or self.leg_spring(state)\
                            or self.flap_flip(state)))
        return logic

    def jiggy_hfp_kickball(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.humbaMT(state) and self.has_explosives(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.humbaMT(state) and \
                    (self.has_explosives(state) or \
                    self.check_mumbo_magic(state, itemName.MUMBOHP))
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.humbaMT(state) and \
                    (self.has_explosives(state) or self.check_mumbo_magic(state, itemName.MUMBOHP))
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.humbaMT(state) and \
                    (self.has_explosives(state) or self.check_mumbo_magic(state, itemName.MUMBOHP))
        return logic



    def jiggy_aliens(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.jiggy_ufo(state) and state.can_reach_region(regionName.JRU, self.player) and self.bill_drill(state) and \
                    self.hatch(state) and self.glide(state) and \
                    self.check_mumbo_magic(state, itemName.MUMBOHP)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.jiggy_ufo(state) and state.can_reach_region(regionName.JRU, self.player) and self.check_mumbo_magic(state, itemName.MUMBOHP) and \
                    self.bill_drill(state) and self.hatch(state) and \
                    ((self.wing_whack(state) and self.tall_jump(state)) or self.glide(state))
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.jiggy_ufo(state) and state.can_reach_region(regionName.JRU, self.player) and self.check_mumbo_magic(state, itemName.MUMBOHP) and \
                    self.bill_drill(state) and self.hatch(state) and \
                    (self.wing_whack(state) or self.tall_jump(state) or self.glide(state))
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.jiggy_ufo(state) and state.can_reach_region(regionName.JRU, self.player) and self.check_mumbo_magic(state, itemName.MUMBOHP) and \
                    self.bill_drill(state) and self.hatch(state) and \
                    (self.wing_whack(state) or self.tall_jump(state) or self.glide(state))
        return logic

    def jiggy_colosseum_split(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.split_up(state) and self.grip_grab(state) and self.climb(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.split_up(state) and self.grip_grab(state)\
                and (self.climb(state) or (self.pack_whack(state) and self.tall_jump(state)))
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.split_up(state) and self.grip_grab(state)\
                and (self.climb(state) or (self.pack_whack(state) and self.tall_jump(state)))
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = (self.split_up(state) and self.grip_grab(state)\
                and (self.climb(state) or (self.pack_whack(state) and self.tall_jump(state))))\
                    or (self.clockwork_eggs(state) and (self.split_up(state) and self.third_person_egg_shooting(state)))
        return logic

    def jiggy_mingy(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = (self.can_shoot_linear_egg(state) or self.beak_barge(state) or self.air_rat_a_tat_rap(state) or self.wonderwing(state))\
                    and self.talon_trot(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.can_shoot_linear_egg(state) or self.beak_barge(state) or self.air_rat_a_tat_rap(state) or self.wonderwing(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.ground_attack(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.ground_attack(state)
        return logic

    def jiggy_mr_fit(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.springy_step_shoes(state) and self.sack_pack(state) and \
                    self.grow_beanstalk(state) and self.can_use_floatus(state) and self.climb(state)\
                    and self.turbo_trainers(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = (self.springy_step_shoes(state) or self.flight_pad(state)) and self.sack_pack(state) and \
                    self.grow_beanstalk(state) and self.can_use_floatus(state) and self.climb(state)\
                    and (self.turbo_trainers(state) or state.has(itemName.HUMBACC, self.player))
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = (self.springy_step_shoes(state) or self.flight_pad(state) or self.clockwork_shot(state)) and self.sack_pack(state) and \
                    self.grow_beanstalk(state) and \
                    (self.can_use_floatus(state) or self.pack_whack(state))\
                    and self.climb(state)\
                    and (self.turbo_trainers(state) or state.has(itemName.HUMBACC, self.player))
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = (self.springy_step_shoes(state) or self.flight_pad(state) or self.clockwork_shot(state)) and self.sack_pack(state) and \
                    self.grow_beanstalk(state) and \
                    (self.can_use_floatus(state) or self.pack_whack(state))\
                    and self.climb(state)\
                    and (self.turbo_trainers(state) or state.has(itemName.HUMBACC, self.player) or self.clockwork_eggs(state))
        return logic

    def jiggy_pot_of_gold(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.blue_eggs(state) and self.fire_eggs(state) and self.grenade_eggs(state) and self.ice_eggs(state)\
                    and self.mumboCCL(state) and (self.flap_flip(state) or self.leg_spring(state))
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.blue_eggs(state) and self.fire_eggs(state) and self.grenade_eggs(state) and self.ice_eggs(state) and self.mumboCCL(state)\
                    and (self.flap_flip(state) or self.leg_spring(state) or self.flight_pad(state))
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.blue_eggs(state) and self.fire_eggs(state) and self.grenade_eggs(state) and self.ice_eggs(state)\
                        and (self.mumboCCL(state) and (self.flap_flip(state) or self.leg_spring(state) or self.flight_pad(state))\
                    or (self.leg_spring(state) or (self.split_up(state) and self.tall_jump(state)))\
                        and (self.flight_pad(state) and self.beak_bomb(state) or self.glide(state)))
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.blue_eggs(state) and self.fire_eggs(state) and self.grenade_eggs(state) and self.ice_eggs(state)\
                        and (self.mumboCCL(state) and (self.flap_flip(state) or self.leg_spring(state) or self.flight_pad(state))\
                    or (self.leg_spring(state) or (self.split_up(state) and self.tall_jump(state)))\
                        and (self.flight_pad(state) and self.beak_bomb(state) or self.glide(state)))
        return logic

    def jiggy_cheese(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.sack_pack(state) and self.grow_beanstalk(state) and \
                    self.can_use_floatus(state) and self.shack_pack(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.sack_pack(state) and self.grow_beanstalk(state) and \
                    self.can_use_floatus(state) and self.shack_pack(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.sack_pack(state) and self.grow_beanstalk(state) and \
                    self.can_use_floatus(state) and self.shack_pack(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.sack_pack(state) and self.grow_beanstalk(state) and \
                        self.can_use_floatus(state) and self.shack_pack(state)\
                    or (self.talon_trot(state) or self.clockwork_warp(state)) and self.flap_flip(state) and self.beak_buster(state) and self.flight_pad(state)\
                    or self.flight_pad(state) and (self.leg_spring(state) or (self.tall_jump(state) and self.wing_whack(state))) and self.clockwork_warp(state)
        return logic

    def jiggy_trash_can(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.wing_whack(state) and self.flight_pad(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.split_up(state)\
                    and (self.flight_pad(state) or self.glide(state))\
                    and (self.wing_whack(state) or self.blue_eggs(state) or self.fire_eggs(state) or self.ice_eggs(state))
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.split_up(state)\
                    and (self.flight_pad(state) or self.glide(state) or ((self.tall_jump(state) or self.leg_spring(state)) and self.wing_whack(state)))\
                    and (self.wing_whack(state) or self.blue_eggs(state) or self.fire_eggs(state) or self.ice_eggs(state))
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.split_up(state)\
                    and (self.flight_pad(state) or self.glide(state) or ((self.tall_jump(state) or self.leg_spring(state)) and self.wing_whack(state)))\
                    and (self.wing_whack(state) or self.blue_eggs(state) or self.fire_eggs(state) or self.ice_eggs(state))
        return logic

    def jiggy_superstash(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.clockwork_eggs(state) and self.grip_grab(state) and self.flight_pad(state) and self.flap_flip(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.clockwork_eggs(state) and self.flight_pad(state) and self.flap_flip(state)\
                     and (self.grip_grab(state) or self.veryLongJump(state) and self.climb(state))
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.clockwork_eggs(state) and self.flight_pad(state) and self.flap_flip(state)\
                     and (self.grip_grab(state) or self.veryLongJump(state) and self.climb(state))
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.clockwork_eggs(state)
        return logic

    def honeycomb_mt_entrance(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.humbaMT(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.humbaMT(state) or \
                    self.clockwork_eggs(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.humbaMT(state) or \
                    self.clockwork_eggs(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.humbaMT(state)\
                    or self.clockwork_eggs(state)\
                    or self.breegull_bash(state)

        return logic

    def honeycomb_bovina(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.grip_grab(state) and self.flap_flip(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = (self.flap_flip(state) and (self.grip_grab(state) or self.beak_buster(state)))\
                    or self.MT_flight_pad(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = (self.flap_flip(state) and (self.grip_grab(state) or self.beak_buster(state)))\
                    or self.MT_flight_pad(state) or self.clockwork_shot(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = (self.flap_flip(state) and (self.grip_grab(state) or self.beak_buster(state)))\
                    or self.MT_flight_pad(state) or self.clockwork_shot(state)
        return logic

    def honeycomb_treasure_chamber(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.can_shoot_any_egg(state) and self.egg_aim(state) and self.talon_trot(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = (self.MT_flight_pad(state) and self.can_shoot_any_egg(state) and (self.grip_grab(state) or self.talon_trot(state)))\
                    or (self.can_shoot_any_egg(state) and self.egg_aim(state) and self.talon_trot(state))
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = (self.MT_flight_pad(state) and self.can_shoot_any_egg(state) and (self.grip_grab(state) or self.clockwork_shot(state) or self.talon_trot(state)))\
                    or (self.can_shoot_any_egg(state) and self.egg_aim(state) and (self.talon_trot(state) or self.clockwork_shot(state)))
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = (self.MT_flight_pad(state) and self.can_shoot_any_egg(state) and (self.grip_grab(state) or self.clockwork_shot(state) or self.talon_trot(state)))\
                    or (self.can_shoot_any_egg(state) and self.egg_aim(state) and (self.talon_trot(state) or self.clockwork_shot(state)))
        return logic


    def honeycomb_prospector(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = (self.flap_flip(state) or self.ggm_trot(state) or self.slightly_elevated_ledge(state)) and self.bill_drill(state)\
                     or self.humbaGGM(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.bill_drill(state) or self.humbaGGM(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.bill_drill(state) or self.humbaGGM(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.bill_drill(state) or self.humbaGGM(state) or self.ground_rat_a_tat_rap(state)
        return logic

    def honeycomb_gm_station(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.ground_attack(state) or self.humbaGGM(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.ground_attack(state) or self.humbaGGM(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.ground_attack(state) or self.humbaGGM(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.ground_attack(state) or self.humbaGGM(state)
        return logic

    def honeycomb_space_zone(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.grip_grab(state) and self.climb(state) and self.flap_flip(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.grip_grab(state) and self.climb(state) and self.flap_flip(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = (self.grip_grab(state) or self.beak_buster(state)) and self.climb(state)\
                        and self.flap_flip(state) and (self.clockwork_shot(state) or self.longJumpToGripGrab(state))\
                    or self.leg_spring(state) and self.glide(state)\
                    or self.clockwork_shot(state) and (self.talon_trot(state) or self.split_up(state))
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = (self.grip_grab(state) or self.beak_buster(state)) and self.climb(state)\
                        and self.flap_flip(state) and (self.clockwork_shot(state) or self.longJumpToGripGrab(state))\
                    or self.clockwork_shot(state) and state.can_reach_region(regionName.GMFD, self.player) and self.ggm_to_ww(state)\
                    or self.leg_spring(state) and self.glide(state)\
                    or self.clockwork_shot(state) and (self.talon_trot(state) or self.split_up(state))
        return logic

    def honeycomb_crazy_castle(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.has_explosives(state) and (self.small_elevation(state) or self.split_up(state))
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.has_explosives(state) and (self.small_elevation(state) or self.split_up(state))
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = (self.has_explosives(state) and (self.small_elevation(state) or self.split_up(state))) or self.clockwork_shot(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = (self.has_explosives(state) and (self.small_elevation(state) or self.split_up(state)))\
                    or self.clockwork_shot(state)\
                    or self.pack_whack(state)
        return logic

    def honeycomb_inferno(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.humbaWW(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.humbaWW(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.humbaWW(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.glitchedInfernoAccess(state)
        return logic

    def honeycomb_seemee(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = state.can_reach_region(regionName.JRLC, self.player) and self.talon_torpedo(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.talon_torpedo(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.talon_torpedo(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.talon_torpedo(state)
        return logic

    def honeycomb_atlantis(self, state: CollectionState) -> bool:
        return True

    def honeycomb_jrl_pipes(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = (self.has_explosives(state) or  self.bill_drill(state)) and \
                    self.grip_grab(state) and self.spring_pad(state) and self.talon_trot(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = ((self.has_explosives(state) or self.bill_drill(state))\
                        and self.grip_grab(state) and self.spring_pad(state) and self.talon_trot(state))\
                    or (self.has_explosives(state) and self.spring_pad(state)\
                        and (self.glide(state) or self.leg_spring(state)))
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = ((self.has_explosives(state) or self.bill_drill(state))\
                        and self.grip_grab(state) and self.spring_pad(state) and self.talon_trot(state))\
                    or (self.has_explosives(state) and self.spring_pad(state)\
                        and (self.glide(state) or self.leg_spring(state)))\
                    or self.clockwork_shot(state) and (self.veryLongJump(state) or self.has_explosives(state) and self.split_up(state))
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = ((self.has_explosives(state) or self.bill_drill(state))\
                        and self.grip_grab(state) and self.spring_pad(state) and self.talon_trot(state))\
                    or (self.has_explosives(state) and self.spring_pad(state)\
                        and (self.glide(state) or self.leg_spring(state)))\
                    or self.clockwork_shot(state) and (self.veryLongJump(state) or self.has_explosives(state) and self.split_up(state))
        return logic

    def honeycomb_lakeside(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.turbo_trainers(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.turbo_trainers(state) or self.TDL_flight_pad(state)\
                or (self.tall_jump(state) and self.veryLongJump(state) and self.grip_grab(state))\
                or self.split_up(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.turbo_trainers(state) or self.TDL_flight_pad(state) or self.clockwork_shot(state)\
                or (self.tall_jump(state) and self.veryLongJump(state) and self.grip_grab(state))\
                or self.split_up(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.turbo_trainers(state) or self.TDL_flight_pad(state) or self.clockwork_shot(state)\
                or (self.tall_jump(state) and self.veryLongJump(state) and self.grip_grab(state))\
                or self.split_up(state)
        return logic

    def honeycomb_styracosaurus(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.bill_drill(state) and self.split_up(state) and self.spring_pad(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.bill_drill(state) and self.split_up(state) and self.spring_pad(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = (self.bill_drill(state) and self.split_up(state) and self.spring_pad(state)) or \
                    (self.leg_spring(state) and self.wing_whack(state) and self.glide(state))\
                    or self.clockwork_shot(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = (self.bill_drill(state) and self.split_up(state) and self.spring_pad(state)) or \
                    (self.leg_spring(state) and self.wing_whack(state) and self.glide(state))\
                    or self.clockwork_shot(state)
        return logic

    def honeycomb_river(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.talon_trot(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.talon_trot(state) or self.split_up(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.talon_trot(state) or self.clockwork_shot(state) or self.humbaTDL(state) or self.split_up(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.talon_trot(state) or self.clockwork_shot(state) or self.humbaTDL(state) or self.split_up(state)
        return logic

    def honeycomb_floor3(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic =  (self.grip_grab(state) and self.flap_flip(state) or self.split_up(state)) and self.spring_pad(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = (self.grip_grab(state) and self.flap_flip(state) or self.split_up(state)) and self.spring_pad(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = ((self.grip_grab(state) and self.flap_flip(state) or self.split_up(state)) and self.spring_pad(state))\
                    or self.clockwork_shot(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = ((self.grip_grab(state) and self.flap_flip(state) or self.split_up(state)) and self.spring_pad(state))\
                    or self.clockwork_shot(state)
        return logic

    def honeycomb_gi_station(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.grip_grab(state) and self.ground_attack(state) and self.spring_pad(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.ground_attack(state) and self.spring_pad(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = (self.ground_attack(state) and self.spring_pad(state)) or self.clockwork_shot(state) or self.leg_spring(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = (self.ground_attack(state) and self.spring_pad(state)) or self.clockwork_shot(state) or self.leg_spring(state)
        return logic

    def honeycomb_volcano(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.hfp_top(state) and self.grenade_eggs(state) and self.egg_aim(state) and self.spring_pad(state) and (self.talon_trot(state) or self.split_up(state))
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.split_up(state) and (self.tall_jump(state) or self.wing_whack(state) or self.glide(state) or self.leg_spring(state))\
                    or self.hfp_top(state) and self.grenade_eggs(state) and self.egg_aim(state) and self.spring_pad(state) and self.talon_trot(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.split_up(state) and (self.tall_jump(state) or self.wing_whack(state) or self.glide(state) or self.leg_spring(state))\
                    or self.hfp_top(state) and self.grenade_eggs(state) and self.egg_aim(state) and self.spring_pad(state) and self.talon_trot(state)\
                    or self.extremelyLongJump(state)\
                    or self.hfp_top(state) and self.clockwork_shot(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.split_up(state) and (self.tall_jump(state) or self.wing_whack(state) or self.glide(state) or self.leg_spring(state))\
                    or self.hfp_top(state) and self.grenade_eggs(state) and self.egg_aim(state) and self.spring_pad(state) and self.talon_trot(state)\
                    or self.extremelyLongJump(state) \
                    or self.hfp_top(state) and self.clockwork_shot(state)
        return logic

    def honeycomb_hfp_station(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.grip_grab(state) and\
                  (self.talon_trot(state) or self.tall_jump(state)) and\
                  (self.flutter(state) or self.air_rat_a_tat_rap(state))
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = (self.grip_grab(state) and\
                  (self.talon_trot(state) or self.tall_jump(state)) and\
                  (self.flutter(state) or self.air_rat_a_tat_rap(state)))\
                    or self.leg_spring(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = (self.grip_grab(state) and\
                  (self.talon_trot(state) or self.tall_jump(state)) and\
                  (self.flutter(state) or self.air_rat_a_tat_rap(state)))\
                    or self.leg_spring(state)\
                     or self.clockwork_shot(state) and self.hfp_top(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = (self.grip_grab(state) and\
                  (self.talon_trot(state) or self.tall_jump(state)) and\
                  (self.flutter(state) or self.air_rat_a_tat_rap(state)))\
                    or self.leg_spring(state)\
                     or self.clockwork_shot(state) and self.hfp_top(state)
        return logic

    def honeycomb_lava_side(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.grip_grab(state) and self.flap_flip(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.grip_grab(state) and self.flap_flip(state) or self.flight_pad(state)\
                    or self.leg_spring(state) and (self.wing_whack(state) or self.glide(state))
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.grip_grab(state) and self.flap_flip(state)\
                    or self.flight_pad(state)\
                    or self.leg_spring(state) and (self.wing_whack(state) or self.glide(state))\
                    or self.hfp_top(state) and self.clockwork_shot(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.grip_grab(state) and self.flap_flip(state) or self.flight_pad(state)\
                    or self.leg_spring(state) and (self.wing_whack(state) or self.glide(state))\
                    or self.hfp_top(state) and self.clockwork_shot(state)
        return logic

    def honeycomb_trash(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.flight_pad(state) or state.has(itemName.HUMBACC, self.player)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.flight_pad(state) or self.glide(state) or state.has(itemName.HUMBACC, self.player)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.flight_pad(state) or self.glide(state) or state.has(itemName.HUMBACC, self.player)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.flight_pad(state) or self.glide(state) or state.has(itemName.HUMBACC, self.player)
        return logic

    def honeycomb_pot(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.flight_pad(state) or state.has(itemName.HUMBACC, self.player)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = (self.flight_pad(state) or self.wing_whack(state) or self.glide(state)) or state.has(itemName.HUMBACC, self.player)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = (self.flight_pad(state) or self.wing_whack(state) or self.glide(state)) or state.has(itemName.HUMBACC, self.player)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = (self.flight_pad(state) or self.wing_whack(state) or self.glide(state)) or state.has(itemName.HUMBACC, self.player)
        return logic

    def plateau_top(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.talon_trot(state) or self.split_up(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.talon_trot(state) or self.split_up(state) or (state.can_reach_region(regionName.IOHCT, self.player) and self.claw_clamber_boots(state))
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.talon_trot(state) or self.split_up(state)\
                    or self.clockwork_shot(state)\
                    or (state.can_reach_region(regionName.IOHCT, self.player) and self.claw_clamber_boots(state))
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.talon_trot(state) or self.split_up(state)\
                    or self.clockwork_shot(state)\
                    or (state.can_reach_region(regionName.IOHCT, self.player) and self.claw_clamber_boots(state))
        return logic

    def cheato_snakehead(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.egg_aim(state) and self.grip_grab(state) and self.spring_pad(state) and self.flap_flip(state) and self.talon_trot(state)\
                        or self.MT_flight_pad(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.grip_grab(state) and self.spring_pad(state) and self.flap_flip(state) and self.can_shoot_any_egg(state) and self.egg_aim(state) and self.talon_trot(state)\
                        or self.MT_flight_pad(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = (self.grip_grab(state) and self.spring_pad(state) and self.flap_flip(state) and self.can_shoot_any_egg(state) and self.egg_aim(state) and self.talon_trot(state))\
                        or self.MT_flight_pad(state)\
                        or self.clockwork_shot(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = ((self.grip_grab(state) and self.spring_pad(state) and self.flap_flip(state) and self.can_shoot_any_egg(state) and self.egg_aim(state) and self.talon_trot(state))\
                        or (self.MT_flight_pad(state)))\
                        or self.clockwork_shot(state)
        return logic

    def cheato_prison(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.prison_compound_as_banjo(state) and self.slightly_elevated_ledge(state) and self.tall_jump(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.prison_compound_as_banjo(state) and self.slightly_elevated_ledge(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.prison_compound_as_banjo(state) and (self.slightly_elevated_ledge(state) or self.clockwork_shot(state))
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.prison_compound_as_banjo(state) and (self.slightly_elevated_ledge(state) or self.clockwork_shot(state))
        return logic

    def cheato_jade_snake_grove(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.grip_grab(state)\
                        and self.talon_trot(state) and self.flap_flip(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.grip_grab(state)\
                        and self.talon_trot(state) and self.flap_flip(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.talon_trot(state) and self.flap_flip(state) and self.grip_grab(state)\
                        or self.egg_aim(state) and self.clockwork_eggs(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.talon_trot(state) and self.flap_flip(state) and self.grip_grab(state)\
                        or self.egg_aim(state) and self.clockwork_eggs(state)
        return logic

    def cheato_gm_entrance(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.springy_step_shoes(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.springy_step_shoes(state) or \
                    (self.climb(state) and (self.flutter(state) or (self.air_rat_a_tat_rap(state) and self.tall_jump(state))))\
                    or (self.GM_boulders(state) and self.leg_spring(state))\
                    or (self.GM_boulders(state) and self.glide(state) and self.tall_jump(state))
                    # or state.can_reach_region(regionName.IOHPL, self.player) and self.PL_to_GGM(state) and self.flutter(state) and (self.grip_grab(state) or self.beak_buster(state)) # Flutter right as you enter the level.
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.springy_step_shoes(state) or \
                    (self.climb(state) and (self.flutter(state) or self.air_rat_a_tat_rap(state)))\
                    or (self.clockwork_shot(state))\
                    or (self.GM_boulders(state) and self.leg_spring(state))\
                    or (self.GM_boulders(state) and self.glide(state) and self.tall_jump(state))\
                    or (self.GM_boulders(state) and self.tall_jump(state) and self.turbo_trainers(state) and (self.wing_whack(state) or self.glide(state)))
                    # or state.can_reach_region(regionName.IOHPL, self.player) and self.PL_to_GGM(state) and self.flutter(state) and (self.grip_grab(state) or self.beak_buster(state))
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.springy_step_shoes(state) or \
                    (self.climb(state) and (self.flutter(state) or self.air_rat_a_tat_rap(state)))\
                    or (self.clockwork_shot(state))\
                    or (self.GM_boulders(state) and self.leg_spring(state))\
                    or (self.GM_boulders(state) and self.glide(state) and self.tall_jump(state))\
                    or (self.GM_boulders(state) and self.tall_jump(state) and self.turbo_trainers(state) and (self.wing_whack(state) or self.glide(state)))
                    # or state.can_reach_region(regionName.IOHPL, self.player) and self.PL_to_GGM(state) and self.flutter(state) and (self.grip_grab(state) or self.beak_buster(state))
        return logic

    def cheato_water_storage(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.grip_grab(state) and self.flap_flip(state) and self.dive(state) and self.climb(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = (self.grip_grab(state) or self.beak_buster(state)) and self.flap_flip(state) and self.dive(state) and self.climb(state)\
                    or self.GM_boulders(state) and self.pack_whack(state) and self.tall_jump(state) and self.dive(state) and self.climb(state) and self.grip_grab(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = (self.grip_grab(state) or self.beak_buster(state)) and self.flap_flip(state) and self.dive(state) and self.climb(state)\
                    or self.GM_boulders(state) and self.pack_whack(state) and self.tall_jump(state) and self.dive(state) and self.climb(state) and self.grip_grab(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = (self.grip_grab(state) or self.beak_buster(state)) and self.flap_flip(state) and self.dive(state) and self.climb(state)\
                    or self.leg_spring(state) and self.glide(state) and self.GM_boulders(state)\
                    or self.GM_boulders(state) and self.pack_whack(state) and self.tall_jump(state) and self.dive(state) and self.climb(state) and self.grip_grab(state)
        return logic

    def cheato_haunted_cavern(self, state: CollectionState) -> bool:
        logic = True
        # You can damage boost from the torch at the end of the path to grip grab the ledge.
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.slightly_elevated_ledge(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.grip_grab(state) or (self.leg_spring(state) and \
                    (self.wing_whack(state) or self.glide(state)))
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.grip_grab(state) or (self.leg_spring(state) and \
                    (self.wing_whack(state) or self.glide(state)))\
                    or self.clockwork_shot(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.grip_grab(state) or (self.leg_spring(state) and \
                    (self.wing_whack(state) or self.glide(state)))\
                    or self.clockwork_shot(state)
        return logic

    def cheato_inferno(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.humbaWW(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.humbaWW(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.humbaWW(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.glitchedInfernoAccess(state)
        return logic

    def cheato_saucer_of_peril(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.jiggy_peril(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.jiggy_peril(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.jiggy_peril(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.jiggy_peril(state)
        return logic

    def cheato_pawno(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = state.has(itemName.DOUBLOON, self.player, 28) and self.small_elevation(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = state.has(itemName.DOUBLOON, self.player, 28) and self.small_elevation(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = state.has(itemName.DOUBLOON, self.player, 28) and (self.small_elevation(state) or self.clockwork_shot(state))
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = state.has(itemName.DOUBLOON, self.player, 28) and (self.small_elevation(state) or self.clockwork_shot(state))
        return logic

    def cheato_seemee(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.talon_torpedo(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.talon_torpedo(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.talon_torpedo(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.talon_torpedo(state)
        return logic

    def cheato_ancient_swimming_baths(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.talon_torpedo(state) and \
                    self.glide(state) and self.tall_jump(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.talon_torpedo(state) and \
                    ((self.glide(state) and self.tall_jump(state)) or self.leg_spring(state) or
                    (self.pack_whack(state) and self.grip_grab(state)))
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.talon_torpedo(state) and ((self.glide(state) and self.tall_jump(state)) or self.leg_spring(state) or
                    self.wing_whack(state) or
                    (self.pack_whack(state) and self.grip_grab(state)))
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.talon_torpedo(state) and ((self.glide(state) and self.tall_jump(state)) or self.leg_spring(state) or
                    (self.check_solo_moves(state, itemName.WWING) and self.tall_jump(state)) or
                    (self.tall_jump(state) and self.pack_whack(state) and self.grip_grab(state)))
        return logic

    def cheato_trex(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.humbaTDL(state) and self.roar(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.humbaTDL(state) and self.roar(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.humbaTDL(state) and self.roar(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.humbaTDL(state) and self.roar(state) or self.clockwork_eggs(state)
        return logic

    def cheato_dippy_pool(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = state.can_reach_region(regionName.CC, self.player) and self.jiggy_dippy(state) and self.dive(state)\
                and ((self.small_elevation(state) and self.springy_step_shoes(state)) or self.TDL_flight_pad(state))
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = state.can_reach_region(regionName.CC, self.player) and self.jiggy_dippy(state) and self.dive(state)\
                and ((self.small_elevation(state) and self.springy_step_shoes(state)) or self.TDL_flight_pad(state))
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = state.can_reach_region(regionName.CC, self.player) and self.jiggy_dippy(state) and self.dive(state)\
                and ((self.small_elevation(state) and self.springy_step_shoes(state)) or self.TDL_flight_pad(state))
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = state.can_reach_region(regionName.CC, self.player) and self.jiggy_dippy(state) and self.dive(state)\
                and ((self.small_elevation(state) and self.springy_step_shoes(state)) or self.TDL_flight_pad(state))
        return logic

    def cheato_tdlboulder(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.bill_drill(state) and self.flap_flip(state) and self.grip_grab(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.bill_drill(state)\
                        and (self.TDL_flight_pad(state)\
                             or self.grip_grab(state) and (self.flap_flip(state) or (self.talon_trot(state) and self.flutter(state))))
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.bill_drill(state)\
                        and (self.TDL_flight_pad(state)\
                             or self.grip_grab(state) and (self.flap_flip(state) or (self.talon_trot(state) and self.flutter(state)))\
                             or state.can_reach_region(regionName.TLTOP, self.player) and self.talon_trot(state) and (self.flutter(state) or self.air_rat_a_tat_rap(state))
                        )
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = (self.bill_drill(state) or self.egg_barge(state))\
                        and (self.TDL_flight_pad(state)\
                             or self.grip_grab(state) and (self.flap_flip(state) or (self.talon_trot(state) and self.flutter(state)))\
                             or state.can_reach_region(regionName.TLTOP, self.player) and self.talon_trot(state) and (self.flutter(state) or self.air_rat_a_tat_rap(state))
                        )
        return logic

    def cheato_loggo(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.has_explosives(state) and self.bill_drill(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.has_explosives(state) and\
                        (self.grenade_eggs(state)\
                         or self.bill_drill(state)\
                         or self.breegull_bash(state)\
                         or self.beak_barge(state)\
                         or self.pack_whack(state))
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.has_explosives(state) and\
                        (self.grenade_eggs(state)\
                         or self.bill_drill(state)\
                         or self.breegull_bash(state)\
                         or self.beak_barge(state)\
                         or self.pack_whack(state))
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.has_explosives(state) and\
                        (self.grenade_eggs(state)\
                         or self.bill_drill(state)\
                         or self.breegull_bash(state)\
                         or self.beak_barge(state)\
                         or self.pack_whack(state))
        return logic

    def cheato_window(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = state.can_reach_region(regionName.GIF, self.player) and (self.egg_aim(state) or self.airborne_egg_aiming(state) or self.beak_bomb(state))
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = state.can_reach_region(regionName.GIF, self.player) and (self.egg_aim(state) or self.airborne_egg_aiming(state) or self.beak_bomb(state))\
                    or state.can_reach_region(regionName.GI1, self.player) and self.leg_spring(state) and self.claw_clamber_boots(state) and self.wing_whack(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = state.can_reach_region(regionName.GIF, self.player) and (self.egg_aim(state) or self.airborne_egg_aiming(state) or self.beak_bomb(state))\
                    or state.can_reach_region(regionName.GI1, self.player) and self.leg_spring(state) and self.claw_clamber_boots(state) and self.wing_whack(state)\
                    or self.clockwork_shot(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = state.can_reach_region(regionName.GIF, self.player) and (self.egg_aim(state) or self.airborne_egg_aiming(state) or self.beak_bomb(state))\
                    or state.can_reach_region(regionName.GI1, self.player) and self.leg_spring(state) and self.claw_clamber_boots(state) and self.wing_whack(state)\
                    or state.can_reach_region(regionName.GI2, self.player) and self.clockwork_shot(state) and self.solo_kazooie_gi(state)\
                    or self.clockwork_shot(state)
        return logic

    def cheato_colosseum(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.long_jump(state) and self.claw_clamber_boots(state) and (self.has_explosives(state) or self.dragon_kazooie(state))
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.long_jump(state) and  self.claw_clamber_boots(state) and (
                        self.has_explosives(state)\
                        or self.check_mumbo_magic(state, itemName.MUMBOHP)\
                        or self.dragon_kazooie(state)
                    )
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.claw_clamber_boots(state) and \
                    (self.has_explosives(state) or
                    self.check_mumbo_magic(state, itemName.MUMBOHP)\
                    or self.dragon_kazooie(state))
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = (self.claw_clamber_boots(state) and \
                        (self.has_explosives(state) or
                        self.check_mumbo_magic(state, itemName.MUMBOHP)\
                        or self.dragon_kazooie(state)))\
                    or self.hfp_top(state) and self.third_person_egg_shooting(state)
        return logic

    def cheato_icicle_grotto(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.climb(state) and (self.clockwork_eggs(state) or self.shack_pack(state))
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.climb(state) and self.shack_pack(state)\
                    or ((self.leg_spring(state) or self.climb(state)) and self.clockwork_eggs(state))
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.hfp_top(state) and\
                    (self.climb(state) and self.shack_pack(state)\
                    or ((self.leg_spring(state) or self.climb(state)) and self.clockwork_eggs(state)))
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.hfp_top(state) and\
                    (self.climb(state) and self.shack_pack(state)\
                    or ((self.leg_spring(state) or self.climb(state)) and self.clockwork_eggs(state)))\
                    or ((self.talon_trot(state) or self.split_up(state)) and self.clockwork_shot(state))
        return logic

    def cheato_icy_pillar(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.hfp_top(state) and self.grenade_eggs(state) and self.egg_aim(state) and self.spring_pad(state) and self.split_up(state) and self.glide(state)\
                    or self.leg_spring(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.split_up(state) and (self.tall_jump(state) or self.wing_whack(state) or self.glide(state))\
                    or self.leg_spring(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = ((self.split_up(state) and (self.tall_jump(state) or self.wing_whack(state) or self.glide(state))))\
                    or self.leg_spring(state)\
                    or (self.grenade_eggs(state) and self.clockwork_shot(state) and self.small_elevation(state) and self.spring_pad(state) and self.talon_trot(state))
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = ((self.split_up(state) and (self.tall_jump(state) or self.wing_whack(state) or self.glide(state))))\
                    or self.leg_spring(state)\
                    or (self.grenade_eggs(state) and self.clockwork_shot(state) and self.small_elevation(state) and self.spring_pad(state) and self.talon_trot(state))
        return logic

    def cheato_potgold(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.jiggy_pot_of_gold(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.jiggy_pot_of_gold(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.jiggy_pot_of_gold(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.jiggy_pot_of_gold(state)
        return logic

    def cheato_spiral(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.spring_pad(state) or self.flight_pad(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.spring_pad(state) or self.flight_pad(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.spring_pad(state) or self.flight_pad(state) or\
                self.clockwork_shot(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.spring_pad(state) or self.flight_pad(state) or\
                self.clockwork_shot(state)
        return logic

    def glowbo_entrance_ggm(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.GGM_slope(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.GGM_slope(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = True
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = True
        return logic

    def glowbo_inferno(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.humbaWW(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.humbaWW(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.humbaWW(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.glitchedInfernoAccess(state)
        return logic

    def glowbo_wigwam(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.flap_flip(state) and self.grip_grab(state)\
                    or self.warp_to_ww_wumba(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = (self.flap_flip(state) and self.grip_grab(state)) \
                    or (self.climb(state) and self.veryLongJump(state))\
                    or self.leg_spring(state)\
                    or self.warp_to_ww_wumba(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = (self.flap_flip(state) and self.grip_grab(state)) \
                    or (self.climb(state) and self.veryLongJump(state) and self.flap_flip(state))\
                    or (self.clockwork_shot(state) and self.climb(state))\
                    or self.leg_spring(state)\
                    or self.warp_to_ww_wumba(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = (self.flap_flip(state) and self.grip_grab(state)) \
                    or (self.climb(state) and self.veryLongJump(state) and self.flap_flip(state))\
                    or (self.clockwork_shot(state) and self.climb(state)\
                    or self.leg_spring(state))\
                    or self.warp_to_ww_wumba(state)
        return logic

    def glowbo_underwigwam(self, state: CollectionState) -> bool:
        return True

    def glowbo_tdl(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = (self.small_elevation(state) or self.TDL_flight_pad(state))
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.small_elevation(state)\
                    or self.TDL_flight_pad(state)\
                    or self.humbaTDL(state)\
                    or self.springy_step_shoes(state)\
                    or self.turbo_trainers(state)\
                    or self.beak_buster(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.small_elevation(state)\
                    or self.TDL_flight_pad(state)\
                    or self.humbaTDL(state)\
                    or self.springy_step_shoes(state)\
                    or self.turbo_trainers(state)\
                    or self.clockwork_shot(state)\
                    or self.beak_buster(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.small_elevation(state)\
                    or self.TDL_flight_pad(state)\
                    or self.humbaTDL(state)\
                    or self.springy_step_shoes(state)\
                    or self.turbo_trainers(state)\
                    or self.clockwork_shot(state)\
                    or self.beak_buster(state)
        return logic

    def glowbo_tdl_mumbo(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.stilt_stride(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = True
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = True
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = True
        return logic

    def glowbo_floor_3(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.slightly_elevated_ledge(state) or self.small_elevation(state) and self.leg_spring(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.slightly_elevated_ledge(state) or self.small_elevation(state) and self.leg_spring(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.slightly_elevated_ledge(state) or self.clockwork_shot(state) or self.small_elevation(state) and self.leg_spring(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.slightly_elevated_ledge(state) or self.clockwork_shot(state) or self.small_elevation(state) and self.leg_spring(state)
        return logic

    def pawno_shelves(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.small_elevation(state) or self.grip_grab(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = (self.small_elevation(state) or self.grip_grab(state))
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.small_elevation(state) or self.grip_grab(state) or self.clockwork_shot(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.small_elevation(state) or self.grip_grab(state) or self.clockwork_shot(state)
        return logic

    def glowbo_cavern(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.small_elevation(state) and self.dive(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.dive(state) or self.shack_pack(state) and self.tall_jump(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.dive(state) or self.shack_pack(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.dive(state) or self.shack_pack(state)
        return logic

    def glowbo_cliff(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.climb(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.climb(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.climb(state) or (self.clockwork_shot(state) and state.can_reach_region(regionName.IOHCT, self.player))
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.climb(state) or (self.clockwork_shot(state) and state.can_reach_region(regionName.IOHCT, self.player))
        return logic

    def mega_glowbo(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.talon_torpedo(state) and state.has(itemName.IKEY, self.player)\
                    and self.dive(state) and self.tall_jump(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.talon_torpedo(state) and state.has(itemName.IKEY, self.player)\
                    and self.dive(state) and\
                    (self.tall_jump(state) or self.beak_buster(state) or self.flutter(state) or self.air_rat_a_tat_rap(state))
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.talon_torpedo(state) and state.has(itemName.IKEY, self.player)\
                    and self.dive(state) and\
                    (self.tall_jump(state) or self.beak_buster(state) or self.clockwork_shot(state) or self.flutter(state) or self.air_rat_a_tat_rap(state))
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.talon_torpedo(state) and state.has(itemName.IKEY, self.player)\
                        and self.dive(state) and\
                        (self.tall_jump(state) or self.beak_buster(state) or self.clockwork_shot(state) or self.flutter(state) or self.air_rat_a_tat_rap(state))
        return logic

    def ice_key(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.grip_grab(state) and self.flap_flip(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.grip_grab(state) and self.flap_flip(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = (self.grip_grab(state) and self.flap_flip(state)) or self.clockwork_shot(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = (self.grip_grab(state) and self.flap_flip(state)) or self.clockwork_shot(state)
        return logic

    def pink_mystery_egg(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = (self.grenade_eggs(state) or (self.airborne_egg_aiming(state) and self.grenade_eggs_item(state))) \
                    and self.flight_pad(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = (self.grenade_eggs(state) or (self.airborne_egg_aiming(state) and self.grenade_eggs_item(state))) \
                    and self.flight_pad(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = (self.grenade_eggs(state) or (self.airborne_egg_aiming(state) and self.grenade_eggs_item(state))) \
                    and self.flight_pad(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = (self.has_explosives(state) or (self.airborne_egg_aiming(state) and self.grenade_eggs_item(state))) \
                    and self.flight_pad(state)
        return logic

    def blue_mystery_egg(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.grip_grab(state) and self.flap_flip(state) and self.flight_pad(state)\
                    and self.tall_jump(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.grip_grab(state) and self.flap_flip(state) and self.flight_pad(state)\
                    and (self.tall_jump(state) or self.beak_buster(state))
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = ((self.grip_grab(state) and self.flap_flip(state) and (self.tall_jump(state) or self.beak_buster(state)))\
                    or self.clockwork_shot(state)) and self.flight_pad(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = ((self.grip_grab(state) and self.flap_flip(state) and (self.tall_jump(state) or self.beak_buster(state)))\
                    or self.clockwork_shot(state)) and self.flight_pad(state)
        return logic

    def jinjo_plateau(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.bill_drill(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.bill_drill(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.bill_drill(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.bill_drill(state) or self.egg_barge(state)
        return logic

    def jinjo_clifftop(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.claw_clamber_boots(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.claw_clamber_boots(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.claw_clamber_boots(state) or self.clockwork_shot(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.claw_clamber_boots(state) and self.climb(state) or self.clockwork_shot(state)
        return logic

    def jinjo_wasteland(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.grip_grab(state) and self.flap_flip(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = (self.grip_grab(state) or self.beak_buster(state)) and self.flap_flip(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = ((self.grip_grab(state) or self.beak_buster(state)) and self.flap_flip(state))\
                        or self.clockwork_shot(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = ((self.grip_grab(state) or self.beak_buster(state)) and self.flap_flip(state))\
                        or self.clockwork_shot(state)
        return logic

    def jinjo_jadesnakegrove(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.grip_grab(state) and self.flap_flip(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.flap_flip(state) and\
                    (self.beak_buster(state) or self.grip_grab(state))
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = (self.flap_flip(state) and (self.beak_buster(state) or self.grip_grab(state))) or\
                    self.clockwork_shot(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = (self.flap_flip(state) and (self.beak_buster(state) or self.grip_grab(state))) or\
                    self.clockwork_shot(state)
        return logic

    def jinjo_stadium(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.MT_flight_pad(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.MT_flight_pad(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.MT_flight_pad(state) or self.clockwork_shot(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.MT_flight_pad(state) or self.clockwork_shot(state)
        return logic

    def jinjo_pool(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.dive(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = True
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = True
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = True
        return logic

    def jinjo_jail(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.humbaGGM(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.humbaGGM(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.humbaGGM(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.humbaGGM(state) or (self.bill_drill(state) and self.clockwork_shot(state))
        return logic

    def jinjo_boulder(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.humbaGGM(state) or (self.ggm_trot(state) and self.bill_drill(state))
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.humbaGGM(state) or (self.ggm_trot(state) and self.bill_drill(state))
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.humbaGGM(state) or (self.ggm_trot(state) and self.bill_drill(state))
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.humbaGGM(state)\
                    or (self.ggm_trot(state) and (self.bill_drill(state) or self.egg_barge(state)))
        return logic

    def jinjo_tent(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.talon_trot(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.talon_trot(state) or self.humbaWW(state) or self.split_up(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.talon_trot(state) or self.humbaWW(state) or self.clockwork_shot(state) or self.split_up(state) or\
                  ((self.grip_grab(state) or self.beak_buster(state)) and self.climb(state) and self.flap_flip(state))
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.talon_trot(state) or self.humbaWW(state) or self.clockwork_shot(state) or self.split_up(state) or\
                  ((self.grip_grab(state) or self.beak_buster(state)) and self.climb(state) and self.flap_flip(state))\
                  or (self.glitchedInfernoAccess(state) and self.turbo_trainers(state))
        return logic

    def jinjo_cave_of_horrors(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.grenade_eggs(state) and self.egg_aim(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.grenade_eggs(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.grenade_eggs(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.grenade_eggs(state)
        return logic

    def jinjo_cactus(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.grip_grab(state) and self.flap_flip(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = (self.grip_grab(state) and self.flap_flip(state))\
                    or (self.climb(state) and self.talon_trot(state) and self.flutter(state))\
                    or self.leg_spring(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = (self.grip_grab(state) and self.flap_flip(state))\
                    or (self.climb(state) and self.talon_trot(state) and (self.flutter(state) or self.air_rat_a_tat_rap(state)))\
                    or self.leg_spring(state)\
                    or self.clockwork_shot(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = (self.grip_grab(state) and self.flap_flip(state))\
                    or (self.climb(state) and self.talon_trot(state) and (self.flutter(state) or self.air_rat_a_tat_rap(state)))\
                    or self.leg_spring(state)\
                    or self.clockwork_shot(state)
        return logic

    def jinjo_van_door(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.has_explosives(state) and \
                    self.humbaWW(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.has_explosives(state) and \
                    self.humbaWW(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.has_explosives(state) and \
                    self.humbaWW(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = (self.has_explosives(state) and self.humbaWW(state)) or self.clockwork_eggs(state)
        return logic

    def jinjo_dodgem(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.talon_trot(state) and self.climb(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.talon_trot(state) and self.climb(state)\
                    or self.leg_spring(state) and self.glide(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = (self.talon_trot(state) or self.clockwork_shot(state)) and self.climb(state)\
                    or self.leg_spring(state) and self.glide(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = (self.talon_trot(state) or self.clockwork_shot(state)) and self.climb(state)\
                    or self.leg_spring(state) and self.glide(state)
        return logic

    def jinjo_alcove(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = state.has(itemName.DOUBLOON, self.player, 28) and self.turbo_trainers(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = (state.has(itemName.DOUBLOON, self.player, 28) and self.turbo_trainers(state))\
                    or (self.has_explosives(state) and (self.pack_whack(state) or self.sack_pack(state)\
                            or (self.leg_spring(state) and self.glide(state))))
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = (state.has(itemName.DOUBLOON, self.player, 28) and self.turbo_trainers(state))\
                    or (self.has_explosives(state) and (self.pack_whack(state) or self.sack_pack(state)\
                        or (self.leg_spring(state) and self.glide(state))))\
                    or self.tall_jump(state) and (self.flutter(state) or self.air_rat_a_tat_rap(state))\
                    or self.clockwork_shot(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = (state.has(itemName.DOUBLOON, self.player, 28) and self.turbo_trainers(state))\
                    or (self.has_explosives(state) and (self.pack_whack(state) or self.sack_pack(state)\
                        or (self.leg_spring(state) and self.glide(state))))\
                    or self.tall_jump(state) and (self.flutter(state) or self.air_rat_a_tat_rap(state))\
                    or self.clockwork_shot(state)
        return logic

    def jinjo_blubber(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.spring_pad(state) or self.flap_flip(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.spring_pad(state) or self.flap_flip(state) or (self.has_explosives(state) and self.leg_spring(state))
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.spring_pad(state) or self.flap_flip(state) or self.clockwork_shot(state) or (self.has_explosives(state) and self.leg_spring(state))
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.spring_pad(state) or self.flap_flip(state) or self.clockwork_shot(state) or (self.has_explosives(state) and self.leg_spring(state))
        return logic

    def jinjo_big_fish(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.jiggy_merry_maggie(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.jiggy_merry_maggie(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.jiggy_merry_maggie(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.jiggy_merry_maggie(state)
        return logic

    def jinjo_seaweed_sanctum(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.grip_grab(state) and self.flap_flip(state) and (
                self.tall_jump(state) and self.grip_grab(state)\
                or state.can_reach_region(regionName.JRBFC, self.player)
            )
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = (self.grip_grab(state) or self.beak_buster(state)) and self.flap_flip(state)\
                    and (
                        (self.slightly_elevated_ledge(state) or self.flap_flip(state))\
                            and self.tall_jump(state)\
                            and (self.beak_buster(state) or self.grip_grab(state))
                        or state.can_reach_region(regionName.JRBFC, self.player)
                    )
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = ((self.grip_grab(state) or self.beak_buster(state)) and self.flap_flip(state)\
                        or self.clockwork_shot(state))\
                    and (
                        (self.slightly_elevated_ledge(state) or self.flap_flip(state))\
                            and self.tall_jump(state)\
                            and (self.beak_buster(state) or self.grip_grab(state))
                        or state.can_reach_region(regionName.JRBFC, self.player)
                    )
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = ((self.grip_grab(state) or self.beak_buster(state)) and self.flap_flip(state)\
                        or self.clockwork_shot(state))\
                    and (
                        (self.slightly_elevated_ledge(state) or self.flap_flip(state))\
                            and self.tall_jump(state)\
                            and (self.beak_buster(state) or self.grip_grab(state))
                        or state.can_reach_region(regionName.JRBFC, self.player)
                    )
        return logic

    def jinjo_sunken_ship(self, state: CollectionState) -> bool:
        return self.humbaJRL(state) or self.sub_aqua_egg_aiming(state) or \
                    self.talon_torpedo(state)

    def jinjo_tdl_entrance(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.TDL_flight_pad(state) and (self.beak_bomb(state) or self.grenade_eggs(state) and self.egg_aim(state))
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.TDL_flight_pad(state) and (self.beak_bomb(state) or self.grenade_eggs(state))
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = (self.TDL_flight_pad(state) and self.beak_bomb(state)) or (self.grenade_eggs(state)\
                    and (self.egg_aim(state) or self.long_jump(state) or self.TDL_flight_pad(state) or self.turbo_trainers(state) or self.split_up(state)))
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = (self.TDL_flight_pad(state) and self.beak_bomb(state)) or (self.grenade_eggs(state)\
                    and (self.egg_aim(state) or self.long_jump(state) or self.TDL_flight_pad(state) or self.turbo_trainers(state) or self.split_up(state)))
        return logic

    def jinjo_big_t_rex(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.mumboTDL(state) and self.humbaTDL(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.mumboTDL(state) and self.humbaTDL(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.mumboTDL(state) and self.humbaTDL(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = (self.mumboTDL(state) and self.humbaTDL(state)) or \
                    self.clockwork_eggs(state)
        return logic

    def jinjo_stomping_plains(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.split_up(state) and self.tall_jump(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.split_up(state) and self.tall_jump(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.split_up(state) and self.tall_jump(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = (self.split_up(state) and self.tall_jump(state)\
                    or self.egg_barge(state) and (self.tall_jump(state) or self.talon_trot(state) or self.springy_step_shoes(state) or self.turbo_trainers(state)))
        return logic

    def jinjo_legspring(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.leg_spring(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.leg_spring(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.leg_spring(state) or self.clockwork_shot(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.leg_spring(state) or self.clockwork_shot(state)
        return logic

    def jinjo_gi_outside(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = state.can_reach_region(regionName.GI2, self.player) and self.floor_2_split_up(state)\
                    and self.pack_whack(state) and (self.wing_whack(state) or self.can_shoot_any_egg(state)) and self.claw_clamber_boots(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = state.can_reach_region(regionName.GI2, self.player) and self.floor_2_split_up(state)\
                        and self.pack_whack(state) and self.wing_whack(state) and self.claw_clamber_boots(state)\
                    or state.can_reach_region(regionName.GIR, self.player) and self.solo_kazooie_gi(state) and (self.wing_whack(state) or self.can_shoot_any_egg(state)) # Both characters drop from the roof, Banjo gets the jinjo.
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = state.can_reach_region(regionName.GI2, self.player) and self.floor_2_split_up(state)\
                        and self.pack_whack(state) and self.wing_whack(state) and self.claw_clamber_boots(state)\
                    or state.can_reach_region(regionName.GIR, self.player) and self.solo_kazooie_gi(state) and (self.wing_whack(state) or self.can_shoot_any_egg(state))
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = state.can_reach_region(regionName.GI2, self.player) and self.floor_2_split_up(state)\
                        and self.pack_whack(state) and self.wing_whack(state) and self.claw_clamber_boots(state)\
                    or state.can_reach_region(regionName.GIR, self.player) and self.solo_kazooie_gi(state) and (self.wing_whack(state) or self.can_shoot_any_egg(state))\
                    or state.can_reach_region(regionName.GIR, self.player) and self.taxi_pack(state)\
                    or (state.can_reach_region(regionName.GIOB, self.player) and self.claw_clamber_boots(state) or state.can_reach_region(regionName.GIR, self.player)) and self.egg_barge(state)
        return logic

    def jinjo_waste_disposal(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.talon_torpedo(state) and self.ice_eggs_item(state)\
                        and self.check_mumbo_magic(state, itemName.MUMBOJR) and self.sub_aqua_egg_aiming(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.talon_torpedo(state) and self.ice_eggs_item(state)\
                        and (self.check_mumbo_magic(state, itemName.MUMBOJR) or self.doubleAir(state)) and self.sub_aqua_egg_aiming(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.ice_eggs_item(state) and self.sub_aqua_egg_aiming(state) and \
                    self.talon_torpedo(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.ice_eggs_item(state) and self.sub_aqua_egg_aiming(state) and \
                    self.talon_torpedo(state)
        return logic

    def jinjo_boiler(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = state.can_reach_region(regionName.GIF, self.player) and self.flight_to_boiler_plant(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = state.can_reach_region(regionName.GIF, self.player) and self.flight_to_boiler_plant(state)\
                    or state.can_reach_region(regionName.GI3, self.player) and self.small_elevation(state) and self.leg_spring(state) and self.glide(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = state.can_reach_region(regionName.GIF, self.player) and self.flight_to_boiler_plant(state)\
                    or state.can_reach_region(regionName.GI3, self.player) and self.small_elevation(state) and self.leg_spring(state) and self.glide(state)\
                    or self.clockwork_shot(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = state.can_reach_region(regionName.GIF, self.player) and self.flight_to_boiler_plant(state)\
                    or state.can_reach_region(regionName.GI3, self.player) and self.small_elevation(state) and self.leg_spring(state) and self.glide(state)\
                    or self.clockwork_shot(state)
        return logic

    def jinjo_hot_pool(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.shack_pack(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.shack_pack(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.shack_pack(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.shack_pack(state) or self.dive(state) and self.tall_jump(state) and self.clockwork_eggs(state) and self.third_person_egg_shooting(state)
        return logic

    def jinjo_hot_waterfall(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.wonderwing(state) and self.flap_flip(state) and self.long_jump(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.wonderwing(state) and self.flap_flip(state) and self.long_jump(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = True
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = True
        return logic

    def jinjo_wind_tunnel(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.humbaHFP(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.humbaHFP(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.humbaHFP(state) or self.clockwork_shot(state) and self.hfp_top(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.humbaHFP(state) or self.clockwork_shot(state) and self.hfp_top(state)
        return logic

    def jinjo_icicle_grotto(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.glide(state) and self.grenade_eggs(state) and \
                    self.egg_aim(state) and self.tall_jump(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.glide(state) or (self.leg_spring(state) and
                    self.wing_whack(state))
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.glide(state) or self.leg_spring(state)\
                    or self.clockwork_shot(state) and (self.tall_jump(state) and (self.split_up(state) or self.talon_trot(state)))
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.glide(state) or self.leg_spring(state)\
                    or self.clockwork_shot(state) and (self.tall_jump(state) and (self.split_up(state) or self.talon_trot(state)))
        return logic

    def jinjo_mildred(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.hfp_top(state) and (self.fire_eggs(state) or self.has_explosives(state) or \
                    self.bill_drill(state) or self.dragon_kazooie(state))
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.hfp_top(state) and (
                (self.small_elevation(state) or self.beak_buster(state)) and (self.fire_eggs(state) or self.has_explosives(state) or self.bill_drill(state) or self.dragon_kazooie(state))\
                or (self.check_mumbo_magic(state, itemName.MUMBOHP) and self.tall_jump(state))\
                or self.split_up(state) and (self.tall_jump(state) and  self.leg_spring(state)) and (self.fire_eggs(state) or self.has_explosives(state)))
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.hfp_top(state) and (
                (self.small_elevation(state) or self.beak_buster(state)) and (self.fire_eggs(state) or self.has_explosives(state) or self.bill_drill(state) or self.dragon_kazooie(state))\
                or (self.check_mumbo_magic(state, itemName.MUMBOHP) and self.tall_jump(state))\
                or self.split_up(state) and (self.tall_jump(state) and self.leg_spring(state)) and (self.fire_eggs(state) or self.has_explosives(state))\
                or self.clockwork_shot(state))
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.hfp_top(state) and (
                (self.small_elevation(state) or self.beak_buster(state)) and (self.fire_eggs(state) or self.has_explosives(state) or self.bill_drill(state) or self.dragon_kazooie(state))\
                or (self.check_mumbo_magic(state, itemName.MUMBOHP) and self.tall_jump(state))\
                or self.split_up(state) and (self.tall_jump(state) and self.leg_spring(state)) and (self.fire_eggs(state) or self.has_explosives(state))\
                or self.clockwork_shot(state))
        return logic

    def jinjo_trash_can(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.shack_pack(state) and self.climb(state) and self.tall_jump(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.shack_pack(state) and self.climb(state) and (self.tall_jump(state) or self.pack_whack(state))\
                    or (self.flight_pad(state) or self.glide(state)) and self.leg_spring(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.shack_pack(state) and self.climb(state) and (self.tall_jump(state) or self.pack_whack(state))\
                    or self.split_up(state)\
                        and (self.flight_pad(state) or self.glide(state) or ((self.tall_jump(state) or self.leg_spring(state)) and self.wing_whack(state)))\
                        and (self.leg_spring(state) or (self.glide(state) and self.tall_jump(state) or self.clockwork_shot(state)))
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.shack_pack(state) and self.climb(state) and (self.tall_jump(state) or self.pack_whack(state))\
                    or self.split_up(state)\
                        and (self.flight_pad(state) or self.glide(state) or ((self.tall_jump(state) or self.leg_spring(state)) and self.wing_whack(state)))\
                        and (self.leg_spring(state) or (self.glide(state) and self.tall_jump(state) or self.clockwork_shot(state)))
        return logic

    def jinjo_cheese(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.flight_pad(state) and (self.sack_pack(state) and self.grow_beanstalk(state) and \
                     self.can_use_floatus(state))
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.flight_pad(state) and ((self.sack_pack(state) and self.grow_beanstalk(state) and \
                     self.can_use_floatus(state)) or self.leg_spring(state))
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.flight_pad(state) and ((self.sack_pack(state) and self.grow_beanstalk(state) and \
                     self.can_use_floatus(state)) or self.clockwork_shot(state) or self.leg_spring(state))
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.flight_pad(state) and ((self.sack_pack(state) and self.grow_beanstalk(state) and \
                     self.can_use_floatus(state)) or self.clockwork_shot(state) or self.leg_spring(state))
        return logic

    def jinjo_central(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.split_up(state) and self.spring_pad(state)\
                    or state.has(itemName.HUMBACC, self.player)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.split_up(state) and (self.spring_pad(state) or self.flight_pad(state))\
                    or self.springy_step_shoes(state) and self.bill_drill(state) and (self.flutter(state) or self.air_rat_a_tat_rap(state) or self.split_up(state))\
                    or self.leg_spring(state)\
                    or state.has(itemName.HUMBACC, self.player)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.split_up(state) and (self.spring_pad(state) or self.flight_pad(state))\
                    or self.clockwork_shot(state)\
                    or self.springy_step_shoes(state) and (self.flutter(state) or self.air_rat_a_tat_rap(state) or self.split_up(state))\
                    or self.leg_spring(state)\
                    or state.has(itemName.HUMBACC, self.player)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.split_up(state) and (self.spring_pad(state) or self.flight_pad(state))\
                    or self.clockwork_shot(state)\
                    or self.springy_step_shoes(state) and (self.flutter(state) or self.air_rat_a_tat_rap(state) or self.split_up(state))\
                    or self.leg_spring(state)\
                    or state.has(itemName.HUMBACC, self.player)
        return logic

    def jinjo_humba_ccl(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.climb(state) or state.has(itemName.HUMBACC, self.player)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.climb(state) or state.has(itemName.HUMBACC, self.player) or self.leg_spring(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.climb(state) or state.has(itemName.HUMBACC, self.player) or self.leg_spring(state) or self.clockwork_shot(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.climb(state) or state.has(itemName.HUMBACC, self.player) or self.leg_spring(state) or self.clockwork_shot(state)
        return logic

    def treble_jv(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.grip_grab(state) and self.flap_flip(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.grip_grab(state) and self.flap_flip(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = ((self.grip_grab(state) or self.beak_buster(state)) and self.flap_flip(state))\
                    or self.clockwork_shot(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = ((self.grip_grab(state) or self.beak_buster(state)) and self.flap_flip(state))\
                    or self.clockwork_shot(state)
        return logic

    def treble_gm(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.dive(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.dive(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.dive(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.dive(state) or (self.GM_boulders(state) and self.leg_spring(state))
        return logic

    def treble_ww(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.humbaWW(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.humbaWW(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.humbaWW(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.humbaWW(state) or self.clockwork_eggs(state)
        return logic

    def treble_jrl(self, state: CollectionState) -> bool:
        return self.sub_aqua_egg_aiming(state) or self.talon_torpedo(state) or self.humbaJRL(state)

    def treble_tdl(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = ((self.flap_flip(state) and self.grip_grab(state)) or self.TDL_flight_pad(state)) and self.bill_drill(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = ((self.flap_flip(state) and (self.grip_grab(state) or self.beak_buster(state)))\
                     or self.TDL_flight_pad(state)) and self.bill_drill(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = ((self.flap_flip(state) and (self.grip_grab(state) or self.beak_buster(state)))\
                     or self.TDL_flight_pad(state)) and self.bill_drill(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = ((self.flap_flip(state) and (self.grip_grab(state) or self.beak_buster(state))) or self.TDL_flight_pad(state))\
                        and (self.bill_drill(state) or self.egg_barge(state) or self.ground_rat_a_tat_rap(state))\
                    or self.humbaTDL(state) and self.mumboTDL(state)
        return logic

    def treble_gi(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = state.can_reach_region(regionName.GI1, self.player) and self.split_up(state) and self.claw_clamber_boots(state)\
                    or state.can_reach_region(regionName.GIF, self.player)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = state.can_reach_region(regionName.GI1, self.player) and (self.split_up(state) and self.claw_clamber_boots(state)\
                    or self.leg_spring(state) and self.glide(state) and\
                        (self.wing_whack(state) or self.egg_aim(state)))\
                    or state.can_reach_region(regionName.GIF, self.player)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = state.can_reach_region(regionName.GI1, self.player) and (self.split_up(state) and self.claw_clamber_boots(state)\
                        or self.leg_spring(state) and self.glide(state) and (self.wing_whack(state) or self.egg_aim(state)))\
                    or state.can_reach_region(regionName.GIF, self.player)\
                    or self.clockwork_shot(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = state.can_reach_region(regionName.GI1, self.player) and (self.split_up(state) and self.claw_clamber_boots(state)\
                        or self.leg_spring(state) and self.glide(state) and (self.wing_whack(state) or self.egg_aim(state)))\
                    or state.can_reach_region(regionName.GIF, self.player)\
                    or self.clockwork_shot(state)
        return logic

    def treble_hfp(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.hfp_top(state) and self.grenade_eggs(state) and self.egg_aim(state) and self.spring_pad(state) and (self.talon_trot(state) or self.split_up(state))
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = (self.split_up(state) and self.ice_cube_kazooie(state) and (self.tall_jump(state) or self.wing_whack(state) or self.glide(state) or self.leg_spring(state)))\
                    or (self.hfp_top(state) and self.grenade_eggs(state) and self.egg_aim(state) and self.spring_pad(state) and self.veryLongJump(state))
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = (self.split_up(state) and self.ice_cube_kazooie(state) and (self.tall_jump(state) or self.wing_whack(state) or self.glide(state) or self.leg_spring(state)))\
                    or (self.hfp_top(state) and (self.grenade_eggs(state) and self.veryLongJump(state) or self.clockwork_shot(state)) and self.egg_aim(state) and self.spring_pad(state))\
                    or (self.extremelyLongJump(state) and self.clockwork_shot(state))
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = (self.split_up(state) and self.ice_cube_kazooie(state) and (self.tall_jump(state) or self.wing_whack(state) or self.glide(state) or self.leg_spring(state)))\
                    or (self.hfp_top(state) and (self.grenade_eggs(state) and self.veryLongJump(state) or self.clockwork_shot(state)) and self.egg_aim(state) and self.spring_pad(state))\
                    or (self.extremelyLongJump(state) and self.clockwork_shot(state))
        return logic

    def treble_ccl(self, state: CollectionState) -> bool:
        return self.notes_ccl_high(state)

    def solo_banjo_waste_disposal(self, state):
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.grip_grab(state) and self.can_use_battery(state) and self.climb(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.can_use_battery(state) and (self.grip_grab(state) and self.climb(state) or self.tall_jump(state))
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.can_use_battery(state) and (self.grip_grab(state) and self.climb(state) or self.tall_jump(state))
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.can_use_battery(state) and (self.grip_grab(state) and self.climb(state) or self.tall_jump(state))
        return logic


    def silo_snooze(self, state: CollectionState) -> bool:
        return self.check_notes(state, locationName.SNPACK) and self.solo_banjo_waste_disposal(state)

    def tswitch_ww(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.grip_grab(state) and self.flap_flip(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.grip_grab(state) and self.flap_flip(state)\
                or self.leg_spring(state)\
                or self.grip_grab(state) and self.pack_whack(state) and self.tall_jump(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.grip_grab(state) and self.flap_flip(state)\
                or self.leg_spring(state)\
                or self.grip_grab(state) and self.pack_whack(state) and self.tall_jump(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.grip_grab(state) and self.flap_flip(state)\
                or self.leg_spring(state)\
                or self.grip_grab(state) and self.pack_whack(state) and self.tall_jump(state)
        return logic

    def tswitch_tdl(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.flap_flip(state)\
                    or self.veryLongJump(state)\
                    or self.TDL_flight_pad(state)\
                    or self.tall_jump(state) and self.grip_grab(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.flap_flip(state)\
                    or self.veryLongJump(state)\
                    or self.TDL_flight_pad(state)\
                    or self.split_up(state)\
                    or self.springy_step_shoes(state)\
                    or self.tall_jump(state) and self.air_rat_a_tat_rap(state)\
                    or self.tall_jump(state) and self.grip_grab(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.flap_flip(state)\
                    or self.veryLongJump(state)\
                    or self.TDL_flight_pad(state)\
                    or self.split_up(state)\
                    or self.springy_step_shoes(state)\
                    or self.tall_jump(state) and self.air_rat_a_tat_rap(state)\
                    or self.tall_jump(state) and self.grip_grab(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.flap_flip(state)\
                    or self.veryLongJump(state)\
                    or self.TDL_flight_pad(state)\
                    or self.split_up(state)\
                    or self.springy_step_shoes(state)\
                    or self.tall_jump(state) and self.air_rat_a_tat_rap(state)\
                    or self.tall_jump(state) and self.grip_grab(state)
        return logic

    def tswitch_gi(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.climb(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.climb(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.climb(state) or self.extremelyLongJump(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.climb(state) or self.extremelyLongJump(state)
        return logic

    def tswitch_lavaside(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.grip_grab(state)\
                    and (self.tall_jump(state) or self.talon_trot(state))\
                    and (self.flutter(state) or self.air_rat_a_tat_rap(state))
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.grip_grab(state)\
                        and (self.tall_jump(state) or self.talon_trot(state))\
                        and (self.flutter(state) or self.air_rat_a_tat_rap(state))\
                    or self.flight_pad(state)\
                    or self.leg_spring(state)\
                    or self.split_up(state) and self.tall_jump(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.grip_grab(state)\
                        and (self.tall_jump(state) or self.talon_trot(state))\
                        and (self.flutter(state) or self.air_rat_a_tat_rap(state))\
                    or self.flight_pad(state)\
                    or self.leg_spring(state)\
                    or self.split_up(state) and self.tall_jump(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.grip_grab(state)\
                        and (self.tall_jump(state) or self.talon_trot(state))\
                        and (self.flutter(state) or self.air_rat_a_tat_rap(state))\
                    or self.flight_pad(state)\
                    or self.leg_spring(state)\
                    or self.split_up(state) and self.tall_jump(state)
        return logic

    def doubloon_ledge(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.split_up(state) and self.has_explosives(state)\
                    and self.spring_pad(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.split_up(state) and self.has_explosives(state)\
                    and (self.spring_pad(state) or self.leg_spring(state))
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.split_up(state) and self.has_explosives(state)\
                        and (
                            self.spring_pad(state)\
                            or self.leg_spring(state)\
                            or self.pack_whack(state) and self.tall_jump(state) and self.grip_grab(state)\
                            or self.glide(state) and self.tall_jump(state)\
                            or self.wing_whack(state) and self.tall_jump(state)
                        )\
                    or self.clockwork_shot(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.split_up(state) and self.has_explosives(state)\
                        and (
                            self.spring_pad(state)\
                            or self.leg_spring(state)\
                            or self.pack_whack(state) and self.tall_jump(state) and self.grip_grab(state)\
                            or self.glide(state) and self.tall_jump(state)\
                            or self.wing_whack(state) and self.tall_jump(state)
                        )\
                    or self.clockwork_shot(state)
        return logic

    def doubloon_dirtpatch(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.bill_drill(state) or self.has_explosives(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.bill_drill(state) or self.has_explosives(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.bill_drill(state) or self.has_explosives(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.bill_drill(state) or self.has_explosives(state)
        return logic

    def doubloon_water(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.dive(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.dive(state) or self.shack_pack(state) and self.has_explosives(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.dive(state) or self.shack_pack(state) and self.has_explosives(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.dive(state) or self.shack_pack(state) and self.has_explosives(state)
        return logic

    def notes_plateau_sign(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.grip_grab(state) and self.flap_flip(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = (self.grip_grab(state) or self.beak_buster(state)) and self.flap_flip(state)\
                    or self.leg_spring(state)\
                    or self.split_up(state) and self.tall_jump(state)\
                    or self.glide(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = ((self.grip_grab(state) or self.beak_buster(state)) and self.flap_flip(state))\
                    or self.clockwork_shot(state)\
                    or self.leg_spring(state)\
                    or self.split_up(state) and self.grip_grab(state)\
                    or self.split_up(state) and self.tall_jump(state)\
                    or self.glide(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = ((self.grip_grab(state) or self.beak_buster(state)) and self.flap_flip(state))\
                    or self.clockwork_shot(state)\
                    or self.leg_spring(state)\
                    or self.split_up(state) and self.grip_grab(state)\
                    or self.split_up(state) and self.tall_jump(state)\
                    or self.glide(state)
        return logic

    def can_reach_honey_b(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.talon_trot(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.talon_trot(state)\
                    or state.can_reach_region(regionName.IOHCT, self.player) and self.claw_clamber_boots(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.talon_trot(state)\
                    or state.can_reach_region(regionName.IOHCT, self.player) and self.claw_clamber_boots(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.talon_trot(state)\
                    or state.can_reach_region(regionName.IOHCT, self.player) and self.claw_clamber_boots(state)
        return logic

    def notes_ww_area51_right(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.has_explosives(state) and self.spring_pad(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.has_explosives(state) and self.spring_pad(state)\
                    or self.leg_spring(state)\
                    or self.glide(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = ((self.has_explosives(state) or self.split_up(state)) and self.spring_pad(state))\
                    or self.leg_spring(state)\
                    or self.clockwork_shot(state)\
                    or self.glide(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = ((self.has_explosives(state) or self.split_up(state)) and self.spring_pad(state))\
                    or self.leg_spring(state)\
                    or self.clockwork_shot(state)\
                    or self.glide(state)
        return logic

    def notes_ww_area51_left(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.has_explosives(state) and self.spring_pad(state) and self.long_jump(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.has_explosives(state) and self.spring_pad(state) and self.long_jump(state)\
                    or self.leg_spring(state)\
                    or self.glide(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.has_explosives(state) and self.spring_pad(state) and self.long_jump(state)\
                    or self.split_up(state) and self.spring_pad(state)\
                    or self.leg_spring(state)\
                    or self.clockwork_shot(state)\
                    or self.glide(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.has_explosives(state) and self.spring_pad(state) and self.long_jump(state)\
                    or self.split_up(state) and self.spring_pad(state)\
                    or self.leg_spring(state)\
                    or self.clockwork_shot(state)\
                    or self.glide(state)
        return logic


    def notes_dive_of_death(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = ((self.grip_grab(state) and self.flap_flip(state)) or self.climb(state)) and self.dive(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = ((self.grip_grab(state) or self.beak_buster(state)) and self.flap_flip(state) or self.climb(state))\
                        and (self.tall_jump(state) or self.dive(state))\
                    or (self.leg_spring(state) or self.glide(state)) and self.tall_jump(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = (self.grip_grab(state) or self.beak_buster(state)) and self.flap_flip(state)\
                    or self.climb(state)\
                    or self.leg_spring(state)\
                    or self.glide(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
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
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.small_elevation(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = True
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = True
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = True
        return logic

    def notes_top_clockwork(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.flap_flip(state) or \
                    (self.tall_jump(state) or (self.talon_trot(state) and self.flutter(state)))\
                        and self.grip_grab(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.flap_flip(state) or \
                    (self.tall_jump(state) or (self.talon_trot(state) and self.flutter(state)))\
                        and self.grip_grab(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = (self.flap_flip(state) or \
                    (self.tall_jump(state) or (self.talon_trot(state) and self.flutter(state)))\
                        and self.grip_grab(state))\
                    or self.clockwork_shot(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = (self.flap_flip(state) or \
                        (self.tall_jump(state) or (self.talon_trot(state) and self.flutter(state)))\
                        and self.grip_grab(state))\
                        or self.clockwork_shot(state)
        return logic

    def notes_green_pile(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.GGM_slope(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.GGM_slope(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.GGM_slope(state) or self.clockwork_shot(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.GGM_slope(state) or self.clockwork_shot(state)
        return logic

    def notes_prospector_easy(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.GGM_slope(state)\
                    or self.flap_flip(state)\
                    or (self.mt_jiggy(state) and self.dilberta_free(state))\
                    or self.tall_jump(state) and self.grip_grab(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = True
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = True
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = True
        return logic

    def notes_prospector_hard(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.GGM_slope(state) or self.flap_flip(state) or (self.mt_jiggy(state) and self.dilberta_free(state))
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = True
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = True
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = True
        return logic

    def notes_gm_mumbo(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.small_elevation(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.small_elevation(state) or self.grip_grab(state) or self.beak_buster(state) or self.ggm_trot(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.small_elevation(state) or self.grip_grab(state) or self.clockwork_shot(state) or self.beak_buster(state) or self.ggm_trot(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.small_elevation(state) or self.grip_grab(state) or self.clockwork_shot(state) or self.beak_buster(state) or self.ggm_trot(state)
        return logic

    def notes_easy_fuel_depot(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.small_elevation(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = True
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = True
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = True
        return logic

    def notes_hard_fuel_depot(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.small_elevation(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.small_elevation(state) or self.ggm_trot(state) or self.beak_buster(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.small_elevation(state) or self.ggm_trot(state) or self.clockwork_shot(state) or self.beak_buster(state) or self.air_rat_a_tat_rap(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.small_elevation(state) or self.ggm_trot(state) or self.clockwork_shot(state) or self.beak_buster(state) or self.air_rat_a_tat_rap(state)
        return logic


    def notes_jrl_blubs(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.sub_aqua_egg_aiming(state) or self.talon_torpedo(state) or self.humbaJRL(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.sub_aqua_egg_aiming(state) or self.talon_torpedo(state) or self.humbaJRL(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.sub_aqua_egg_aiming(state) or self.talon_torpedo(state) or self.humbaJRL(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.sub_aqua_egg_aiming(state) or self.talon_torpedo(state) or self.humbaJRL(state)
        return logic

    def notes_jrl_eels(self, state: CollectionState) -> bool:
        return True

    def notes_jolly(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.talon_trot(state) or (self.tall_jump(state) and self.grip_grab(state))\
                or self.flap_flip(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.small_elevation(state) or self.long_jump(state) or self.roll(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.small_elevation(state) or self.long_jump(state) or self.clockwork_shot(state) or self.roll(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.small_elevation(state) or self.long_jump(state) or self.clockwork_shot(state) or self.roll(state)
        return logic

    def notes_river_passage(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.dive(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.dive(state) or self.humbaTDL(state) or self.shack_pack(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.dive(state) or self.humbaTDL(state) or self.shack_pack(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.dive(state) or self.humbaTDL(state) or self.shack_pack(state)
        return logic

    def notes_tdl_station_right(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.small_elevation(state)\
                    or self.humbaTDL(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.small_elevation(state)\
                    or self.humbaTDL(state)\
                    or self.split_up(state)\
                    or self.springy_step_shoes(state)\
                    or self.turbo_trainers(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.small_elevation(state)\
                    or self.humbaTDL(state)\
                    or self.split_up(state)\
                    or self.springy_step_shoes(state)\
                    or self.turbo_trainers(state)\
                    or self.clockwork_shot(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.small_elevation(state)\
                    or self.humbaTDL(state)\
                    or self.split_up(state)\
                    or self.springy_step_shoes(state)\
                    or self.turbo_trainers(state)\
                    or self.clockwork_shot(state)
        return logic

    def notes_roar_cage(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.long_jump(state)\
                    or self.springy_step_shoes(state)\
                    or self.TDL_flight_pad(state)\
                    or self.humbaTDL(state) and self.roar(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.long_jump(state)\
                    or self.springy_step_shoes(state)\
                    or self.TDL_flight_pad(state)\
                    or self.humbaTDL(state) and self.roar(state)\
                    or self.split_up(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.long_jump(state)\
                    or self.springy_step_shoes(state)\
                    or self.TDL_flight_pad(state)\
                    or self.humbaTDL(state) and self.roar(state)\
                    or self.split_up(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.long_jump(state)\
                    or self.springy_step_shoes(state)\
                    or self.TDL_flight_pad(state)\
                    or self.humbaTDL(state) and self.roar(state)\
                    or self.split_up(state)
        return logic

    def notes_gi_floor1(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.grip_grab(state) and self.climb(state) and self.flap_flip(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.F1_to_F2(state)\
                or (self.grip_grab(state) and self.climb(state) and self.flap_flip(state))
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.claw_clamber_boots(state)\
                    or (self.grip_grab(state) and self.climb(state) and self.flap_flip(state))\
                    or self.pack_whack(state) and self.tall_jump(state) and self.climb(state)\
                    or self.leg_spring(state)\
                    or self.clockwork_shot(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.claw_clamber_boots(state)\
                    or (self.grip_grab(state) and self.climb(state) and self.flap_flip(state))\
                    or self.pack_whack(state) and self.tall_jump(state) and self.climb(state)\
                    or self.leg_spring(state)\
                    or self.clockwork_shot(state)
        return logic

    def notes_gi_train_station_easy(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.small_elevation(state) or self.leg_spring(state) or self.grip_grab(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.small_elevation(state) or self.leg_spring(state) or self.beak_buster(state) or self.grip_grab(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = True
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = True
        return logic

    def notes_gi_train_station_hard(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.small_elevation(state) or self.leg_spring(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.small_elevation(state) or self.leg_spring(state) or self.beak_buster(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = True
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = True
        return logic

    # Because jumping on a slope is not intended...
    def notes_aircon_hard(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.tall_jump(state) or self.split_up(state) or self.talon_trot(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = True
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = True
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = True
        return logic

    def notes_leg_spring(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = (self.climb(state) or (self.has_explosives(state) and self.small_elevation(state)))
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = (self.climb(state) or (self.has_explosives(state) and self.small_elevation(state)))
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = (self.climb(state) or (self.has_explosives(state) and self.small_elevation(state)))\
                    or self.clockwork_shot(state)\
                    or self.claw_clamber_boots(state) and self.extremelyLongJump(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = (self.climb(state) or (self.has_explosives(state) and self.small_elevation(state)))\
                    or self.clockwork_shot(state)\
                    or self.claw_clamber_boots(state) and self.extremelyLongJump(state)
        return logic

    def notes_short_stack(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.small_elevation(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.small_elevation(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = True
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = True
        return logic

    def notes_waste_disposal(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.can_use_battery(state) and (self.grip_grab(state) and self.climb(state))
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.can_use_battery(state) and (self.grip_grab(state) and self.climb(state) or self.tall_jump(state))
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.can_use_battery(state) and (self.grip_grab(state) and self.climb(state) or self.tall_jump(state))
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = (self.can_use_battery(state) and (self.grip_grab(state) and self.climb(state) or self.tall_jump(state)))\
                    or self.clockwork_shot(state) and self.flap_flip(state)
        return logic


    def notes_floor_3(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic =  ((self.grip_grab(state) and self.flap_flip(state) or self.split_up(state)) and self.spring_pad(state) and self.climb(state))\
                    or (self.climb(state) and self.veryLongJump(state))\
                    or self.small_elevation(state) and self.leg_spring(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = ((self.grip_grab(state) and self.flap_flip(state) or self.split_up(state)) and self.spring_pad(state) and self.climb(state))\
                    or (self.climb(state) and self.veryLongJump(state))\
                    or self.small_elevation(state) and self.leg_spring(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = ((self.grip_grab(state) and self.flap_flip(state) or self.split_up(state)) and self.spring_pad(state) and self.climb(state))\
                    or (self.climb(state) and self.veryLongJump(state))\
                    or self.clockwork_shot(state)\
                    or self.small_elevation(state) and self.leg_spring(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = ((self.grip_grab(state) and self.flap_flip(state) or self.split_up(state)) and self.spring_pad(state) and self.climb(state))\
                    or (self.climb(state) and self.veryLongJump(state))\
                    or self.clockwork_shot(state)\
                    or self.small_elevation(state) and self.leg_spring(state)
        return logic

    def notes_oil_drill(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic =  self.hfp_top(state) and (self.flap_flip(state) or self.talon_trot(state)) and self.ice_cube_BK(state)\
                    or self.hfp_top(state) and self.split_up(state) and self.grip_grab(state) and self.pack_whack(state)\
                    or self.hfp_top(state) and self.split_up(state) and self.ice_cube_kazooie(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.hfp_top(state) and (self.flap_flip(state) or self.talon_trot(state) or self.flight_pad(state)) and self.ice_cube_BK(state)\
                    or self.hfp_top(state) and self.split_up(state) and (self.grip_grab(state) or self.tall_jump(state)) and self.pack_whack(state)\
                    or self.hfp_top(state) and self.split_up(state) and self.ice_cube_kazooie(state)\
                    or self.humbaHFP(state)\
                    or self.hfp_top(state) and self.claw_clamber_boots(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.hfp_top(state) and (self.flap_flip(state) or self.talon_trot(state) or self.flight_pad(state)) and self.ice_cube_BK(state)\
                    or self.hfp_top(state) and self.split_up(state) and (self.grip_grab(state) or self.tall_jump(state)) and self.pack_whack(state)\
                    or self.hfp_top(state) and self.split_up(state) and self.ice_cube_kazooie(state)\
                    or self.humbaHFP(state)\
                    or self.hfp_top(state) and self.clockwork_shot(state)\
                    or self.hfp_top(state) and self.claw_clamber_boots(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.hfp_top(state) and (self.flap_flip(state) or self.talon_trot(state) or self.flight_pad(state)) and self.ice_cube_BK(state)\
                    or self.hfp_top(state) and self.split_up(state) and (self.grip_grab(state) or self.tall_jump(state)) and self.pack_whack(state)\
                    or self.hfp_top(state) and self.split_up(state) and self.ice_cube_kazooie(state)\
                    or self.humbaHFP(state)\
                    or self.hfp_top(state) and self.clockwork_shot(state)\
                    or self.hfp_top(state) and self.claw_clamber_boots(state)
        return logic

    def notes_ladder(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.hfp_top(state) or self.split_up(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.hfp_top(state) or self.split_up(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.hfp_top(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.hfp_top(state)
        return logic

    def notes_ccl_silo(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.shack_pack(state) and (
                        state.has(itemName.WARPCC1, self.player) and state.has(itemName.WARPCC2, self.player)\
                        or self.can_use_floatus(state)
                    )
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.shack_pack(state) and (
                        state.has(itemName.WARPCC1, self.player) and state.has(itemName.WARPCC2, self.player)\
                        or self.can_use_floatus(state)
                    )\
                    or self.clockwork_eggs(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.shack_pack(state) and (
                        state.has(itemName.WARPCC1, self.player) and state.has(itemName.WARPCC2, self.player)\
                        or self.can_use_floatus(state)
                    )\
                    or self.clockwork_eggs(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.shack_pack(state) and (
                        state.has(itemName.WARPCC1, self.player) and state.has(itemName.WARPCC2, self.player)\
                        or self.can_use_floatus(state)
                    )\
                    or self.clockwork_eggs(state)
        return logic

    def notes_cheese(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = (self.climb(state) and self.sack_pack(state))\
                    or self.notes_ccl_high(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = (self.climb(state) and self.sack_pack(state))\
                    or self.notes_ccl_high(state)\
                    or self.springy_step_shoes(state) and self.split_up(state)\
                    or self.claw_clamber_boots and self.glide(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.climb(state)\
                    or (self.springy_step_shoes(state))\
                    or self.notes_ccl_high(state)\
                    or self.clockwork_shot(state)\
                    or self.springy_step_shoes(state) and self.split_up(state)\
                    or self.claw_clamber_boots and self.glide(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.climb(state)\
                    or (self.springy_step_shoes(state))\
                    or self.notes_ccl_high(state)\
                    or self.clockwork_shot(state)\
                    or self.springy_step_shoes(state) and self.split_up(state)\
                    or self.claw_clamber_boots and self.glide(state)
        return logic

    def notes_ccl_high(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.flight_pad(state) or state.has(itemName.HUMBACC, self.player)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.flight_pad(state) or state.has(itemName.HUMBACC, self.player)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.flight_pad(state) or state.has(itemName.HUMBACC, self.player)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic =self.flight_pad(state) or state.has(itemName.HUMBACC, self.player)
        return logic

    def notes_sack_race(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.flight_pad(state)\
                    or self.long_jump(state) and self.climb(state)\
                    or state.has(itemName.HUMBACC, self.player)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.flight_pad(state)\
                    or self.climb(state) and (self.long_jump(state) or self.grip_grab(state) or self.pack_whack(state) or self.sack_pack(state))\
                    or state.has(itemName.HUMBACC, self.player)\
                    or self.claw_clamber_boots and self.glide(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.flight_pad(state)\
                    or self.climb(state) and (self.long_jump(state) or self.grip_grab(state) or self.pack_whack(state) or self.sack_pack(state))\
                    or self.leg_spring(state) and (self.glide(state) or self.wing_whack(state))\
                    or state.has(itemName.HUMBACC, self.player)\
                    or self.claw_clamber_boots and self.glide(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.flight_pad(state)\
                    or self.climb(state) and (self.long_jump(state) or self.grip_grab(state) or self.pack_whack(state) or self.sack_pack(state))\
                    or self.leg_spring(state) and (self.glide(state) or self.wing_whack(state))\
                    or state.has(itemName.HUMBACC, self.player)\
                    or self.claw_clamber_boots and self.glide(state)
        return logic

    def ccl_glowbo_pool(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.dive(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = True
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = True # Jumping in the pool outside and going through the loading zone gives dive for free.
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = True
        return logic

    def notes_ccl_low(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = True
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = True
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = True
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = True
        return logic

    def notes_dippy(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.dive(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.dive(state) or self.shack_pack(state) or self.beak_buster(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = True
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = True
        return logic


    def check_mumbo_magic(self, state: CollectionState, name) -> bool:
        for item_name in self.mumbo_magic:
            if name == item_name:
                return state.has(name, self.player)

    def check_humba_magic(self, state: CollectionState, name) -> bool:
        for item_name in self.humba_magic:
            if name == item_name:
                return state.has(name, self.player)

    def check_solo_moves(self, state: CollectionState, name) -> bool:
        for item_name in self.solo_moves:
            if name == item_name:
                return state.has(name, self.player) and self.split_up(state)

    def check_notes(self, state: CollectionState, silo: locationName) -> bool:
        amount = self.world.jamjars_siloname_costs[silo]
        count: int = 0
        count = state.count(itemName.TREBLE, self.player) * 20
        count += state.count(itemName.BASS, self.player) * 10
        count += state.count(itemName.NOTE, self.player) * 5
        return count >= amount

    def silo_bill_drill(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.check_notes(state, locationName.BDRILL)\
                    and (self.flap_flip(state)\
                         or (self.tall_jump(state) or self.talon_trot(state) and self.flutter(state)) and self.grip_grab(state))
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.check_notes(state, locationName.BDRILL)\
                    and (self.flap_flip(state)\
                         or (self.tall_jump(state) or self.talon_trot(state) and self.flutter(state)) and self.grip_grab(state))
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.check_notes(state, locationName.BDRILL)\
                    and (self.flap_flip(state)\
                        or (self.tall_jump(state) or self.talon_trot(state) and self.flutter(state)) and self.grip_grab(state)\
                        or self.turbo_trainers(state))
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.check_notes(state, locationName.BDRILL)\
                    and (self.flap_flip(state)\
                        or (self.tall_jump(state) or self.talon_trot(state) and self.flutter(state)) and self.grip_grab(state)\
                        or self.turbo_trainers(state))
        return logic

    def silo_spring(self, state:CollectionState) -> bool:
        if self.world.options.logic_type == LogicType.option_intended:
            return self.flap_flip(state) and self.grip_grab(state)\
                    or self.TDL_flight_pad(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            return self.flap_flip(state) and (self.grip_grab(state) or self.beak_buster(state))\
                    or self.TDL_flight_pad(state)\
                    or self.veryLongJump(state)\
                    or self.turbo_trainers(state)\
                    or self.springy_step_shoes(state)

        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            return self.flap_flip(state) and (self.grip_grab(state) or self.beak_buster(state))\
                    or self.TDL_flight_pad(state)\
                    or self.veryLongJump(state)\
                    or self.turbo_trainers(state)\
                    or self.springy_step_shoes(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            return self.flap_flip(state) and (self.grip_grab(state) or self.beak_buster(state))\
                    or self.TDL_flight_pad(state)\
                    or self.veryLongJump(state)\
                    or self.turbo_trainers(state)\
                    or self.springy_step_shoes(state)

    def can_access_talon_torpedo_silo(self, state:CollectionState) -> bool:
        if self.world.options.logic_type == LogicType.option_intended:
            return self.grip_grab(state) and self.tall_jump(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            return (self.grip_grab(state) or self.beak_buster(state)) and self.tall_jump(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            return (self.grip_grab(state) or self.beak_buster(state)) and self.tall_jump(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            return (self.grip_grab(state) or self.beak_buster(state)) and self.tall_jump(state)

    def can_access_taxi_pack_silo(self, state:CollectionState) -> bool:
        if self.world.options.logic_type == LogicType.option_intended:
            return self.split_up(state) and (self.tall_jump(state) and (self.grip_grab(state) or self.sack_pack(state)))
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            return self.split_up(state) and\
                        (self.tall_jump(state) and (self.grip_grab(state) or
                        self.pack_whack(state) and self.tall_jump(state)\
                        or self.pack_whack(state) and self.grip_grab(state)\
                        or self.sack_pack(state)))
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            return self.split_up(state) and\
                        (self.tall_jump(state) and (self.grip_grab(state)\
                        or self.pack_whack(state) and self.tall_jump(state)\
                        or self.pack_whack(state) and self.grip_grab(state)\
                        or self.sack_pack(state)))
        elif self.world.options.logic_type == LogicType.option_glitches:
            return self.split_up(state) and\
                        (self.tall_jump(state) and (self.grip_grab(state) or
                        self.pack_whack(state) and self.tall_jump(state)\
                        or self.pack_whack(state) and self.grip_grab(state)\
                        or self.sack_pack(state)))

    def can_access_glide_silo(self, state:CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            # Through icicle grotto
            logic = self.hfp_top(state) and self.grenade_eggs(state) and self.egg_aim(state) and self.spring_pad(state) and (self.talon_trot(state) or self.split_up(state))
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.split_up(state) and (self.tall_jump(state) or self.wing_whack(state) or self.glide(state) or self.leg_spring(state))
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.split_up(state) and (self.tall_jump(state) or self.wing_whack(state) or self.glide(state) or self.leg_spring(state))
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.split_up(state) and (self.tall_jump(state) or self.wing_whack(state) or self.glide(state) or self.leg_spring(state))
        return logic

    def can_access_sack_pack_silo(self, state:CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.shack_pack(state) and (
                        state.has(itemName.WARPCC1, self.player) and state.has(itemName.WARPCC2, self.player)\
                        or self.can_use_floatus(state)
                    )
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.shack_pack(state) and (
                        state.has(itemName.WARPCC1, self.player) and state.has(itemName.WARPCC2, self.player)\
                        or self.can_use_floatus(state)
                    )
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.shack_pack(state) and (
                        state.has(itemName.WARPCC1, self.player) and state.has(itemName.WARPCC2, self.player)\
                        or self.can_use_floatus(state)
                    )
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.shack_pack(state) and (
                        state.has(itemName.WARPCC1, self.player) and state.has(itemName.WARPCC2, self.player)\
                        or self.can_use_floatus(state)
                    )
        return logic

    def nest_lair_top(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.small_elevation(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.small_elevation(state) or self.grip_grab(state) or self.beak_buster(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.small_elevation(state)\
                    or self.grip_grab(state)\
                    or self.beak_buster(state)\
                    or self.air_rat_a_tat_rap(state)\
                    or self.flutter(state)\
                    or self.clockwork_shot(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.small_elevation(state)\
                    or self.grip_grab(state)\
                    or self.beak_buster(state)\
                    or self.air_rat_a_tat_rap(state)\
                    or self.flutter(state)\
                    or self.clockwork_shot(state)
        return logic

    def SM_to_GL(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.flight_pad(state) or self.flap_flip(state) and self.climb(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.flight_pad(state) or self.flap_flip(state) and self.climb(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.flight_pad(state)\
                    or self.flap_flip(state) and self.climb(state)\
                    or (self.tall_jump(state) or self.talon_trot(state) and self.flutter(state)) and self.beak_buster(state) and self.climb(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.flight_pad(state)\
                    or self.flap_flip(state) and self.climb(state)\
                    or (self.tall_jump(state) or self.talon_trot(state) and self.flutter(state)) and self.beak_buster(state) and self.climb(state)
        return logic

    def nest_sm_waterfall_top(self, state: CollectionState) -> bool:
        return self.flight_pad(state)

    def nest_sm_waterfall_platform(self, state: CollectionState) -> bool:
        if self.world.options.logic_type == LogicType.option_intended:
            return self.flight_pad(state)\
                    or self.small_elevation(state)\
                    or self.air_rat_a_tat_rap(state)\
                    or self.flutter(state)\
                    or self.flap_flip(state)\
                    or self.grip_grab(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            return self.flight_pad(state)\
                    or self.small_elevation(state)\
                    or self.air_rat_a_tat_rap(state)\
                    or self.flutter(state)\
                    or self.flap_flip(state)\
                    or self.grip_grab(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            return self.flight_pad(state)\
                    or self.small_elevation(state)\
                    or self.air_rat_a_tat_rap(state)\
                    or self.flutter(state)\
                    or self.flap_flip(state)\
                    or self.grip_grab(state)\
                    or self.clockwork_shot(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            return self.flight_pad(state)\
                    or self.small_elevation(state)\
                    or self.air_rat_a_tat_rap(state)\
                    or self.flutter(state)\
                    or self.flap_flip(state)\
                    or self.grip_grab(state)\
                    or self.clockwork_shot(state)

    def nest_bottles_house(self, state: CollectionState) -> bool:
        if self.world.options.logic_type == LogicType.option_intended:
            return self.small_elevation(state) or self.grip_grab(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            return self.small_elevation(state) or self.grip_grab(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            return self.small_elevation(state) or self.grip_grab(state) or self.clockwork_shot(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            return self.small_elevation(state) or self.grip_grab(state) or self.clockwork_shot(state)

    def nest_pl_dirt_pile(self, state: CollectionState) -> bool:
            return self.plateau_top(state)

    def nest_cliff_top_hard(self, state: CollectionState) -> bool:
        if self.world.options.logic_type == LogicType.option_intended:
            return self.small_elevation(state) or self.grip_grab(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            return self.small_elevation(state)\
                    or self.grip_grab(state)\
                    or self.beak_buster(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            return self.small_elevation(state)\
                    or self.grip_grab(state)\
                    or self.clockwork_shot(state)\
                    or self.beak_buster(state)\
                    or self.flutter(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            return self.small_elevation(state)\
                    or self.grip_grab(state)\
                    or self.clockwork_shot(state)\
                    or self.beak_buster(state)\
                    or self.flutter(state)

    def nest_another_digger_tunnel(self, state: CollectionState) -> bool:
        if self.world.options.logic_type == LogicType.option_intended:
            return self.dive(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            return self.dive(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            return self.dive(state) or self.beak_buster(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            return self.dive(state) or self.beak_buster(state)

    def nest_quagmire_hard(self, state: CollectionState) -> bool:
        if self.world.options.logic_type == LogicType.option_intended:
            return self.small_elevation(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            return self.small_elevation(state) or self.beak_buster(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            return self.small_elevation(state) or self.clockwork_shot(state) or self.beak_buster(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            return self.small_elevation(state) or self.clockwork_shot(state) or self.beak_buster(state)

    def nest_quagmire_easy(self, state: CollectionState) -> bool:
            return True

    def nest_quagmire_medium(self, state: CollectionState) -> bool:
        if self.world.options.logic_type == LogicType.option_intended:
            return self.small_elevation(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            return self.small_elevation(state) or self.air_rat_a_tat_rap(state) or self.beak_buster(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            return self.small_elevation(state) or self.air_rat_a_tat_rap(state) or self.clockwork_shot(state) or self.beak_buster(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            return self.small_elevation(state) or self.air_rat_a_tat_rap(state) or self.clockwork_shot(state) or self.beak_buster(state)

    def nest_mt_stadium(self, state: CollectionState) -> bool:
        if self.world.options.logic_type == LogicType.option_intended:
            return self.MT_flight_pad(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            return self.MT_flight_pad(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            return self.MT_flight_pad(state) or self.clockwork_shot(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            return self.MT_flight_pad(state) or self.clockwork_shot(state)

    def nest_pillars(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = (self.dive(state) or self.slightly_elevated_ledge(state) and self.tall_jump(state)) and self.prison_compound_as_banjo(state)\
                    or self.prison_compound_as_stony(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = (self.dive(state) or self.slightly_elevated_ledge(state) or self.beak_buster(state)) and self.prison_compound_as_banjo(state)\
                    or self.prison_compound_as_stony(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = (self.dive(state)\
                    or self.slightly_elevated_ledge(state)\
                    or self.beak_buster(state)\
                    or self.clockwork_shot(state)) and self.prison_compound_as_banjo(state)\
                    or self.prison_compound_as_stony(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = (self.dive(state)\
                    or self.slightly_elevated_ledge(state)\
                    or self.beak_buster(state)\
                    or self.clockwork_shot(state)) and self.prison_compound_as_banjo(state)\
                    or self.prison_compound_as_stony(state)
        return logic


    def nest_mt_cell_left(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = (self.slightly_elevated_ledge(state) or self.flap_flip(state)) and self.tall_jump(state) and self.prison_compound_as_banjo(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = (self.slightly_elevated_ledge(state) or self.flap_flip(state)) and self.prison_compound_as_banjo(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.prison_compound_as_banjo(state) and (self.slightly_elevated_ledge(state) or self.flap_flip(state) or self.clockwork_shot(state) and self.tall_jump(state))
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.prison_compound_as_banjo(state) and (self.slightly_elevated_ledge(state) or self.flap_flip(state) or self.clockwork_shot(state) and self.tall_jump(state))
        return logic

    def nest_mt_cell_right(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = (self.slightly_elevated_ledge(state) or self.flap_flip(state)) and self.tall_jump(state) and self.prison_compound_as_banjo(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = (self.slightly_elevated_ledge(state) or self.flap_flip(state)) and self.prison_compound_as_banjo(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.prison_compound_as_banjo(state) and (self.slightly_elevated_ledge(state) or self.flap_flip(state) or self.clockwork_shot(state))
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.prison_compound_as_banjo(state) and (self.slightly_elevated_ledge(state) or self.flap_flip(state) or self.clockwork_shot(state))
        return logic

    def nest_bill_drill(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.slightly_elevated_ledge(state) or self.flap_flip(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = ((self.talon_trot(state) or self.springy_step_shoes(state) or self.turbo_trainers(state)) and (self.flutter(state) or self.air_rat_a_tat_rap(state)) or self.tall_jump(state)) and self.grip_grab(state)\
                    or self.flap_flip(state)\
                    or self.GM_boulders(state) and self.split_up(state)\
                    or self.humbaGGM(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = ((self.talon_trot(state) or self.springy_step_shoes(state)) and (self.flutter(state) or self.air_rat_a_tat_rap(state)) or self.tall_jump(state)) and self.grip_grab(state)\
                    or self.flap_flip(state)\
                    or self.turbo_trainers(state)\
                    or self.clockwork_shot(state)\
                    or self.GM_boulders(state) and self.split_up(state)\
                    or self.humbaGGM(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = ((self.talon_trot(state) or self.springy_step_shoes(state)) and (self.flutter(state) or self.air_rat_a_tat_rap(state)) or self.tall_jump(state)) and self.grip_grab(state)\
                    or self.flap_flip(state)\
                    or self.turbo_trainers(state)\
                    or self.clockwork_shot(state)\
                    or self.GM_boulders(state) and self.split_up(state)\
                    or self.humbaGGM(state)
        return logic

    def nest_flooded_caves(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.humbaGGM(state) and self.dive(state)

        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.dive(state)\
                    and (self.humbaGGM(state)\
                        or self.talon_trot(state) and (self.flutter(state) or self.air_rat_a_tat_rap(state))\
                        or self.roll(state) and self.tall_jump(state) and (self.flutter(state) or self.air_rat_a_tat_rap(state)))

        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.dive(state)\
                    and (self.humbaGGM(state)\
                        or self.talon_trot(state) and (self.flutter(state) or self.air_rat_a_tat_rap(state))\
                        or self.roll(state) and self.tall_jump(state) and (self.flutter(state) or self.air_rat_a_tat_rap(state)))

        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.dive(state)\
                    and (self.humbaGGM(state)\
                        or self.talon_trot(state) and (self.flutter(state) or self.air_rat_a_tat_rap(state))\
                        or self.roll(state) and self.tall_jump(state) and (self.flutter(state) or self.air_rat_a_tat_rap(state)))
        return logic

    def nest_outside_power_hut(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.GM_boulders(state) and self.small_elevation(state)

        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.GM_boulders(state) and (\
                        self.small_elevation(state)\
                        or self.beak_buster(state)\
                        or self.turbo_trainers(state)\
                        or self.split_up(state))

        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.GM_boulders(state) and (\
                        self.small_elevation(state)\
                        or self.beak_buster(state)\
                        or self.turbo_trainers(state)\
                        or self.split_up(state)\
                        or self.clockwork_shot(state)
                    )

        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.GM_boulders(state) and (\
                        self.small_elevation(state)\
                        or self.beak_buster(state)\
                        or self.turbo_trainers(state)\
                        or self.split_up(state)\
                        or self.clockwork_shot(state)
                    )
        return logic

    def nest_ggm_mumbo(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.small_elevation(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.small_elevation(state) or self.grip_grab(state) or self.beak_buster(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.small_elevation(state) or self.grip_grab(state) or self.clockwork_shot(state) or self.beak_buster(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.small_elevation(state) or self.grip_grab(state) or self.clockwork_shot(state) or self.beak_buster(state)
        return logic

    def nest_toxic_gas_cave(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.GM_boulders(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.GM_boulders(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.GM_boulders(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.GM_boulders(state) or self.ground_rat_a_tat_rap(state) or self.beak_barge(state) or self.egg_barge(state)
        return logic

    def nest_canary_low(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.humbaGGM(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.humbaGGM(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.humbaGGM(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.humbaGGM(state)
        return logic

    def nest_canary_high(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.humbaGGM(state) and (self.small_elevation(state) or self.grip_grab(state))
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.humbaGGM(state) and (self.small_elevation(state) or self.grip_grab(state))
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.humbaGGM(state) and (self.small_elevation(state) or self.grip_grab(state) or self.clockwork_shot(state))
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.humbaGGM(state) and (self.small_elevation(state) or self.grip_grab(state) or self.clockwork_shot(state))
        return logic

    def nest_pump_room(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = (self.flap_flip(state)\
                        or self.leg_spring(state)\
                        or self.split_up(state) and self.grip_grab(state)
                    ) and self.has_explosives(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = (self.flap_flip(state)\
                        or self.leg_spring(state)\
                        or self.split_up(state) and self.grip_grab(state)\
                        or self.pack_whack(state) and self.tall_jump(state)\
                    ) and self.has_explosives(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = (self.flap_flip(state)\
                    or self.leg_spring(state)\
                    or self.split_up(state) and self.grip_grab(state)\
                    or self.pack_whack(state) and self.tall_jump(state)\
                    or self.clockwork_shot(state) and self.small_elevation(state)
                    ) and self.has_explosives(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = (self.flap_flip(state)\
                    or self.leg_spring(state)\
                    or self.split_up(state) and self.grip_grab(state)\
                    or self.pack_whack(state) and self.tall_jump(state)\
                    or self.clockwork_shot(state) and self.small_elevation(state)
                    ) and self.has_explosives(state)
        return logic

    def nest_big_top(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.grenade_eggs_item(state) and self.airborne_egg_aiming(state) and self.can_kill_fruity(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.grenade_eggs_item(state) and self.airborne_egg_aiming(state) and self.can_kill_fruity(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.grenade_eggs_item(state) and self.airborne_egg_aiming(state) and self.can_kill_fruity(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.grenade_eggs_item(state) and self.airborne_egg_aiming(state) and self.can_kill_fruity(state)
        return logic

    def nest_jolly_gunpowder(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.dive(state) or self.grenade_eggs(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.dive(state) or self.has_explosives(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.dive(state) or self.has_explosives(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.dive(state) or self.has_explosives(state)
        return logic

    def nest_seaweed_bottom(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.flap_flip(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.flap_flip(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.flap_flip(state)\
                    or self.clockwork_shot(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.flap_flip(state)\
                    or self.clockwork_shot(state)
        return logic

    def nest_seaweed_others(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.tall_jump(state) and self.grip_grab(state) and (
                        self.flap_flip(state)\
                        or (self.tall_jump(state) or self.talon_trot(state) and self.flutter(state)) and self.grip_grab(state)
                    )
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.tall_jump(state) and self.grip_grab(state) and (
                        self.flap_flip(state)\
                        or (self.tall_jump(state) or self.talon_trot(state) and self.flutter(state)) and self.grip_grab(state)
                    )\
                    or state.can_reach_region(regionName.JRBFC, self.player) and (self.flutter(state) or self.air_rat_a_tat_rap(state))
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.tall_jump(state) and self.grip_grab(state) and (
                        self.flap_flip(state)\
                        or (self.tall_jump(state) or self.talon_trot(state) and self.flutter(state)) and self.grip_grab(state)\
                        or self.clockwork_shot(state)
                    )\
                    or state.can_reach_region(regionName.JRBFC, self.player) and (
                        self.flutter(state) or self.air_rat_a_tat_rap(state)\
                        or self.clockwork_shot(state)
                    )
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.tall_jump(state) and self.grip_grab(state) and (
                        self.flap_flip(state)\
                        or (self.tall_jump(state) or self.talon_trot(state) and self.flutter(state)) and self.grip_grab(state)\
                        or self.clockwork_shot(state)
                    )\
                    or state.can_reach_region(regionName.JRBFC, self.player) and (
                        self.flutter(state) or self.air_rat_a_tat_rap(state)\
                        or self.clockwork_shot(state)
                    )
        return logic

    def nest_seaweed_top(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.grip_grab(state) and self.flap_flip(state) and (
                self.tall_jump(state) and self.grip_grab(state)\
                or state.can_reach_region(regionName.JRBFC, self.player)
            )
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = (self.grip_grab(state) or self.beak_buster(state)) and self.flap_flip(state)\
                    and (
                        (self.slightly_elevated_ledge(state) or self.flap_flip(state))\
                            and self.tall_jump(state)\
                            and (self.beak_buster(state) or self.grip_grab(state))
                        or state.can_reach_region(regionName.JRBFC, self.player)
                    )
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = ((self.grip_grab(state) or self.beak_buster(state)) and self.flap_flip(state)\
                        or self.clockwork_shot(state))\
                    and (
                        (self.slightly_elevated_ledge(state) or self.flap_flip(state))\
                            and self.tall_jump(state)\
                            and (self.beak_buster(state) or self.grip_grab(state))
                        or state.can_reach_region(regionName.JRBFC, self.player)
                    )
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = ((self.grip_grab(state) or self.beak_buster(state)) and self.flap_flip(state)\
                        or self.clockwork_shot(state))\
                    and (
                        (self.slightly_elevated_ledge(state) or self.flap_flip(state))\
                            and self.tall_jump(state)\
                            and (self.beak_buster(state) or self.grip_grab(state))
                        or state.can_reach_region(regionName.JRBFC, self.player)
                    )
        return logic

    def nest_bacon(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.sub_aqua_egg_aiming(state) and self.has_linear_egg(state)\
                    or self.humbaJRL(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.sub_aqua_egg_aiming(state) and self.has_linear_egg(state)\
                    or self.humbaJRL(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.sub_aqua_egg_aiming(state) and self.has_linear_egg(state)\
                    or self.humbaJRL(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.sub_aqua_egg_aiming(state) and self.has_linear_egg(state)\
                    or self.humbaJRL(state)
        return logic

    def nest_lord_woo(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = (state.has(itemName.MUMBOJR, self.player) or self.humbaJRL(state))\
                        and self.grenade_eggs(state) and self.sub_aqua_egg_aiming(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = (state.has(itemName.MUMBOJR, self.player) or self.doubleAir(state) or self.humbaJRL(state))\
                        and self.grenade_eggs(state) and self.sub_aqua_egg_aiming(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.grenade_eggs(state) and self.sub_aqua_egg_aiming(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.grenade_eggs(state) and self.sub_aqua_egg_aiming(state)
        return logic

    def nest_tdl_waterfall_alcove(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.flap_flip(state) and self.grip_grab(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.flap_flip(state) and self.grip_grab(state)\
                    or self.flutter(state)\
                    or self.air_rat_a_tat_rap(state)\
                    or self.split_up(state)\
                    or self.humbaTDL(state) and self.roar(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
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
        elif self.world.options.logic_type == LogicType.option_glitches:
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
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.small_elevation(state)\
                    or state.can_reach_region(regionName.CHUFFY, self.player) and state.has(itemName.CHUFFY, self.player) and state.has(itemName.TRAINSWTD, self.player)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.small_elevation(state)\
                    or self.turbo_trainers(state)\
                    or self.springy_step_shoes(state)\
                    or state.can_reach_region(regionName.CHUFFY, self.player) and state.has(itemName.CHUFFY, self.player) and state.has(itemName.TRAINSWTD, self.player)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = True
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = True
        return logic

    def nest_tdl_wall_with_holes(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.talon_trot(state) or self.tall_jump(state) and self.grip_grab(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.talon_trot(state)\
                    or self.tall_jump(state) and self.grip_grab(state)\
                    or self.humbaTDL(state)\
                    or self.leg_spring(state)\
                    or self.glide(state)\
                    or self.pack_whack(state)\
                    or self.springy_step_shoes(state)\
                    or self.turbo_trainers(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.talon_trot(state)\
                    or self.tall_jump(state) and self.grip_grab(state)\
                    or self.humbaTDL(state)\
                    or self.leg_spring(state)\
                    or self.glide(state)\
                    or self.pack_whack(state)\
                    or self.sack_pack(state)\
                    or self.springy_step_shoes(state)\
                    or self.turbo_trainers(state)\
                    or self.clockwork_shot(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.talon_trot(state)\
                    or self.tall_jump(state) and self.grip_grab(state)\
                    or self.humbaTDL(state)\
                    or self.leg_spring(state)\
                    or self.glide(state)\
                    or self.pack_whack(state)\
                    or self.sack_pack(state)\
                    or self.springy_step_shoes(state)\
                    or self.turbo_trainers(state)\
                    or self.clockwork_shot(state)
        return logic

    def nest_river_passage_entrance(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.tall_jump(state) or self.grip_grab(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.tall_jump(state)\
                    or self.grip_grab(state)\
                    or self.pack_whack(state)\
                    or self.wing_whack(state)\
                    or self.glide(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.tall_jump(state)\
                    or self.grip_grab(state)\
                    or self.pack_whack(state)\
                    or self.wing_whack(state)\
                    or self.glide(state)\
                    or self.clockwork_shot(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.tall_jump(state)\
                    or self.grip_grab(state)\
                    or self.pack_whack(state)\
                    or self.wing_whack(state)\
                    or self.glide(state)\
                    or self.clockwork_shot(state)
        return logic

    def nest_mountain_flight_pad(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.tall_jump(state) or self.grip_grab(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.tall_jump(state)\
                    or self.grip_grab(state)\
                    or self.beak_buster(state)\
                    or self.leg_spring(state) and self.glide(state)\
                    or state.can_reach_region(regionName.TLTOP, self.player) and self.split_up(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.tall_jump(state)\
                    or self.grip_grab(state)\
                    or self.beak_buster(state)\
                    or self.leg_spring(state) and self.glide(state)\
                    or state.can_reach_region(regionName.TLTOP, self.player) and self.split_up(state)\
                    or self.clockwork_shot(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.tall_jump(state)\
                    or self.grip_grab(state)\
                    or self.beak_buster(state)\
                    or self.leg_spring(state) and self.glide(state)\
                    or state.can_reach_region(regionName.TLTOP, self.player) and self.split_up(state)\
                    or self.clockwork_shot(state)
        return logic

    def nest_mountain_underwater(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.dive(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.dive(state) or self.humbaTDL(state) or self.shack_pack(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.dive(state) or self.humbaTDL(state) or self.shack_pack(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.dive(state) or self.humbaTDL(state) or self.shack_pack(state)
        return logic

    def nest_river_passage(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.tall_jump(state) and self.grip_grab(state) and (self.flap_flip(state) or self.split_up(state))
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.tall_jump(state) and self.grip_grab(state) and (self.flap_flip(state) or self.split_up(state))\
                    or self.leg_spring(state) and self.glide(state)\
                    or self.pack_whack(state) and self.tall_jump(state)\
                    or self.pack_whack(state) and self.grip_grab(state)\
                    or self.sack_pack(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.tall_jump(state) and self.grip_grab(state) and (self.flap_flip(state) or self.split_up(state))\
                    or self.leg_spring(state) and self.glide(state)\
                    or self.pack_whack(state) and self.tall_jump(state)\
                    or self.pack_whack(state) and self.grip_grab(state)\
                    or self.sack_pack(state)\
                    or self.clockwork_shot(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.tall_jump(state) and self.grip_grab(state) and (self.flap_flip(state) or self.split_up(state))\
                    or self.leg_spring(state) and self.glide(state)\
                    or self.pack_whack(state) and self.tall_jump(state)\
                    or self.pack_whack(state) and self.grip_grab(state)\
                    or self.sack_pack(state)\
                    or self.clockwork_shot(state)
        return logic

    def nest_unga_egg(self, state: CollectionState) -> bool:
        return state.can_reach_region(regionName.MT, self.player) and self.jiggy_treasure_chamber(state)\
               or self.small_elevation(state)

    def nest_gi_outside_right(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = state.can_reach_region(regionName.GIO, self.player) and self.outside_gi_to_outside_back(state)\
                    or state.can_reach_region(regionName.GIOB, self.player) and self.climb(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = state.can_reach_region(regionName.GIO, self.player) and self.outside_gi_to_outside_back(state)\
                    or state.can_reach_region(regionName.GIOB, self.player) and self.climb(state)\
                    or state.can_reach_region(regionName.GI1, self.player) and (self.split_up(state) and self.tall_jump(state) or self.leg_spring(state))\
                    or state.can_reach_region(regionName.GI2, self.player) and (self.floor_2_split_up(state) and (self.tall_jump(state) or self.leg_spring(state)))\
                    or state.can_reach_region(regionName.GIF, self.player)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = state.can_reach_region(regionName.GIO, self.player) and self.outside_gi_to_outside_back(state)\
                    or state.can_reach_region(regionName.GIOB, self.player) and self.climb(state)\
                    or state.can_reach_region(regionName.GI1, self.player) and (self.split_up(state) and self.tall_jump(state) or self.leg_spring(state))\
                    or state.can_reach_region(regionName.GI2, self.player) and (self.floor_2_split_up(state) and (self.tall_jump(state) or self.leg_spring(state)))\
                    or state.can_reach_region(regionName.GIF, self.player)\
                    or self.clockwork_shot(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = state.can_reach_region(regionName.GIO, self.player) and self.outside_gi_to_outside_back(state)\
                    or state.can_reach_region(regionName.GIOB, self.player) and self.climb(state)\
                    or state.can_reach_region(regionName.GI1, self.player) and (self.split_up(state) and self.tall_jump(state) or self.leg_spring(state))\
                    or state.can_reach_region(regionName.GI2, self.player) and (self.floor_2_split_up(state) and (self.tall_jump(state) or self.leg_spring(state)))\
                    or state.can_reach_region(regionName.GIF, self.player)\
                    or self.clockwork_shot(state)
        return logic

    def nest_gi_outside_left(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.climb(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.climb(state)\
                    or state.can_reach_region(regionName.GI1, self.player) and self.leg_spring(state)\
                    or state.can_reach_region(regionName.GI2, self.player) and self.floor_2_split_up(state) and self.leg_spring(state)\
                    or state.can_reach_region(regionName.GIF, self.player)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.climb(state)\
                    or state.can_reach_region(regionName.GIOB, self.player) and self.claw_clamber_boots(state)\
                    or state.can_reach_region(regionName.GI1, self.player) and self.leg_spring(state)\
                    or state.can_reach_region(regionName.GI2, self.player) and self.floor_2_split_up(state) and self.leg_spring(state)\
                    or state.can_reach_region(regionName.GIF, self.player)\
                    or self.clockwork_shot(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.climb(state)\
                    or state.can_reach_region(regionName.GIOB, self.player) and self.claw_clamber_boots(state)\
                    or state.can_reach_region(regionName.GI1, self.player) and self.leg_spring(state)\
                    or state.can_reach_region(regionName.GI2, self.player) and self.floor_2_split_up(state) and self.leg_spring(state)\
                    or state.can_reach_region(regionName.GIF, self.player)\
                    or self.clockwork_shot(state)
        return logic

    def nest_gi_floor1_top_pipe(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.split_up(state) and self.claw_clamber_boots(state) and (self.spring_pad(state) or self.wing_whack(state) or (self.egg_aim(state) and self.glide(state)))
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.split_up(state) and\
                    ((self.claw_clamber_boots(state) or state.can_reach_region(regionName.GI2, self.player)) and self.spring_pad(state)\
                        or self.claw_clamber_boots(state) and (self.wing_whack(state) or self.glide(state)) and (self.egg_aim(state) or self.wing_whack(state)))
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.split_up(state) and\
                    ((self.claw_clamber_boots(state) or state.can_reach_region(regionName.GI2, self.player)) and self.spring_pad(state)\
                        or self.claw_clamber_boots(state) and (self.wing_whack(state) or self.glide(state)) and (self.egg_aim(state) or self.wing_whack(state)))
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.split_up(state) and\
                    ((self.claw_clamber_boots(state) or state.can_reach_region(regionName.GI2, self.player)) and self.spring_pad(state)\
                        or self.claw_clamber_boots(state) and (self.wing_whack(state) or self.glide(state)) and (self.egg_aim(state) or self.wing_whack(state)))
        return logic

    def nest_gi_floor1_high_pipe(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.claw_clamber_boots(state) and (self.leg_spring(state) or self.spring_pad(state))
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.claw_clamber_boots(state) and (self.leg_spring(state) or self.spring_pad(state))\
                    or state.can_reach_region(regionName.GI2, self.player) and (self.floor_2_split_up(state) and self.leg_spring(state) or self.F2_to_F1(state) and self.spring_pad(state))\
                    or self.claw_clamber_boots(state) and (self.wing_whack(state) or self.glide(state)) and (self.egg_aim(state) or self.wing_whack(state))
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.claw_clamber_boots(state) and (self.leg_spring(state) or self.spring_pad(state) or self.clockwork_shot(state))\
                    or state.can_reach_region(regionName.GI2, self.player) and (self.floor_2_split_up(state) and self.leg_spring(state) or self.F2_to_F1(state) and (self.spring_pad(state) or self.clockwork_shot(state)))\
                    or self.claw_clamber_boots(state) and (self.wing_whack(state) or self.glide(state)) and (self.egg_aim(state) or self.wing_whack(state))
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.claw_clamber_boots(state) and (self.leg_spring(state) or self.spring_pad(state) or self.clockwork_shot(state))\
                    or state.can_reach_region(regionName.GI2, self.player) and (self.floor_2_split_up(state) and self.leg_spring(state) or self.F2_to_F1(state) and (self.spring_pad(state) or self.clockwork_shot(state)))\
                    or self.claw_clamber_boots(state) and (self.wing_whack(state) or self.glide(state)) and (self.egg_aim(state) or self.wing_whack(state))
        return logic

    def nest_gi_outside_waste_disposal(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.slightly_elevated_ledge(state) or self.split_up(state) or self.flap_flip(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.slightly_elevated_ledge(state) or self.split_up(state) or self.flap_flip(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.slightly_elevated_ledge(state) or self.split_up(state) or self.clockwork_shot(state) or self.flap_flip(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.slightly_elevated_ledge(state) or self.split_up(state) or self.clockwork_shot(state) or self.flap_flip(state)
        return logic

    def nest_outside_trash_compactor(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.snooze_pack(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = True # You have to get crushed anyway in the intended strat. Is it fair that doing it without snooze pack is in easy tricks?
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = True
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = True
        return logic

    def nest_gi_train_station_small_box(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.small_elevation(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = True
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = True
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = True
        return logic

    def nest_gi_train_station_medium_box(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.slightly_elevated_ledge(state)\
                    or self.flap_flip(state)\
                    or self.leg_spring(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.slightly_elevated_ledge(state)\
                    or self.flap_flip(state)\
                    or self.split_up(state)\
                    or self.flutter(state)\
                    or self.air_rat_a_tat_rap(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.slightly_elevated_ledge(state)\
                    or self.flap_flip(state)\
                    or self.split_up(state)\
                    or self.flutter(state)\
                    or self.air_rat_a_tat_rap(state)\
                    or self.clockwork_shot(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.slightly_elevated_ledge(state)\
                    or self.flap_flip(state)\
                    or self.split_up(state)\
                    or self.flutter(state)\
                    or self.air_rat_a_tat_rap(state)\
                    or self.clockwork_shot(state)
        return logic

    def nest_trash_compactor(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.snooze_pack(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.snooze_pack(state)\
                    or self.split_up(state) and self.tall_jump(state)\
                    or self.wing_whack(state)\
                    or self.glide(state)\
                    or self.leg_spring(state)\
                    or self.flap_flip(state)\
                    or self.clockwork_eggs(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.snooze_pack(state)\
                    or self.split_up(state) and self.tall_jump(state)\
                    or self.wing_whack(state)\
                    or self.glide(state)\
                    or self.leg_spring(state)\
                    or self.clockwork_eggs(state)\
                    or self.flap_flip(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.snooze_pack(state)\
                    or self.split_up(state) and self.tall_jump(state)\
                    or self.wing_whack(state)\
                    or self.glide(state)\
                    or self.leg_spring(state)\
                    or self.clockwork_eggs(state)\
                    or self.flap_flip(state)
        return logic

    def nest_elevator_shaft_floor2(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.climb(state)\
                    or state.can_reach_region(regionName.GI2EM, self.player) and self.floor_2_em_room_to_elevator_shaft(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.climb(state)\
                    or state.can_reach_region(regionName.GI2EM, self.player) and self.floor_2_em_room_to_elevator_shaft(state)\
                    or state.can_reach_region(regionName.GI3B, self.player) and self.boiler_plant_to_elevator_shaft(state) and self.beak_buster(state)\
                    or state.can_reach_region(regionName.GI4B, self.player) and self.floor_4_back_to_elevator_shaft(state) and self.beak_buster(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.climb(state)\
                    or state.can_reach_region(regionName.GI2EM, self.player) and self.floor_2_em_room_to_elevator_shaft(state)\
                    or state.can_reach_region(regionName.GI3B, self.player) and self.boiler_plant_to_elevator_shaft(state)\
                    or state.can_reach_region(regionName.GI4B, self.player) and (self.health_7(state) or self.beak_buster(state)) and self.floor_4_back_to_elevator_shaft(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.climb(state)\
                    or state.can_reach_region(regionName.GI2EM, self.player) and self.floor_2_em_room_to_elevator_shaft(state)\
                    or state.can_reach_region(regionName.GI3B, self.player) and self.boiler_plant_to_elevator_shaft(state)\
                    or state.can_reach_region(regionName.GI4B, self.player) and (self.health_7(state) or self.beak_buster(state)) and self.floor_4_back_to_elevator_shaft(state)
        return logic

    def nest_elevator_shaft_floor3(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.climb(state)\
                    or state.can_reach_region(regionName.GI3B, self.player) and self.boiler_plant_to_elevator_shaft(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.climb(state)\
                    or state.can_reach_region(regionName.GI3B, self.player) and self.boiler_plant_to_elevator_shaft(state)\
                    or state.can_reach_region(regionName.GI4B, self.player) and self.floor_4_back_to_elevator_shaft(state) and self.beak_buster(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.climb(state)\
                    or state.can_reach_region(regionName.GI3B, self.player) and self.boiler_plant_to_elevator_shaft(state)\
                    or state.can_reach_region(regionName.GI4B, self.player) and self.floor_4_back_to_elevator_shaft(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.climb(state)\
                    or state.can_reach_region(regionName.GI3B, self.player) and self.boiler_plant_to_elevator_shaft(state)\
                    or state.can_reach_region(regionName.GI4B, self.player) and self.floor_4_back_to_elevator_shaft(state)
        return logic

    def nest_elevator_shaft_floor4(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.climb(state)\
                    or state.can_reach_region(regionName.GI4B, self.player) and self.floor_4_back_to_elevator_shaft(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.climb(state)\
                    or state.can_reach_region(regionName.GI4B, self.player) and self.floor_4_back_to_elevator_shaft(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.climb(state)\
                    or state.can_reach_region(regionName.GI4B, self.player) and self.floor_4_back_to_elevator_shaft(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.climb(state)\
                    or state.can_reach_region(regionName.GI4B, self.player) and self.floor_4_back_to_elevator_shaft(state)
        return logic

    def nest_funny_platform(self, state: CollectionState) -> bool:
        if self.world.options.logic_type == LogicType.option_intended:
            logic = state.can_reach_region(regionName.GI2, self.player) and self.claw_clamber_boots(state) and self.flap_flip(state) and self.grip_grab(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = state.can_reach_region(regionName.GI2, self.player) and self.claw_clamber_boots(state) and (self.flap_flip(state) and self.grip_grab(state))\
                    or state.can_reach_region(regionName.GI2, self.player) and self.solo_kazooie_gi(state)\
                        and (self.leg_spring(state) or self.claw_clamber_boots(state) and (self.can_shoot_any_egg(state) or self.wing_whack(state)))\
                        and self.glide(state)\
                    or state.can_reach_region(regionName.GI3, self.player) and\
                        self.climb(state) and (self.veryLongJump(state) or self.flap_flip(state) or self.tall_jump(state)) and self.grip_grab(state)\
                    or state.can_reach_region(regionName.GI3, self.player) and self.small_elevation(state)\
                        and self.split_up(state) and self.leg_spring(state) and self.glide(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = state.can_reach_region(regionName.GI2, self.player) and self.claw_clamber_boots(state)\
                        and ((self.flap_flip(state) and self.grip_grab(state))\
                             or self.talon_trot(state) and (self.flutter(state) or self.air_rat_a_tat_rap(state)))\
                    or state.can_reach_region(regionName.GI2, self.player) and self.solo_kazooie_gi(state)\
                        and (self.leg_spring(state) or self.claw_clamber_boots(state) and (self.can_shoot_any_egg(state) or self.wing_whack(state)))\
                        and self.glide(state)\
                    or state.can_reach_region(regionName.GI3, self.player) and\
                        self.climb(state) and (self.veryLongJump(state) or self.flap_flip(state) or self.tall_jump(state)) and self.grip_grab(state)\
                    or state.can_reach_region(regionName.GI3, self.player) and self.small_elevation(state)\
                        and self.split_up(state) and self.leg_spring(state) and self.glide(state)\
                    or self.clockwork_shot(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = state.can_reach_region(regionName.GI2, self.player) and self.claw_clamber_boots(state)\
                        and ((self.flap_flip(state) and self.grip_grab(state))\
                             or self.talon_trot(state) and (self.flutter(state) or self.air_rat_a_tat_rap(state)))\
                    or state.can_reach_region(regionName.GI2, self.player) and self.solo_kazooie_gi(state)\
                        and (self.leg_spring(state) or self.claw_clamber_boots(state) and (self.can_shoot_any_egg(state) or self.wing_whack(state)))\
                        and self.glide(state)\
                    or state.can_reach_region(regionName.GI3, self.player) and\
                        self.climb(state) and (self.veryLongJump(state) or self.flap_flip(state) or self.tall_jump(state)) and self.grip_grab(state)\
                    or state.can_reach_region(regionName.GI3, self.player) and self.small_elevation(state)\
                        and self.split_up(state) and self.leg_spring(state) and self.glide(state)\
                    or self.clockwork_shot(state)
        return logic

    def nest_magnet(self, state: CollectionState) -> bool:
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.tall_jump(state)\
                    or self.talon_trot(state)\
                    or self.flutter(state)\
                    or self.air_rat_a_tat_rap(state)\
                    or state.can_reach_region(regionName.GI2, self.player) and self.floor_2_to_em_room(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.tall_jump(state)\
                    or self.talon_trot(state)\
                    or self.flutter(state)\
                    or self.air_rat_a_tat_rap(state)\
                    or state.can_reach_region(regionName.GI2, self.player) and self.floor_2_to_em_room(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.tall_jump(state)\
                    or self.talon_trot(state)\
                    or self.flutter(state)\
                    or self.air_rat_a_tat_rap(state)\
                    or state.can_reach_region(regionName.GI2, self.player) and self.floor_2_to_em_room(state)\
                    or self.clockwork_shot(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.tall_jump(state)\
                    or self.talon_trot(state)\
                    or self.flutter(state)\
                    or self.air_rat_a_tat_rap(state)\
                    or state.can_reach_region(regionName.GI2, self.player) and self.floor_2_to_em_room(state)\
                    or self.clockwork_shot(state)
        return logic

    def nest_floor3_boxes(self, state: CollectionState) -> bool:
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.slightly_elevated_ledge(state) or self.small_elevation(state) and self.leg_spring(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.slightly_elevated_ledge(state) or self.small_elevation(state) and self.leg_spring(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.slightly_elevated_ledge(state) or self.clockwork_shot(state) or self.small_elevation(state) and self.leg_spring(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.slightly_elevated_ledge(state) or self.clockwork_shot(state) or self.small_elevation(state) and self.leg_spring(state)
        return logic

    def nest_floor3_shortcut(self, state: CollectionState) -> bool:
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.small_elevation(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.small_elevation(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.small_elevation(state) or self.clockwork_shot(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.small_elevation(state) or self.clockwork_shot(state)
        return logic

    def nest_floor4_front(self, state: CollectionState) -> bool:
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.small_elevation(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.small_elevation(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.small_elevation(state) or self.clockwork_shot(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.small_elevation(state) or self.clockwork_shot(state)
        return logic

    def nest_outside_QC(self, state: CollectionState) -> bool:
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.climb(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.climb(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.climb(state)\
                    or self.pack_whack(state) and self.tall_jump(state)\
                    or self.split_up(state) and (self.leg_spring(state) or self.spring_pad(state))
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.climb(state)\
                    or self.pack_whack(state) and self.tall_jump(state)\
                    or self.split_up(state) and (self.leg_spring(state) or self.spring_pad(state))\
                    or self.precise_clockwork_warp(state) and (self.spring_pad(state) or self.flap_flip(state))\
                    or state.can_reach_region(regionName.GIES, self.player) and self.elevator_shaft_to_floor_4(state)
        return logic

    def nest_quality_control(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.can_use_battery(state) and self.climb(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.can_use_battery(state) and self.climb(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.can_use_battery(state) and self.climb(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.can_use_battery(state) and self.climb(state)\
                    or self.precise_clockwork_warp(state) and (self.spring_pad(state) or self.flap_flip(state))
        return logic

    def nest_floor5_small_stack(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.small_elevation(state)\
                    or self.split_up(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.small_elevation(state)\
                    or self.split_up(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.small_elevation(state)\
                    or self.split_up(state)\
                    or self.clockwork_shot(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.small_elevation(state)\
                    or self.split_up(state)\
                    or self.clockwork_shot(state)
        return logic

    def nest_egg_fan_easy(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = (self.tall_jump(state) or self.flutter(state) or self.air_rat_a_tat_rap(state)) and self.climb(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.climb(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.climb(state)\
                    or self.leg_spring(state) and (self.wing_whack(state) or self.glide(state))
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.climb(state)\
                    or self.leg_spring(state) and (self.wing_whack(state) or self.glide(state))
        return logic

    # This one is a lot harder than the other ones!
    def nest_egg_fan_hard(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.can_beat_weldar(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.can_beat_weldar(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.can_beat_weldar(state)\
                    or (self.climb(state) or self.leg_spring(state) and (self.wing_whack(state) or self.glide(state))) and self.clockwork_shot(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.can_beat_weldar(state)\
                    or (self.climb(state) or self.leg_spring(state) and (self.wing_whack(state) or self.glide(state))) and self.clockwork_shot(state)
        return logic

    def nest_outside_repair_depot(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.flap_flip(state) and self.climb(state) and self.grip_grab(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.flap_flip(state) and self.climb(state) and (self.grip_grab(state)\
                        or (self.tall_jump(state) and (self.flutter(state) or self.air_rat_a_tat_rap(state))))
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.flap_flip(state) and self.climb(state) and (self.grip_grab(state)\
                        or (self.tall_jump(state) and (self.flutter(state) or self.air_rat_a_tat_rap(state))))\
                    or self.leg_spring(state) and (self.glide(state) or self.wing_whack(state))\
                    or self.clockwork_shot(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.flap_flip(state) and self.climb(state) and (self.grip_grab(state)\
                        or (self.tall_jump(state) and (self.flutter(state) or self.air_rat_a_tat_rap(state))))\
                    or self.leg_spring(state) and (self.glide(state) or self.wing_whack(state))\
                    or self.clockwork_shot(state)
        return logic

    def nest_waste_disposal_water_pump(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.jrl_waste_disposal(state) and self.flap_flip(state) and self.climb(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.jrl_waste_disposal(state) and self.flap_flip(state) and self.climb(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            #If someone finds a setup for a clockwork shot for these nests, I'll add it to the logic.
            logic = self.jrl_waste_disposal(state) and self.climb(state)\
                         and (self.flap_flip(state)\
                            or self.tall_jump(state) and self.flutter(state)\
                            or self.extremelyLongJump(state)\
                            or self.tall_jump(state) and self.beak_buster(state)\
                            or self.talon_trot(state) and self.flutter(state) and self.beak_buster(state)\
                        )
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.jrl_waste_disposal(state) and self.climb(state)\
                         and (self.flap_flip(state)\
                            or self.tall_jump(state) and self.flutter(state)\
                            or self.extremelyLongJump(state)\
                            or self.tall_jump(state) and self.beak_buster(state)\
                            or self.talon_trot(state) and self.flutter(state) and self.beak_buster(state)\
                        )
        return logic

    def jrl_waste_disposal(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = (self.has_explosives(state) or self.bill_drill(state))\
                        and (self.talon_trot(state)\
                             or self.tall_jump(state) and self.roll(state) and self.flutter(state)
                        )
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = (self.has_explosives(state) or self.bill_drill(state))\
                    and (self.talon_trot(state)\
                        or self.tall_jump(state) and self.roll(state) and self.flutter(state)\
                        or state.has(itemName.DOUBLOON, self.player, 28) and self.turbo_trainers(state)
                    )
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = (self.has_explosives(state) or self.bill_drill(state))\
                    and (self.talon_trot(state)\
                        or self.tall_jump(state) and self.roll(state) and self.flutter(state)\
                        or state.has(itemName.DOUBLOON, self.player, 28) and self.turbo_trainers(state)
                    )
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = (self.has_explosives(state) or self.bill_drill(state))\
                    and (self.talon_trot(state)\
                        or self.tall_jump(state) and self.roll(state) and self.flutter(state)\
                        or state.has(itemName.DOUBLOON, self.player, 28) and self.turbo_trainers(state)
                    )
        return logic

    def nest_clinkers_lobby(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.claw_clamber_boots(state) and self.climb(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.claw_clamber_boots(state) and self.climb(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.claw_clamber_boots(state) and self.climb(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.claw_clamber_boots(state)\
                    and (self.clockwork_warp(state) and (self.spring_pad(state) or self.flap_flip(state))\
                        or state.can_reach_region(regionName.GIES, self.player) and self.elevator_shaft_to_floor_4(state)\
                        or self.climb(state))
        return logic

    def nest_hfp_entrance_shelter(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.flight_pad(state) or self.leg_spring(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.flight_pad(state)\
                    or self.leg_spring(state)\
                    or self.glide(state)\
                    or self.tall_jump(state) and self.wing_whack(state)\
                    or self.flap_flip(state) and (self.grip_grab(state) or self.beak_buster(state))
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.flight_pad(state)\
                    or self.leg_spring(state)\
                    or self.glide(state)\
                    or self.clockwork_shot(state)\
                    or self.tall_jump(state) and self.wing_whack(state)\
                    or self.flap_flip(state) and (self.grip_grab(state) or self.beak_buster(state))
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.flight_pad(state)\
                    or self.leg_spring(state)\
                    or self.glide(state)\
                    or self.clockwork_shot(state)\
                    or self.tall_jump(state) and self.wing_whack(state)\
                    or self.flap_flip(state) and (self.grip_grab(state) or self.beak_buster(state))
        return logic

    def nest_ice_cube(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.ice_cube_BK(state) and self.hfp_top(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.hfp_top(state)\
                        and (self.ice_cube_BK(state)\
                             or self.split_up(state) and self.ice_cube_kazooie(state)\
                             or state.has(itemName.MUMBOHP, self.player)\
                             or self.pack_whack(state)\
                             or self.humbaHFP(state)
                             )
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.hfp_top(state)\
                        and (self.ice_cube_BK(state)\
                             or self.split_up(state) and self.ice_cube_kazooie(state)\
                             or state.has(itemName.MUMBOHP, self.player)\
                             or self.pack_whack(state)\
                             or self.humbaHFP(state)
                             )
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.hfp_top(state)\
                        and (self.ice_cube_BK(state)\
                             or self.split_up(state) and self.ice_cube_kazooie(state)\
                             or state.has(itemName.MUMBOHP, self.player)\
                             or self.pack_whack(state)\
                             or self.humbaHFP(state)
                             )
        return logic

    def nest_icy_side_train_station_easy(self, state: CollectionState) -> bool:
        return self.jiggy_ice_station(state)

    def nest_icy_side_train_station_hard(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.can_beat_king_coal(state) and self.grenade_eggs(state) and \
                    state.has(itemName.TRAINSWHP1, self.player) and state.has(itemName.TRAINSWHP2, self.player) and \
                    self.egg_aim(state) and state.can_reach_region(regionName.WW, self.player)\
                    and self.flight_pad(state) and self.dive(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.can_beat_king_coal(state) and self.grenade_eggs(state) and \
                    state.has(itemName.TRAINSWHP1, self.player) and state.has(itemName.TRAINSWHP2, self.player) and \
                    state.can_reach_region(regionName.WW, self.player)\
                    and self.flight_pad(state) and (self.beak_buster(state) or self.dive(state))
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.can_beat_king_coal(state) and self.grenade_eggs(state) and \
                    state.has(itemName.TRAINSWHP1, self.player) and state.has(itemName.TRAINSWHP2, self.player) and \
                    state.can_reach_region(regionName.WW, self.player)\
                    and self.flight_pad(state) and (self.beak_buster(state) or self.dive(state))
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.can_beat_king_coal(state) and self.grenade_eggs(state) and \
                    state.has(itemName.TRAINSWHP1, self.player) and state.has(itemName.TRAINSWHP2, self.player) and \
                    state.can_reach_region(regionName.WW, self.player)\
                    and self.flight_pad(state) and (self.beak_buster(state) or self.dive(state))
        return logic

    def nest_hfp_spring_pad(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.hfp_top(state) and self.spring_pad(state) and self.talon_trot(state) and self.ice_cube_BK(state)\
                    or self.hfp_top(state) and self.spring_pad(state) and self.split_up(state) and self.ice_cube_kazooie(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = (self.split_up(state) and self.ice_cube_kazooie(state) and (self.tall_jump(state) or self.wing_whack(state) or self.glide(state) or self.leg_spring(state)))\
                    or (self.hfp_top(state) and self.spring_pad(state) and self.talon_trot(state) and self.ice_cube_BK(state))
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = (self.split_up(state) and self.ice_cube_kazooie(state) and (self.tall_jump(state) or self.wing_whack(state) or self.glide(state) or self.leg_spring(state)))\
                    or (self.hfp_top(state) and (self.spring_pad(state) and self.ice_cube_BK(state) or self.clockwork_shot(state)) and self.talon_trot(state))\
                    or (self.extremelyLongJump(state) and self.clockwork_shot(state))
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = (self.split_up(state) and self.ice_cube_kazooie(state) and (self.tall_jump(state) or self.wing_whack(state) or self.glide(state) or self.leg_spring(state)))\
                    or (self.hfp_top(state) and (self.spring_pad(state) and self.ice_cube_BK(state) or self.clockwork_shot(state)) and self.talon_trot(state))\
                    or (self.extremelyLongJump(state) and self.clockwork_shot(state))
        return logic

    def nest_ccl_flight(self, state: CollectionState) -> bool:
        return self.flight_pad(state) or state.has(itemName.HUMBACC, self.player)

    def nest_jelly_castle(self, state: CollectionState) -> bool:
        return self.nest_ccl_flight(state)\
                or self.climb(state) and (self.small_elevation(state) or self.split_up(state))

    def nest_ccl_dippy(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.nest_ccl_flight(state) or self.dive(state) and self.talon_torpedo(state) and self.flap_flip(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = True # Slide from pot of gold token pile
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = True
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = True
        return logic

    def nest_outside_trash_can(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.climb(state) and self.tall_jump(state) or self.nest_ccl_flight(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.climb(state) and (self.tall_jump(state) or self.pack_whack(state))\
                    or (self.flight_pad(state) or self.glide(state))\
                    or self.nest_ccl_flight(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.climb(state) and (self.tall_jump(state) or self.pack_whack(state))\
                    or (self.flight_pad(state) or self.glide(state) or ((self.tall_jump(state) or self.leg_spring(state)) and self.wing_whack(state)))\
                    or self.nest_ccl_flight(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.climb(state) and (self.tall_jump(state) or self.pack_whack(state))\
                    or (self.flight_pad(state) or self.glide(state) or ((self.tall_jump(state) or self.leg_spring(state)) and self.wing_whack(state)))\
                    or self.nest_ccl_flight(state)
        return logic

    def nest_inside_trash_can(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.flight_pad(state) and self.leg_spring(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.climb(state) and self.shack_pack(state) and self.pack_whack(state)\
                    or self.split_up(state)\
                        and (self.flight_pad(state) or self.glide(state) or (self.leg_spring(state) and self.wing_whack(state)))\
                        and self.leg_spring(state)

        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.climb(state) and self.shack_pack(state) and (self.pack_whack(state) or self.tall_jump(state) and self.grip_grab(state))\
                    or self.split_up(state)\
                        and (self.flight_pad(state) or self.glide(state) or (self.leg_spring(state) and self.wing_whack(state)))\
                        and (self.leg_spring(state) or (self.glide(state) and self.tall_jump(state) or self.clockwork_shot(state)))

        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.climb(state) and self.shack_pack(state) and (self.pack_whack(state) or self.tall_jump(state) and self.grip_grab(state))\
                    or self.split_up(state)\
                        and (self.flight_pad(state) or self.glide(state) or (self.leg_spring(state) and self.wing_whack(state)))\
                        and (self.leg_spring(state) or (self.glide(state) and self.tall_jump(state) or self.clockwork_shot(state)))\
                    or self.flight_pad(state) and self.clockwork_warp(state) and self.climb(state)
        return logic

    def nest_near_superstash(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.grip_grab(state) and self.flap_flip(state) or state.has(itemName.HUMBACC, self.player)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.flap_flip(state) and self.grip_grab(state) or self.veryLongJump(state) and (self.climb(state) or self.flight_pad(state))\
                    or state.has(itemName.HUMBACC, self.player)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.flap_flip(state) and self.grip_grab(state) or self.veryLongJump(state) and (self.climb(state) or self.flight_pad(state))\
                    or self.clockwork_shot(state)\
                    or state.has(itemName.HUMBACC, self.player)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.flap_flip(state) and self.grip_grab(state) or self.veryLongJump(state) and (self.climb(state) or self.flight_pad(state))\
                    or self.clockwork_shot(state)\
                    or state.has(itemName.HUMBACC, self.player)
        return logic

    def nest_pot_of_gold(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.mumboCCL(state) and (self.flap_flip(state) or self.leg_spring(state))
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.mumboCCL(state) and (self.flap_flip(state) or self.leg_spring(state) or self.flight_pad(state))
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = (self.mumboCCL(state) and (self.flap_flip(state) or self.leg_spring(state) or self.flight_pad(state))\
                     or (self.leg_spring(state) or (self.split_up(state) and self.tall_jump(state))) and self.flight_pad(state) and self.beak_bomb(state))
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = (self.mumboCCL(state) and (self.flap_flip(state) or self.leg_spring(state) or self.flight_pad(state))\
                     or (self.leg_spring(state) or (self.split_up(state) and self.tall_jump(state))) and self.flight_pad(state) and self.beak_bomb(state))
        return logic

    def nest_chilly_willy(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.fire_eggs(state) and self.claw_clamber_boots(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.fire_eggs(state) and self.claw_clamber_boots(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            # In case people go for the damage boost for Chilly Willy then die before getting the jiggy, we also require Pack Whack to prevent softlocks.
            logic = self.claw_clamber_boots(state)\
                     or (self.pack_whack(state) and self.tall_jump(state) and self.flutter(state) and \
                         (self.talon_trot(state) or self.flap_flip(state)))
        elif self.world.options.logic_type == LogicType.option_glitches:
            # In case people go for the damage boost for Chilly Willy then die before getting the jiggy, we also require Pack Whack to prevent softlocks.
            logic = self.claw_clamber_boots(state)\
                     or (self.pack_whack(state) and self.tall_jump(state) and self.flutter(state) and \
                         (self.talon_trot(state) or self.flap_flip(state)))
        return logic

    def nest_hfp_kickball_egg(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.long_jump(state) and self.small_elevation(state) and self.has_explosives(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.long_jump(state) and self.small_elevation(state) and self.has_explosives(state)\
                    or state.has(itemName.MUMBOHP, self.player) and self.tall_jump(state)\
                    or self.long_jump(state) and self.dragon_kazooie(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.has_explosives(state) or state.has(itemName.MUMBOHP, self.player)\
                    or self.dragon_kazooie(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.has_explosives(state) or state.has(itemName.MUMBOHP, self.player)\
                    or self.dragon_kazooie(state)
        return logic

    def nest_hfp_kickball_feather(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.long_jump(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.long_jump(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = True
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = True
        return logic

    def nest_stomping_plains_footprint(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.tall_jump(state) and self.split_up(state)\
                    or self.snooze_pack(state)\
                    or self.talon_trot(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.tall_jump(state) and self.split_up(state)\
                    or self.snooze_pack(state)\
                    or self.talon_trot(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.tall_jump(state) and self.split_up(state)\
                    or self.snooze_pack(state)\
                    or self.talon_trot(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.tall_jump(state) and self.split_up(state)\
                    or self.snooze_pack(state)\
                    or self.talon_trot(state)
        return logic

    def signpost_jiggywiggy_back(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.small_elevation(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.small_elevation(state)\
                    or self.flutter(state)\
                    or self.air_rat_a_tat_rap(state)\
                    or self.beak_buster(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.small_elevation(state)\
                    or self.flutter(state)\
                    or self.air_rat_a_tat_rap(state)\
                    or self.beak_buster(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.small_elevation(state)\
                    or self.flutter(state)\
                    or self.air_rat_a_tat_rap(state)\
                    or self.beak_buster(state)
        return logic

    def signpost_code_chamber(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.grip_grab(state)\
                    and self.talon_trot(state) and self.flap_flip(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.grip_grab(state)\
                    and self.talon_trot(state) and self.flap_flip(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.grip_grab(state)\
                    and self.talon_trot(state) and self.flap_flip(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.grip_grab(state)\
                    and self.talon_trot(state) and self.flap_flip(state)
        return logic

    def signpost_gloomy_cavern(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.GM_boulders(state) and (self.small_elevation(state) or self.split_up(state))
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.GM_boulders(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.GM_boulders(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.GM_boulders(state)
        return logic

    def signpost_chuffy(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = state.can_reach_region(regionName.GM, self.player) and self.flap_flip(state)\
                    or state.can_reach_region(regionName.WW, self.player) and state.has(itemName.TRAINSWWW, self.player) and state.has(itemName.CHUFFY, self.player)\
                    or state.can_reach_region(regionName.TL, self.player) and state.has(itemName.TRAINSWTD, self.player) and state.has(itemName.CHUFFY, self.player)\
                    or state.can_reach_region(regionName.GI1, self.player) and state.has(itemName.TRAINSWGI, self.player) and state.has(itemName.CHUFFY, self.player)\
                    or state.can_reach_region(regionName.IOHCT, self.player) and state.has(itemName.TRAINSWIH, self.player) and state.has(itemName.CHUFFY, self.player)

        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = state.can_reach_region(regionName.GM, self.player) and (self.small_elevation(state) or self.beak_buster(state) or self.humbaGGM(state))\
                    or state.can_reach_region(regionName.WW, self.player) and state.has(itemName.TRAINSWWW, self.player) and state.has(itemName.CHUFFY, self.player)\
                    or state.can_reach_region(regionName.TL, self.player) and state.has(itemName.TRAINSWTD, self.player) and state.has(itemName.CHUFFY, self.player)\
                    or state.can_reach_region(regionName.GI1, self.player) and state.has(itemName.TRAINSWGI, self.player) and state.has(itemName.CHUFFY, self.player)\
                    or state.can_reach_region(regionName.IOHCT, self.player) and state.has(itemName.TRAINSWIH, self.player) and state.has(itemName.CHUFFY, self.player)\
                    or state.can_reach_region(regionName.HP, self.player) and state.has(itemName.TRAINSWHP1, self.player) and self.hfp_top(state)\
                        and (self.leg_spring(state)\
                            or self.tall_jump(state) and self.pack_whack(state)\
                            or self.flap_flip(state)\
                            or self.claw_clamber_boots(state)\
                            or self.flight_pad(state))
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = state.can_reach_region(regionName.GM, self.player) and (self.small_elevation(state) or self.beak_buster(state) or self.humbaGGM(state))\
                    or state.can_reach_region(regionName.WW, self.player) and state.has(itemName.TRAINSWWW, self.player) and state.has(itemName.CHUFFY, self.player)\
                    or state.can_reach_region(regionName.TL, self.player) and state.has(itemName.TRAINSWTD, self.player) and state.has(itemName.CHUFFY, self.player)\
                    or state.can_reach_region(regionName.GI1, self.player) and state.has(itemName.TRAINSWGI, self.player) and state.has(itemName.CHUFFY, self.player)\
                    or state.can_reach_region(regionName.IOHCT, self.player) and state.has(itemName.TRAINSWIH, self.player) and state.has(itemName.CHUFFY, self.player)\
                    or state.can_reach_region(regionName.HP, self.player) and state.has(itemName.TRAINSWHP1, self.player) and self.hfp_top(state)\
                        and (self.leg_spring(state)\
                            or self.tall_jump(state) and self.pack_whack(state)\
                            or self.flap_flip(state)\
                            or self.claw_clamber_boots(state)\
                            or self.flight_pad(state))
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = state.can_reach_region(regionName.GM, self.player) and (self.small_elevation(state) or self.beak_buster(state) or self.humbaGGM(state))\
                    or state.can_reach_region(regionName.WW, self.player) and state.has(itemName.TRAINSWWW, self.player) and state.has(itemName.CHUFFY, self.player)\
                    or state.can_reach_region(regionName.TL, self.player) and state.has(itemName.TRAINSWTD, self.player) and state.has(itemName.CHUFFY, self.player)\
                    or state.can_reach_region(regionName.GI1, self.player) and state.has(itemName.TRAINSWGI, self.player) and state.has(itemName.CHUFFY, self.player)\
                    or state.can_reach_region(regionName.IOHCT, self.player) and state.has(itemName.TRAINSWIH, self.player) and state.has(itemName.CHUFFY, self.player)\
                    or state.can_reach_region(regionName.HP, self.player) and state.has(itemName.TRAINSWHP1, self.player) and self.hfp_top(state)\
                        and (self.leg_spring(state)\
                            or self.tall_jump(state) and self.pack_whack(state)\
                            or self.flap_flip(state)\
                            or self.claw_clamber_boots(state)\
                            or self.flight_pad(state))
        return logic

    def signpost_pump_master(self, state: CollectionState) -> bool:
        if self.world.options.logic_type == LogicType.option_intended:
            logic = (self.flap_flip(state)\
                        or self.leg_spring(state)\
                        or self.split_up(state) and self.grip_grab(state)
                    ) and self.has_explosives(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = (self.flap_flip(state)\
                        or self.leg_spring(state)\
                        or self.split_up(state) and self.grip_grab(state)\
                        or self.pack_whack(state) and self.tall_jump(state)\
                    ) and self.has_explosives(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = (self.flap_flip(state)\
                        or self.leg_spring(state)\
                        or self.split_up(state) and self.grip_grab(state)\
                        or self.pack_whack(state) and self.tall_jump(state)
                    ) and self.has_explosives(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = (self.flap_flip(state)\
                        or self.leg_spring(state)\
                        or self.split_up(state) and self.grip_grab(state)\
                        or self.pack_whack(state) and self.tall_jump(state)
                    ) and self.has_explosives(state)
        return logic

    def signpost_gobi(self, state: CollectionState) -> bool:
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.grenade_eggs(state) and self.egg_aim(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.grenade_eggs(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.grenade_eggs(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.grenade_eggs(state)
        return logic

    def signpost_smugglers(self, state: CollectionState) -> bool:
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.has_explosives(state) or self.dive(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.has_explosives(state) or self.dive(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.has_explosives(state) or self.dive(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.has_explosives(state) or self.dive(state)
        return logic

    def signpost_jrl_pipes(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = (self.has_explosives(state) or self.bill_drill(state)) and \
                    self.grip_grab(state) and self.spring_pad(state) and self.talon_trot(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = ((self.has_explosives(state) or self.bill_drill(state))\
                        and self.grip_grab(state) and self.spring_pad(state) and self.talon_trot(state))\
                    or (self.has_explosives(state) and self.spring_pad(state)\
                        and (self.glide(state) or self.leg_spring(state)))
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = ((self.has_explosives(state) or self.bill_drill(state))\
                        and self.grip_grab(state) and self.spring_pad(state) and self.talon_trot(state))\
                    or (self.has_explosives(state) and self.spring_pad(state)\
                        and (self.glide(state) or self.leg_spring(state)))
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = ((self.has_explosives(state) or self.bill_drill(state))\
                        and self.grip_grab(state) and self.spring_pad(state) and self.talon_trot(state))\
                    or (self.has_explosives(state) and self.spring_pad(state)\
                        and (self.glide(state) or self.leg_spring(state)))
        return logic

    def signpost_trex(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.humbaTDL(state) and self.roar(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.humbaTDL(state) and self.roar(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.humbaTDL(state) and self.roar(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.humbaTDL(state) and self.roar(state) or self.clockwork_warp(state)
        return logic

    def signpost_mountain_top(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = (self.tall_jump(state) or self.grip_grab(state)) and self.flight_pad(state)\
                    or state.can_reach_region(regionName.TLTOP, self.player)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.flight_pad(state) and (
                        self.tall_jump(state)\
                        or self.grip_grab(state)\
                        or self.beak_buster(state)\
                        or self.leg_spring(state) and self.glide(state)\
                        or state.can_reach_region(regionName.TLTOP, self.player) and self.split_up(state)
                    )\
                    or state.can_reach_region(regionName.TLTOP, self.player)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.flight_pad(state) and (
                        self.tall_jump(state)\
                        or self.grip_grab(state)\
                        or self.beak_buster(state)\
                        or self.leg_spring(state) and self.glide(state)\
                        or state.can_reach_region(regionName.TLTOP, self.player) and self.split_up(state)
                    )\
                    or state.can_reach_region(regionName.TLTOP, self.player)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.flight_pad(state) and (
                        self.tall_jump(state)\
                        or self.grip_grab(state)\
                        or self.beak_buster(state)\
                        or self.leg_spring(state) and self.glide(state)\
                        or state.can_reach_region(regionName.TLTOP, self.player) and self.split_up(state)
                    )\
                    or state.can_reach_region(regionName.TLTOP, self.player)
        return logic

    def signpost_river_passage(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.tall_jump(state) and self.grip_grab(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.tall_jump(state) and self.grip_grab(state)\
                    or self.leg_spring(state) and self.glide(state)\
                    or self.pack_whack(state) and self.grip_grab(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.tall_jump(state) and self.grip_grab(state)\
                    or self.leg_spring(state) and self.glide(state)\
                    or self.pack_whack(state) and self.grip_grab(state)\
                    or self.sack_pack(state) and self.tall_jump(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.tall_jump(state) and self.grip_grab(state)\
                    or self.leg_spring(state) and self.glide(state)\
                    or self.pack_whack(state) and self.grip_grab(state)\
                    or self.sack_pack(state) and self.tall_jump(state)
        return logic

    def signpost_gi_outside(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = state.can_reach_region(regionName.GIO, self.player) and self.outside_gi_to_outside_back(state)\
                    or state.can_reach_region(regionName.GIOB, self.player) and self.climb(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = state.can_reach_region(regionName.GIO, self.player) and self.outside_gi_to_outside_back(state)\
                    or state.can_reach_region(regionName.GIOB, self.player) and self.climb(state)\
                    or state.can_reach_region(regionName.GI1, self.player) and (self.split_up(state) and self.tall_jump(state) or self.leg_spring(state))\
                    or state.can_reach_region(regionName.GI2, self.player) and (self.floor_2_split_up(state) and (self.tall_jump(state) or self.leg_spring(state)))\
                    or state.can_reach_region(regionName.GIF, self.player)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = state.can_reach_region(regionName.GIO, self.player) and self.outside_gi_to_outside_back(state)\
                    or state.can_reach_region(regionName.GIOB, self.player) and self.climb(state)\
                    or state.can_reach_region(regionName.GI1, self.player) and (self.split_up(state) and self.tall_jump(state) or self.leg_spring(state))\
                    or state.can_reach_region(regionName.GI2, self.player) and (self.floor_2_split_up(state) and (self.tall_jump(state) or self.leg_spring(state)))\
                    or state.can_reach_region(regionName.GIF, self.player)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = state.can_reach_region(regionName.GIO, self.player) and self.outside_gi_to_outside_back(state)\
                    or state.can_reach_region(regionName.GIOB, self.player) and self.climb(state)\
                    or state.can_reach_region(regionName.GI1, self.player) and (self.split_up(state) and self.tall_jump(state) or self.leg_spring(state))\
                    or state.can_reach_region(regionName.GI2, self.player) and (self.floor_2_split_up(state) and (self.tall_jump(state) or self.leg_spring(state)))\
                    or state.can_reach_region(regionName.GIF, self.player)
        return logic


    def signpost_elevator_shaft(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.climb(state) and self.tall_jump(state) and (self.flutter(state) or self.air_rat_a_tat_rap(state))
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.climb(state) and (
                        self.flutter(state)\
                        or self.air_rat_a_tat_rap(state)\
                        or self.tall_jump(state) and self.beak_buster(state)
                    )
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.climb(state) and (
                        self.flutter(state)\
                        or self.air_rat_a_tat_rap(state)\
                        or self.tall_jump(state) and self.beak_buster(state)
                    )
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.climb(state) and (
                        self.flutter(state)\
                        or self.air_rat_a_tat_rap(state)\
                        or self.tall_jump(state) and self.beak_buster(state)
                    )
        return logic

    def signpost_ccl_underwater(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.dive(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.dive(state) or self.shack_pack(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.dive(state) or self.shack_pack(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.dive(state) or self.shack_pack(state)
        return logic

    def signpost_pool_rim(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.flap_flip(state) and self.grip_grab(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = True
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = True
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = True
        return logic

    def warp_pad_ggm_mumbo(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.small_elevation(state) or self.warp_to_ggm_mumbo(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.small_elevation(state)\
                    or self.grip_grab(state)\
                    or self.beak_buster(state)\
                    or self.ggm_trot(state)\
                    or self.warp_to_ggm_mumbo(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.small_elevation(state)\
                    or self.grip_grab(state)\
                    or self.beak_buster(state)\
                    or self.ggm_trot(state)\
                    or self.warp_to_ggm_mumbo(state)\
                    or self.clockwork_shot(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.small_elevation(state)\
                    or self.grip_grab(state)\
                    or self.beak_buster(state)\
                    or self.ggm_trot(state)\
                    or self.warp_to_ggm_mumbo(state)\
                    or self.clockwork_shot(state)
        return logic

    def warp_pad_ggm_wumba(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.ggm_trot(state) or self.warp_to_ggm_wumba(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.ggm_trot(state) or self.warp_to_ggm_wumba(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.ggm_trot(state) or self.clockwork_shot(state) or self.warp_to_ggm_wumba(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.ggm_trot(state) or self.clockwork_shot(state) or self.warp_to_ggm_wumba(state)
        return logic

    def warp_pad_ww_wumba(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.flap_flip(state) and self.grip_grab(state)\
                    or self.warp_to_ww_wumba(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.flap_flip(state)\
                        and ((self.flap_flip(state) and self.grip_grab(state)) \
                            or (self.climb(state) and self.veryLongJump(state)))\
                    or self.warp_to_ww_wumba(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.flap_flip(state) and self.grip_grab(state) \
                    or self.climb(state) and self.veryLongJump(state) and self.flap_flip(state)\
                    or self.clockwork_shot(state) and self.climb(state)\
                    or self.leg_spring(state)\
                    or self.warp_to_ww_wumba(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.flap_flip(state) and self.grip_grab(state) \
                    or self.climb(state) and self.veryLongJump(state) and self.flap_flip(state)\
                    or self.clockwork_shot(state) and self.climb(state)\
                    or self.warp_to_ww_wumba(state)
        return logic

    def warp_to_ww_wumba(self, state: CollectionState) -> bool:
        return state.has(itemName.WARPWW4, self.player) and (
                    state.has(itemName.WARPWW1, self.player)\
                    or state.has(itemName.WARPWW2, self.player)\
                    or state.has(itemName.WARPWW3, self.player)\
                    or state.has(itemName.WARPWW5, self.player) and state.can_reach_region(regionName.WWI, self.player)\
                )

    def warp_to_inferno(self, state: CollectionState) -> bool:
        return state.has(itemName.WARPWW5, self.player) and (
                    state.has(itemName.WARPWW1, self.player)\
                    or state.has(itemName.WARPWW2, self.player)\
                    or state.has(itemName.WARPWW3, self.player)\
                    or state.has(itemName.WARPWW4, self.player) and state.can_reach_location(locationName.WARPWW4, self.player)\
                )

    # The Wumba warp pad is always as hard or harder to reach, so warping from Wumba to Mumbo is not considered to avoid infinite loops.
    def warp_to_ggm_mumbo(self, state: CollectionState) -> bool:
        return state.has(itemName.WARPGM2, self.player) and (
                    state.has(itemName.WARPGM1, self.player)\
                    or state.has(itemName.WARPGM4, self.player)\
                    or state.has(itemName.WARPGM5, self.player)\
                )

    def warp_to_ggm_wumba(self, state: CollectionState) -> bool:
        return state.has(itemName.WARPGM3, self.player) and (
                    state.has(itemName.WARPGM1, self.player)\
                    or state.has(itemName.WARPGM2, self.player)\
                    or state.has(itemName.WARPGM4, self.player)\
                    or state.has(itemName.WARPGM5, self.player)\
                )

    def warp_pad_tdl_mumbo(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.stilt_stride(state)\
                    or self.warp_to_tdl_mumbo(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = True
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = True
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = True
        return logic

    def warp_to_tdl_mumbo(self, state: CollectionState) -> bool:
        state.has(itemName.WARPTL3, self.player) and (
            state.has(itemName.WARPTL1, self.player)\
            or state.has(itemName.WARPTL2, self.player) and state.can_reach_region(regionName.TLSP, self.player)\
            or state.has(itemName.WARPTL4, self.player) and state.can_reach_location(locationName.WARPTL4, self.player)\
            or state.has(itemName.WARPTL5, self.player) and state.can_reach_region(regionName.TLTOP, self.player)\
        )

    def warp_pad_tdl_wumba(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.small_elevation(state) or self.warp_to_tdl_wumba(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = True
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = True
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = True
        return logic

    def tdl_to_warp_pads(self, state: CollectionState) -> bool:
        return state.has(itemName.WARPTL1, self.player)\
                or state.has(itemName.WARPTL3, self.player) and state.can_reach_location(locationName.WARPTL3, self.player)\
                or state.has(itemName.WARPTL4, self.player) and state.can_reach_location(locationName.WARPTL4, self.player)

    def warp_to_tdl_wumba(self, state: CollectionState) -> bool:
        state.has(itemName.WARPTL4, self.player) and (
            state.has(itemName.WARPTL1, self.player)\
            or state.has(itemName.WARPTL2, self.player) and state.can_reach_region(regionName.TLSP, self.player)\
            or state.has(itemName.WARPTL3, self.player) and state.can_reach_location(locationName.WARPTL3, self.player)\
            or state.has(itemName.WARPTL5, self.player) and state.can_reach_region(regionName.TLTOP, self.player)\
        )

    # TODO: readd leg spring + glide
    def tdl_to_tdl_top(self, state: CollectionState) -> bool:
        if self.world.options.logic_type == LogicType.option_intended:
            return self.springy_step_shoes(state)\
                        and (self.tall_jump(state) and (self.flutter(state) or self.air_rat_a_tat_rap(state))\
                            or self.talon_trot(state))
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            return self.springy_step_shoes(state)\
                        and (self.tall_jump(state) and (self.flutter(state) or self.air_rat_a_tat_rap(state))\
                            or self.talon_trot(state))
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            return self.springy_step_shoes(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            return (self.springy_step_shoes(state) or \
                    (self.flight_pad(state) and (self.tall_jump(state) or self.beak_buster(state) or self.grip_grab(state))\
                     and (self.beak_bomb(state) or self.clockwork_warp(state))))

    def warp_pad_floor_1(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.split_up(state)\
                    or state.can_reach_region(regionName.GIWARP, self.player) and state.has(itemName.WARPGI1, self.player)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.split_up(state)\
                    or state.can_reach_region(regionName.GIWARP, self.player) and state.has(itemName.WARPGI1, self.player)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.split_up(state)\
                    or state.can_reach_region(regionName.GIWARP, self.player) and state.has(itemName.WARPGI1, self.player)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.split_up(state)\
                    or state.can_reach_region(regionName.GIWARP, self.player) and state.has(itemName.WARPGI1, self.player)\
                    or state.can_reach_region(regionName.GIO, self.player) and self.clockwork_shot(state)
        return logic

    def warp_pad_floor_4(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.small_elevation(state)\
                    or state.can_reach_region(regionName.GIWARP, self.player) and state.has(itemName.WARPGI4, self.player)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.small_elevation(state)\
                    or state.can_reach_region(regionName.GIWARP, self.player) and state.has(itemName.WARPGI4, self.player)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = True
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = True
        return logic

    def warp_to_hfp_top(self, state: CollectionState) -> bool:
        return state.has(itemName.WARPHP1, self.player) and (
                    state.has(itemName.WARPHP2, self.player)\
                    or state.has(itemName.WARPHP3, self.player)\
                    or state.has(itemName.WARPHP4, self.player)\
                    or state.has(itemName.WARPHP5, self.player)\
                )

    def warp_pad_icicle_grotto(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.hfp_top(state) and self.spring_pad(state) and self.talon_trot(state)\
                    or self.hfp_top(state) and self.spring_pad(state) and self.split_up(state)\
                    or self.warp_to_icicle_grotto(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.split_up(state) and (self.tall_jump(state) or self.wing_whack(state) or self.glide(state) or self.leg_spring(state))\
                    or self.hfp_top(state) and self.spring_pad(state) and self.talon_trot(state)\
                    or self.warp_to_icicle_grotto(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.split_up(state) and (self.tall_jump(state) or self.wing_whack(state) or self.glide(state) or self.leg_spring(state))\
                    or self.hfp_top(state) and self.spring_pad(state) and self.talon_trot(state)\
                    or (self.extremelyLongJump(state) and self.clockwork_shot(state))\
                    or self.warp_to_icicle_grotto(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.split_up(state) and (self.tall_jump(state) or self.wing_whack(state) or self.glide(state) or self.leg_spring(state))\
                    or self.hfp_top(state) and self.spring_pad(state) and self.talon_trot(state)\
                    or (self.extremelyLongJump(state) and self.clockwork_shot(state))\
                    or self.warp_to_icicle_grotto(state)
        return logic

    def warp_to_icicle_grotto(self, state: CollectionState) -> bool:
        return state.has(itemName.WARPHP5, self.player) and (
                    state.has(itemName.WARPHP1, self.player)\
                    or state.has(itemName.WARPHP2, self.player) and self.hfp_top(state)\
                    or state.has(itemName.WARPHP3, self.player) and self.hfp_top(state)\
                    or state.has(itemName.WARPHP4, self.player) and self.hfp_top(state)\
                )

    def warp_pad_ck_top(self, state: CollectionState) -> bool:
        if self.world.options.logic_type == LogicType.option_intended:
            return self.pack_whack(state)\
                    or self.sack_pack(state)\
                    or self.shack_pack(state)\
                    or state.has(itemName.WARPCK1, self.player) and state.has(itemName.WARPCK2, self.player)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            return self.pack_whack(state)\
                    or self.sack_pack(state)\
                    or self.shack_pack(state)\
                    or state.has(itemName.WARPCK1, self.player) and state.has(itemName.WARPCK2, self.player)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            return self.pack_whack(state)\
                    or self.sack_pack(state)\
                    or self.shack_pack(state)\
                    or state.has(itemName.WARPCK1, self.player) and state.has(itemName.WARPCK2, self.player)
        elif self.world.options.logic_type == LogicType.option_glitches:
            return self.pack_whack(state)\
                    or self.sack_pack(state)\
                    or self.shack_pack(state)\
                    or state.has(itemName.WARPCK1, self.player) and state.has(itemName.WARPCK2, self.player)

    def has_fire(self, state: CollectionState) -> bool:
        return self.fire_eggs(state) or self.dragon_kazooie(state)

    def dragon_kazooie(self, state: CollectionState) -> bool:
        return self.check_humba_magic(state, itemName.HUMBAIH) and state.can_reach_region(regionName.IOHPG, self.player) and self.ground_rat_a_tat_rap(state)

    def has_explosives(self, state: CollectionState) -> bool:
        if self.world.options.logic_type == LogicType.option_intended:
            return self.grenade_eggs(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            return self.grenade_eggs(state) or self.clockwork_eggs(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            return self.grenade_eggs(state) or self.clockwork_eggs(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            return self.grenade_eggs(state) or self.clockwork_eggs(state)

    def can_pass_octopi(self, state: CollectionState) -> bool:
        if self.world.options.logic_type == LogicType.option_intended:
            return self.ice_eggs_item(state) and self.check_mumbo_magic(state, itemName.MUMBOJR) and self.sub_aqua_egg_aiming(state)\
                    or self.humbaJRL(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            return self.ice_eggs_item(state) and (self.doubleAir(state) or self.check_mumbo_magic(state, itemName.MUMBOJR)) and self.sub_aqua_egg_aiming(state)\
                    or self.humbaJRL(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            return True
        elif self.world.options.logic_type == LogicType.option_glitches:
            return True

    def can_escape_big_fish_cave_from_water(self, state: CollectionState) -> bool:
        if self.world.options.logic_type == LogicType.option_intended:
            return self.ice_eggs_item(state) and self.check_mumbo_magic(state, itemName.MUMBOJR) and self.sub_aqua_egg_aiming(state)\
                    or self.humbaJRL(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            return self.ice_eggs_item(state) and self.check_mumbo_magic(state, itemName.MUMBOJR) and self.sub_aqua_egg_aiming(state)\
                    or self.ice_eggs_item(state) and self.doubleAir(state) and self.sub_aqua_egg_aiming(state)\
                        and (
                            self.air_pit_from_jrl_warp_pads(state) and state.has(itemName.WARPJR4, self.player)\
                            or self.dive(state)
                        )\
                    or self.humbaJRL(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            return self.check_mumbo_magic(state, itemName.MUMBOJR)\
                    or self.air_pit_from_jrl_warp_pads(state) and state.has(itemName.WARPJR4, self.player)\
                    or self.dive(state)\
                    or self.humbaJRL(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            return self.check_mumbo_magic(state, itemName.MUMBOJR)\
                    or self.air_pit_from_jrl_warp_pads(state) and state.has(itemName.WARPJR4, self.player)\
                    or self.dive(state)\
                    or self.humbaJRL(state)

    def can_escape_locker_cavern(self, state: CollectionState) -> bool:
        if self.world.options.logic_type == LogicType.option_intended:
            return self.ice_eggs_item(state) and self.check_mumbo_magic(state, itemName.MUMBOJR) and self.sub_aqua_egg_aiming(state)\
                    or self.humbaJRL(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            return self.ice_eggs_item(state) and self.check_mumbo_magic(state, itemName.MUMBOJR) and self.sub_aqua_egg_aiming(state)\
                    or self.ice_eggs_item(state) and self.doubleAir(state) and self.sub_aqua_egg_aiming(state)\
                        and self.air_pit_from_jrl_warp_pads(state) and state.has(itemName.WARPJR5, self.player)\
                    or self.humbaJRL(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            return self.check_mumbo_magic(state, itemName.MUMBOJR)\
                    or self.air_pit_from_jrl_warp_pads(state) and state.has(itemName.WARPJR5, self.player)\
                    or self.humbaJRL(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            return self.check_mumbo_magic(state, itemName.MUMBOJR)\
                    or self.air_pit_from_jrl_warp_pads(state) and state.has(itemName.WARPJR5, self.player)\
                    or self.humbaJRL(state)

    def can_escape_sunken_ship(self, state: CollectionState) -> bool:
        if self.world.options.logic_type == LogicType.option_intended:
            return self.ice_eggs_item(state) and self.check_mumbo_magic(state, itemName.MUMBOJR) and self.sub_aqua_egg_aiming(state)\
                    or self.humbaJRL(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            return self.ice_eggs_item(state) and self.check_mumbo_magic(state, itemName.MUMBOJR) and self.sub_aqua_egg_aiming(state)\
                    or self.ice_eggs_item(state) and self.doubleAir(state) and self.sub_aqua_egg_aiming(state)\
                        and self.air_pit_from_jrl_warp_pads(state) and state.has(itemName.WARPJR3, self.player)\
                    or self.humbaJRL(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            return self.check_mumbo_magic(state, itemName.MUMBOJR)\
                    or self.air_pit_from_jrl_warp_pads(state) and state.has(itemName.WARPJR3, self.player)\
                    or self.humbaJRL(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            return self.check_mumbo_magic(state, itemName.MUMBOJR)\
                    or self.air_pit_from_jrl_warp_pads(state) and state.has(itemName.WARPJR3, self.player)\
                    or self.humbaJRL(state)

    def can_escape_from_locker_cavern(self, state: CollectionState) -> bool:
        if self.world.options.logic_type == LogicType.option_intended:
            return self.ice_eggs_item(state) and self.check_mumbo_magic(state, itemName.MUMBOJR) and self.sub_aqua_egg_aiming(state)\
                    or self.humbaJRL(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            return self.ice_eggs_item(state) and self.check_mumbo_magic(state, itemName.MUMBOJR) and self.sub_aqua_egg_aiming(state)\
                    or self.ice_eggs_item(state) and self.doubleAir(state) and self.sub_aqua_egg_aiming(state)\
                        and self.air_pit_from_jrl_warp_pads(state) and state.has(itemName.WARPJR5, self.player)\
                    or self.humbaJRL(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            return self.check_mumbo_magic(state, itemName.MUMBOJR)\
                    or self.air_pit_from_jrl_warp_pads(state) and state.has(itemName.WARPJR5, self.player)\
                    or self.humbaJRL(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            return self.check_mumbo_magic(state, itemName.MUMBOJR)\
                    or self.air_pit_from_jrl_warp_pads(state) and state.has(itemName.WARPJR5, self.player)\
                    or self.humbaJRL(state)

    def sunken_ship_to_ggm(self, state: CollectionState) -> bool:
        if self.world.options.logic_type == LogicType.option_intended:
            return self.ice_eggs_item(state) and self.check_mumbo_magic(state, itemName.MUMBOJR)\
                    and self.sub_aqua_egg_aiming(state) and self.talon_torpedo(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            return self.ice_eggs_item(state) and self.check_mumbo_magic(state, itemName.MUMBOJR)\
                        and self.sub_aqua_egg_aiming(state) and self.talon_torpedo(state)\
                    or self.ice_eggs_item(state) and self.doubleAir(state) and self.sub_aqua_egg_aiming(state)\
                        and self.air_pit_from_jrl_warp_pads(state) and state.has(itemName.WARPJR4, self.player) and self.talon_torpedo(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            return self.ice_eggs_item(state) and self.check_mumbo_magic(state, itemName.MUMBOJR)\
                        and self.sub_aqua_egg_aiming(state) and self.talon_torpedo(state)\
                    or self.ice_eggs_item(state) and self.sub_aqua_egg_aiming(state)\
                        and self.air_pit_from_jrl_warp_pads(state) and state.has(itemName.WARPJR4, self.player) and self.talon_torpedo(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            return self.ice_eggs_item(state) and self.check_mumbo_magic(state, itemName.MUMBOJR)\
                        and self.sub_aqua_egg_aiming(state) and self.talon_torpedo(state)\
                    or self.ice_eggs_item(state) and self.sub_aqua_egg_aiming(state)\
                        and self.air_pit_from_jrl_warp_pads(state) and state.has(itemName.WARPJR4, self.player) and self.talon_torpedo(state)

    def seaweed_to_bfc(self, state: CollectionState) -> bool:
        if self.world.options.logic_type == LogicType.option_intended:
            return self.tall_jump(state) and self.grip_grab(state) and self.dive(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            return self.dive(state)\
                    and (self.slightly_elevated_ledge(state) or self.flap_flip(state))\
                    and self.tall_jump(state)\
                    and (self.beak_buster(state) or self.grip_grab(state))
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            return self.dive(state)\
                    and (self.slightly_elevated_ledge(state) or self.flap_flip(state))\
                    and self.tall_jump(state)\
                    and (self.beak_buster(state) or self.grip_grab(state))
        elif self.world.options.logic_type == LogicType.option_glitches:
            return self.dive(state)\
                    and (self.slightly_elevated_ledge(state) or self.flap_flip(state))\
                    and self.tall_jump(state)\
                    and (self.beak_buster(state) or self.grip_grab(state))

    def MT_flight_pad(self, state: CollectionState) -> bool:
        return self.flight_pad(state) and\
                (self.check_mumbo_magic(state, itemName.MUMBOMT)\
                    or (self.bill_drill(state) and (self.small_elevation(state) or self.flutter(state))))

    def prison_compound_open(self, state: CollectionState) -> bool:
        return self.has_explosives(state) or self.check_mumbo_magic(state, itemName.MUMBOMT)

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
                    self.prison_compound_open(state)\
                    or state.has(itemName.WARPMT3, self.player)\
                        and (state.has(itemName.WARPMT1, self.player) or state.has(itemName.WARPMT2, self.player)\
                             or state.has(itemName.WARPMT4, self.player) or state.has(itemName.WARPMT5, self.player))
                )

    def kickball_stadium_as_banjo(self, state: CollectionState) -> bool:
        return state.can_reach_region(regionName.HP, self.player) and self.HFP_to_MT(state)\
                or state.has(itemName.WARPMT5, self.player) and (
                    state.has(itemName.WARPMT1, self.player)\
                    or state.has(itemName.WARPMT2, self.player)\
                    or state.has(itemName.WARPMT3, self.player) and self.prison_compound_as_banjo(state)\
                    or state.has(itemName.WARPMT4, self.player) and state.can_reach_region(regionName.MTJSG, self.player)
                )

    def dilberta_free(self, state: CollectionState) -> bool:
        if self.world.options.logic_type == LogicType.option_intended:
            return self.prison_compound_as_banjo(state) and self.bill_drill(state)

        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            return self.prison_compound_as_banjo(state) and self.bill_drill(state)

        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            return self.prison_compound_as_banjo(state) and self.bill_drill(state)

        elif self.world.options.logic_type == LogicType.option_glitches:
            return self.prison_compound_as_banjo(state) and self.bill_drill(state)

    def GM_boulders(self, state: CollectionState) -> bool:
        return (self.bill_drill(state) and self.small_elevation(state)) or self.humbaGGM(state)

    def canary_mary_free(self, state: CollectionState) -> bool:
        if self.world.options.logic_type == LogicType.option_intended:
            return self.humbaGGM(state)

        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            return self.humbaGGM(state) or self.clockwork_eggs(state)

        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            return self.humbaGGM(state) or self.clockwork_eggs(state)

        elif self.world.options.logic_type == LogicType.option_glitches:
            return self.humbaGGM(state) or self.clockwork_eggs(state)

    def can_beat_king_coal(self, state) -> bool:
        hasAttack = False
        if self.world.options.logic_type == LogicType.option_intended:
            hasAttack = self.blue_eggs(state) or self.grenade_eggs(state) or self.ice_eggs(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            hasAttack = self.blue_eggs(state) or self.grenade_eggs(state) or self.ice_eggs(state) or self.beak_barge(state) or self.roll(state) or self.air_rat_a_tat_rap(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            hasAttack = self.blue_eggs(state) or self.grenade_eggs(state) or self.ice_eggs(state) or self.beak_barge(state) or self.roll(state)\
            or self.air_rat_a_tat_rap(state) or self.ground_rat_a_tat_rap(state) or self.breegull_bash(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            hasAttack = self.blue_eggs(state) or self.grenade_eggs(state) or self.ice_eggs(state) or self.beak_barge(state) or self.roll(state)\
            or self.air_rat_a_tat_rap(state) or self.ground_rat_a_tat_rap(state) or self.breegull_bash(state)

        if not self.world.options.randomize_chuffy:
            return self.mumboGGM(state) and state.can_reach_region(regionName.GM, self.player) and self.ggm_to_chuffy(state) and hasAttack
        else:
            return state.has(itemName.CHUFFY, self.player) and hasAttack


    #deprecated but might be useful for ticket randomization
    def can_kill_fruity(self, state: CollectionState) -> bool:
        return self.has_explosives(state) or \
               self.humbaWW(state)

    def saucer_door_open(self, state: CollectionState) -> bool:
        if self.world.options.logic_type == LogicType.option_intended:
            return self.longJumpToGripGrab(state) and self.flap_flip(state) and self.climb(state)\
                  and (self.has_explosives(state) or self.beak_barge(state)) or\
                  self.backdoors_enabled(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            return (self.longJumpToGripGrab(state) and self.flap_flip(state) and self.climb(state) and (self.has_explosives(state) or self.beak_barge(state)))\
                or (self.egg_aim(state) and self.grenade_eggs(state) and self.amaze_o_gaze(state) and self.climb(state))\
                or (self.has_explosives(state) and self.leg_spring(state) and self.glide(state))\
                or self.backdoors_enabled(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            return (self.longJumpToGripGrab(state) and self.flap_flip(state) and self.climb(state) and (self.has_explosives(state) or self.beak_barge(state)))\
                or (self.egg_aim(state) and self.grenade_eggs(state) and self.amaze_o_gaze(state))\
                or (self.has_explosives(state) and self.leg_spring(state) and self.glide(state))\
                or self.backdoors_enabled(state)\
                or self.clockwork_shot(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            return (self.longJumpToGripGrab(state) and self.flap_flip(state) and self.climb(state) and (self.has_explosives(state) or self.beak_barge(state)))\
                or (self.egg_aim(state) and self.grenade_eggs(state) and self.amaze_o_gaze(state))\
                or (self.has_explosives(state) and self.leg_spring(state) and self.glide(state))\
                or self.backdoors_enabled(state)\
                or self.clockwork_shot(state)\
                or (state.can_reach_region(regionName.GM, self.player) and self.humbaGGM(state) and self.small_elevation(state) and self.clockwork_eggs(state)) # You can shoot a clockwork through the door from GGM.


    def can_reach_saucer(self, state: CollectionState) -> bool:
        return (self.longJumpToGripGrab(state) and self.flap_flip(state) and self.climb(state)) or (state.can_reach_region(regionName.GM, self.player) and self.small_elevation(state))


    def longJumpToGripGrab(self, state: CollectionState) -> bool:
        return self.grip_grab(state) and (self.air_rat_a_tat_rap(state) or self.flutter(state))

    def can_beat_terry(self, state: CollectionState) -> bool:
        # I assume nobody wants to do this fight with clockwork eggs.
        if self.world.options.logic_type == LogicType.option_intended:
            return self.egg_aim(state) and self.can_shoot_linear_egg(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            return self.egg_aim(state)  and self.can_shoot_linear_egg(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            return self.can_shoot_linear_egg(state) and (self.flap_flip(state) or self.egg_aim(state))
        elif self.world.options.logic_type == LogicType.option_glitches:
            return self.can_shoot_any_egg(state) and (self.flap_flip(state) or self.egg_aim(state))

    def tdl_top(self, state: CollectionState) -> bool:
        if self.world.options.logic_type == LogicType.option_intended:
            return self.springy_step_shoes(state)\
                        and (self.tall_jump(state) and (self.flutter(state) or self.air_rat_a_tat_rap(state))\
                            or self.split_up(state)\
                            or self.talon_trot(state))
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            return self.springy_step_shoes(state)\
                        and (self.tall_jump(state) and (self.flutter(state) or self.air_rat_a_tat_rap(state))\
                            or self.split_up(state)\
                            or self.talon_trot(state))
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            return (self.springy_step_shoes(state) or self.leg_spring(state) and self.glide(state))
        elif self.world.options.logic_type == LogicType.option_glitches:
            return (self.springy_step_shoes(state) or \
                    self.leg_spring(state) and self.glide(state) or\
                    (self.flight_pad(state) and (self.tall_jump(state) or self.beak_buster(state) or self.grip_grab(state))\
                     and (self.beak_bomb(state) or self.clockwork_warp(state))))

    def smuggle_food(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.claw_clamber_boots(state) and self.talon_trot(state) and self.has_explosives(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.claw_clamber_boots(state) and self.talon_trot(state) and self.has_explosives(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.has_explosives(state) or self.spring_pad(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.has_explosives(state) or self.spring_pad(state)
        return logic

    def oogle_boogles_open(self, state) -> bool:
        return self.humbaTDL(state) and self.mumboTDL(state)

    def access_oogle_boogle(self, state) -> bool:
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.oogle_boogles_open(state) or state.can_reach_region(regionName.WW, self.player) and self.ww_tdl_backdoor(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.oogle_boogles_open(state) or state.can_reach_region(regionName.WW, self.player) and self.ww_tdl_backdoor(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.oogle_boogles_open(state) or state.can_reach_region(regionName.WW, self.player) and self.ww_tdl_backdoor(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.oogle_boogles_open(state)\
                    or state.can_reach_region(regionName.WW, self.player) and self.ww_tdl_backdoor(state)\
                    or self.clockwork_warp(state)
        return logic

    def enter_GI(self, state: CollectionState) -> bool:
        return self.can_beat_king_coal(state) or self.claw_clamber_boots(state)

    def GI_front_door(self, state: CollectionState) -> bool:
        return self.enter_GI(state) and self.split_up(state)

    def can_reach_GI_2F(self, state: CollectionState) -> bool:
        return self.claw_clamber_boots(state) or \
               (self.GI_front_door(state) and
                self.leg_spring(state) and
                self.glide(state) and
                (self.wing_whack(state) or
                self.egg_aim(state)))

    def can_beat_weldar(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.can_use_battery(state) and self.mumboGI(state) and \
               self.humbaGI(state) and self.grenade_eggs(state) and \
               self.bill_drill(state) and self.climb(state) and self.flap_flip(state)\
                and self.grip_grab(state)\
                and state.has(itemName.WARPGI2, self.player) and state.has(itemName.WARPGI3, self.player)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.can_use_battery(state) and self.mumboGI(state) and \
               self.humbaGI(state) and self.grenade_eggs(state) and \
               self.bill_drill(state) and self.climb(state) and self.flap_flip(state) and\
               state.has(itemName.WARPGI2, self.player) and state.has(itemName.WARPGI3, self.player) and\
               (self.grip_grab(state) or (self.tall_jump(state) and (self.flutter(state) or self.air_rat_a_tat_rap(state))))
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.can_use_battery(state) and self.mumboGI(state) and \
               self.humbaGI(state) and self.grenade_eggs(state) and \
               self.bill_drill(state) and self.climb(state) and self.flap_flip(state) and\
               state.has(itemName.WARPGI2, self.player) and state.has(itemName.WARPGI3, self.player) and\
               ((self.grip_grab(state) or (self.tall_jump(state) and (self.flutter(state) or self.air_rat_a_tat_rap(state))))\
                    or self.extremelyLongJump(state))
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.can_use_battery(state) and self.mumboGI(state) and \
               self.humbaGI(state) and self.grenade_eggs(state) and \
               self.bill_drill(state) and self.climb(state) and self.flap_flip(state) and\
               state.has(itemName.WARPGI2, self.player) and state.has(itemName.WARPGI3, self.player) and\
               ((self.grip_grab(state) or (self.tall_jump(state) and (self.flutter(state) or self.air_rat_a_tat_rap(state))))\
                    or self.extremelyLongJump(state))
        return logic


    def jiggy_underwater_waste_disposal(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.can_beat_weldar(state) and self.shack_pack(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.can_beat_weldar(state) and self.shack_pack(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.can_beat_weldar(state) and self.shack_pack(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            # Getting the jiggy from waste disposal through the wall.
            logic = (self.can_beat_weldar(state) and (self.shack_pack(state) or self.leg_spring(state)))\
                    or self.can_use_battery(state) and (
                        (self.climb(state) and self.flap_flip(state) and self.talon_torpedo(state)\
                         and self.dive(state) and self.wonderwing(state))
                         or (self.shack_pack(state) and self.climb(state) and self.grip_grab(state)))
        return logic

    def jiggy_clinkers(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.claw_clamber_boots(state) and self.breegull_blaster(state) and self.climb(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.claw_clamber_boots(state) and self.breegull_blaster(state) and self.climb(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.claw_clamber_boots(state) and self.breegull_blaster(state) and self.climb(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.claw_clamber_boots(state) and self.breegull_blaster(state)\
                    and (self.precise_clockwork_warp(state) and (self.spring_pad(state) or self.flap_flip(state))\
                        or state.can_reach_region(regionName.GIES, self.player) and self.elevator_shaft_to_floor_4(state)\
                        or self.climb(state))
        return logic

    def can_use_battery(self, state: CollectionState) -> bool:
        return self.pack_whack(state) and self.taxi_pack(state)

    def MT_to_JSG(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = state.has(itemName.MUMBOMT, self.player)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = state.has(itemName.MUMBOMT, self.player)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = state.has(itemName.MUMBOMT, self.player)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.MT_flight_pad(state) and self.beak_bomb(state) or state.has(itemName.MUMBOMT, self.player)
        return logic

    def MT_to_KS(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.humbaMT(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.humbaMT(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.humbaMT(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.MT_flight_pad(state) and self.beak_bomb(state) or self.humbaMT(state)
        return logic

    def glitchedInfernoAccess(self, state: CollectionState) -> bool:
        return self.humbaWW(state) or self.clockwork_eggs(state) and self.tall_jump(state)

    def HFP_to_MT(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.has_explosives(state)\
                    or self.dragon_kazooie(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.has_explosives(state) or \
                    self.check_mumbo_magic(state, itemName.MUMBOHP)\
                    or self.dragon_kazooie(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.has_explosives(state) or \
                    self.check_mumbo_magic(state, itemName.MUMBOHP)\
                    or self.dragon_kazooie(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.has_explosives(state) or \
                    self.check_mumbo_magic(state, itemName.MUMBOHP)\
                    or self.dragon_kazooie(state)
        return logic



    def HFP_to_JRL(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.HFP_hot_water_cooled(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.HFP_hot_water_cooled(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.HFP_hot_water_cooled(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.HFP_hot_water_cooled(state)\
                    or (self.grip_grab(state) and (self.flutter(state) or self.air_rat_a_tat_rap(state)) and self.ground_rat_a_tat_rap(state) and self.tall_jump(state))
        return logic

    def WorldUnlocks_req(self, state: CollectionState, locationId: int) -> bool: #1
        world = ""
        for worldLoc, locationno in self.world.randomize_order.items():
            if locationno == locationId:
                world = worldLoc
                break
        if world == "":
            return False
        amt = self.world.randomize_worlds[world]
        return state.has(itemName.JIGGY, self.player, amt)


    def mt_jiggy(self, state: CollectionState) -> bool: #1
        if self.world.worlds_randomized:
            return state.has(itemName.MTA, self.player)
        else:
            amt = self.world.randomize_worlds[regionName.MT]
            return state.has(itemName.JIGGY, self.player, amt)

    def MT_to_WH(self, state: CollectionState) -> bool: #1
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.mt_jiggy(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = True
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = True
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = True
        return logic

    def WH_to_PL(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.slightly_elevated_ledge(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.slightly_elevated_ledge(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.slightly_elevated_ledge(state) or (self.flap_flip(state) and self.beak_buster(state))
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.slightly_elevated_ledge(state) or (self.flap_flip(state) and self.beak_buster(state))
        return logic

    def GGM_to_PL(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.gm_jiggy(state) and self.climb(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.climb(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.climb(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.climb(state)
        return logic

    def escape_ggm_loading_zone(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.gm_jiggy(state) and self.climb(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.climb(state) or self.beak_buster(state) or self.flutter(state) or self.air_rat_a_tat_rap(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.climb(state) or self.beak_buster(state) or self.flutter(state) or self.air_rat_a_tat_rap(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.climb(state) or self.beak_buster(state) or self.flutter(state) or self.air_rat_a_tat_rap(state)
        return logic


    def PG_to_PL(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = False
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = True
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = True
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = True
        return logic

    def CT_to_PL(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = False
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = True
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = True
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = True
        return logic

    def gm_jiggy(self, state: CollectionState) -> bool: #4
        if self.world.worlds_randomized:
            return state.has(itemName.GGA, self.player)
        else:
            amt = self.world.randomize_worlds[regionName.GM]
            return state.has(itemName.JIGGY, self.player, amt)


    def can_access_water_storage_jinjo_from_GGM(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = False
        elif self.world.options.logic_type == LogicType.option_easy_tricks : # normal
            logic = self.wing_whack(state) and self.leg_spring(state) and\
                        self.glide(state) and self.GM_boulders(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = (self.wing_whack(state) and self.leg_spring(state) and\
                        self.glide(state) and self.GM_boulders(state))\
                    or self.clockwork_shot(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = (self.wing_whack(state) and self.leg_spring(state) and\
                                                 self.glide(state) and self.GM_boulders(state))\
                    or self.clockwork_shot(state)
        return logic

    # If you warp to a warp pad in JRL, this checks to see if you have enough air to get the checks in the region that you warp to.
    def air_pit_from_jrl_warp_pads(self, state: CollectionState) -> bool:
        return state.has(itemName.WARPJR1, self.player)\
                or state.has(itemName.WARPJR2, self.player) and self.dive(state)\
                or state.has(itemName.WARPJR4, self.player) and self.dive(state)

    def PL_to_PG(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.fire_eggs(state) and self.egg_aim(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks : # normal
            logic = self.fire_eggs(state) and self.egg_aim(state)\
                    or self.talon_trot(state) and self.fire_eggs(state)\
                    or self.split_up(state) and self.fire_eggs(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.fire_eggs(state) and self.egg_aim(state)\
                    or self.talon_trot(state) and self.fire_eggs(state)\
                    or self.split_up(state) and self.fire_eggs(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.fire_eggs(state) and self.egg_aim(state)\
                    or self.talon_trot(state) and self.fire_eggs(state)\
                    or self.split_up(state) and self.fire_eggs(state)
        return logic

    def PL_to_GGM(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.gm_jiggy(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks : # normal
            logic = self.gm_jiggy(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.gm_jiggy(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.gm_jiggy(state)\
                    or (self.beak_buster(state) and (self.flap_flip(state) or self.tall_jump(state) or (self.talon_trot(state) and self.flutter(state) )))
        return logic

    def hatch_to_TDL(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.backdoors_enabled(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks : # normal
            logic = self.backdoors_enabled(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.backdoors_enabled(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = (self.clockwork_eggs(state) and self.egg_aim(state)) or self.backdoors_enabled(state)
        return logic

    def ww_jiggy(self, state: CollectionState) -> bool: #8
        if self.world.worlds_randomized:
            return state.has(itemName.WWA, self.player)
        else:
            amt = self.world.randomize_worlds[regionName.WW]
            return state.has(itemName.JIGGY, self.player, amt)

    def jrl_jiggy(self, state: CollectionState) -> bool: #14
        if self.world.worlds_randomized:
            return state.has(itemName.JRA, self.player)
        else:
            amt = self.world.randomize_worlds[regionName.JR]
            return state.has(itemName.JIGGY, self.player, amt)

    def tdl_jiggy(self, state: CollectionState) -> bool: #20
        if self.world.worlds_randomized:
            return state.has(itemName.TDA, self.player)
        else:
            amt = self.world.randomize_worlds[regionName.TL]
            return state.has(itemName.JIGGY, self.player, amt)


    def gi_jiggy(self, state: CollectionState) -> bool: #28
        if self.world.worlds_randomized:
            return state.has(itemName.GIA, self.player)
        else:
            amt = self.world.randomize_worlds[regionName.GIO]
            return state.has(itemName.JIGGY, self.player, amt)

    def ck_jiggy(self, state: CollectionState) -> bool: #55
        if self.world.worlds_randomized:
            return state.has(itemName.CKA, self.player)
        else:
            amt = self.world.randomize_worlds[regionName.CK]
            return state.has(itemName.JIGGY, self.player, amt)

    def quag_to_CK(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.claw_clamber_boots(state) and self.ck_jiggy(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.claw_clamber_boots(state) and self.ck_jiggy(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.claw_clamber_boots(state) and self.ck_jiggy(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = (self.clockwork_warp(state) and self.talon_trot(state) or self.claw_clamber_boots(state))\
                    and (self.ck_jiggy(state) or (self.climb(state) and self.tall_jump(state) and self.beak_buster(state) and (self.flutter(state) or self.air_rat_a_tat_rap(state))))
        return logic

    def mt_tdl_backdoor(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.egg_aim(state) and\
                (self.flap_flip(state) or self.slightly_elevated_ledge(state)) and\
                  ((self.grip_grab(state) and self.spring_pad(state) and self.flap_flip(state)) or self.MT_flight_pad(state)) and\
                   self.backdoors_enabled(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = (self.flap_flip(state) or self.slightly_elevated_ledge(state)) and\
                  ((self.grip_grab(state) and self.spring_pad(state) and self.flap_flip(state) and self.egg_aim(state))\
                    or (self.MT_flight_pad(state) and self.can_shoot_any_egg(state))) and\
                   self.backdoors_enabled(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = (self.flap_flip(state) or self.slightly_elevated_ledge(state)) and\
                  ((self.grip_grab(state) and self.spring_pad(state) and self.flap_flip(state) and self.egg_aim(state))\
                    or (self.MT_flight_pad(state) and self.can_shoot_any_egg(state))) and\
                   self.backdoors_enabled(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = (self.flap_flip(state) or self.slightly_elevated_ledge(state)) and\
                  ((self.grip_grab(state) and self.spring_pad(state) and self.flap_flip(state) and self.egg_aim(state))\
                    or (self.MT_flight_pad(state) and self.can_shoot_any_egg(state))) and\
                   self.backdoors_enabled(state)
        return logic

    def mt_hfp_backdoor(self, state: CollectionState) -> bool:
        return self.backdoors_enabled(state) and self.kickball_stadium_as_banjo(state)


    def ww_tdl_backdoor(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.has_explosives(state) and self.claw_clamber_boots(state) and\
                self.talon_trot(state) and self.backdoors_enabled(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.has_explosives(state) and self.claw_clamber_boots(state) and\
                self.talon_trot(state) and self.backdoors_enabled(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.has_explosives(state) and self.claw_clamber_boots(state) and\
                (self.talon_trot(state) or ((self.grip_grab(state) or self.beak_buster(state)) and\
                self.climb(state) and self.flap_flip(state))) and self.backdoors_enabled(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.has_explosives(state) and self.claw_clamber_boots(state) and\
                (self.talon_trot(state) or ((self.grip_grab(state) or self.beak_buster(state)) and\
                self.climb(state) and self.flap_flip(state))) and self.backdoors_enabled(state)
        return logic


    def ggm_to_fuel_depot(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.humbaGGM(state) and self.small_elevation(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.humbaGGM(state) and self.small_elevation(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.humbaGGM(state) and self.small_elevation(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.humbaGGM(state) and self.small_elevation(state)
        return logic

    def ggm_to_ww(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.backdoors_enabled(state) and self.small_elevation(state) and self.humbaGGM(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.backdoors_enabled(state) and self.small_elevation(state) and self.humbaGGM(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.backdoors_enabled(state) and self.small_elevation(state) and self.humbaGGM(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = (self.clockwork_eggs(state) or self.backdoors_enabled(state)) and self.small_elevation(state) and self.humbaGGM(state)
        return logic

    def ww_to_fuel_depot(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.climb(state) and self.flap_flip(state) and self.grip_grab(state) and self.longJumpToGripGrab(state) and self.saucer_door_open(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.climb(state) and self.flap_flip(state) and self.grip_grab(state) and self.longJumpToGripGrab(state) and self.saucer_door_open(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.climb(state) and self.flap_flip(state) and (self.grip_grab(state) or self.beak_buster(state)) and self.longJumpToGripGrab(state) and self.saucer_door_open(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.climb(state) and self.flap_flip(state) and (self.grip_grab(state) or self.beak_buster(state)) and self.longJumpToGripGrab(state) and self.saucer_door_open(state)
        return logic

    def a51_nests_from_WW(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.has_explosives(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.has_explosives(state) or self.glide(state) or self.leg_spring(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.has_explosives(state)\
                    or self.glide(state)\
                    or self.leg_spring(state)\
                    or self.split_up(state) and self.spring_pad(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.has_explosives(state)\
                    or self.glide(state)\
                    or self.leg_spring(state)\
                    or self.split_up(state) and self.spring_pad(state)
        return logic

    def ww_to_inferno(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.humbaWW(state) or self.warp_to_inferno(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.humbaWW(state) or self.warp_to_inferno(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.humbaWW(state) or self.warp_to_inferno(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.glitchedInfernoAccess(state) or self.warp_to_inferno(state)
        return logic

    def a51_nests_from_TDL(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.oogle_boogles_open(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.oogle_boogles_open(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.oogle_boogles_open(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.oogle_boogles_open(state) or self.clockwork_warp(state)
        return logic

    def backdoors_enabled(self, state: CollectionState) -> bool:
        return self.world.options.backdoors

    def ggm_to_chuffy(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.climb(state) and self.small_elevation(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.small_elevation(state) or self.climb(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.small_elevation(state) or self.climb(state) or self.beak_buster(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.small_elevation(state) or self.climb(state) or self.beak_buster(state)
        return logic

    def ww_to_chuffy(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = state.has(itemName.TRAINSWWW, self.player) and (self.climb(state) and self.small_elevation(state))
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = state.has(itemName.TRAINSWWW, self.player) and (self.small_elevation(state) or self.climb(state))
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = state.has(itemName.TRAINSWWW, self.player) and (self.small_elevation(state) or self.climb(state))
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = state.has(itemName.TRAINSWWW, self.player) and (self.small_elevation(state) or self.climb(state))
        return logic

    def ioh_to_chuffy(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = state.has(itemName.TRAINSWIH, self.player) and (self.climb(state) and self.small_elevation(state))
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = state.has(itemName.TRAINSWIH, self.player) and (self.small_elevation(state) or self.climb(state))
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = state.has(itemName.TRAINSWIH, self.player) and (self.small_elevation(state) or self.climb(state) or self.beak_buster(state))
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = state.has(itemName.TRAINSWIH, self.player) and (self.small_elevation(state) or self.climb(state) or self.beak_buster(state))
        return logic

    # For this one, the ladder is farther off the ground.
    def tdl_to_chuffy(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = state.has(itemName.TRAINSWTD, self.player)\
                        and (self.climb(state) and self.small_elevation(state))
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = state.has(itemName.TRAINSWTD, self.player)\
                        and ((self.small_elevation(state) or self.beak_buster(state)) and self.climb(state)\
                            or self.flap_flip(state) and self.beak_buster(state))
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = state.has(itemName.TRAINSWTD, self.player)\
                        and (((self.small_elevation(state) or self.beak_buster(state)) and self.climb(state))\
                            or self.extremelyLongJump(state)\
                            or self.flap_flip(state) and self.beak_buster(state))
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = state.has(itemName.TRAINSWTD, self.player)\
                        and (((self.small_elevation(state) or self.beak_buster(state)) and self.climb(state))\
                            or self.extremelyLongJump(state)\
                            or self.flap_flip(state) and self.beak_buster(state))
        return logic

    #The train door is at ground level.
    def gi_to_chuffy(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = state.has(itemName.TRAINSWGI, self.player)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = state.has(itemName.TRAINSWGI, self.player)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = state.has(itemName.TRAINSWGI, self.player)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = state.has(itemName.TRAINSWGI, self.player)
        return logic

    #This one is pixels higher than WW or IoH, you can't just short jump to the ladder.
    def hfp_to_chuffy(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = state.has(itemName.TRAINSWHP1, self.player) and self.climb(state) and self.small_elevation(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = state.has(itemName.TRAINSWHP1, self.player) and (self.climb(state) and (self.small_elevation(state) or self.beak_buster(state)) or self.talon_trot(state))
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = state.has(itemName.TRAINSWHP1, self.player) and (self.climb(state) and (self.small_elevation(state) or self.beak_buster(state)) or self.talon_trot(state))
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = state.has(itemName.TRAINSWHP1, self.player) and (self.climb(state) and (self.small_elevation(state) or self.beak_buster(state)) or self.talon_trot(state))
        return logic

    def PGU_to_PG(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.grip_grab(state) or self.tall_jump(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.grip_grab(state) or self.tall_jump(state) or (self.beak_buster(state) and (self.flutter(state) or self.air_rat_a_tat_rap(state)))
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.grip_grab(state) or self.tall_jump(state) or self.beak_buster(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.grip_grab(state) or self.tall_jump(state) or self.beak_buster(state)
        return logic



    def QM_to_WL(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.grip_grab(state) and self.flap_flip(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = (self.grip_grab(state) or self.beak_buster(state)) and self.flap_flip(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = (self.grip_grab(state) or self.beak_buster(state)) and self.flap_flip(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = (self.grip_grab(state) or self.beak_buster(state)) and self.flap_flip(state)
        return logic

    def outside_gi_to_floor1(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = False
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = False
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = False
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.clockwork_shot(state)
        return logic

    def outside_gi_to_outside_back(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.climb(state) and self.flap_flip(state) and self.long_jump(state) and self.grip_grab(state) # The intended way to not take damage!
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.climb(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.climb(state) or self.extremelyLongJump(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.climb(state) or self.extremelyLongJump(state)
        return logic

    def outside_gi_back_to_floor2(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = False
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = False
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = False
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.clockwork_eggs(state) and (self.climb(state) or self.extremelyLongJump(state))
        return logic

    def outside_gi_to_flight(self, state: CollectionState) -> bool:
        return self.outside_gi_to_outside_back(state) and self.flight_pad(state) and self.gi_flight_pad_switch(state)

    def outside_gi_back_to_flight(self, state: CollectionState) -> bool:
        return self.climb(state) and self.flight_pad(state) and self.gi_flight_pad_switch(state)

    def outside_gi_back_to_floor_4(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = False
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.claw_clamber_boots(state) and (self.flutter(state) or self.air_rat_a_tat_rap(state)) and self.small_elevation(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.claw_clamber_boots(state) and (self.flutter(state) or self.air_rat_a_tat_rap(state)) and self.small_elevation(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.claw_clamber_boots(state) and (self.flutter(state) or self.air_rat_a_tat_rap(state)) and self.small_elevation(state)
        return logic

    def outside_gi_back_to_floor_3(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = False
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.claw_clamber_boots(state) and (self.flutter(state) or self.air_rat_a_tat_rap(state))
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.claw_clamber_boots(state) and (self.flutter(state) or self.air_rat_a_tat_rap(state))
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.claw_clamber_boots(state) and (self.flutter(state) or self.air_rat_a_tat_rap(state))
        return logic

    def em_chamber_to_elevator_shaft(self, state: CollectionState) -> bool:
        return self.elevator_door(state)

    def boiler_plant_to_elevator_shaft(self, state: CollectionState) -> bool:
        return self.elevator_door(state)

    def floor_4_back_to_elevator_shaft(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.climb(state) and self.elevator_door(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.climb(state) and self.elevator_door(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.climb(state) and self.elevator_door(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.climb(state) and self.elevator_door(state)\
                    or state.can_reach_region(regionName.GI4, self.player) and self.clockwork_warp(state) and (self.spring_pad(state) or self.flap_flip(state))
        return logic

    # If you can fly, then you can enter floor 1 from the window.
    def flight_to_floor_1(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = (self.beak_bomb(state) or self.egg_aim(state) or self.airborne_egg_aiming(state))\
                    and (self.flutter(state) or self.air_rat_a_tat_rap(state))
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = (self.beak_bomb(state)\
                        or self.egg_aim(state)\
                        or self.airborne_egg_aiming(state)\
                        or self.has_explosives(state))\
                    and (self.flutter(state) or self.air_rat_a_tat_rap(state))
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = (self.beak_bomb(state)\
                    or self.egg_aim(state)\
                    or self.airborne_egg_aiming(state)\
                    or self.has_explosives(state))
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = (self.beak_bomb(state)\
                    or self.egg_aim(state)\
                    or self.airborne_egg_aiming(state)\
                    or self.has_explosives(state))
        return logic

    def flight_to_boiler_plant(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.flight_pad(state) and (self.beak_bomb(state) or self.has_explosives(state) and (self.egg_aim(state) or self.airborne_egg_aiming(state)))
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.flight_pad(state) and (self.beak_bomb(state) or self.has_explosives(state) and (self.egg_aim(state) or self.airborne_egg_aiming(state)))
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.flight_pad(state) and (self.beak_bomb(state) or self.has_explosives(state) and (self.egg_aim(state) or self.airborne_egg_aiming(state)))
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.flight_pad(state) and (self.beak_bomb(state) or self.has_explosives(state) and (self.egg_aim(state) or self.airborne_egg_aiming(state)))
        return logic

    def roof_to_upper_floors(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = False
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.beak_buster(state) or self.flutter(state) or self.air_rat_a_tat_rap(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = True
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = True
        return logic

    def roof_to_ground_level(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = False
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.beak_buster(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.beak_buster(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.beak_buster(state)
        return logic

    # This is disgusting, but will get rewritten later.
    def roof_to_floor5(self, state: CollectionState) -> bool:
        return self.leg_spring(state) or self.spring_pad(state)

    def elevator_shaft_to_floor_1(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.climb(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.climb(state) or self.beak_buster(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.climb(state) or self.beak_buster(state)\
                    or state.can_reach_region(regionName.GI2EM, self.player) and self.em_chamber_to_elevator_shaft(state)\
                    or state.can_reach_region(regionName.GI3B, self.player) and self.health_7(state) and self.boiler_plant_to_elevator_shaft(state)\
                    or state.can_reach_region(regionName.GI4B, self.player) and self.health_10(state) and self.floor_4_back_to_elevator_shaft(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.climb(state) or self.beak_buster(state)\
                    or state.can_reach_region(regionName.GI2EM, self.player) and self.em_chamber_to_elevator_shaft(state)\
                    or state.can_reach_region(regionName.GI3B, self.player) and self.health_7(state) and self.boiler_plant_to_elevator_shaft(state)\
                    or state.can_reach_region(regionName.GI4B, self.player) and self.health_10(state) and self.floor_4_back_to_elevator_shaft(state)
        return logic

    def elevator_shaft_to_em(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = False
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = False
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = False
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = (self.climb(state)\
                        or state.can_reach_region(regionName.GI3B, self.player) and self.boiler_plant_to_elevator_shaft(state)\
                        or state.can_reach_region(regionName.GI4B, self.player) and (self.health_7(state) or self.beak_buster(state)) and self.floor_4_back_to_elevator_shaft(state))\
                    and self.breegull_bash(state)
        return logic

    def elevator_shaft_to_boiler_plant(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = False
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = False
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = False
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = (self.climb(state)\
                        or state.can_reach_region(regionName.GI4B, self.player) and self.floor_4_back_to_elevator_shaft(state))\
                    and self.breegull_bash(state)
        return logic

    def elevator_shaft_to_floor_4(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = False
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = False
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = False
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.climb(state) and (self.breegull_bash(state) or self.grenade_eggs(state) and self.egg_aim(state))
        return logic


    def health_6(self, state: CollectionState) -> bool:
        return state.can_reach_region(regionName.IOHPL, self.player) and state.has(itemName.HONEY, self.player, 1) and self.talon_trot(state)

    def health_7(self, state: CollectionState) -> bool:
        return state.can_reach_region(regionName.IOHPL, self.player) and state.has(itemName.HONEY, self.player, 4) and self.talon_trot(state)

    def health_8(self, state: CollectionState) -> bool:
        return state.can_reach_region(regionName.IOHPL, self.player) and state.has(itemName.HONEY, self.player, 9) and self.talon_trot(state)

    def health_9(self, state: CollectionState) -> bool:
        return state.can_reach_region(regionName.IOHPL, self.player) and state.has(itemName.HONEY, self.player, 16) and self.talon_trot(state)

    def health_10(self, state: CollectionState) -> bool:
        return state.can_reach_region(regionName.IOHPL, self.player) and state.has(itemName.HONEY, self.player, 25) and self.talon_trot(state)

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
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.claw_clamber_boots(state) and (self.spring_pad(state) or self.leg_spring(state))
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.claw_clamber_boots(state) and (self.spring_pad(state) or self.leg_spring(state))\
                    or self.leg_spring(state) and self.glide(state) and (self.wing_whack(state) or self.egg_aim(state))
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.claw_clamber_boots(state) and (self.spring_pad(state) or self.leg_spring(state))\
                    or self.leg_spring(state) and self.glide(state) and (self.wing_whack(state) or self.egg_aim(state))
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.claw_clamber_boots(state) and (self.spring_pad(state) or self.leg_spring(state))\
                    or self.leg_spring(state) and self.glide(state) and (self.wing_whack(state) or self.egg_aim(state))
        return logic

    def F1_to_F5(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.gi_low_flight_pad_solo_kazooie(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.gi_low_flight_pad_solo_kazooie(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.gi_low_flight_pad_solo_kazooie(state)\
                    or self.split_up(state) and self.claw_clamber_boots(state) and self.leg_spring(state) and (self.wing_whack(state) or self.egg_aim(state)) and self.flight_pad(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.gi_low_flight_pad_solo_kazooie(state)\
                    or self.split_up(state) and self.claw_clamber_boots(state) and self.leg_spring(state) and (self.wing_whack(state) or self.egg_aim(state)) and self.flight_pad(state)
        return logic

    def F2_to_F1(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.grip_grab(state) and self.flap_flip(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = (self.grip_grab(state) or self.beak_buster(state)) and self.flap_flip(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = (self.grip_grab(state) or self.beak_buster(state)) and self.flap_flip(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = (self.grip_grab(state) or self.beak_buster(state)) and self.flap_flip(state)
        return logic


    def F2_to_F3(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = (self.flap_flip(state) and self.grip_grab(state) and self.claw_clamber_boots(state) and self.climb(state))
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = ((self.flap_flip(state) and self.grip_grab(state) or self.veryLongJump(state)) and self.claw_clamber_boots(state) and self.climb(state))\
                    or self.leg_spring(state) and self.floor_2_split_up(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = ((self.flap_flip(state) and self.grip_grab(state) or self.veryLongJump(state)) and self.claw_clamber_boots(state) and self.climb(state))\
                    or self.leg_spring(state) and self.floor_2_split_up(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = ((self.flap_flip(state) and self.grip_grab(state) or self.veryLongJump(state))\
                        and self.claw_clamber_boots(state)\
                        and (self.climb(state) or (self.grenade_eggs(state) and self.third_person_egg_shooting(state) and self.flap_flip(state) and self.beak_buster(state))))\
                    or self.leg_spring(state) and self.floor_2_split_up(state)
        return logic

    def floor_2_to_em_room(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.floor_2_split_up(state) and self.grip_grab(state) and self.can_use_battery(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.floor_2_split_up(state) and self.can_use_battery(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.floor_2_split_up(state) and self.can_use_battery(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.floor_2_split_up(state) and self.can_use_battery(state)
        return logic

    def floor_2_em_room_to_elevator_shaft(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.elevator_door(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.elevator_door(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.elevator_door(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.elevator_door(state)
        return logic

    def floor_2_split_up(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.split_up(state) and\
                    (self.climb(state) or self.has_explosives(state))
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.split_up(state) and\
                    (self.climb(state) or self.has_explosives(state))
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.split_up(state) and\
                    (self.climb(state) or self.has_explosives(state) or self.claw_clamber_boots(state) and self.extremelyLongJump(state))
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.split_up(state) and\
                    (self.climb(state) or self.has_explosives(state) or self.claw_clamber_boots(state) and self.extremelyLongJump(state))
        return logic

    def F3_to_F2(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.climb(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.climb(state) or (self.flap_flip(state) and self.beak_buster(state) and self.veryLongJump(state))
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.climb(state) or (self.flap_flip(state) and self.veryLongJump(state))
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.climb(state) or (self.flap_flip(state) and self.veryLongJump(state))
        return logic

    def F3_to_F4(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = (self.climb(state) or self.leg_spring(state)) and self.small_elevation(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = (self.climb(state) or self.leg_spring(state)) and self.small_elevation(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = (self.climb(state) or self.leg_spring(state)) and self.small_elevation(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = (self.climb(state) or self.leg_spring(state)) and self.small_elevation(state)
        return logic

    # This function is used to know if bringing solo Kazooie to a floor using warp pads is possible.
    def solo_kazooie_gi(self, state: CollectionState) -> bool:
        return self.split_up(state) and (\
                state.can_reach_region(regionName.GI1, self.player)\
                or state.can_reach_region(regionName.GI2, self.player) and self.floor_2_split_up(state)\
                or state.can_reach_region(regionName.GI3, self.player) and self.small_elevation(state) and (self.tall_jump(state) or self.leg_spring(state))\
                or state.can_reach_region(regionName.GI4, self.player) and self.small_elevation(state)\
                )

    def drop_down_from_higher_floors_outside(self, state: CollectionState) -> bool:
        if self.world.options.logic_type == LogicType.option_intended:
            logic = False
        elif self.world.options.logic_type == LogicType.option_easy_tricks : # normal
            logic = self.beak_buster(state) or self.flutter(state) or self.air_rat_a_tat_rap(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = True
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = True
        return logic

    def escape_floor_4_bk(self, state: CollectionState) -> bool:
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.springy_step_shoes(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks : # normal
            logic = self.springy_step_shoes(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.springy_step_shoes(state) or self.flap_flip(state) and self.grip_grab(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.springy_step_shoes(state) or self.flap_flip(state) and self.grip_grab(state)
        return logic

    def floor_4_to_outside_back(self, state: CollectionState) -> bool:
        return self.escape_floor_4_bk(state) and self.drop_down_from_higher_floors_outside(state)

    def floor_3_to_outside_back(self, state: CollectionState) -> bool:
        return self.climb(state) and self.drop_down_from_higher_floors_outside(state)

    def floor_4_to_floor_3(self, state: CollectionState) -> bool:
        #Small elevation to reach the floor 4 split up pad
        return self.escape_floor_4_bk(state) or self.leg_spring(state) and (self.small_elevation(state) or self.solo_kazooie_gi(state))

    def floor_4_to_floor_4_back(self, state: CollectionState) -> bool:
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.mumboGI(state) and self.tall_jump(state)\
                    and state.has(itemName.WARPGI3, self.player) and state.has(itemName.WARPGI4, self.player)
        elif self.world.options.logic_type == LogicType.option_easy_tricks : # normal
            logic = self.mumboGI(state) and self.tall_jump(state)\
                    and state.has(itemName.WARPGI3, self.player) and state.has(itemName.WARPGI4, self.player)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.mumboGI(state) and self.tall_jump(state)\
                    and state.has(itemName.WARPGI3, self.player) and state.has(itemName.WARPGI4, self.player)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.mumboGI(state) and self.tall_jump(state)\
                        and state.has(itemName.WARPGI3, self.player) and state.has(itemName.WARPGI4, self.player)\
                    or self.tall_jump(state) and self.pack_whack(state)\
                    or self.precise_clockwork_warp(state) and (self.spring_pad(state) or self.flap_flip(state))
        return logic

    def floor_4_to_floor_5(self, state: CollectionState) -> bool:
        if self.world.options.logic_type == LogicType.option_intended:
            logic = False
        elif self.world.options.logic_type == LogicType.option_easy_tricks : # normal
            logic = self.leg_spring(state) and self.flight_pad(state) and self.solo_kazooie_gi(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.leg_spring(state) and self.flight_pad(state) and self.solo_kazooie_gi(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.leg_spring(state) and self.flight_pad(state) and self.solo_kazooie_gi(state)
        return logic

    def floor_3_to_floor_5(self, state: CollectionState) -> bool:
        if self.world.options.logic_type == LogicType.option_intended:
            logic = False
        elif self.world.options.logic_type == LogicType.option_easy_tricks : # normal
            logic = self.leg_spring(state) and self.flight_pad(state) and self.solo_kazooie_gi(state) and self.gi_flight_pad_switch(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.leg_spring(state) and self.flight_pad(state) and self.solo_kazooie_gi(state) and self.gi_flight_pad_switch(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.leg_spring(state) and self.flight_pad(state) and self.solo_kazooie_gi(state) and self.gi_flight_pad_switch(state)
        return logic

    def floor_3_to_boiler_plant(self, state: CollectionState) -> bool:
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.flap_flip(state) and self.grip_grab(state)\
                    or self.climb(state) and self.slightly_elevated_ledge(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks : # normal
            logic = self.flap_flip(state) and self.grip_grab(state)\
                    or self.climb(state) and self.slightly_elevated_ledge(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.flap_flip(state) and self.grip_grab(state)\
                    or self.climb(state) and self.slightly_elevated_ledge(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.flap_flip(state) and self.grip_grab(state)\
                    or self.climb(state) and self.slightly_elevated_ledge(state)
        return logic

    def WL_to_PGU(self, state: CollectionState) -> bool:
        logic = True
        # Going through the loading zone gives you dive for free, which is a thing beginners would not know.
        # If nestsanity is turned on, players are forced to go through the digger tunnel
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.talon_torpedo(state) and self.dive(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks : # normal
            logic = self.talon_torpedo(state)\
                    and (not self.world.options.nestsanity or self.dive(state) or self.beak_buster(state))
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.talon_torpedo(state)\
                    and (not self.world.options.nestsanity or self.dive(state) or self.beak_buster(state))
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = (not self.world.options.nestsanity or self.dive(state) or self.beak_buster(state))
        return logic

    def tdl_to_hatch(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.long_jump(state)\
                    or self.springy_step_shoes(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.long_jump(state)\
                    or self.springy_step_shoes(state)\
                    or self.split_up(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.long_jump(state)\
                    or self.springy_step_shoes(state)\
                    or state.can_reach_region(regionName.TLTOP, self.player)\
                    or self.split_up(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.long_jump(state)\
                    or self.springy_step_shoes(state)\
                    or self.TDL_flight_pad(state)\
                    or self.split_up(state)\
                    or state.can_reach_region(regionName.TLTOP, self.player)
        return logic

    def can_dive_in_jrl(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.dive(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.dive(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.dive(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.dive(state)
        return logic

    def JRL_to_CT(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.jrl_jiggy(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = True
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = True
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = True
        return logic

    def HFP_to_CTHFP(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.hfp_jiggy(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = True
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = True
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = True
        return logic

    def CCL_to_WL(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.ccl_jiggy(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = True
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = True
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = True
        return logic

    def CK_to_Quag(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.ck_jiggy(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = True
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = True
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = True
        return logic

    def TDL_to_IOHWL(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.tdl_jiggy(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = True
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = True
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = True
        return logic

    def TDL_to_WW(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.oogle_boogles_open(state) and (self.spring_pad(state) or self.has_explosives(state))
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.oogle_boogles_open(state) and (self.spring_pad(state) or self.has_explosives(state))
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.oogle_boogles_open(state) and (self.spring_pad(state) or self.has_explosives(state))
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = (self.spring_pad(state) or self.has_explosives(state)) and (self.oogle_boogles_open(state) or \
                self.clockwork_warp(state))
        return logic

    def hfp_jiggy(self, state: CollectionState) -> bool: # 36
        if self.world.worlds_randomized:
            return state.has(itemName.HFA, self.player)
        else:
            amt = self.world.randomize_worlds[regionName.HP]
            return state.has(itemName.JIGGY, self.player, amt)

    def ccl_jiggy(self, state: CollectionState) -> bool: # 45
        if self.world.worlds_randomized:
            return state.has(itemName.CCA, self.player)
        else:
            amt = self.world.randomize_worlds[regionName.CC]
            return state.has(itemName.JIGGY, self.player, amt)

    def HFP_hot_water_cooled(self, state) -> bool:
        if self.world.options.backdoors:
            return state.can_reach_region(regionName.HP, self.player) and\
               self.split_up(state) and\
               (self.dive(state) or self.shack_pack(state))
        else:
            return state.can_reach_region(regionName.HP, self.player) and\
               state.can_reach_region(regionName.CC, self.player) and \
               self.split_up(state) and\
               self.ground_attack(state) and\
               (self.dive(state) or self.shack_pack(state))

    def can_use_floatus(self, state) -> bool:
        return self.taxi_pack(state) and self.hatch(state)

    def grow_beanstalk(self, state: CollectionState) -> bool:
        return self.bill_drill(state) and self.mumboCCL(state) and self.flight_pad(state) and self.climb(state)

    def check_hag1_options(self, state: CollectionState) -> bool:
        enough_jiggies = self.world.options.open_hag1 == 1 or state.has(itemName.JIGGY, self.player, 70)
        if self.world.options.logic_type == LogicType.option_intended:
            return enough_jiggies and \
                self.warp_pad_ck_top(state) and \
                self.breegull_blaster(state) and \
                self.clockwork_eggs(state)\
                and self.can_shoot_linear_egg(state)\
                and (self.talon_trot(state) and self.tall_jump(state))
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            return enough_jiggies and \
                self.warp_pad_ck_top(state) and \
                self.breegull_blaster(state) and \
                self.clockwork_eggs(state)\
                and self.can_shoot_linear_egg(state)\
                and (self.talon_trot(state) or self.tall_jump(state))
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            return enough_jiggies and \
                self.warp_pad_ck_top(state) and \
                self.breegull_blaster(state) and \
                self.clockwork_eggs(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            return enough_jiggies and \
                self.warp_pad_ck_top(state) and \
                self.breegull_blaster(state) and \
                self.clockwork_eggs(state)

    def reach_cheato(self, state: CollectionState, page_amt: int) -> bool:
        return state.has(itemName.PAGES, self.player, page_amt)

    def has_BK_move(self, state: CollectionState, move) -> bool:
        if move == itemName.BEGGS:
            raise ValueError("Use self.blueEgg(state) instead!")
        if move not in [itemName.DIVE, itemName.FPAD, itemName.GRAT, itemName.ROLL, itemName.ARAT, itemName.BBARGE, itemName.TJUMP, itemName.FLUTTER, itemName.FFLIP, itemName.CLIMB, itemName.TTROT, itemName.BBUST, itemName.WWING, itemName.SSTRIDE, itemName.TTRAIN, itemName.BBOMB, itemName.EGGAIM, itemName.EGGSHOOT]:
            raise ValueError("Not a BK move! {}".format(move))
        if self.world.options.randomize_bk_moves == RandomizeBKMoveList.option_none:
            return True
        if self.world.options.randomize_bk_moves == RandomizeBKMoveList.option_mcjiggy_special and move in [itemName.TTROT, itemName.TJUMP]:
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
        return self.blue_eggs(state) or self.fire_eggs(state) or self.grenade_eggs(state) or self.ice_eggs(state) or self.beak_barge(state) or self.roll(state) or self.air_rat_a_tat_rap(state)

    def can_shoot_any_egg(self, state: CollectionState) -> bool:
        return self.egg_aim(state) or self.third_person_egg_shooting(state)

    # The regular variant of the function check to see if you can shoot the eggs, the "item" variant only checks if you have the egg item
    def blue_eggs(self, state: CollectionState) -> bool:
        if not self.can_shoot_any_egg(state):
            return False
        return self.blue_eggs_item(state)

    def blue_eggs_item(self, state: CollectionState) -> bool:
        if self.world.options.egg_behaviour == EggsBehaviour.option_random_starting_egg or \
            self.world.options.egg_behaviour == EggsBehaviour.option_simple_random_starting_egg:
            return state.has(itemName.BEGGS, self.player)
        return True

    def fire_eggs(self, state: CollectionState) -> bool:
        if not self.can_shoot_any_egg(state):
            return False
        return self.fire_eggs_item(state)

    def fire_eggs_item(self, state: CollectionState) -> bool:
        if self.world.options.egg_behaviour == EggsBehaviour.option_progressive_eggs:
            return state.has(itemName.PEGGS, self.player, 1)
        return state.has(itemName.FEGGS, self.player)

    def grenade_eggs(self, state: CollectionState) -> bool:
        if not self.can_shoot_any_egg(state):
            return False
        return self.grenade_eggs_item(state)

    def grenade_eggs_item(self, state: CollectionState) -> bool:
        if self.world.options.egg_behaviour == EggsBehaviour.option_progressive_eggs:
            return state.has(itemName.PEGGS, self.player, 2)
        return state.has(itemName.GEGGS, self.player)

    def ice_eggs(self, state: CollectionState) -> bool:
        if not self.can_shoot_any_egg(state):
            return False
        return self.ice_eggs_item(state)

    def ice_eggs_item(self, state: CollectionState) -> bool:
        if self.world.options.egg_behaviour == EggsBehaviour.option_progressive_eggs:
            return state.has(itemName.PEGGS, self.player, 3)
        return state.has(itemName.IEGGS, self.player)

    def clockwork_eggs(self, state: CollectionState) -> bool:
        if not self.can_shoot_any_egg(state):
            return False
        return self.clockwork_eggs_item(state)

    def clockwork_eggs_item(self, state: CollectionState) -> bool:
        if self.world.options.egg_behaviour == EggsBehaviour.option_progressive_eggs:
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
        if self.world.options.skip_klungo == 1:
            return True
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.mobile_attack(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.mobile_attack(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.ground_attack(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.ground_attack(state)
        return logic

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

    def long_jump(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.talon_trot(state) or self.flutter(state) or self.air_rat_a_tat_rap(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.talon_trot(state) or self.flutter(state) or self.air_rat_a_tat_rap(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.talon_trot(state) or self.flutter(state) or self.air_rat_a_tat_rap(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.talon_trot(state) or self.flutter(state) or self.air_rat_a_tat_rap(state)
        return logic

    def veryLongJump(self, state: CollectionState) -> bool:
        return self.talon_trot(state) and (self.flutter(state) or self.air_rat_a_tat_rap(state)) or\
                (self.tall_jump(state) and self.roll(state) and self.flutter(state))

    def extremelyLongJump(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = False
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = False
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.talon_trot(state) and (self.flutter(state) or self.air_rat_a_tat_rap(state)) and self.beak_buster(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.talon_trot(state) and (self.flutter(state) or self.air_rat_a_tat_rap(state)) and self.beak_buster(state)
        return logic

    def humbaMT(self, state: CollectionState) -> bool:
        return state.can_reach_region(regionName.MTJSG, self.player) and state.has(itemName.HUMBAMT, self.player)

    def humbaGGM(self, state: CollectionState) -> bool:
        return state.has(itemName.HUMBAGM, self.player) and state.can_reach_location(locationName.WARPGM3, self.player)


    def mumboGGM(self, state: CollectionState) -> bool:
        return self.small_elevation(state) and state.has(itemName.MUMBOGM, self.player)

    def ggm_trot(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.talon_trot(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.talon_trot(state) or self.turbo_trainers(state) or self.springy_step_shoes(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.talon_trot(state) or self.turbo_trainers(state) or self.springy_step_shoes(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.talon_trot(state) or self.turbo_trainers(state) or self.springy_step_shoes(state)
        return logic

    def humbaWW(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = state.has(itemName.HUMBAWW, self.player) and (
                        self.flap_flip(state) and self.grip_grab(state)\
                        or self.warp_to_ww_wumba(state)
                    )
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = state.has(itemName.HUMBAWW, self.player) and (
                        self.flap_flip(state) and self.grip_grab(state) \
                        or self.climb(state) and self.veryLongJump(state) and self.flap_flip(state)\
                        or self.warp_to_ww_wumba(state)
                    )
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = state.has(itemName.HUMBAWW, self.player) and (
                        self.flap_flip(state) and self.grip_grab(state) \
                        or self.climb(state) and self.veryLongJump(state) and self.flap_flip(state)\
                        or self.warp_to_ww_wumba(state)
                    )
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = state.has(itemName.HUMBAWW, self.player) and (
                        self.flap_flip(state) and self.grip_grab(state) \
                        or self.climb(state) and self.veryLongJump(state) and self.flap_flip(state)\
                        or self.warp_to_ww_wumba(state)
                    )
        return logic

    def mumboWW(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = state.can_reach_region(regionName.WWI, self.player) and state.has(itemName.MUMBOWW, self.player)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = state.can_reach_region(regionName.WWI, self.player) and state.has(itemName.MUMBOWW, self.player)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = state.can_reach_region(regionName.WWI, self.player) and state.has(itemName.MUMBOWW, self.player)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = state.can_reach_region(regionName.WWI, self.player) and state.has(itemName.MUMBOWW, self.player)\
                    and self.escape_inferno_as_mumbo(state)
        return logic

    def escape_inferno_as_mumbo(self, state: CollectionState) -> bool:
        return self.humbaWW(state)\
                or state.has(itemName.WARPWW5, self.player) and (
                    state.has(itemName.WARPWW1, self.player)\
                    or state.has(itemName.WARPWW2, self.player)\
                    or state.has(itemName.WARPWW3, self.player)\
                    or state.has(itemName.WARPWW4, self.player)
                )

    def mumboTDL(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.stilt_stride(state) and state.has(itemName.MUMBOTD, self.player)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = state.has(itemName.MUMBOTD, self.player)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = state.has(itemName.MUMBOTD, self.player)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = state.has(itemName.MUMBOTD, self.player)
        return logic

    def mumboGI(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.small_elevation(state) and state.has(itemName.MUMBOGI, self.player) and state.can_reach_region(regionName.GI3, self.player)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.small_elevation(state) and state.has(itemName.MUMBOGI, self.player) and state.can_reach_region(regionName.GI3, self.player)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = state.has(itemName.MUMBOGI, self.player) and state.can_reach_region(regionName.GI3, self.player) and \
                    self.small_elevation(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = state.has(itemName.MUMBOGI, self.player) and state.can_reach_region(regionName.GI3, self.player) and \
                    self.small_elevation(state)
        return logic

    def humbaGI(self, state: CollectionState) -> bool:
        return state.has(itemName.HUMBAGI, self.player) and state.can_reach_region(regionName.GI2, self.player)

    def humbaHFP(self, state: CollectionState) -> bool:
        return self.hfp_top(state) and state.has(itemName.HUMBAHP, self.player)

    def mumboCCL(self, state: CollectionState) -> bool:
        return self.tall_jump(state) and state.has(itemName.MUMBOCC, self.player)

    def humbaJRL(self, state: CollectionState) -> bool:
        return state.can_reach_region(regionName.JRAT, self.player) and state.has(itemName.HUMBAJR, self.player)

    def humbaTDL(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.small_elevation(state) and state.has(itemName.HUMBATD, self.player)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = state.has(itemName.HUMBATD, self.player)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = state.has(itemName.HUMBATD, self.player)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = state.has(itemName.HUMBATD, self.player)
        return logic

    def bargasaurus_roar(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.humbaTDL(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.humbaTDL(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.humbaTDL(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.humbaTDL(state)
        return logic

    def roar(self, state: CollectionState) -> bool:
        return state.has(itemName.ROAR, self.player) or not self.world.options.randomize_dino_roar

    def TDL_flight_pad(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.can_beat_terry(state) and self.springy_step_shoes(state) and self.flight_pad(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.can_beat_terry(state) and self.flight_pad(state)\
                    and (self.springy_step_shoes(state) or (self.talon_trot(state) and self.flutter(state)))
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.can_beat_terry(state) and self.flight_pad(state)\
                    and (self.springy_step_shoes(state) or (self.talon_trot(state) and self.flutter(state)))
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.can_beat_terry(state) and self.flight_pad(state)\
                    and (self.springy_step_shoes(state) or (self.talon_trot(state) and self.flutter(state)))
        return logic

    def GGM_slope(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.ggm_trot(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.ggm_trot(state) or (self.GM_boulders(state) and self.split_up(state))
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.ggm_trot(state) or (self.GM_boulders(state) and self.split_up(state))
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.ggm_trot(state) or (self.GM_boulders(state) and self.split_up(state))
        return logic

    def clockwork_shot(self, state: CollectionState) -> bool:
        return self.clockwork_eggs(state) and self.egg_aim(state)

    def egg_barge(self, state: CollectionState) -> bool:
        return (self.blue_eggs(state) or self.fire_eggs(state) or self.ice_eggs(state)) and self.third_person_egg_shooting(state) and self.beak_barge(state)

    def can_dive_in_JRL(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.dive(state) and state.has(itemName.MUMBOJR, self.player)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.dive(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.dive(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.dive(state)
        return logic

    def hfp_top(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.small_elevation(state)\
                    or self.flight_pad(state)\
                    or (state.can_reach_region(regionName.CHUFFY, self.player) and state.has(itemName.TRAINSWHP1, self.player))\
                    or self.has_explosives(state)\
                    or self.warp_to_hfp_top(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.small_elevation(state)\
                    or self.flight_pad(state)\
                    or state.can_reach_region(regionName.CHUFFY, self.player) and state.has(itemName.TRAINSWHP1, self.player)\
                    or self.has_explosives(state)\
                    or state.has(itemName.MUMBOHP, self.player)\
                    or self.dragon_kazooie(state)\
                    or self.warp_to_hfp_top(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.small_elevation(state)\
                    or self.flight_pad(state)\
                    or self.split_up(state)\
                    or state.can_reach_region(regionName.CHUFFY, self.player) and state.has(itemName.TRAINSWHP1, self.player)\
                    or self.has_explosives(state)\
                    or state.has(itemName.MUMBOHP, self.player)\
                    or self.dragon_kazooie(state)\
                    or self.warp_to_hfp_top(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.small_elevation(state)\
                    or self.flight_pad(state)\
                    or self.split_up(state)\
                    or state.can_reach_region(regionName.CHUFFY, self.player) and state.has(itemName.TRAINSWHP1, self.player)\
                    or self.has_explosives(state)\
                    or state.has(itemName.MUMBOHP, self.player)\
                    or self.dragon_kazooie(state)\
                    or self.warp_to_hfp_top(state)
        return logic

    def notes_boggy(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.ice_cube_BK(state) and self.hfp_top(state) and self.small_elevation(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.hfp_top(state)\
                        and (self.ice_cube_BK(state) and (self.small_elevation(state) or self.beak_buster(state))\
                             or self.split_up(state) and (self.leg_spring(state) or self.tall_jump(state)) and self.ice_cube_kazooie(state)\
                             or self.tall_jump(state) and state.has(itemName.MUMBOHP, self.player)\
                             or self.pack_whack(state)\
                             or self.humbaHFP(state)
                             )
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.hfp_top(state)\
                        and (self.ice_cube_BK(state) and (self.small_elevation(state) or self.beak_buster(state))\
                             or self.split_up(state) and (self.leg_spring(state) or self.tall_jump(state)) and self.ice_cube_kazooie(state)\
                             or self.tall_jump(state) and state.has(itemName.MUMBOHP, self.player)\
                             or self.pack_whack(state)\
                             or self.clockwork_shot(state)\
                             or self.humbaHFP(state)
                             )
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.hfp_top(state)\
                        and (self.ice_cube_BK(state) and (self.small_elevation(state) or self.beak_buster(state))\
                             or self.split_up(state) and (self.leg_spring(state) or self.tall_jump(state)) and self.ice_cube_kazooie(state)\
                             or self.tall_jump(state) and state.has(itemName.MUMBOHP, self.player)\
                             or self.pack_whack(state)\
                             or self.clockwork_shot(state)\
                             or self.humbaHFP(state)
                             )
        return logic

    def notes_lower_icy_side(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.ice_cube_BK(state) and self.hfp_top(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.hfp_top(state)\
                        and (self.ice_cube_BK(state)\
                             or self.split_up(state) and self.ice_cube_kazooie(state)\
                             or state.has(itemName.MUMBOHP, self.player)\
                             or self.pack_whack(state)\
                             or self.humbaHFP(state)
                             )
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.hfp_top(state)\
                        and (self.ice_cube_BK(state)\
                             or self.split_up(state) and self.ice_cube_kazooie(state)\
                             or state.has(itemName.MUMBOHP, self.player)\
                             or self.pack_whack(state)\
                             or self.humbaHFP(state)
                             )
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.hfp_top(state)\
                        and (self.ice_cube_BK(state)\
                             or self.split_up(state) and self.ice_cube_kazooie(state)\
                             or state.has(itemName.MUMBOHP, self.player)\
                             or self.pack_whack(state)\
                             or self.humbaHFP(state)
                             )
        return logic

    def notes_upper_icy_side(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.ice_cube_BK(state) and self.hfp_top(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.hfp_top(state)\
                        and (self.ice_cube_BK(state)\
                             or self.split_up(state) and self.ice_cube_kazooie(state)\
                             or state.has(itemName.MUMBOHP, self.player)\
                             or self.pack_whack(state)\
                             or self.humbaHFP(state)
                             )
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.hfp_top(state)\
                        and (self.ice_cube_BK(state)\
                             or self.split_up(state) and self.ice_cube_kazooie(state)\
                             or state.has(itemName.MUMBOHP, self.player)\
                             or self.pack_whack(state)\
                             or self.humbaHFP(state)
                             )
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.hfp_top(state)\
                        and (self.ice_cube_BK(state)\
                             or self.split_up(state) and self.ice_cube_kazooie(state)\
                             or state.has(itemName.MUMBOHP, self.player)\
                             or self.pack_whack(state)\
                             or self.humbaHFP(state)
                             )
        return logic

    def ice_cube_BK(self, state: CollectionState) -> bool:
        return self.blue_eggs(state) or self.fire_eggs(state) or self.has_explosives(state) or self.beak_barge(state) or self.roll(state)\
            or self.air_rat_a_tat_rap(state) or self.ground_rat_a_tat_rap(state) or self.beak_buster(state) or self.breegull_bash(state) or self.wonderwing(state)

    def ice_cube_kazooie(self, state: CollectionState) -> bool:
        return self.split_up(state) and (self.has_explosives(state) or self.fire_eggs(state) or self.blue_eggs(state) or self.wing_whack(state))

    def gi_flight_pad_switch(self, state: CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = state.can_reach_region(regionName.GI4, self.player)\
                    or self.humbaGI(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = state.can_reach_region(regionName.GI4, self.player)\
                    or self.humbaGI(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = state.can_reach_region(regionName.GI4, self.player)\
                    or self.humbaGI(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = state.can_reach_region(regionName.GI4, self.player)\
                    or self.humbaGI(state)
        return logic

    def big_al_burgers(self, state:CollectionState) -> bool:
        logic = True
        if self.world.options.logic_type == LogicType.option_intended:
            logic = self.tall_jump(state)
        elif self.world.options.logic_type == LogicType.option_easy_tricks:
            logic = self.tall_jump(state) or self.leg_spring(state) or self.glide(state)
        elif self.world.options.logic_type == LogicType.option_hard_tricks:
            logic = self.tall_jump(state) or self.leg_spring(state) or self.glide(state)
        elif self.world.options.logic_type == LogicType.option_glitches:
            logic = self.tall_jump(state) or self.leg_spring(state) or self.glide(state)
        return logic

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

        if self.world.options.nestsanity:
            for location, rules in self.nest_rules.items():
                nest = self.world.multiworld.get_location(location, self.player)
                set_rule(nest, rules)

        if self.world.options.randomize_signposts:
            for location, rules in self.signpost_rules.items():
                sign = self.world.multiworld.get_location(location, self.player)
                set_rule(sign, rules)

        if self.world.options.skip_puzzles:
            for location, rules in self.access_rules.items():
                access = self.world.multiworld.get_location(location, self.player)
                set_rule(access, rules)

        set_rule(self.world.multiworld.get_location(locationName.ROARDINO, self.player), lambda state: self.bargasaurus_roar(state))


        if self.world.options.cheato_rewards:
            for location, rules in self.cheato_rewards_rules.items():
                cheato = self.world.multiworld.get_location(location, self.player)
                set_rule(cheato, rules)

        if self.world.options.honeyb_rewards:
            for location, rules in self.honeyb_rewards_rules.items():
                honeyb = self.world.multiworld.get_location(location, self.player)
                set_rule(honeyb, rules)

        for location, rules in self.scrit_scrat_scrut_rules.items():
                dinos = self.world.multiworld.get_location(location, self.player)
                set_rule(dinos, rules)

        for location, rules in self.warp_pad_rules.items():
                warp_pads = self.world.multiworld.get_location(location, self.player)
                set_rule(warp_pads, rules)

        if self.world.options.victory_condition == VictoryCondition.option_minigame_hunt:
            for location, rules in self.gametoken_rules.items():
                tokens = self.world.multiworld.get_location(location, self.player)
                set_rule(tokens, rules)
            self.world.multiworld.completion_condition[self.player] = lambda state: state.has(itemName.MUMBOTOKEN, self.player, self.world.options.minigame_hunt_length)
        elif self.world.options.victory_condition == VictoryCondition.option_boss_hunt:
            for location, rules in self.bosstoken_rules.items():
                tokens = self.world.multiworld.get_location(location, self.player)
                set_rule(tokens, rules)
            self.world.multiworld.completion_condition[self.player] = lambda state: state.has(itemName.MUMBOTOKEN, self.player, self.world.options.boss_hunt_length)
        elif self.world.options.victory_condition == VictoryCondition.option_jinjo_family_rescue:
            for location, rules in self.jinjotoken_rules.items():
                tokens = self.world.multiworld.get_location(location, self.player)
                set_rule(tokens, rules)
            self.world.multiworld.completion_condition[self.player] = lambda state: state.has(itemName.MUMBOTOKEN, self.player, self.world.options.jinjo_family_rescue_length)
        elif self.world.options.victory_condition == VictoryCondition.option_wonderwing_challenge:
            for location, rules in self.bosstoken_rules.items():
                tokens = self.world.multiworld.get_location(location, self.player)
                set_rule(tokens, rules)
            for location, rules in self.gametoken_rules.items():
                tokens = self.world.multiworld.get_location(location, self.player)
                set_rule(tokens, rules)
            for location, rules in self.jinjotoken_rules.items():
                tokens = self.world.multiworld.get_location(location, self.player)
                set_rule(tokens, rules)
            self.world.multiworld.completion_condition[self.player] = lambda state: state.has(itemName.MUMBOTOKEN, self.player, 32) \
            and self.check_hag1_options(state)
        elif self.world.options.victory_condition == VictoryCondition.option_token_hunt:
            self.world.multiworld.completion_condition[self.player] = lambda state: state.has(itemName.MUMBOTOKEN, self.player, self.world.options.token_hunt_length)
        elif self.world.options.victory_condition == VictoryCondition.option_boss_hunt_and_hag1:
            for location, rules in self.bosstoken_rules.items():
                tokens = self.world.multiworld.get_location(location, self.player)
                set_rule(tokens, rules)
            self.world.multiworld.completion_condition[self.player] = lambda state: state.has(itemName.MUMBOTOKEN, self.player, self.world.options.boss_hunt_length) and state.has("Kick Around", self.player)
        else:
            self.world.multiworld.completion_condition[self.player] = lambda state: state.has("Kick Around", self.player)
