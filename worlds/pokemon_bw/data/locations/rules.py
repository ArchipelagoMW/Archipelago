from .. import ExtendedRule, InclusionRule
from ..pokemon import species
from ..items import tm_hm


# Item requirements

can_use_strength: ExtendedRule = lambda state, world: (
    state.has("HM04 Strength", world.player)
    and state.has_any(world.strength_species, world.player)
)

can_use_surf: ExtendedRule = lambda state, world: (
    state.has("HM03 Surf", world.player)
    and state.has_any(world.surf_species, world.player)
)

can_use_cut: ExtendedRule = lambda state, world: (
    state.has("HM01 Cut", world.player)
    and state.has_any(world.cut_species, world.player)
)

can_use_waterfall: ExtendedRule = lambda state, world: (
    state.has_all(("HM03 Surf", "HM05 Waterfall"), world.player)
    and state.has_any(world.surf_species, world.player)
    and state.has_any(world.waterfall_species, world.player)
)

can_use_dive: ExtendedRule = lambda state, world: (
    state.has_all(("HM03 Surf", "HM06 Dive"), world.player)
    and state.has_any(world.surf_species, world.player)
    and state.has_any(world.dive_species, world.player)
)

can_use_flash: ExtendedRule = lambda state, world: (
    state.has("TM70 Flash", world.player)
    and state.has_any(world.flash_species, world.player)
)

can_use_surf_or_strength: ExtendedRule = lambda state, world: (
    (
        state.has("HM03 Surf", world.player)
        and state.has_any(world.surf_species, world.player)
    ) or (
        state.has("HM04 Strength", world.player)
        and state.has_any(world.strength_species, world.player)
    )
)

can_fish: ExtendedRule = lambda state, world: state.has("Super Rod", world.player)
has_rage_candy_bar: ExtendedRule = lambda state, world: state.has("Rage Candy Bar", world.player)
has_basement_key: ExtendedRule = lambda state, world: state.has("Basement Key", world.player)
has_parcel: ExtendedRule = lambda state, world: state.has("Parcel", world.player)
has_loot_sack: ExtendedRule = lambda state, world: state.has("Loot Sack", world.player)
has_dragon_skull: ExtendedRule = lambda state, world: state.has("Dragon Skull", world.player)
has_liberty_pass: ExtendedRule = lambda state, world: state.has("Liberty Pass", world.player)
has_machine_part: ExtendedRule = lambda state, world: state.has("Machine Part", world.player)
has_explorer_kit: ExtendedRule = lambda state, world: state.has("Explorer Kit", world.player)
has_tidal_bell: ExtendedRule = lambda state, world: state.has("Tidal Bell", world.player)
has_oaks_letter: ExtendedRule = lambda state, world: state.has("Oak's Letter", world.player)
has_blue_card: ExtendedRule = lambda state, world: state.has("Blue Card", world.player)
has_red_chain: ExtendedRule = lambda state, world: state.has("Red Chain", world.player)
has_any_legendary_stone: ExtendedRule = lambda state, world: state.has_any(("Light Stone", "Dark Stone"), world.player)
has_lock_capsule: ExtendedRule = lambda state, world: state.has("Lock Capsule", world.player)
has_all_grams: ExtendedRule = lambda state, world: state.has_all(("Wingull Gram 1", "Wingull Gram 2", "Wingull Gram 3"), world.player)

has_root_fossil: ExtendedRule = lambda state, world: state.has("Root Fossil", world.player)
has_claw_fossil: ExtendedRule = lambda state, world: state.has("Claw Fossil", world.player)
has_helix_fossil: ExtendedRule = lambda state, world: state.has("Helix Fossil", world.player)
has_dome_fossil: ExtendedRule = lambda state, world: state.has("Dome Fossil", world.player)
has_old_amber: ExtendedRule = lambda state, world: state.has("Old Amber", world.player)
has_armor_fossil: ExtendedRule = lambda state, world: state.has("Armor Fossil", world.player)
has_skull_fossil: ExtendedRule = lambda state, world: state.has("Skull Fossil", world.player)
has_cover_fossil: ExtendedRule = lambda state, world: state.has("Cover Fossil", world.player)
has_plume_fossil: ExtendedRule = lambda state, world: state.has("Plume Fossil", world.player)


