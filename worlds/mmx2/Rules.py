from worlds.generic.Rules import add_rule, set_rule
from BaseClasses import CollectionState

from . import MMX2World
from .Names import LocationName, ItemName, RegionName, EventName

mavericks = [
    "Wheel Gator",
    "Bubble Crab",
    "Flame Stag",
    "Morph Moth",
    "Magna Centipede",
    "Crystal Snail",
    "Overdrive Ostrich",
    "Wire Sponge",
]

bosses = {
    "Wheel Gator": [
        f"{RegionName.wheel_gator_end} -> {RegionName.wheel_gator_boss}",
        LocationName.x_hunter_stage_4_wheel_gator,
        EventName.wheel_gator_rematch,
    ],
    "Bubble Crab": [
        f"{RegionName.bubble_crab_inside} -> {RegionName.bubble_crab_boss}",
        LocationName.x_hunter_stage_4_bubble_crab,
        EventName.bubble_crab_rematch,
    ],
    "Flame Stag": [
        f"{RegionName.flame_stag_gas} -> {RegionName.flame_stag_boss}",
        LocationName.x_hunter_stage_4_flame_stag,
        EventName.flame_stag_rematch,
    ],
    "Morph Moth": [
        f"{RegionName.morph_moth_after_parasite_2} -> {RegionName.morph_moth_boss}",
        LocationName.x_hunter_stage_4_morph_moth,
        EventName.morph_moth_rematch,
    ],
    "Magna Centipede": [
        f"{RegionName.magna_centipede_after_security} -> {RegionName.magna_centipede_boss}",
        LocationName.x_hunter_stage_4_magna_centipede,
        EventName.magna_centipede_rematch,
    ],
    "Crystal Snail": [
        f"{RegionName.crystal_snail_uphill} -> {RegionName.crystal_snail_boss}",
        LocationName.x_hunter_stage_4_crystal_snail,
        EventName.crystal_snail_rematch,
    ],
    "Overdrive Ostrich": [
        f"{RegionName.overdrive_ostrich_inside} -> {RegionName.overdrive_ostrich_boss}",
        LocationName.x_hunter_stage_4_overdrive_ostrich,
        EventName.overdrive_ostrich_rematch,
    ],
    "Wire Sponge": [
        f"{RegionName.wire_sponge_outside} -> {RegionName.wire_sponge_boss}",
        LocationName.x_hunter_stage_4_wire_sponge,
        EventName.wire_sponge_rematch,
    ],
    "Violen": [
        LocationName.violen_defeated
    ],
    "Serges": [
        LocationName.serges_defeated,
        f"{RegionName.x_hunter_stage_2_start} -> {RegionName.x_hunter_stage_2_boss}",
        EventName.x_hunter_stage_2_clear,
    ],
    "Agile": [
        LocationName.agile_defeated,
    ],
    "Magna Quartz": [
        f"{RegionName.crystal_snail_start} -> {RegionName.crystal_snail_quartz}"
    ],
    "Chop Register": [
        f"{RegionName.magna_centipede_start} -> {RegionName.magna_centipede_blade}",
    ],
    "Raider Killer": [
        f"{RegionName.magna_centipede_after_blade} -> {RegionName.magna_centipede_security}",
    ],
    "Pararoid S-38": [
        f"{RegionName.morph_moth_start} -> {RegionName.morph_moth_parasite_1}",
        f"{RegionName.morph_moth_after_parasite_1} -> {RegionName.morph_moth_parasite_2}",
    ],
    "Neo Violen": [
        f"{RegionName.x_hunter_stage_1_start} -> {RegionName.x_hunter_stage_1_boss}",
        EventName.x_hunter_stage_1_clear,
    ],
    "Serges Tank": [
        f"{RegionName.x_hunter_stage_2_start} -> {RegionName.x_hunter_stage_2_boss}",
        EventName.x_hunter_stage_2_clear,
    ],
    "Agile Flyer": [
        f"{RegionName.x_hunter_stage_3_start} -> {RegionName.x_hunter_stage_3_boss}",
        EventName.x_hunter_stage_3_clear,
    ],
    "Zero": [
        f"{RegionName.x_hunter_stage_5} -> {RegionName.x_hunter_stage_5_zero}",
    ],
    "Sigma": [
        f"{RegionName.x_hunter_stage_5_zero} -> {RegionName.x_hunter_stage_5_sigma}"
    ],
    "Sigma Virus": [
        f"{RegionName.x_hunter_stage_5_zero} -> {RegionName.x_hunter_stage_5_sigma}"
    ]
}


