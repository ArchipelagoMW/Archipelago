from BaseClasses import CollectionState
from .data import Items
from .Rac2Options import Rac2Options


def can_dynamo(state: CollectionState, player: int) -> bool:
    return state.has(Items.DYNAMO.name, player)


def can_tractor(state: CollectionState, player: int) -> bool:
    return state.has(Items.TRACTOR_BEAM.name, player)


def can_swingshot(state: CollectionState, player: int) -> bool:
    return state.has(Items.SWINGSHOT.name, player)


def can_thermanate(state: CollectionState, player: int) -> bool:
    return state.has(Items.THERMANATOR.name, player)


def can_improved_jump(state: CollectionState, player: int) -> bool:
    return state.has_any([Items.HELI_PACK.name, Items.THRUSTER_PACK.name], player)


def can_heli(state: CollectionState, player: int) -> bool:
    return state.has(Items.HELI_PACK.name, player)


def can_grind(state: CollectionState, player: int) -> bool:
    return state.has(Items.GRIND_BOOTS.name, player)


def can_gravity(state: CollectionState, player: int) -> bool:
    return state.has(Items.GRAVITY_BOOTS.name, player)


def can_charge(state: CollectionState, player: int) -> bool:
    return state.has(Items.CHARGE_BOOTS.name, player)


def can_hypnotize(state: CollectionState, player: int) -> bool:
    return state.has(Items.HYPNOMATIC.name, player)


def can_glide(state: CollectionState, player: int) -> bool:
    return state.has(Items.GLIDER.name, player)


def can_levitate(state: CollectionState, player: int) -> bool:
    return state.has(Items.LEVITATOR.name, player)


def can_electrolyze(state: CollectionState, player: int) -> bool:
    return state.has(Items.ELECTROLYZER.name, player)


def can_infiltrate(state: CollectionState, player: int) -> bool:
    return state.has(Items.INFILTRATOR.name, player)


def can_spiderbot(state: CollectionState, player: int) -> bool:
    if not state.multiworld.worlds[player].options.randomize_megacorp_vendor:
        return state.has(Items.JOBA_COORDS.name, player)

    return state.has(Items.SPIDERBOT_GLOVE.name, player)


def has_qwark_statuette(state: CollectionState, player: int) -> bool:
    return state.has(Items.QWARK_STATUETTE.name, player)


def has_hypnomatic_parts(state: CollectionState, player: int) -> bool:
    return state.has(Items.HYPNOMATIC_PART.name, player, 3)


FIRST_PERSON_EASY = 1
FIRST_PERSON_MEDIUM = 2
FIRST_PERSON_HARD = 3


def get_options(state: CollectionState, player: int) -> Rac2Options:
    return state.multiworld.worlds[player].options


def oozla_end_store_cutscene_rule(state: CollectionState, player: int) -> bool:
    options = get_options(state, player)

    if options.first_person_mode_glitch_in_logic >= FIRST_PERSON_MEDIUM:
        return True

    return can_dynamo(state, player)


def oozla_tractor_puzzle_pb_rule(state: CollectionState, player: int) -> bool:
    options = get_options(state, player)

    if options.first_person_mode_glitch_in_logic >= FIRST_PERSON_EASY:
        return True

    return can_tractor(state, player)


def oozla_swamp_ruins_pb_rule(state: CollectionState, player: int) -> bool:
    options = get_options(state, player)

    if options.first_person_mode_glitch_in_logic >= FIRST_PERSON_MEDIUM:
        return True

    return can_dynamo(state, player)


def oozla_swamp_monster_ii_rule(state: CollectionState, player: int) -> bool:
    return (can_dynamo(state, player)
            and can_gravity(state, player))


def maktar_photo_booth_rule(state: CollectionState, player: int) -> bool:
    options = get_options(state, player)

    if options.first_person_mode_glitch_in_logic >= FIRST_PERSON_MEDIUM:
        return (can_electrolyze(state, player)
                or can_heli(state, player))

    return can_electrolyze(state, player)


def maktar_deactivate_jamming_array_rule(state: CollectionState, player: int) -> bool:
    return can_tractor(state, player)


