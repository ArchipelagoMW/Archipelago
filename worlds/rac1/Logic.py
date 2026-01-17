from BaseClasses import CollectionState
from .data import Items


def can_swingshot(state: CollectionState, player: int) -> bool:
    return state.has(Items.SWINGSHOT.name, player)


def can_improved_jump(state: CollectionState, player: int) -> bool:
    return state.has_any([Items.HELI_PACK.name, Items.THRUSTER_PACK.name], player)


def can_heli_high_jump(state: CollectionState, player: int) -> bool:  # relevant for eudora gold bolt
    return state.has(Items.HELI_PACK.name, player)


def can_glide(state: CollectionState, player: int) -> bool:  # gliding is not possible without the heli pack
    return state.has(Items.HELI_PACK.name, player)


def can_ground_pound(state: CollectionState, player: int) -> bool:
    return state.has(Items.THRUSTER_PACK.name, player)


def has_hydro_pack(state: CollectionState, player: int) -> bool:
    return state.has(Items.HYDRO_PACK.name, player)


def can_grind(state: CollectionState, player: int) -> bool:
    return state.has(Items.GRINDBOOTS.name, player)


def has_magneboots(state: CollectionState, player: int) -> bool:
    return state.has(Items.MAGNEBOOTS.name, player)


def can_taunt(state: CollectionState, player: int) -> bool:
    return state.has(Items.TAUNTER.name, player)


def has_hydrodisplacer(state: CollectionState, player: int) -> bool:
    return state.has(Items.HYDRODISPLACER.name, player)


def has_raritanium(state: CollectionState, player: int) -> bool:
    return state.has(Items.RARITANIUM.name, player)


def has_zoomerator(state: CollectionState, player: int) -> bool:
    return state.has(Items.ZOOMERATOR.name, player)


def has_hoverboard(state: CollectionState, player: int) -> bool:
    return state.has(Items.HOVERBOARD.name, player)


def has_o2_mask(state: CollectionState, player: int) -> bool:
    return state.has(Items.O2_MASK.name, player)


def has_trespasser(state: CollectionState, player: int) -> bool:
    return state.has(Items.TRESPASSER.name, player)


def has_visibomb(state: CollectionState, player: int) -> bool:
    return state.has(Items.VISIBOMB.name, player)


def has_hologuise(state: CollectionState, player: int) -> bool:
    return state.has(Items.HOLOGUISE.name, player)


def has_pilots_helmet(state: CollectionState, player: int) -> bool:
    return state.has(Items.PILOTS_HELMET.name, player)


def has_codebot(state: CollectionState, player: int) -> bool:
    return state.has(Items.CODEBOT.name, player)


def has_taunter(state: CollectionState, player: int) -> bool:
    return state.has(Items.TAUNTER.name, player)


def has_metal_detector(state: CollectionState, player: int) -> bool:
    return state.has(Items.METAL_DETECTOR.name, player)


def has_explosive_weapon(state: CollectionState, player: int) -> bool:
    return state.has_any([Items.BOMB_GLOVE.name, Items.DEVASTATOR.name], player)


def has_long_range_weapon(state: CollectionState, player: int) -> bool:
    return (state.has_any([Items.BLASTER.name,
                           Items.DEVASTATOR.name,
                           Items.VISIBOMB.name,
                           Items.RYNO.name], player))


# Novalis
def novalis_underwater_caves_rule(state: CollectionState, player: int) -> bool:
    return has_hydro_pack(state, player)


# Eudora
def eudora_suck_cannon_rule(state: CollectionState, player: int) -> bool:
    return (can_improved_jump(state, player)
            and can_glide(state, player))


def eudora_henchman_rule(state: CollectionState, player: int) -> bool:
    return (can_swingshot(state, player)
            and has_trespasser(state, player)
            and can_improved_jump(state, player))


# Rilgar
def rilgar_hoverboard_rule(state: CollectionState, player: int) -> bool:
    return (has_hoverboard(state, player)
            and can_improved_jump(state, player))


def rilgar_bouncer_rule(state: CollectionState, player: int) -> bool:
    return (can_swingshot(state, player)
            and can_improved_jump(state, player)
            and has_hydrodisplacer(state, player))


def rilgar_underwater_bolt_rule(state: CollectionState, player: int) -> bool:
    return (rilgar_bouncer_rule(state, player)
            and has_o2_mask(state, player))


def rilgar_ryno_rule(state: CollectionState, player: int) -> bool:
    return (can_improved_jump(state, player)
            and has_metal_detector(state, player))


# Blarg
def blarg_outside_gold_bolt_rule(state: CollectionState, player: int) -> bool:
    return (has_o2_mask(state, player)
            and has_trespasser(state, player))


# Umbris
def umbris_snagglebeast_rule(state: CollectionState, player: int) -> bool:
    return (can_swingshot(state, player)
            and can_glide(state, player)
            and has_hydrodisplacer(state, player))


def umbris_pressure_bolt_rule(state: CollectionState, player: int) -> bool:
    return (can_swingshot(state, player)
            and can_glide(state, player))