def set_rules(world: MMX2World):
    player = world.player
    multiworld = world.multiworld
    jammed_buster = world.options.jammed_buster.value

    multiworld.completion_condition[player] = lambda state: state.has(ItemName.victory, player)

    # Hunter base entrance rules
    set_rule(multiworld.get_entrance(f"{RegionName.intro_stage} -> {RegionName.wheel_gator}", player),
             lambda state: state.has(ItemName.stage_wheel_gator, player))
    set_rule(multiworld.get_entrance(f"{RegionName.intro_stage} -> {RegionName.bubble_crab}", player),
             lambda state: state.has(ItemName.stage_bubble_crab, player))
    set_rule(multiworld.get_entrance(f"{RegionName.intro_stage} -> {RegionName.flame_stag}", player),
             lambda state: state.has(ItemName.stage_flame_stag, player))
    set_rule(multiworld.get_entrance(f"{RegionName.intro_stage} -> {RegionName.morph_moth}", player),
             lambda state: state.has(ItemName.stage_morph_moth, player))
    set_rule(multiworld.get_entrance(f"{RegionName.intro_stage} -> {RegionName.magna_centipede}", player),
             lambda state: state.has(ItemName.stage_magna_centipede, player))
    set_rule(multiworld.get_entrance(f"{RegionName.intro_stage} -> {RegionName.crystal_snail}", player),
             lambda state: state.has(ItemName.stage_crystal_snail, player))
    set_rule(multiworld.get_entrance(f"{RegionName.intro_stage} -> {RegionName.overdrive_ostrich}", player),
             lambda state: state.has(ItemName.stage_overdrive_ostrich, player))
    set_rule(multiworld.get_entrance(f"{RegionName.intro_stage} -> {RegionName.wire_sponge}", player),
             lambda state: state.has(ItemName.stage_wire_sponge, player))

    # X-Hunter Base entrance rules
    base_open = world.options.base_open.value
    entrance = multiworld.get_entrance(f"{RegionName.intro_stage} -> {RegionName.x_hunter_stage}", player)

    if len(base_open) == 0:
        set_rule(entrance, lambda state: state.has(ItemName.stage_x_hunter, player))
    else:
        if "Medals" in base_open and world.options.base_medal_count.value > 0:
            add_rule(entrance, lambda state: state.has(ItemName.maverick_medal, player, world.options.base_medal_count.value))
        if "Weapons" in base_open and world.options.base_weapon_count.value > 0:
            add_rule(entrance, lambda state: state.has_group("Weapons", player, world.options.base_weapon_count.value))
        if "Armor Upgrades" in base_open and world.options.base_upgrade_count.value > 0:
            add_rule(entrance, lambda state: state.has_group("Armor Upgrades", player, world.options.base_upgrade_count.value))
        if "Heart Tanks" in base_open and world.options.base_heart_tank_count.value > 0:
            add_rule(entrance, lambda state: state.has(ItemName.heart_tank, player, world.options.base_heart_tank_count.value))
        if "Sub Tanks" in base_open and world.options.base_sub_tank_count.value > 0:
            add_rule(entrance, lambda state: state.has(ItemName.sub_tank, player, world.options.base_sub_tank_count.value))

    # X-Hunter Base rules
    if world.options.base_all_levels.value:
        set_rule(multiworld.get_entrance(f"{RegionName.x_hunter_stage} -> {RegionName.x_hunter_stage_4}", player),
                 lambda state: (
                     state.has(EventName.x_hunter_stage_1_clear, player) and 
                     state.has(EventName.x_hunter_stage_2_clear, player) and 
                     state.has(EventName.x_hunter_stage_3_clear, player)
                    ))
    else:
        set_rule(multiworld.get_entrance(f"{RegionName.x_hunter_stage_1_boss} -> {RegionName.x_hunter_stage_2}", player),
                 lambda state: state.has(EventName.x_hunter_stage_1_clear, player))
        set_rule(multiworld.get_entrance(f"{RegionName.x_hunter_stage_2_boss} -> {RegionName.x_hunter_stage_3}", player),
                 lambda state: state.has(EventName.x_hunter_stage_2_clear, player))
        set_rule(multiworld.get_entrance(f"{RegionName.x_hunter_stage_3_boss} -> {RegionName.x_hunter_stage_4}", player),
                 lambda state: state.has(EventName.x_hunter_stage_3_clear, player))
        
    set_rule(multiworld.get_entrance(f"{RegionName.x_hunter_stage_4_voice} -> {RegionName.x_hunter_stage_5}", player),
                lambda state: state.has(EventName.x_hunter_stage_4_clear, player))
        
    # Set Boss rematch rules
    if world.options.base_boss_rematch_count.value > 0:
        set_rule(multiworld.get_entrance(f"{RegionName.x_hunter_stage_4_lobby} -> {RegionName.x_hunter_stage_4_voice}", player),
                lambda state: state.has(EventName.boss_rematch_clear, player, world.options.base_boss_rematch_count.value))
    
    # X-Hunter base 2 entrance
        add_rule(multiworld.get_entrance(f"{RegionName.x_hunter_stage_2} -> {RegionName.x_hunter_stage_2_start}", player),
                lambda state: (
                    state.has(ItemName.legs, player) or 
                    state.has(ItemName.crystal_hunter, player) or 
                    (
                        state.has(ItemName.arms, player, jammed_buster + 1) and
                        state.has(ItemName.speed_burner, player)
                    )
                ))

    # X-Hunter arena entrance rules
    set_rule(multiworld.get_entrance(f"{RegionName.wheel_gator_mid} -> {RegionName.x_hunter_arena}", player), 
             lambda state: state.has(ItemName.maverick_medal, player, world.options.x_hunters_medal_count.value))
    set_rule(multiworld.get_entrance(f"{RegionName.bubble_crab_open} -> {RegionName.x_hunter_arena}", player), 
             lambda state: state.has(ItemName.maverick_medal, player, world.options.x_hunters_medal_count.value))
    set_rule(multiworld.get_entrance(f"{RegionName.flame_stag_volcano} -> {RegionName.x_hunter_arena}", player), 
             lambda state: state.has(ItemName.maverick_medal, player, world.options.x_hunters_medal_count.value))
    set_rule(multiworld.get_entrance(f"{RegionName.morph_moth_after_parasite_1} -> {RegionName.x_hunter_arena}", player), 
             lambda state: state.has(ItemName.maverick_medal, player, world.options.x_hunters_medal_count.value))
    set_rule(multiworld.get_entrance(f"{RegionName.magna_centipede_after_blade} -> {RegionName.x_hunter_arena}", player), 
             lambda state: state.has(ItemName.maverick_medal, player, world.options.x_hunters_medal_count.value))
    set_rule(multiworld.get_entrance(f"{RegionName.crystal_snail_arena} -> {RegionName.x_hunter_arena}", player), 
             lambda state: state.has(ItemName.maverick_medal, player, world.options.x_hunters_medal_count.value))
    set_rule(multiworld.get_entrance(f"{RegionName.crystal_snail_arena} -> {RegionName.crystal_snail_after_arena}", player), 
             lambda state: 
                state.has(ItemName.maverick_medal, player, world.options.x_hunters_medal_count.value) and
                (
                    state.can_reach_location(LocationName.agile_defeated, player) or 
                    state.can_reach_location(LocationName.serges_defeated, player) or 
                    state.can_reach_location(LocationName.violen_defeated, player)
                )
            )
    set_rule(multiworld.get_entrance(f"{RegionName.overdrive_ostrich_arena} -> {RegionName.x_hunter_arena}", player), 
             lambda state: (
                    state.has(ItemName.maverick_medal, player, world.options.x_hunters_medal_count.value) and
                    state.has(ItemName.spin_wheel, player)
                ))
    set_rule(multiworld.get_entrance(f"{RegionName.wire_sponge_elevator} -> {RegionName.x_hunter_arena}", player), 
             lambda state: state.has(ItemName.maverick_medal, player, world.options.x_hunters_medal_count.value))
    
    # Wheel Gator rules
    add_rule(multiworld.get_location(LocationName.wheel_gator_arms, player),
             lambda state: (
                state.has(ItemName.legs, player) or 
                (
                    state.has(ItemName.arms, player, jammed_buster + 1) and
                    state.has(ItemName.speed_burner, player)
                )
             ))
    add_rule(multiworld.get_location(LocationName.wheel_gator_heart_tank, player),
             lambda state: (
                state.has(ItemName.arms, player, jammed_buster + 1) and
                state.has(ItemName.speed_burner, player)
             ))
    
    # Bubble Crab rules
    add_rule(multiworld.get_location(LocationName.bubble_crab_sub_tank, player),
             lambda state: (
                state.has(ItemName.arms, player, jammed_buster + 1) and
                state.has(ItemName.bubble_splash, player)
             ))
    
    # Morph Moth rules
    add_rule(multiworld.get_location(LocationName.morph_moth_heart_tank, player),
             lambda state: state.has(ItemName.crystal_hunter, player))
    add_rule(multiworld.get_location(LocationName.morph_moth_body, player),
             lambda state: state.has(ItemName.spin_wheel, player))
    
    # Magna Centipede rules
    add_rule(multiworld.get_location(LocationName.magna_centipede_heart_tank, player),
             lambda state: (
                state.has(ItemName.arms, player, jammed_buster + 1) and
                state.has(ItemName.speed_burner, player)
             ))
    add_rule(multiworld.get_location(LocationName.magna_centipede_sub_tank, player),
             lambda state: (
                state.has(ItemName.legs, player) or 
                (
                    state.has(ItemName.arms, player, jammed_buster + 1) and
                    state.has(ItemName.speed_burner, player)
                )
             ))
    
    # Crystal Snail rules
    add_rule(multiworld.get_location(LocationName.crystal_snail_heart_tank, player),
             lambda state: (
                state.has(ItemName.legs, player) or 
                (
                    state.has(ItemName.arms, player, jammed_buster + 1) and
                    state.has(ItemName.speed_burner, player)
                )
             ))

    # Overdrive Ostrich rules
    add_rule(multiworld.get_location(LocationName.overdrive_ostrich_leg, player),
             lambda state: state.has(ItemName.spin_wheel, player))
    
    # X-Hunter Base 3 rules
    add_rule(multiworld.get_location(LocationName.x_hunter_stage_3_shoryuken, player),
             lambda state: (
                state.has(ItemName.legs, player) and
                state.has(ItemName.arms, player, jammed_buster + 1) and
                state.has(ItemName.speed_burner, player) and
                state.has(ItemName.crystal_hunter, player)
             ))

    # Handle bosses weakness
    if world.options.logic_boss_weakness.value or world.options.boss_weakness_strictness.value >= 2:
        add_boss_weakness_logic(world)

    # Handle pickupsanity logic
    if world.options.pickupsanity.value:
        add_pickupsanity_logic(world)

    # Handle helmet logic
    if world.options.logic_helmet_checkpoints.value:
        add_helmet_logic(world)