def maktar_jamming_array_pb_rule(state: CollectionState, player: int) -> bool:
    return can_tractor(state, player)


def endako_rescue_clank_rule(state: CollectionState, player: int) -> bool:
    return can_electrolyze(state, player)


def endako_crane_pb_rule(state: CollectionState, player: int) -> bool:
    return can_electrolyze(state, player)


def endako_crane_nt_rule(state: CollectionState, player: int) -> bool:
    return (can_electrolyze(state, player)
            and can_infiltrate(state, player))


def barlow_inventor_rule(state: CollectionState, player: int) -> bool:
    options = get_options(state, player)

    if options.first_person_mode_glitch_in_logic >= FIRST_PERSON_EASY:
        return True

    return can_swingshot(state, player)


def barlow_overbike_race_rule(state: CollectionState, player: int) -> bool:
    options = get_options(state, player)

    if options.first_person_mode_glitch_in_logic >= FIRST_PERSON_MEDIUM:
        return can_electrolyze(state, player)

    return (can_improved_jump(state, player)
            and can_electrolyze(state, player))


def barlow_hound_cave_pb_rule(state: CollectionState, player: int) -> bool:
    return can_swingshot(state, player)


def notak_top_pier_telescreen_rule(state: CollectionState, player: int) -> bool:
    options = get_options(state, player)

    if options.first_person_mode_glitch_in_logic >= FIRST_PERSON_EASY:
        return True

    return (can_improved_jump(state, player)
            and can_thermanate(state, player))


def notak_worker_bots_rule(state: CollectionState, player: int) -> bool:
    options = get_options(state, player)

    if options.first_person_mode_glitch_in_logic >= FIRST_PERSON_MEDIUM:
        return True

    return (can_heli(state, player)
            and can_thermanate(state, player))


def notak_timed_dynamo_rule(state: CollectionState, player: int) -> bool:
    options = get_options(state, player)

    if options.first_person_mode_glitch_in_logic >= FIRST_PERSON_MEDIUM:
        return True

    return (can_dynamo(state, player)
            and can_thermanate(state, player)
            and can_improved_jump(state, player))


def siberius_defeat_thief_rule(state: CollectionState, player: int) -> bool:
    return can_swingshot(state, player)


def siberius_flamebot_ledge_pb_rule(state: CollectionState, player: int) -> bool:
    options = get_options(state, player)

    if options.first_person_mode_glitch_in_logic >= FIRST_PERSON_EASY:
        return True

    return can_tractor(state, player)


def siberius_fenced_area_pb_rule(state: CollectionState, player: int) -> bool:
    options = get_options(state, player)

    if options.first_person_mode_glitch_in_logic >= FIRST_PERSON_EASY:
        return True

    return can_heli(state, player)


def tabora_meet_angelar_rule(state: CollectionState, player: int) -> bool:
    return (can_heli(state, player)
            and can_swingshot(state, player))


def tabora_underground_mines_end_rule(state: CollectionState, player: int) -> bool:
    options = get_options(state, player)

    if options.first_person_mode_glitch_in_logic >= FIRST_PERSON_EASY:
        return (can_heli(state, player)
                and can_swingshot(state, player))

    return (can_heli(state, player)
            and can_swingshot(state, player)
            and can_thermanate(state, player))


def tabora_canyon_glide_pb_rule(state: CollectionState, player: int) -> bool:
    options = get_options(state, player)

    if options.first_person_mode_glitch_in_logic >= FIRST_PERSON_EASY:
        return (can_heli(state, player)
                and can_swingshot(state, player)
                and can_glide(state, player))

    return (can_heli(state, player)
            and can_swingshot(state, player)
            and can_thermanate(state, player)
            and can_glide(state, player))


def tabora_northeast_desert_pb_rule(state: CollectionState, player: int) -> bool:
    return (can_heli(state, player)
            and can_swingshot(state, player))


def tabora_canyon_glide_pillar_nt_rule(state: CollectionState, player: int) -> bool:
    options = get_options(state, player)

    if options.first_person_mode_glitch_in_logic >= FIRST_PERSON_EASY:
        return (can_heli(state, player)
                and can_swingshot(state, player)
                and can_glide(state, player))

    return (can_heli(state, player)
            and can_swingshot(state, player)
            and can_thermanate(state, player)
            and can_glide(state, player))


