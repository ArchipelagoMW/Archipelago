from worlds.generic.Rules import forbid_item, set_rule, add_rule
from BaseClasses import MultiWorld, CollectionState

from .Locations import ABREV_TO_LOCATION
from .Items import progression_items
from .Options import SOTNOptions
from .data.Constants import EXTENSIONS, RELIC_NAMES


def sotn_has_transformation(state: CollectionState, player: int) -> bool:
    return (state.has("Soul of bat", player) or state.has("Soul of wolf", player) or
            state.has("Form of mist", player))


def sotn_has_jump(state: CollectionState, player: int) -> bool:
    return state.has("Leap stone", player) or state.has("Gravity boots", player)


def sotn_has_flying(state: CollectionState, player: int) -> bool:
    return (state.has("Soul of bat", player) or
            (state.has("Form of mist", player) and state.has("Power of mist", player)) or
            (state.has("Gravity boots", player) and state.has("Leap stone", player)))


def sotn_has_any(state: CollectionState, player: int) -> bool:
    return sotn_has_jump(state, player) or sotn_has_flying(state, player)


def sotn_has_bat(state: CollectionState, player: int) -> bool:
    return state.has("Soul of bat", player) and state.has("Echo of bat", player)


def sotn_has_wolf(state: CollectionState, player: int) -> bool:
    return state.has("Soul of wolf", player) and state.has("Power of wolf", player)


def sotn_has_reverse(state: CollectionState, player: int) -> bool:
    return state.has("Holy glasses", player) and sotn_has_flying(state, player)


def sotn_has_dracula(state: CollectionState, player: int) -> bool:
    return (sotn_has_reverse(state, player) and state.has("Heart of vlad", player) and
            state.has("Rib of vlad", player) and state.has("Tooth of vlad", player) and
            state.has("Eye of vlad", player) and state.has("Ring of vlad", player))


def sotn_has_spike(state: CollectionState, player: int) -> bool:
    return ((state.has("Soul of bat", player) and state.has("Echo of bat", player)) or
            (state.has("Spike breaker", player) and sotn_has_any(state, player)))


