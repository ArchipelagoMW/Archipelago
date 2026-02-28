# This file is auto-generated! DO NOT MODIFY BY HAND!

from enum import Enum, IntEnum

item_name_to_id = {
    "nothing": 0,
    "Glove orb": 4,
    "Sword orb": 5,
    "Axe orb": 6,
    "Spear orb": 7,
    "Whip orb": 8,
    "Bow orb": 9,
    "Boomerang orb": 10,
    "Javelin orb": 11,
    "boy": 12,
    "girl": 13,
    "sprite": 14,
    "sea hare tail": 15,
    "gold tower key": 16,
    "midge mallet": 17,
    "moogle belt": 18,
    "flammie drum": 19,
    "water seed": 21,
    "earth seed": 22,
    "wind seed": 23,
    "fire seed": 24,
    "light seed": 25,
    "dark seed": 26,
    "moon seed": 27,
    "dryad seed": 28,
    "undine spells": 29,
    "gnome spells": 30,
    "sylphid spells": 31,
    "salamando spells": 32,
    "lumina spells": 33,
    "shade spells": 34,
    "luna spells": 35,
    "dryad spells": 36,
    "glove": 37,
    "sword": 38,
    "axe": 39,
    "spear": 40,
    "whip": 41,
    "bow": 42,
    "boomerang": 43,
    "javelin": 44,
    "GP 0": 50,
    "GP 1": 51,
    "GP 2": 52,
    "GP 3": 53,
    "GP 4": 54,
    "GP 5": 55,
    "GP 6": 56,
    "GP 7": 57,
    "GP 8": 58,
    "GP 9": 59,
    "GP 10": 60,
    "GP 11": 61,
    "GP 12": 62,
    "GP 13": 63,
    "GP 14": 64,
    "GP 15": 65,
    "GP 16": 66,
}
location_name_to_id = {
    "mech rider 3": 4,
    "buffy": 5,
    "dread slime": 6,
    "gnome item 1": 7,
    "gnome item 2": 8,
    "fire seed": 9,
    "luna item 1": 10,
    "luna item 2": 11,
    "kakkara": 12,
    "lumina spells": 13,
    "lumina seed": 14,
    "chest next to whip chest": 15,
    "shade palace glove orb chest": 16,
    "sunken continent sword orb chest": 17,
    "lumina tower axe orb chest": 18,
    "fire palace axe orb chest": 19,
    "lumina tower spear orb chest": 20,
    "sunken continent boomerang orb chest": 21,
    "fire palace chest 1": 22,
    "fire palace chest 2": 23,
    "santa": 24,
    "shade spells": 25,
    "shade seed": 26,
    "thunder gigas": 27,
    "red dragon": 28,
    "blue dragon": 29,
    "mana tree": 30,
    "matango flammie": 31,
    "jehk": 32,
    "hydra": 33,
    "kettlekin": 34,
    "shade palace chest": 35,
    "luka item 1": 36,
    "luka item 2": 37,
    "sylphid item 1": 38,
    "sylphid item 2": 39,
    "whip chest": 40,
    "moogle village glove orb chest": 41,
    "ice castle glove orb chest": 42,
    "pandora sword orb chest": 43,
    "northtown ruins sword orb chest": 44,
    "moogle village axe orb chest": 45,
    "northtown castle axe orb chest": 46,
    "northtown ruins spear orb chest": 47,
    "pandora spear orb chest": 48,
    "santa spear orb chest": 49,
    "kilroy whip orb chest": 50,
    "northtown castle whip orb chest": 51,
    "northtown ruins bow orb chest": 52,
    "potos chest": 53,
    "pandora chest 1": 54,
    "pandora chest 2": 55,
    "pandora chest 3": 56,
    "pandora chest 4": 57,
    "magic rope chest": 58,
    "northtown castle chest": 59,
    "matango inn javelin orb chest": 60,
    "watts": 61,
    "undine item 1": 62,
    "undine item 2": 63,
    "salamando": 64,
    "dryad spells": 65,
    "dryad seed": 66,
    "mara": 67,
    "turtle island": 68,
    "dwarf elder": 69,
    "tropicallo item1": 70,
    "tropicallo item2": 71,
    "girl": 72,
    "solar": 73,
    "kilroy": 74,
    "mantis ant": 75,
    "axe beak": 76,
    "snow dragon": 77,
    "dragon worm": 78,
    "doom wall": 79,
    "vampire": 80,
    "mech rider 2": 81,
    "watermelon": 82,
    "hexas": 83,
    "wall face": 84,
    "metal mantis": 85,
    "jema at tasnica": 86,
    "triple tonpole": 87,
    "sword pedestal": 88,
    "boy starter weapon": 268,
    "girl starter weapon": 269,
    "sprite starter weapon": 270,
}
item_name_groups: dict[str, set[str]] = {}