def umbris_jump_bolt_rule(state: CollectionState, player: int) -> bool:
    return (can_swingshot(state, player)
            and can_glide(state, player)
            and has_hydrodisplacer(state, player))


# Orxon
def orxon_nanotech_rule(state: CollectionState, player: int) -> bool:
    return (has_o2_mask(state, player)
            and can_glide(state, player))


def orxon_ultra_nanotech_rule(state: CollectionState, player: int) -> bool:
    return (orxon_nanotech_rule(state, player)
            and has_metal_detector(state, player))


def orxon_visibomb_rule(state: CollectionState, player: int) -> bool:
    return (has_o2_mask(state, player)
            and has_metal_detector(state, player))


def orxon_visibomb_bolt_rule(state: CollectionState, player: int) -> bool:
    return (has_o2_mask(state, player)
            and has_visibomb(state, player)
            and can_glide(state, player)
            and can_swingshot(state, player)
            and has_magneboots(state, player))


def orxon_ratchet_infobot_rule(state: CollectionState, player: int) -> bool:
    return (has_o2_mask(state, player)
            and can_glide(state, player)
            and can_swingshot(state, player)
            and has_magneboots(state, player))


# Pokitaru
def pokitaru_ship_rule(state: CollectionState, player: int) -> bool:
    return (has_pilots_helmet(state, player)
            and can_ground_pound(state, player))


def pokitaru_persuader_rule(state: CollectionState, player: int) -> bool:
    return (has_raritanium(state, player)
            and has_trespasser(state, player)
            and has_hydrodisplacer(state, player))


def pokitaru_gold_bolt_rule(state: CollectionState, player: int) -> bool:
    return (can_swingshot(state, player)
            and can_ground_pound(state, player))


# Hoven
def hoven_infobot_rule(state: CollectionState, player: int) -> bool:
    return (has_long_range_weapon(state, player)
            and can_improved_jump(state, player))


def hoven_raritanium_rule(state: CollectionState, player: int) -> bool:
    return (can_swingshot(state, player)
            and can_improved_jump(state, player))


# Gemlik
def gemlik_quark_rule(state: CollectionState, player: int) -> bool:
    return (has_magneboots(state, player)
            and can_improved_jump(state, player)
            and has_long_range_weapon(state, player)
            and has_trespasser(state, player)
            and can_swingshot(state, player))


def gemlik_bolt_rule(state: CollectionState, player: int) -> bool:
    return (has_visibomb(state, player)
            and can_improved_jump(state, player)
            and has_trespasser(state, player))


# Oltanis
def oltanis_main_bolt_rule(state: CollectionState, player: int) -> bool:
    return (can_grind(state, player)
            and can_swingshot(state, player))


def oltanis_final_bolt_rule(state: CollectionState, player: int) -> bool:
    return (can_grind(state, player)
            and can_swingshot(state, player)
            and has_magneboots(state, player))


# Quartu
def quartu_infiltrate_rule(state: CollectionState, player: int) -> bool:
    return (has_hologuise(state, player)
            and can_swingshot(state, player)
            and can_ground_pound(state, player))


def quartu_codebot_rule(state: CollectionState, player: int) -> bool:
    return (has_codebot(state, player)
            and can_swingshot(state, player))


def quartu_bolt_grabber_rule(state: CollectionState, player: int) -> bool:
    return (has_hydro_pack(state, player)
            and has_o2_mask(state, player))


# Kalebo III
def kalebo_hologuise_rule(state: CollectionState, player: int) -> bool:
    return (has_hoverboard(state, player)
            and can_swingshot(state, player)
            and can_grind(state, player))


# Drek's Fleet
def fleet_infobot_rule(state: CollectionState, player: int) -> bool:
    return (has_magneboots(state, player)
            and has_pilots_helmet(state, player)
            and has_hologuise(state, player)
            and can_swingshot(state, player))


def fleet_water_rule(state: CollectionState, player: int) -> bool:
    return (has_o2_mask(state, player)
            and has_hydro_pack(state, player))


def fleet_second_bolt_rule(state: CollectionState, player: int) -> bool:
    return (has_magneboots(state, player)
            and has_pilots_helmet(state, player)
            and has_hologuise(state, player)
            and can_swingshot(state, player))


# Veldin
def veldin_global_rule(state: CollectionState, player: int) -> bool:
    return (has_trespasser(state, player)
            and has_magneboots(state, player)
            and has_hydrodisplacer(state, player)
            and can_ground_pound(state, player))


def veldin_grind_bolt_rule(state: CollectionState, player: int) -> bool:
    return (veldin_global_rule(state, player)
            and can_grind(state, player)
            and can_swingshot(state, player))


def veldin_halfway_bolt_rule(state: CollectionState, player: int) -> bool:
    return veldin_global_rule(state, player)


def veldin_taunter_bolt_rule(state: CollectionState, player: int) -> bool:
    return (veldin_global_rule(state, player)
            and has_taunter(state, player))


def veldin_defeat_drek_rule(state: CollectionState, player: int) -> bool:
    return (veldin_global_rule(state, player)
            and can_swingshot(state, player))