def set_rules(world: MultiWorld, player: int, options: SOTNOptions) -> None:
    open_are = options.open_no4.value
    open_no4 = options.open_are.value
    extension = options.extension.value

    location = world.get_location("Reverse Center Cube - Kill Dracula", player)
    set_rule(location, lambda state: sotn_has_dracula(state, player))

    # Player might break TOP_Turkey_1 with spell and miss the loot, forbid progression items
    if ABREV_TO_LOCATION["TOP_Turkey_1"] in EXTENSIONS[extension]:
        location = world.get_location(ABREV_TO_LOCATION["TOP_Turkey_1"], player)
        for k in progression_items.keys():
            forbid_item(location, k, player)

    # Vessels can be on gold ring, but cause some weird visual glitches
    location = world.get_location(ABREV_TO_LOCATION["NO4_Gold ring_10"], player)
    forbid_item(location, "Heart Vessel", player)
    forbid_item(location, "Life Vessel", player)

    # Forbid vessels on no_offset locations and chi turkey, Vlad relics, Jewel of open, Trio and holy glasses
    for loc in ["Heart of vlad", "Tooth of vlad", "Rib of vlad", "Ring of vlad", "Eye of vlad", "Jewel of open",
                "NO1_Pot roast_77699032", "NO3_Pot roast_79337332", "NO3_Turkey_79340208", "NZ1_Bwaka knife_89601956",
                "NZ1_Pot roast_89601948", "NZ1_Shuriken_89601952", "NZ1_TNT_89601960", "RNO1_Dim sum set_84398220",
                "RNO3_Pot roast_85880396", "RNZ1_Bwaka knife_94094164", "RNZ1_Pot roast_94094156", "RARE_Life Vessel_8",
                "RNZ1_Shuriken_94094160", "RNZ1_TNT_94094168", "CHI_Turkey_73307650", "CEN_Holy glasses_72803176"]:
        if loc in EXTENSIONS[extension]:
            location = world.get_location(ABREV_TO_LOCATION[loc], player)
            forbid_item(location, "Heart Vessel", player)
            forbid_item(location, "Life Vessel", player)

    # Forbid relics on no_offset locations, chi turkey
    for loc in ["NO1_Pot roast_77699032", "NO3_Pot roast_79337332", "NO3_Turkey_79340208", "NZ1_Bwaka knife_89601956",
                "NZ1_Pot roast_89601948", "NZ1_Shuriken_89601952", "NZ1_TNT_89601960", "RNO1_Dim sum set_84398220",
                "RNO3_Pot roast_85880396", "RNZ1_Bwaka knife_94094164", "RNZ1_Pot roast_94094156",
                "RNZ1_Shuriken_94094160", "RNZ1_TNT_94094168", "CHI_Turkey_73307650"]:
        if loc in EXTENSIONS[extension]:
            location = world.get_location(ABREV_TO_LOCATION[loc], player)
            for r in RELIC_NAMES:
                forbid_item(location, r, player)
    # TODO Jewel might need some restrictions Green tea RCHI too

    # Relic rules not bound by region
    location = world.get_location(ABREV_TO_LOCATION["Soul of bat"], player)
    set_rule(location, lambda state: state.has("Form of mist", player) and sotn_has_any(state, player))
    location = world.get_location(ABREV_TO_LOCATION["Echo of bat"], player)
    add_rule(location, lambda state: sotn_has_transformation(state, player))
    location = world.get_location(ABREV_TO_LOCATION["Power of wolf"], player)
    set_rule(location, lambda state: sotn_has_flying(state, player))
    location = world.get_location(ABREV_TO_LOCATION["Skill of wolf"], player)
    set_rule(location, lambda state: state.has("Gravity boots", player) or sotn_has_flying(state, player))
    location = world.get_location(ABREV_TO_LOCATION["Gravity boots"], player)
    set_rule(location, lambda state: sotn_has_flying(state, player))
    location = world.get_location(ABREV_TO_LOCATION["Holy symbol"], player)
    add_rule(location, lambda state: state.has("Merman statue", player))
    location = world.get_location(ABREV_TO_LOCATION["Bat card"], player)
    set_rule(location, lambda state: sotn_has_flying(state, player) or state.has("Gravity boots", player))
    location = world.get_location(ABREV_TO_LOCATION["Faerie card"], player)
    set_rule(location, lambda state: sotn_has_any(state, player))

    # Item rules not bound by region
    # ARE - Colosseum
    if "ARE_Holy sword_7" in EXTENSIONS[extension]:
        location = world.get_location(ABREV_TO_LOCATION["ARE_Holy sword_7"], player)
        add_rule(location, lambda state: state.has("Gravity boots", player) or sotn_has_flying(state, player))

    # CAT - Catacombs
    # Spike Breaker area
    loc_pool = []
    for loc in ["CAT_Library card_4", "CAT_Cross shuriken_11", "CAT_Cross shuriken_12", "CAT_Karma coin_13",
                "CAT_Karma coin_14", "CAT_Pork bun_15", "CAT_Spike breaker_16"]:
        if loc in EXTENSIONS[extension]:
            loc_pool.append(world.get_location(ABREV_TO_LOCATION[loc], player))
    for loc in loc_pool:
        add_rule(loc, lambda state: sotn_has_spike(state, player))
    # Ballroom mask area
    loc_pool = []
    for loc in ["CAT_Icebrand_1", "CAT_Heart Vessel_6", "CAT_Ballroom mask_7"]:
        if loc in EXTENSIONS[extension]:
            loc_pool.append(world.get_location(ABREV_TO_LOCATION[loc], player))
    for loc in loc_pool:
        add_rule(loc, lambda state: state.has("Gravity boots", player) or sotn_has_flying(state, player))

    # CHI - Abandoned Mine
    loc_pool = []
    for loc in ["CHI_Power of sire_0", "CHI_Ring of ares_4", "CHI_Barley tea_8", "CHI_Peanuts_9",
                "CHI_Peanuts_10", "CHI_Peanuts_11", "CHI_Peanuts_12", "CHI_Turkey_73307650"]:
        if loc in EXTENSIONS[extension]:
            loc_pool.append(world.get_location(ABREV_TO_LOCATION[loc], player))
    for loc in loc_pool:
        add_rule(loc, lambda state: state.has("Demon card", player))

    # DAI - Royal Chapel
    loc_pool = []
    for loc in ["DAI_Ankh of life_0", "DAI_Morningstar_1", "DAI_Mystic pendant_4", "DAI_Magic missile_5",
                "DAI_Shuriken_6", "DAI_TNT_7", "DAI_Boomerang_8"]:
        if loc in EXTENSIONS[extension]:
            loc_pool.append(world.get_location(ABREV_TO_LOCATION[loc], player))
    for loc in loc_pool:
        add_rule(loc, lambda state: sotn_has_any(state, player))
    location = world.get_location(ABREV_TO_LOCATION["DAI_Silver ring_2"], player)
    add_rule(location, lambda state: (state.has("Form of mist", player) and
                                      state.has("Jewel of open", player) and
                                      state.has("Spike breaker", player)))

    # LIB - Long Library
    loc_pool = []
    for loc in ["LIB_Stone mask_1", "LIB_Holy rod_2", "LIB_Takemitsu_5", "LIB_Onyx_6",
                "LIB_Frankfurter_7", "LIB_Potion_8", "LIB_Antivenom_9", "LIB_Topaz circlet_10"]:
        if loc in EXTENSIONS[extension]:
            loc_pool.append(world.get_location(ABREV_TO_LOCATION[loc], player))
    for loc in loc_pool:
        add_rule(loc, lambda state: sotn_has_any(state, player))

    # NO0 - Marble Gallery
    loc_pool = []
    for loc in ["NO0_Hammer_12", "NO0_Str. potion_13"]:
        if loc in EXTENSIONS[extension]:
            loc_pool.append(world.get_location(ABREV_TO_LOCATION[loc], player))
    for loc in loc_pool:
        add_rule(loc, lambda state: state.has("Gravity boots", player) or sotn_has_flying(state, player))
    if "NO0_Life Vessel_0" in EXTENSIONS[extension]:
        location = world.get_location(ABREV_TO_LOCATION["NO0_Life Vessel_0"], player)
        if open_are:
            set_rule(location, lambda state: state.has("Jewel of open", player))
        else:
            set_rule(location, lambda state: sotn_has_any(state, player))
    loc_pool = []
    for loc in ["NO0_Life apple_3", "NO0_Hammer_4", "NO0_Potion_5"]:
        if loc in EXTENSIONS[extension]:
            loc_pool.append(world.get_location(ABREV_TO_LOCATION[loc], player))
    for loc in loc_pool:
        add_rule(loc, lambda state: sotn_has_flying(state, player))
    loc_pool = []
    for loc in ["NO0_Library card_10", "NO0_Attack potion_11"]:
        if loc in EXTENSIONS[extension]:
            loc_pool.append(world.get_location(ABREV_TO_LOCATION[loc], player))
    for loc in loc_pool:
        add_rule(loc, lambda state: state.has("Jewel of open", player))
    loc_pool = []
    for loc in ["NO0_Alucart shield_1", "NO0_Heart Vessel_2", "NO0_Alucart mail_6", "NO0_Alucart sword_7"]:
        if loc in EXTENSIONS[extension]:
            loc_pool.append(world.get_location(ABREV_TO_LOCATION[loc], player))
    for loc in loc_pool:
        add_rule(loc, lambda state: (sotn_has_reverse(state, player) or
                                     (state.has("Cube of zoe", player) and sotn_has_any(state, player))))
    loc_pool = []
    for loc in ["NO0_Life Vessel_8", "NO0_Heart Vessel_9"]:
        if loc in EXTENSIONS[extension]:
            loc_pool.append(world.get_location(ABREV_TO_LOCATION[loc], player))
    for loc in loc_pool:
        add_rule(loc, lambda state: state.has("Silver ring", player) and state.has("Gold ring", player))

    # NO1 - Outer Wall
    if "NO1_Garnet_3" in EXTENSIONS[extension]:
        location = world.get_location(ABREV_TO_LOCATION["NO1_Garnet_3"], player)
        add_rule(location, lambda state: sotn_has_any(state, player))
    if "NO1_Pot roast_77699032" in EXTENSIONS[extension]:
        location = world.get_location(ABREV_TO_LOCATION["NO1_Pot roast_77699032"], player)
        for r in RELIC_NAMES:
            forbid_item(location, r, player)

    # NO3 - Castle Entrance
    if "NO3_Life Vessel_8" in EXTENSIONS[extension]:
        location = world.get_location(ABREV_TO_LOCATION["NO3_Life Vessel_8"], player)
        add_rule(location, lambda state: sotn_has_flying(state, player))
    if "NO3_Holy mail_5" in EXTENSIONS[extension]:
        location = world.get_location(ABREV_TO_LOCATION["NO3_Holy mail_5"], player)
        add_rule(location, lambda state: state.has("Gravity boots", player) or sotn_has_flying(state, player))
    if "NO3_Life Vessel_6" in EXTENSIONS[extension]:
        location = world.get_location(ABREV_TO_LOCATION["NO3_Life Vessel_6"], player)
        if not open_no4:
            add_rule(location, lambda state: state.has("Jewel of open", player))
    loc_pool = []
    for loc in ["NO3_Life apple_2", "NP3_Jewel sword_9"]:
        if loc in EXTENSIONS[extension]:
            loc_pool.append(world.get_location(ABREV_TO_LOCATION[loc], player))
    for loc in loc_pool:
        add_rule(loc, lambda state: state.has("Soul of wolf", player) and state.has("Soul of bat", player))

    # NO4 - Underground Caverns
    loc_pool = []
    for loc in ["NO4_Antivenom_4", "NO4_Life Vessel_5"]:
        if loc in EXTENSIONS[extension]:
            loc_pool.append(world.get_location(ABREV_TO_LOCATION[loc], player))
    for loc in loc_pool:
        add_rule(loc, lambda state: state.has("Holy symbol", player))
    if "NO4_Herald shield_7" in EXTENSIONS[extension]:
        location = world.get_location(ABREV_TO_LOCATION["NO4_Herald shield_7"], player)
        add_rule(location, lambda state: (sotn_has_flying(state, player) or
                                          sotn_has_wolf(state, player) or
                                          state.has("Leap stone", player)))
    if "NO4_Zircon_9" in EXTENSIONS[extension]:
        location = world.get_location(ABREV_TO_LOCATION["NO4_Zircon_9"], player)
        add_rule(location, lambda state: sotn_has_any(state, player) or sotn_has_flying(state, player))
    if "NO4_Onyx_22" in EXTENSIONS[extension]:
        location = world.get_location(ABREV_TO_LOCATION["NO4_Onyx_22"], player)
        add_rule(location, lambda state: state.has("Merman statue", player) or sotn_has_flying(state, player))
    loc_pool = []
    for loc in ["NO4_Knuckle duster_23", "NO4_Life Vessel_24"]:
        if loc in EXTENSIONS[extension]:
            loc_pool.append(world.get_location(ABREV_TO_LOCATION[loc], player))
    for loc in loc_pool:
        add_rule(loc, lambda state: state.has("Holy symbol", player))
    if "NO4_Elixir_25" in EXTENSIONS[extension]:
        location = world.get_location(ABREV_TO_LOCATION["NO4_Elixir_25"], player)
        add_rule(location, lambda state: state.has("Holy symbol", player) and state.has("Merman statue", player))
    loc_pool = []
    for loc in ["NO4_Life Vessel_28", "NO4_Heart Vessel_29"]:
        if loc in EXTENSIONS[extension]:
            loc_pool.append(world.get_location(ABREV_TO_LOCATION[loc], player))
    for loc in loc_pool:
        add_rule(loc, lambda state: (state.has("Leap stone", player) or sotn_has_flying(state, player) or
                                     sotn_has_wolf(state, player)))
    loc_pool = []
    for loc in ["NO4_Secret boots_31", "NO4_Toadstool_33"]:
        if loc in EXTENSIONS[extension]:
            loc_pool.append(world.get_location(ABREV_TO_LOCATION[loc], player))
    for loc in loc_pool:
        add_rule(loc, lambda state: sotn_has_any(state, player))
    if "NO4_Nunchaku_36" in EXTENSIONS[extension]:
        location = world.get_location(ABREV_TO_LOCATION["NO4_Nunchaku_36"], player)
        add_rule(location, lambda state: state.has("Holy symbol", player))

    # TOP - Castle Keep
    loc_pool = []
    for loc in ["TOP_Turquoise_0", "TOP_Turkey_1"]:
        if loc in EXTENSIONS[extension]:
            loc_pool.append(world.get_location(ABREV_TO_LOCATION[loc], player))
    for loc in loc_pool:
        add_rule(loc, lambda state: sotn_has_any(state, player))

    # RCAT - Floating Catacombs
    # Spike breaker area
    loc_pool = []
    for loc in ["RCAT_Resist thunder_2", "RCAT_Resist fire_3", "RCAT_Karma coin_4", "RCAT_Karma coin_5",
                "RCAT_Red bean bun_6", "RCAT_Elixir_7", "RCAT_Library card_8"]:
        if loc in EXTENSIONS[extension]:
            loc_pool.append(world.get_location(ABREV_TO_LOCATION[loc], player))
    for loc in loc_pool:
        add_rule(loc, lambda state: (state.has("Soul of bat", player) or
                                     (state.has("Form of mist", player) and state.has("Power of mist", player)) or
                                     (state.has("Spike breaker", player) and
                                      (state.has("Gravity boots", player) or state.has("Leap stone", player)))))

    # RCHI - Cave
    loc_pool = []
    for loc in ["RCHI_Power of sire_0", "RCHI_Life apple_1"]:
        if loc in EXTENSIONS[extension]:
            loc_pool.append(world.get_location(ABREV_TO_LOCATION[loc], player))
    for loc in loc_pool:
        add_rule(loc, lambda state: state.has("Demon card", player))

    # RDAI - Anti-Chapel
    if "RDAI_Twilight cloak_16" in EXTENSIONS[extension]:
        location = world.get_location(ABREV_TO_LOCATION["RDAI_Twilight cloak_16"], player)
        add_rule(location, lambda state: (state.has("Spike breaker", player) and state.has("Form of mist", player)) or
                 state.has("Power of mist", player) and state.has("Form of mist", player))

    # RLIB - Forbidden Library
    if "RLIB_Staurolite_8" in EXTENSIONS[extension]:
        location = world.get_location(ABREV_TO_LOCATION["RLIB_Staurolite_8"], player)
        add_rule(location, lambda state: state.has("Form of mist", player))

    # RNO0 - Black Marble Gallery
    if "RNO0_Meal ticket_9" in EXTENSIONS[extension]:
        location = world.get_location(ABREV_TO_LOCATION["RNO0_Meal ticket_9"], player)
        add_rule(location, lambda state: state.has("Jewel of open", player))

    # RNO1 - Reverse Outer Wall
    loc_pool = []
    for loc in ["RNO1_Shotel_1", "RNO1_Hammer_2"]:
        if loc in EXTENSIONS[extension]:
            loc_pool.append(world.get_location(ABREV_TO_LOCATION[loc], player))
    for loc in loc_pool:
        add_rule(loc, lambda state: state.has("Form of mist", player))

    # RNO2 - Death Wing's Lair
    loc_pool = []
    for loc in ["RNO2_Heart Vessel_11", "Rib of vlad"]:
        if loc in EXTENSIONS[extension]:
            loc_pool.append(world.get_location(ABREV_TO_LOCATION[loc], player))
    for loc in loc_pool:
        add_rule(loc, lambda state: sotn_has_transformation(state, player))

    # RNO3 - Reverse Entrance
    loc_pool = []
    for loc in ["RNO3_Zircon_4", "RNO3_Opal_5", "RNO3_Beryl circlet_6"]:
        if loc in EXTENSIONS[extension]:
            loc_pool.append(world.get_location(ABREV_TO_LOCATION[loc], player))
    for loc in loc_pool:
        add_rule(loc, lambda state: state.has("Soul of wolf", player) and state.has("Soul of bat", player))

    # RNO4 - Reverse Caverns
    loc_pool = []
    for loc in ["RNO4_Life Vessel_6", "RNO4_Potion_8"]:
        if loc in EXTENSIONS[extension]:
            loc_pool.append(world.get_location(ABREV_TO_LOCATION[loc], player))
    for loc in loc_pool:
        add_rule(loc, lambda state: state.has("Gravity boots", player))
    if "RNO4_Bat pentagram_5" in EXTENSIONS[extension]:
        location = world.get_location(ABREV_TO_LOCATION["RNO4_Bat pentagram_5"], player)
        add_rule(location, lambda state: state.has("Leap stone", player) or state.has("Soul of bat", player))
    if "RNO4_Heart Vessel_7" in EXTENSIONS[extension]:
        location = world.get_location(ABREV_TO_LOCATION["RNO4_Heart Vessel_7"], player)
        add_rule(location, lambda state: state.has("Gravity boots", player) and state.has("Holy symbol", player))