def dobbo_defeat_thug_leader_rule(state: CollectionState, player: int) -> bool:
    options = get_options(state, player)

    if options.first_person_mode_glitch_in_logic >= FIRST_PERSON_EASY:
        return can_swingshot(state, player)

    return (can_swingshot(state, player)
            and can_improved_jump(state, player)
            and can_dynamo(state, player))


def dobbo_facility_terminal_rule(state: CollectionState, player: int) -> bool:
    options = get_options(state, player)

    if options.first_person_mode_glitch_in_logic >= FIRST_PERSON_MEDIUM:
        return True

    return (can_swingshot(state, player)
            and can_glide(state, player)
            and can_dynamo(state, player)
            and can_electrolyze(state, player))


def dobbo_spiderbot_room_pb_rule(state: CollectionState, player: int) -> bool:
    options = get_options(state, player)

    if options.first_person_mode_glitch_in_logic >= FIRST_PERSON_EASY:
        return can_swingshot(state, player)

    return (can_swingshot(state, player)
            and can_dynamo(state, player)
            and can_spiderbot(state, player))


def dobbo_facility_glide_pb_rule(state: CollectionState, player: int) -> bool:
    options = get_options(state, player)

    if options.first_person_mode_glitch_in_logic >= FIRST_PERSON_MEDIUM:
        return True

    return (can_swingshot(state, player)
            and can_glide(state, player)
            and can_dynamo(state, player))


def dobbo_facility_glide_nt_rule(state: CollectionState, player: int) -> bool:
    options = get_options(state, player)

    if options.first_person_mode_glitch_in_logic >= FIRST_PERSON_MEDIUM:
        return True

    return (can_swingshot(state, player)
            and can_glide(state, player)
            and can_dynamo(state, player))


def joba_hoverbike_race_rule(state: CollectionState, player: int) -> bool:
    return can_swingshot(state, player)


def joba_shady_salesman_rule(state: CollectionState, player: int) -> bool:
    options = get_options(state, player)

    if options.first_person_mode_glitch_in_logic >= FIRST_PERSON_MEDIUM:
        return True

    return (can_dynamo(state, player)
            and can_improved_jump(state, player))


def joba_arena_battle_rule(state: CollectionState, player: int) -> bool:
    options = get_options(state, player)

    if options.first_person_mode_glitch_in_logic >= FIRST_PERSON_MEDIUM:
        return can_levitate(state, player)

    return (can_dynamo(state, player)
            and can_improved_jump(state, player)
            and can_levitate(state, player))


def joba_arena_cage_match_rule(state: CollectionState, player: int) -> bool:
    options = get_options(state, player)

    if options.first_person_mode_glitch_in_logic >= FIRST_PERSON_MEDIUM:
        return can_levitate(state, player)

    return (can_dynamo(state, player)
            and can_improved_jump(state, player)
            and can_levitate(state, player))


def joba_hidden_cliff_pb_rule(state: CollectionState, player: int) -> bool:
    options = get_options(state, player)

    if options.first_person_mode_glitch_in_logic >= FIRST_PERSON_MEDIUM:
        return True

    return (can_dynamo(state, player)
            and can_swingshot(state, player))


def joba_levitator_tower_pb_rule(state: CollectionState, player: int) -> bool:
    options = get_options(state, player)

    if options.first_person_mode_glitch_in_logic >= FIRST_PERSON_MEDIUM:
        return can_levitate(state, player)

    return (can_dynamo(state, player)
            and can_improved_jump(state, player)
            and can_levitate(state, player))


def joba_timed_dynamo_nt_rule(state: CollectionState, player: int) -> bool:
    options = get_options(state, player)

    if options.first_person_mode_glitch_in_logic >= FIRST_PERSON_MEDIUM:
        return True

    return can_dynamo(state, player)