def check_weaknesses(state: CollectionState, player: int, rulesets: list) -> bool:
    states = list()
    for i in range(len(rulesets)):
        valid = state.has_all_counts(rulesets[i], player)
        states.append(valid)
    return any(states)


def add_boss_weakness_logic(world: MMX2World):
    player = world.player
    multiworld = world.multiworld
    jammed_buster = world.options.jammed_buster.value

    boss_dict = {}
    for boss, regions in bosses.items():
        boss_dict[boss] = regions.copy()
        if boss in mavericks and world.options.base_boss_rematch_count.value == 0:
            boss_dict[boss].pop()
            boss_dict[boss].pop()

    for boss, regions in boss_dict.items():
        weaknesses = world.boss_weaknesses[boss]
        rulesets = list()
        for weakness in weaknesses:
            if weakness[0] is None:
                rulesets = None
                break
            weakness = weakness[0]
            ruleset = dict()
            if "Check Charge" in weakness[0]:
                ruleset[ItemName.arms] = jammed_buster + int(weakness[0][-1:]) - 1
            else:
                ruleset[weakness[0]] = 1
            if len(weakness) != 1:
                ruleset[weakness[1]] = 1
            rulesets.append(ruleset)

        if rulesets is not None:
            for region in regions:
                if "->" in region:
                    add_rule(multiworld.get_entrance(region, player),
                                lambda state, rulesets=rulesets: check_weaknesses(state, player, rulesets))
                else:
                    add_rule(multiworld.get_location(region, player),
                                lambda state, rulesets=rulesets: check_weaknesses(state, player, rulesets))