# Badge requirements

has_trio_badge: ExtendedRule = lambda state, world: state.has("Trio Badge", world.player)
has_basic_badge: ExtendedRule = lambda state, world: state.has("Basic Badge", world.player)
has_insect_badge: ExtendedRule = lambda state, world: state.has("Insect Badge", world.player)
has_bolt_badge: ExtendedRule = lambda state, world: state.has("Bolt Badge", world.player)
has_quake_badge: ExtendedRule = lambda state, world: state.has("Quake Badge", world.player)
has_jet_badge: ExtendedRule = lambda state, world: state.has("Jet Badge", world.player)
has_freeze_badge: ExtendedRule = lambda state, world: state.has("Freeze Badge", world.player)
has_legend_badge: ExtendedRule = lambda state, world: state.has("Legend Badge", world.player)


# Season requirements

can_set_winter: ExtendedRule = lambda state, world: (
    world.options.season_control == "vanilla" or (
        state.can_reach_region("Nimbasa City", world.player) and (
            world.options.season_control == "changeable" or state.has("Winter", world.player)
        )
    )
)

can_set_other_than_winter: ExtendedRule = lambda state, world: (
    world.options.season_control == "vanilla" or (
        state.can_reach_region("Nimbasa City", world.player) and (
            world.options.season_control == "changeable" or state.has_any(("Spring", "Summer", "Autumn"), world.player)
        )
    )
)

can_catch_all_deerlings: ExtendedRule = lambda state, world: (
    (
        "Randomize" not in world.options.randomize_wild_pokemon
        and world.options.season_control == "vanilla"
    )
    or state.has_all((
        "Deerling (Spring)", "Deerling (Summer)", "Deerling (Autumn)", "Deerling (Winter)"
    ), world.player)
)

can_use_strength_and_set_other_than_winter: ExtendedRule = lambda state, world: (
    can_use_strength(state, world) and can_set_other_than_winter(state, world)
)

encounter_can_set_spring: ExtendedRule = lambda state, world: (
    state.can_reach_region("Nimbasa City", world.player) and (
        world.options.season_control == "changeable" or state.has("Spring", world.player)
    )
)

encounter_can_set_summer: ExtendedRule = lambda state, world: (
    state.can_reach_region("Nimbasa City", world.player) and (
        world.options.season_control == "changeable" or state.has("Summer", world.player)
    )
)

encounter_can_set_autumn: ExtendedRule = lambda state, world: (
    state.can_reach_region("Nimbasa City", world.player) and (
        world.options.season_control == "changeable" or state.has("Autumn", world.player)
    )
)

encounter_can_set_winter: ExtendedRule = lambda state, world: (
    state.can_reach_region("Nimbasa City", world.player) and (
        world.options.season_control == "changeable" or state.has("Winter", world.player)
    )
)


# Region requirements

can_beat_ghetsis: ExtendedRule = lambda state, world: state.can_reach_region("N's Castle", world.player)
can_encounter_swords_of_justice: ExtendedRule = lambda state, world: state.can_reach_region("Mistralton Cave Inner", world.player)
can_cut_dreamyard_tree: ExtendedRule = lambda state, world: state.can_reach_region("Dreamyard North", world.player)
can_go_deeper_into_relic_castle: ExtendedRule = lambda state, world: state.can_reach_region("Relic Castle Lower Floors", world.player)
can_go_to_relic_castle_basement: ExtendedRule = lambda state, world: state.can_reach_region("Relic Castle Tower Lower Floors", world.player)
can_find_woman_on_village_bridge: ExtendedRule = lambda state, world: state.can_reach_region("Village Bridge", world.player)
can_go_to_nimbasa_city: ExtendedRule = lambda state, world: state.can_reach_region("Nimbasa City", world.player)
can_go_to_mistralton_city: ExtendedRule = lambda state, world: state.can_reach_region("Mistralton City", world.player)