def todano_search_rocket_silo_rule(state: CollectionState, player: int) -> bool:
    options = get_options(state, player)

    if options.first_person_mode_glitch_in_logic >= FIRST_PERSON_EASY:
        return True

    return (can_electrolyze(state, player)
            and can_improved_jump(state, player)
            and can_infiltrate(state, player))


def todano_stuart_zurgo_trade_rule(state: CollectionState, player: int) -> bool:
    options = get_options(state, player)

    if options.first_person_mode_glitch_in_logic >= FIRST_PERSON_HARD:
        return has_qwark_statuette(state, player)

    if options.first_person_mode_glitch_in_logic >= FIRST_PERSON_EASY:
        return (can_tractor(state, player)
                and has_qwark_statuette(state, player))

    return (can_electrolyze(state, player)
            and can_tractor(state, player)
            and has_qwark_statuette(state, player))


def todano_facility_interior_rule(state: CollectionState, player: int) -> bool:
    options = get_options(state, player)

    if options.first_person_mode_glitch_in_logic >= FIRST_PERSON_HARD:
        return True

    if options.first_person_mode_glitch_in_logic >= FIRST_PERSON_EASY:
        return can_tractor(state, player)

    return (can_electrolyze(state, player)
            and can_tractor(state, player))


def todano_near_stuart_zurgo_pb_rule(state: CollectionState, player: int) -> bool:
    options = get_options(state, player)

    if options.first_person_mode_glitch_in_logic >= FIRST_PERSON_HARD:
        return True

    if options.first_person_mode_glitch_in_logic >= FIRST_PERSON_EASY:
        return can_tractor(state, player)

    return (can_electrolyze(state, player)
            and can_tractor(state, player))


def todano_spiderbot_conveyor_pb_rule(state: CollectionState, player: int) -> bool:
    options = get_options(state, player)

    if options.first_person_mode_glitch_in_logic >= FIRST_PERSON_EASY:
        return (can_tractor(state, player)
                and can_improved_jump(state, player)
                and can_spiderbot(state, player))

    return (can_electrolyze(state, player)
            and can_tractor(state, player)
            and can_improved_jump(state, player)
            and can_spiderbot(state, player))


def todano_rocket_silo_nt_rule(state: CollectionState, player: int) -> bool:
    options = get_options(state, player)

    if options.first_person_mode_glitch_in_logic >= FIRST_PERSON_EASY:
        return True

    return (can_electrolyze(state, player)
            and can_infiltrate(state, player))


def boldan_find_fizzwidget_rule(state: CollectionState, player: int) -> bool:
    options = get_options(state, player)

    if options.first_person_mode_glitch_in_logic >= FIRST_PERSON_HARD:
        return True

    if options.first_person_mode_glitch_in_logic >= FIRST_PERSON_MEDIUM:
        return (can_gravity(state, player)
                and can_improved_jump(state, player))

    if options.first_person_mode_glitch_in_logic >= FIRST_PERSON_EASY:
        return (can_swingshot(state, player)
                and can_gravity(state, player))

    return (can_levitate(state, player)
            and can_swingshot(state, player)
            and can_gravity(state, player))


def boldan_spiderbot_alley_pb_rule(state: CollectionState, player: int) -> bool:
    options = get_options(state, player)

    if options.first_person_mode_glitch_in_logic >= FIRST_PERSON_EASY:
        return True

    return (can_levitate(state, player)
            and can_spiderbot(state, player))


def boldan_floating_platform_rule(state: CollectionState, player: int) -> bool:
    options = get_options(state, player)

    if options.first_person_mode_glitch_in_logic >= FIRST_PERSON_MEDIUM:
        return True

    if options.first_person_mode_glitch_in_logic >= FIRST_PERSON_EASY:
        return can_gravity(state, player)

    return (can_levitate(state, player)
            and can_gravity(state, player))


def boldan_fountain_nt_rule(state: CollectionState, player: int) -> bool:
    options = get_options(state, player)

    if options.first_person_mode_glitch_in_logic >= FIRST_PERSON_EASY:
        return True

    return can_levitate(state, player)