def add_pickupsanity_logic(world: MMX2World):
    player = world.player
    multiworld = world.multiworld
    jammed_buster = world.options.jammed_buster.value

    # Bubble Crab
    add_rule(multiworld.get_location(LocationName.bubble_crab_1up, player),
             lambda state: state.has(ItemName.spin_wheel, player))
    add_rule(multiworld.get_location(LocationName.bubble_crab_energy_1, player),
             lambda state: (
                state.has(ItemName.legs, player) or
                (
                    state.has(ItemName.arms, player, jammed_buster + 1) and
                    state.has(ItemName.speed_burner, player)
                ) or (
                    state.has(ItemName.arms, player, jammed_buster + 1) and
                    state.has(ItemName.bubble_splash, player)
                )
             ))
    
    # Morph Moth
    add_rule(multiworld.get_location(LocationName.morph_moth_1up_1, player),
             lambda state: state.has(ItemName.crystal_hunter, player))

    # Flame Stag
    add_rule(multiworld.get_location(LocationName.flame_stag_1up_3, player),
             lambda state: state.has(ItemName.legs, player))

    # Overdrive Ostrich
    add_rule(multiworld.get_location(LocationName.overdrive_ostrich_hp_1, player),
             lambda state: state.has(ItemName.spin_wheel, player))
    
    # X-Hunter Base 2
    add_rule(multiworld.get_location(LocationName.x_hunter_stage_2_hp, player),
             lambda state: state.has(ItemName.spin_wheel, player))
    add_rule(multiworld.get_location(LocationName.x_hunter_stage_2_1up, player),
             lambda state: (
                state.has(ItemName.legs, player) and
                state.has(ItemName.arms, player, jammed_buster + 1) and
                state.has(ItemName.speed_burner, player) and
                state.has(ItemName.spin_wheel, player)
             ))
    
    # X-Hunter Base 3
    add_rule(multiworld.get_location(LocationName.x_hunter_stage_3_hp_1, player),
             lambda state: (
                state.has(ItemName.legs, player) and
                state.has(ItemName.strike_chain, player)
             ))
    add_rule(multiworld.get_location(LocationName.x_hunter_stage_3_1up_1, player),
             lambda state: (
                state.has(ItemName.legs, player) and
                state.has(ItemName.strike_chain, player)
             ))
    add_rule(multiworld.get_location(LocationName.x_hunter_stage_3_1up_2, player),
             lambda state: state.has(ItemName.crystal_hunter, player))
    add_rule(multiworld.get_location(LocationName.x_hunter_stage_3_hp_7, player),
             lambda state: state.has(ItemName.crystal_hunter, player))
    add_rule(multiworld.get_location(LocationName.x_hunter_stage_3_hp_8, player),
             lambda state: state.has(ItemName.crystal_hunter, player))
    add_rule(multiworld.get_location(LocationName.x_hunter_stage_3_1up_3, player),
             lambda state: (
                state.has(ItemName.legs, player) and
                state.has(ItemName.arms, player, jammed_buster + 1) and
                state.has(ItemName.speed_burner, player) and
                state.has(ItemName.crystal_hunter, player)
             ))
    add_rule(multiworld.get_location(LocationName.x_hunter_stage_3_1up_4, player),
             lambda state: (
                state.has(ItemName.legs, player) or
                (
                    state.has(ItemName.arms, player, jammed_buster + 1) and
                    state.has(ItemName.speed_burner, player)
                )
             ))


def add_helmet_logic(world: MMX2World):
    player = world.player
    multiworld = world.multiworld

    set_rule(multiworld.get_entrance(f"{RegionName.morph_moth} -> {RegionName.morph_moth_after_parasite_1}", player), 
             lambda state: state.has(ItemName.helmet, player, 1))
    set_rule(multiworld.get_entrance(f"{RegionName.morph_moth} -> {RegionName.morph_moth_after_parasite_2}", player), 
             lambda state: state.has(ItemName.helmet, player, 1))
    
    set_rule(multiworld.get_entrance(f"{RegionName.magna_centipede} -> {RegionName.magna_centipede_after_blade}", player), 
             lambda state: state.has(ItemName.helmet, player, 1))
    set_rule(multiworld.get_entrance(f"{RegionName.magna_centipede} -> {RegionName.magna_centipede_after_security}", player), 
             lambda state: state.has(ItemName.helmet, player, 1))
    
    set_rule(multiworld.get_entrance(f"{RegionName.crystal_snail} -> {RegionName.crystal_snail_downhill}", player), 
             lambda state: state.has(ItemName.helmet, player, 1))
