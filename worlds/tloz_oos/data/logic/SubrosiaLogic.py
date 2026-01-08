from worlds.tloz_oos.data.logic.LogicPredicates import *


def make_subrosia_logic(player: int):
    return [
        # Portals ###############################################################

        ["volcanoes east portal", "subrosia temple sector", True, None],
        ["subrosia market portal", "subrosia market sector", True, None],
        ["strange brothers portal", "subrosia hide and seek sector", True, lambda state: oos_has_feather(state, player)],
        ["house of pirates portal", "subrosia pirates sector", True, None],
        ["great furnace portal", "subrosia furnace sector", True, None],
        ["volcanoes west portal", "subrosia volcano sector", True, None],
        ["d8 entrance portal", "d8 entrance", True, None],

        # TODO when alt starting locations are implemented, there probably needs to be a way to re-use this forced transition
        ["pirates after bell", "western coast after ship", False, None],

        # Regions ###############################################################

        ["subrosia temple sector", "subrosia market sector", False, lambda state: \
            oos_can_jump_1_wide_liquid(state, player, False)],
        ["subrosia market sector", "subrosia temple sector", False, lambda state: any([
            oos_can_date_rosa(state, player),
            oos_can_jump_1_wide_liquid(state, player, False)
        ])],
        ["subrosia market sector", "subrosia east junction", False, lambda state: any([
            oos_has_magnet_gloves(state, player),
            # As it is a "diagonal" pit, it is considered as a 3.5-wide pit
            oos_can_jump_3_wide_liquid(state, player)
        ])],
        ["subrosia east junction", "subrosia market sector", False, lambda state: any([
            # This backwards route adds itself on top of the two-way route right above this one, adding the option
            # to remove the rock using the bracelet to turn this pit into a 2-wide jump
            all([
                oos_has_bracelet(state, player),
                oos_can_jump_2_wide_pit(state, player)
            ]),
            oos_has_magnet_gloves(state, player),
            # As it is a "diagonal" pit, it is considered as a 3.5-wide pit
            oos_can_jump_3_wide_liquid(state, player)  # Could deserve an upgrade but isn't quite worth a hell classification
        ])],

        ["subrosia temple sector", "subrosia bridge sector", True, lambda state: oos_has_feather(state, player)],
        ["subrosia volcano sector", "subrosia bridge sector", False, lambda state: all([
            oos_has_bracelet(state, player),
            oos_can_jump_3_wide_liquid(state, player)
        ])],
        ["subrosia volcano sector", "bomb temple remains", False, lambda state: oos_has_bombs(state, player)],

        ["subrosia hide and seek sector", "subrosia market sector", False, lambda state: all([
            oos_has_bracelet(state, player),
            oos_has_feather(state, player),
            any([
                oos_can_jump_2_wide_liquid(state, player),
                oos_has_magnet_gloves(state, player)
            ])
        ])],
        ["subrosia market sector", "subrosia hide and seek sector", False, lambda state: all([
            # H&S skip, with bracelet : https://youtu.be/lH1yvshG3LE
            # H&S skip, without bracelet : https://youtube.com/clip/Ugkx6EcYk0akEEgfO1SuhSfAO3Px5KCTtUKD
            oos_option_hell_logic(state, player),
            oos_has_feather(state, player),
            oos_can_use_pegasus_seeds(state, player),
            oos_has_bombs(state, player),
            # Old H&S skip doesn't require bracelet
        ])],
        ["subrosia hide and seek sector", "subrosia temple sector", True, lambda state: oos_can_jump_4_wide_liquid(state, player)],
        ["subrosia hide and seek sector", "subrosia pirates sector", True, lambda state: oos_has_feather(state, player)],

        ["subrosia east junction", "subrosia furnace sector", False, lambda state: oos_has_feather(state, player)],
        ["subrosia furnace sector", "subrosia east junction", False, lambda state: any([
            oos_has_feather(state, player),
            all([
                oos_option_medium_logic(state, player),
                oos_has_switch_hook(state, player)
            ])
        ])],

        # Locations ###############################################################

        ["subrosia temple sector", "subrosian dance hall", False, None],
        ["subrosia temple sector", "subrosian smithy ore", False, lambda state: any([
            state.has("Hard Ore", player),
            oos_self_locking_item(state, player, "subrosian smithy ore", "Hard Ore")
        ])],
        ["subrosia temple sector", "subrosian smithy bell", False, lambda state: any([
            state.has("Rusty Bell", player),
            oos_self_locking_item(state, player, "subrosian smithy bell", "Rusty Bell")
        ])],
        ["subrosia temple sector", "smith secret", False, lambda state: oos_has_shield(state, player)],

        ["subrosia temple sector", "temple of seasons", False, None],
        ["subrosia temple sector", "tower of winter", False, lambda state: any([
            oos_has_feather(state, player),
            oos_can_trigger_far_switch(state, player)
        ])],
        ["subrosia temple sector", "tower of summer", False, lambda state: all([
            oos_can_date_rosa(state, player),
            oos_has_bracelet(state, player),
        ])],
        ["subrosia temple sector", "tower of autumn", False, lambda state: all([
            oos_has_feather(state, player),
            state.has("Bomb Flower", player)
        ])],
        ["subrosia temple sector", "subrosian secret", False, lambda state: all([
            oos_can_jump_1_wide_pit(state, player, False),
            oos_has_magic_boomerang(state, player)
        ])],

        ["subrosia market sector", "subrosia seaside", False, lambda state: oos_has_shovel(state, player)],
        ["subrosia market sector", "subrosia market star ore", False, lambda state: any([
            state.has("Star Ore", player),
            oos_self_locking_item(state, player, "subrosia market star ore", "Star Ore")
        ])],
        ["subrosia market sector", "subrosia market ore chunks", False, lambda state: \
            oos_can_buy_market(state, player)],

        ["subrosia hide and seek sector", "subrosia hide and seek", False, lambda state: oos_has_shovel(state, player)],
        ["subrosia hide and seek sector", "tower of spring", False, lambda state: oos_has_feather(state, player)],
        ["subrosia hide and seek sector", "subrosian wilds chest", False, lambda state: all([
            oos_has_feather(state, player),
            any([
                oos_has_magnet_gloves(state, player),
                oos_can_jump_4_wide_pit(state, player)
            ])
        ])],
        ["subrosian wilds chest", "subrosian wilds digging spot", False, lambda state: all([
            any([
                oos_can_jump_3_wide_pit(state, player),
                oos_has_magnet_gloves(state, player)
            ]),
            oos_has_feather(state, player),
            oos_has_shovel(state, player)
        ])],

        ["subrosia hide and seek sector", "subrosian house", False, lambda state: oos_has_feather(state, player)],
        ["subrosia hide and seek sector", "subrosian 2d cave", False, lambda state: oos_has_feather(state, player)],

        ["subrosia bridge sector", "subrosia, open cave", False, None],
        ["subrosia bridge sector", "subrosia, locked cave", False, lambda state: all([
            oos_can_date_rosa(state, player),
            oos_has_feather(state, player)
        ])],
        ["subrosia bridge sector", "subrosian chef trade", False, lambda state: any([
            state.has("Iron Pot", player),
            oos_self_locking_item(state, player, "subrosian chef trade", "Iron Pot")
        ])],

        ["subrosia east junction", "subrosia village chest", False, lambda state: any([
            oos_has_magnet_gloves(state, player),
            oos_can_jump_4_wide_pit(state, player),
            all([
                # early red ore : https://youtu.be/fB10dV2Gunk
                oos_option_hell_logic(state, player),
                oos_has_feather(state, player),
                oos_can_use_pegasus_seeds(state, player),
                oos_has_bombs(state, player)
            ])
        ])],

        ["subrosia furnace sector", "great furnace", False, lambda state: all([
            state.has("_opened_tower_of_autumn", player),
            any([
                state.has("Red Ore", player),
                oos_self_locking_item(state, player, "great furnace", "Red Ore")
            ]),
            any([
                state.has("Blue Ore", player),
                oos_self_locking_item(state, player, "great furnace", "Blue Ore")
            ]),
        ])],
        ["subrosia furnace sector", "subrosian sign guy", False, lambda state: oos_can_break_sign(state, player)],
        ["subrosia furnace sector", "subrosian buried bomb flower", False, lambda state: all([
            oos_has_feather(state, player),
            oos_has_bracelet(state, player)
        ])],

        ["subrosia temple sector", "subrosia temple digging spot", False, lambda state: oos_has_shovel(state, player)],
        ["subrosia temple sector", "subrosia bath digging spot", False, lambda state: all([
            oos_can_jump_1_wide_pit(state, player, False),
            any([
                oos_can_jump_3_wide_liquid(state, player),
                oos_has_magnet_gloves(state, player)
            ]),
            oos_has_shovel(state, player)
        ])],
        ["subrosia market sector", "subrosia market digging spot", False, lambda state: oos_has_shovel(state, player)],

        ["subrosia bridge sector", "subrosia bridge digging spot", False, lambda state: oos_has_shovel(state, player)],

        ["subrosia pirates sector", "pirates after bell", False, lambda state: state.has("Pirate's Bell", player)],
    ]