class WorkingDataKey(Enum):
    BOY_CLASS = "boyClass"
    GIRL_CLASS = "girlClass"
    SPRITE_CLASS = "spriteClass"
    BOY_EXISTS = "boyExists"
    GIRL_EXISTS = "girlExists"
    SPRITE_EXISTS = "spriteExists"
    BOY_IN_LOGIC = "findBoy"
    GIRL_IN_LOGIC = "findGirl"
    SPRITE_IN_LOGIC = "findSprite"
    BOY_START_WEAPON_INDEX = "boyStartWeapon"
    GIRL_START_WEAPON_INDEX = "girlStartWeapon"
    SPRITE_START_WEAPON_INDEX = "spriteStartWeapon"


class ItemId(IntEnum):
    nothing = 0
    glove_orb = 4
    sword_orb = 5
    axe_orb = 6
    spear_orb = 7
    whip_orb = 8
    bow_orb = 9
    boomerang_orb = 10
    javelin_orb = 11
    boy = 12
    girl = 13
    sprite = 14
    sea_hare_tail = 15
    gold_tower_key = 16
    midge_mallet = 17
    moogle_belt = 18
    flammie_drum = 19
    water_seed = 21
    earth_seed = 22
    wind_seed = 23
    fire_seed = 24
    light_seed = 25
    dark_seed = 26
    moon_seed = 27
    dryad_seed = 28
    undine_spells = 29
    gnome_spells = 30
    sylphid_spells = 31
    salamando_spells = 32
    lumina_spells = 33
    shade_spells = 34
    luna_spells = 35
    dryad_spells = 36
    glove = 37
    sword = 38
    axe = 39
    spear = 40
    whip = 41
    bow = 42
    boomerang = 43
    javelin = 44
    gp0 = 50
    gp1 = 51
    gp2 = 52
    gp3 = 53
    gp4 = 54
    gp5 = 55
    gp6 = 56
    gp7 = 57
    gp8 = 58
    gp9 = 59
    gp10 = 60
    gp11 = 61
    gp12 = 62
    gp13 = 63
    gp14 = 64
    gp15 = 65
    gp16 = 66