def aranos_control_room_rule(state: CollectionState, player: int) -> bool:
    options = get_options(state, player)

    if options.first_person_mode_glitch_in_logic >= FIRST_PERSON_HARD:
        return True

    if options.first_person_mode_glitch_in_logic >= FIRST_PERSON_MEDIUM:
        return (can_infiltrate(state, player)
                and can_levitate(state, player))

    return (can_gravity(state, player)
            and can_infiltrate(state, player)
            and can_levitate(state, player))


def aranos_plumber_rule(state: CollectionState, player: int) -> bool:
    options = get_options(state, player)

    if options.first_person_mode_glitch_in_logic >= FIRST_PERSON_MEDIUM:
        return True

    return (can_gravity(state, player)
            and can_levitate(state, player))


def aranos_under_ship_pb_rule(state: CollectionState, player: int) -> bool:
    options = get_options(state, player)

    if options.first_person_mode_glitch_in_logic >= FIRST_PERSON_MEDIUM:
        return can_heli(state, player)

    return (can_gravity(state, player)
            and can_heli(state, player))


def aranos_omniwrench_12000_rule(state: CollectionState, player: int) -> bool:
    options = get_options(state, player)

    if options.first_person_mode_glitch_in_logic >= FIRST_PERSON_MEDIUM:
        return True

    return can_gravity(state, player)


def snivelak_rescue_angelak_rule(state: CollectionState, player: int) -> bool:
    options = get_options(state, player)

    if options.first_person_mode_glitch_in_logic >+ FIRST_PERSON_EASY:
        return can_swingshot(state, player)

    return (can_swingshot(state, player)
            and can_grind(state, player)
            and can_gravity(state, player)
            and can_dynamo(state, player))


def snivelak_dynamo_pb_rule(state: CollectionState, player: int) -> bool:
    options = get_options(state, player)

    if options.first_person_mode_glitch_in_logic >= FIRST_PERSON_EASY:
        return can_swingshot(state, player)

    return (can_swingshot(state, player)
            and can_grind(state, player)
            and can_gravity(state, player)
            and can_dynamo(state, player)
            and can_heli(state, player))


def snivelak_swingshot_tower_nt_rule(state: CollectionState, player: int) -> bool:
    options = get_options(state, player)

    if options.first_person_mode_glitch_in_logic >= FIRST_PERSON_EASY:
        return can_swingshot(state, player)

    return (can_swingshot(state, player)
            and can_heli(state, player))


def smolg_balloon_transmission_rule(state: CollectionState, player: int) -> bool:
    options = get_options(state, player)

    if options.first_person_mode_glitch_in_logic >= FIRST_PERSON_EASY:
        return can_electrolyze(state, player)

    return (can_improved_jump(state, player)
            and can_dynamo(state, player)
            and can_electrolyze(state, player))


def smolg_distribution_facility_end_rule(state: CollectionState, player: int) -> bool:
    options = get_options(state, player)

    if options.first_person_mode_glitch_in_logic >= FIRST_PERSON_EASY:
        return can_electrolyze(state, player)

    return (can_improved_jump(state, player)
            and can_dynamo(state, player)
            and can_electrolyze(state, player)
            and can_grind(state, player)
            and can_infiltrate(state, player))


def smolg_mutant_crab_rule(state: CollectionState, player: int) -> bool:
    options = get_options(state, player)

    if options.first_person_mode_glitch_in_logic >= FIRST_PERSON_EASY:
        if not can_levitate(state, player):
            return False
        return (can_swingshot(state, player)
                or can_electrolyze(state, player))

    return (can_swingshot(state, player)
            and can_levitate(state, player))


def smolg_floating_platform_pb_rule(state: CollectionState, player: int) -> bool:
    options = get_options(state, player)

    if options.first_person_mode_glitch_in_logic >= FIRST_PERSON_EASY:
        if not can_levitate(state, player):
            return False
        return (can_swingshot(state, player)
                or can_electrolyze(state, player))

    return (can_swingshot(state, player)
            and can_levitate(state, player))


def smolg_warehouse_pb_rule(state: CollectionState, player: int) -> bool:
    options = get_options(state, player)

    if options.first_person_mode_glitch_in_logic >= FIRST_PERSON_EASY:
        return True

    return (can_dynamo(state, player)
            and can_improved_jump(state, player))