# Encounter requirements

has_forces_of_nature: ExtendedRule = lambda state, world: state.has_all(("Thundurus", "Tornadus"), world.player)
has_celebi: ExtendedRule = lambda state, world: state.has("Celebi", world.player)
has_legendary_beasts: ExtendedRule = lambda state, world: state.has_all(("Entei", "Raikou", "Suicune"), world.player)
has_25_species: ExtendedRule = lambda state, world: state.count_from_list_unique(species.unova_species, world.player) >= 25
has_51_species: ExtendedRule = lambda state, world: state.count_from_list_unique(species.unova_species, world.player) >= 51
has_60_species: ExtendedRule = lambda state, world: state.count_from_list_unique(species.unova_species, world.player) >= 60
has_115_species: ExtendedRule = lambda state, world: state.count_from_list_unique(species.unova_species, world.player) >= 115


# Miscellaneous requirements

has_fighting_type_species: ExtendedRule = lambda state, world: (
    state.has_any(world.fighting_type_species, world.player)
)

has_any_tm_hm: ExtendedRule = lambda state, world: (
    state.has_any(tm_hm.tm, world.player) or state.has_any(tm_hm.hm, world.player)
)

striaton_hidden_item: ExtendedRule = lambda state, world: state.can_reach_region("Route 3", world.player) or can_use_surf(state, world)
dark_cave: ExtendedRule = lambda state, world: "Require Flash" not in world.options.modify_logic or can_use_flash(state, world)
challengers_cave: ExtendedRule = lambda state, world: has_red_chain(state, world) and dark_cave(state, world)
mistralton_cave: ExtendedRule = lambda state, world: can_use_surf(state, world) and dark_cave(state, world)
trial_chamber: ExtendedRule = lambda state, world: can_encounter_swords_of_justice(state, world) and can_use_strength(state, world)

extended_rules_list: tuple = (
    can_use_strength, can_use_surf, can_use_cut, can_use_waterfall, can_use_dive, can_use_flash,
    can_use_surf_or_strength,

    can_fish, has_rage_candy_bar, has_basement_key, has_parcel, has_loot_sack, has_dragon_skull, has_liberty_pass,
    has_machine_part, has_explorer_kit, has_tidal_bell, has_oaks_letter, has_blue_card, has_red_chain,
    has_any_legendary_stone, has_lock_capsule, has_all_grams,

    has_root_fossil, has_claw_fossil, has_helix_fossil, has_dome_fossil, has_old_amber,
    has_armor_fossil, has_skull_fossil, has_cover_fossil, has_plume_fossil,

    has_trio_badge, has_basic_badge, has_insect_badge, has_bolt_badge,
    has_quake_badge, has_jet_badge, has_freeze_badge, has_legend_badge,

    can_set_winter, can_set_other_than_winter, can_catch_all_deerlings, can_use_strength_and_set_other_than_winter,
    encounter_can_set_spring, encounter_can_set_summer, encounter_can_set_autumn, encounter_can_set_winter,

    can_beat_ghetsis, can_encounter_swords_of_justice, can_cut_dreamyard_tree, can_go_deeper_into_relic_castle,
    can_go_to_relic_castle_basement, can_find_woman_on_village_bridge, can_go_to_nimbasa_city,
    can_go_to_mistralton_city,

    has_forces_of_nature, has_celebi, has_legendary_beasts,
    has_25_species, has_51_species, has_60_species, has_115_species,

    has_fighting_type_species, has_any_tm_hm,
    striaton_hidden_item, dark_cave, challengers_cave, mistralton_cave, trial_chamber,
)


# Encounter inclusion rules

changeable_seasons: InclusionRule = lambda world: world.options.season_control != "vanilla"
disabled: InclusionRule = lambda world: False  # Due to missing wild randomization
randomized_wild: InclusionRule = lambda world: "Randomize" in world.options.randomize_wild_pokemon