class LocationId(IntEnum):
    mech_rider3 = 4
    buffy = 5
    dread_slime = 6
    gnome_item1 = 7
    gnome_item2 = 8
    fire_seed = 9
    luna_item1 = 10
    luna_item2 = 11
    kakkara = 12
    lumina_spells = 13
    lumina_seed = 14
    chest_next_to_whip_chest = 15
    shade_palace_glove_orb_chest = 16
    sunken_continent_sword_orb_chest = 17
    lumina_tower_axe_orb_chest = 18
    fire_palace_axe_orb_chest = 19
    lumina_tower_spear_orb_chest = 20
    sunken_continent_boomerang_orb_chest = 21
    fire_palace_chest1 = 22
    fire_palace_chest2 = 23
    santa = 24
    shade_spells = 25
    shade_seed = 26
    thunder_gigas = 27
    red_dragon = 28
    blue_dragon = 29
    mana_tree = 30
    matango_flammie = 31
    jehk = 32
    hydra = 33
    kettlekin = 34
    shade_palace_chest = 35
    luka_item1 = 36
    luka_item2 = 37
    sylphid_item1 = 38
    sylphid_item2 = 39
    whip_chest = 40
    moogle_village_glove_orb_chest = 41
    ice_castle_glove_orb_chest = 42
    pandora_sword_orb_chest = 43
    northtown_ruins_sword_orb_chest = 44
    moogle_village_axe_orb_chest = 45
    northtown_castle_axe_orb_chest = 46
    northtown_ruins_spear_orb_chest = 47
    pandora_spear_orb_chest = 48
    santa_spear_orb_chest = 49
    kilroy_whip_orb_chest = 50
    northtown_castle_whip_orb_chest = 51
    northtown_ruins_bow_orb_chest = 52
    potos_chest = 53
    pandora_chest1 = 54
    pandora_chest2 = 55
    pandora_chest3 = 56
    pandora_chest4 = 57
    magic_rope_chest = 58
    northtown_castle_chest = 59
    matango_inn_javelin_orb_chest = 60
    watts = 61
    undine_item1 = 62
    undine_item2 = 63
    salamando = 64
    dryad_spells = 65
    dryad_seed = 66
    mara = 67
    turtle_island = 68
    dwarf_elder = 69
    tropicallo_item1 = 70
    tropicallo_item2 = 71
    girl = 72
    solar = 73
    kilroy = 74
    mantis_ant = 75
    axe_beak = 76
    snow_dragon = 77
    dragon_worm = 78
    doom_wall = 79
    vampire = 80
    mech_rider2 = 81
    watermelon = 82
    hexas = 83
    wall_face = 84
    metal_mantis = 85
    jema_at_tasnica = 86
    triple_tonpole = 87
    sword_pedestal = 88
    boy_starter_weapon = 268
    girl_starter_weapon = 269
    sprite_starter_weapon = 270


character_exists_keys = {
    "boy": WorkingDataKey.BOY_EXISTS,
    "girl": WorkingDataKey.GIRL_EXISTS,
    "sprite": WorkingDataKey.SPRITE_EXISTS,
}
character_in_logic_keys = {
    "boy": WorkingDataKey.BOY_IN_LOGIC,
    "girl": WorkingDataKey.GIRL_IN_LOGIC,
    "sprite": WorkingDataKey.SPRITE_IN_LOGIC,
}
character_class_keys = {
    "boy": WorkingDataKey.BOY_CLASS,
    "girl": WorkingDataKey.GIRL_CLASS,
    "sprite": WorkingDataKey.SPRITE_CLASS,
}
character_starter_weapon_keys = {
    "boy": WorkingDataKey.BOY_START_WEAPON_INDEX,
    "girl": WorkingDataKey.GIRL_START_WEAPON_INDEX,
    "sprite": WorkingDataKey.SPRITE_START_WEAPON_INDEX,
}
spell_progression = {
    "OGboy": "noCaster",
    "OGgirl": "girlCaster",
    "OGsprite": "spriteCaster",
}
progression_items: frozenset[ItemId] = frozenset(
    (
        ItemId.axe,
        ItemId.sword,
        ItemId.whip,
        ItemId.water_seed,
        ItemId.earth_seed,
        ItemId.wind_seed,
        ItemId.fire_seed,
        ItemId.light_seed,
        ItemId.dark_seed,
        ItemId.moon_seed,
        ItemId.dryad_seed,
        ItemId.undine_spells,
        ItemId.gnome_spells,
        ItemId.sylphid_spells,
        ItemId.salamando_spells,
        ItemId.lumina_spells,
        ItemId.shade_spells,
        ItemId.luna_spells,
        ItemId.dryad_spells,
        ItemId.gold_tower_key,
        ItemId.sea_hare_tail,
        ItemId.flammie_drum,
    )
)
useful_items: frozenset[ItemId] = frozenset(
    (
        ItemId.midge_mallet,
        ItemId.moogle_belt,
    )
)
character_items: frozenset[ItemId] = frozenset(
    (
        ItemId.boy,
        ItemId.girl,
        ItemId.sprite,
    )
)
progression_event_rewards: frozenset[str] = frozenset(
    (
        "anyCaster",
        "girlCaster",
        "spriteCaster",
        "Did the thing",
    )
)