def damosel_hypnotist_rule(state: CollectionState, player: int) -> bool:
    return (can_swingshot(state, player)
            and can_improved_jump(state, player)
            and can_thermanate(state, player)
            and has_hypnomatic_parts(state, player))


def damosel_train_rails_rule(state: CollectionState, player: int) -> bool:
    return can_grind(state, player)


def damosel_frozen_mountain_pb_rule(state: CollectionState, player: int) -> bool:
    return (can_swingshot(state, player)
            and can_improved_jump(state, player)
            and can_thermanate(state, player)
            and can_grind(state, player))


def damosel_pyramid_pb_rule(state: CollectionState, player: int) -> bool:
    return (can_swingshot(state, player)
            and can_improved_jump(state, player)
            and can_hypnotize(state, player))


def grelbin_find_angela_rule(state: CollectionState, player: int) -> bool:
    options = get_options(state, player)

    if options.first_person_mode_glitch_in_logic >= FIRST_PERSON_EASY:
        return True

    return can_hypnotize(state, player)


def grelbin_mystic_more_moonstones_rule(state: CollectionState, player: int) -> bool:
    return (can_glide(state, player)
            and can_infiltrate(state, player))


def grelbin_ice_plains_pb_rule(state: CollectionState, player: int) -> bool:
    return (can_glide(state, player)
            and can_infiltrate(state, player))


def grelbin_underwater_tunnel_pb_rule(state: CollectionState, player: int) -> bool:
    return can_hypnotize(state, player)


def grelbin_yeti_cave_pb_rule(state: CollectionState, player: int) -> bool:
    return (can_glide(state, player)
            and can_infiltrate(state, player)
            and can_hypnotize(state, player))


def yeedil_defeat_mutated_protopet_rule(state: CollectionState, player: int) -> bool:
    options = get_options(state, player)

    if options.first_person_mode_glitch_in_logic >= FIRST_PERSON_HARD:
        return can_infiltrate(state, player)

    if options.first_person_mode_glitch_in_logic >= FIRST_PERSON_MEDIUM:
        return (can_hypnotize(state, player)
                and can_swingshot(state, player)
                and can_infiltrate(state, player))

    if options.first_person_mode_glitch_in_logic >= FIRST_PERSON_EASY:
        return (can_hypnotize(state, player)
                and can_swingshot(state, player)
                and can_infiltrate(state, player)
                and can_dynamo(state, player)
                and can_improved_jump(state, player))

    return (can_hypnotize(state, player)
            and can_swingshot(state, player)
            and can_infiltrate(state, player)
            and can_dynamo(state, player)
            and can_improved_jump(state, player)
            and can_electrolyze(state, player))


def yeedil_bridge_grindrail_pb_rule(state: CollectionState, player: int) -> bool:
    options = get_options(state, player)

    if options.first_person_mode_glitch_in_logic >= FIRST_PERSON_EASY:
        return True

    return can_grind(state, player)


def yeedil_tractor_pillar_pb_rule(state: CollectionState, player: int) -> bool:
    options = get_options(state, player)

    if options.first_person_mode_glitch_in_logic >= FIRST_PERSON_HARD:
        return can_infiltrate(state, player)

    if options.first_person_mode_glitch_in_logic >= FIRST_PERSON_MEDIUM:
        return (can_hypnotize(state, player)
                and can_swingshot(state, player)
                and can_infiltrate(state, player))

    if options.first_person_mode_glitch_in_logic >= FIRST_PERSON_EASY:
        return (can_hypnotize(state, player)
                and can_swingshot(state, player)
                and can_infiltrate(state, player)
                and can_dynamo(state, player)
                and can_improved_jump(state, player)
                and can_tractor(state, player)
                and can_grind(state, player))

    return (can_hypnotize(state, player)
            and can_swingshot(state, player)
            and can_infiltrate(state, player)
            and can_dynamo(state, player)
            and can_improved_jump(state, player)
            and can_electrolyze(state, player)
            and can_tractor(state, player)
            and can_grind(state, player))
