from typing import TYPE_CHECKING, Callable

from BaseClasses import CollectionState, MultiWorld
from worlds.AutoWorld import LogicMixin
from worlds.generic.Rules import set_rule
from ..options import (
    BigKeySettings,
    DamageMagnification,
    LogicRules,
    SmallKeySettings,
    TotEntrance,
)
from .Macros import *
from ..Locations import LOCATION_TABLE

if TYPE_CHECKING:
    from .. import TPWorld


class TPLogic(LogicMixin):

    multiworld: MultiWorld

    def _tp_glitched(self, player: int) -> bool:
        return (
            self.multiworld.worlds[player].options.logic_rules.value
            == LogicRules.option_glitched
        )

    def _tp_shops_shuffled(self, player: int) -> bool:
        return self.multiworld.worlds[player].options.shop_items_shuffled.value

    def _tp_is_small_key_anywhere(self, player: int) -> bool:
        return (
            self.multiworld.worlds[player].options.small_key_settings.value
            == SmallKeySettings.option_anywhere
        )

    def _tp_is_big_key_anywhere(self, player: int) -> bool:
        return (
            self.multiworld.worlds[player].options.big_key_settings.value
            == BigKeySettings.option_anywhere
        )

    def _tp_small_key_settings(self, player: int) -> int:
        return self.multiworld.worlds[player].options.small_key_settings.value

    def _tp_big_key_settings(self, player: int) -> int:
        return self.multiworld.worlds[player].options.big_key_settings.value

    # def _tp_skip_prologue(self, player: int) -> bool:
    #     return self.multiworld.worlds[player].options.skip_prologue.value

    # def _tp_skip_mdh(self, player: int) -> bool:
    #     return self.multiworld.worlds[player].options.skip_mdh.value

    # def _tp_faron_twilight_cleared(self, player: int) -> bool:
    #     return self.multiworld.worlds[player].options.faron_twilight_cleared.value

    # def _tp_eldin_twilight_cleared(self, player: int) -> bool:
    #     return self.multiworld.worlds[player].options.eldin_twilight_cleared.value

    # def _tp_lanayru_twilight_cleared(self, player: int) -> bool:
    #     return self.multiworld.worlds[player].options.lanayru_twilight_cleared.value

    def _tp_skip_arbiters_entrance(self, player: int) -> bool:
        return self.multiworld.worlds[
            player
        ].options.skip_arbiters_grounds_entrance.value

    def _tp_skip_lakebed_entrance(self, player: int) -> bool:
        return self.multiworld.worlds[player].options.skip_lakebed_entrance.value

    def _tp_skip_city_in_the_sky_entrance(self, player: int) -> bool:
        return self.multiworld.worlds[
            player
        ].options.skip_city_in_the_sky_entrance.value

    def _tp_skip_snowpeak_entrance(self, player: int) -> bool:
        return self.multiworld.worlds[player].options.skip_snowpeak_entrance.value

    def _tp_tot_entrance(self, player: int) -> int:
        return self.multiworld.worlds[player].options.tot_entrance.value

    def _tp_palace_requirements(self, player: int) -> int:
        return self.multiworld.worlds[player].options.palace_requirements.value

    def _tp_castle_requirements(self, player: int) -> int:
        return self.multiworld.worlds[player].options.castle_requirements.value

    def _tp_goron_mines_enterance(self, player: int) -> int:
        return self.multiworld.worlds[player].options.goron_mines_entrance.value

    def _tp_faron_woods_logic(self, player: int) -> int:
        return self.multiworld.worlds[player].options.faron_woods_logic.value

    def _tp_open_map(self, player: int) -> bool:
        return self.multiworld.worlds[player].options.open_map.value

    # def _tp_barren_dungeons(self, player: int) -> bool:
    #     return self.multiworld.worlds[player].options.barren_dungeons.value

    def _tp_increase_wallet(self, player: int) -> bool:
        return self.multiworld.worlds[player].options.increase_wallet.value

    def _tp_bonks_do_damage(self, player: int) -> bool:
        return self.multiworld.worlds[player].options.bonks_do_damage.value

    def _tp_damage_magnification(self, player: int) -> int:
        return self.multiworld.worlds[player].options.damage_magnification.value

    def _tp_transform_anywhere(self, player: int) -> bool:
        return self.multiworld.worlds[player].options.transform_anywhere.value


def set_location_access_rules(world: "TPWorld"):

    def set_rule_if_exists(
        location_name: str,
        rule: Callable[[CollectionState], bool],
        glitched_rule: Callable[[CollectionState], bool] = None,
    ) -> None:
        # Only worry about logic if the location can be a progress item (and location_name not in world.nonprogress_locations) do not worry bout yet
        assert location_name in LOCATION_TABLE, f"{location=}"
        location = world.get_location(location_name)

        if (
            world.options.logic_rules.value == LogicRules.option_glitched
            and glitched_rule
        ):
            # assert glitched_rule, f"{location=} has no glitched rule"
            set_rule(location, glitched_rule)
        # elif world.options.logic_rules.value == LogicRules.option_no_logic:
        #     set_rule(exit, lambda state: (True))
        else:
            set_rule(location, rule)

    player = world.player

    world.multiworld.completion_condition[player] = lambda state: state.has(
        "Victory", player
    )

    set_rule_if_exists(
        "Arbiters Grounds Big Key Chest",
        lambda state: (
            (
                state.has("Arbiters Grounds Small Key", player, 5)
                # Holdover from Keysy
                # or (
                #     state._tp_small_key_settings(player)
                #     == SmallKeySettings.option_anywhere
                # )
            )
            and state.has("Progressive Clawshot", player, 1)
            and state.has("Spinner", player)
            and can_smash(state, player)
        ),
        lambda state: (
            (
                (
                    state.has("Arbiters Grounds Small Key", player, 5)
                    # Holdover from Keysy
                    # or (
                    #     state._tp_small_key_settings(player)
                    #     == SmallKeySettings.option_anywhere
                    # )
                )
                or (
                    state.has("Arbiters Grounds Small Key", player, 4)
                    and state.has("Shadow Crystal", player)
                )
            )
            and state.has("Progressive Clawshot", player, 1)
            and state.has("Spinner", player)
            and can_smash(state, player)
        ),
    )
    set_rule_if_exists(
        "Arbiters Grounds Death Sword Chest",
        lambda state: (
            can_defeat_DeathSword(state, player)
            and state.has("Progressive Clawshot", player, 1)
            and can_defeat_Bubble(state, player)
            and can_defeat_Stalfos(state, player)
            and (
                state.has("Arbiters Grounds Small Key", player, 5)
                # Holdover from Keysy
                # or (
                #     state._tp_small_key_settings(player)
                #     == SmallKeySettings.option_anywhere
                # )
            )
        ),
        lambda state: (
            can_defeat_DeathSword(state, player)
            and state.has("Progressive Clawshot", player, 1)
            and can_defeat_Bubble(state, player)
            and can_defeat_Stalfos(state, player)
            and (
                (
                    state.has("Arbiters Grounds Small Key", player, 5)
                    # Holdover from Keysy
                    # or (
                    #     state._tp_small_key_settings(player)
                    #     == SmallKeySettings.option_anywhere
                    # )
                )
                or (
                    state.has("Arbiters Grounds Small Key", player, 4)
                    and state.has("Shadow Crystal", player)
                )
            )
        ),
    )
    set_rule_if_exists(
        "Arbiters Grounds Dungeon Reward",
        lambda state: (can_defeat_Stallord(state, player)),
    )
    set_rule_if_exists(
        "Arbiters Grounds East Lower Turnable Redead Chest",
        lambda state: (state.has("Shadow Crystal", player)),
    )
    set_rule_if_exists(
        "Arbiters Grounds East Turning Room Poe",
        lambda state: (
            state.has("Shadow Crystal", player)
            and state.has("Progressive Clawshot", player, 1)
        ),
    )
    set_rule_if_exists(
        "Arbiters Grounds East Upper Turnable Chest",
        lambda state: (
            (
                state.has("Arbiters Grounds Small Key", player, 2)
                # Holdover from Keysy
                # or (
                #     state._tp_small_key_settings(player)
                #     == SmallKeySettings.option_anywhere
                # )
            )
        ),
    )
    set_rule_if_exists(
        "Arbiters Grounds East Upper Turnable Redead Chest",
        lambda state: (
            has_damaging_item(state, player)
            and (
                state.has("Arbiters Grounds Small Key", player, 2)
                # Holdover from Keysy
                # or (
                #     state._tp_small_key_settings(player)
                #     == SmallKeySettings.option_anywhere
                # )
            )
        ),
    )
    set_rule_if_exists(
        "Arbiters Grounds Entrance Chest",
        lambda state: (can_break_wooden_door(state, player)),
    )
    set_rule_if_exists(
        "Arbiters Grounds Ghoul Rat Room Chest",
        lambda state: (
            can_defeat_Bubble(state, player)
            and can_defeat_Stalchild(state, player)
            and can_defeat_RedeadKnight(state, player)
            and (
                state.has("Arbiters Grounds Small Key", player, 3)
                # Holdover from Keysy
                # or (
                #     state._tp_small_key_settings(player)
                #     == SmallKeySettings.option_anywhere
                # )
            )
        ),
    )
    set_rule_if_exists(
        "Arbiters Grounds Hidden Wall Poe",
        lambda state: (
            state.has("Shadow Crystal", player)
            and can_defeat_RedeadKnight(state, player)
            and (
                state.has("Arbiters Grounds Small Key", player, 3)
                # Holdover from Keysy
                # or (
                #     state._tp_small_key_settings(player)
                #     == SmallKeySettings.option_anywhere
                # )
            )
        ),
    )
    set_rule_if_exists(
        "Arbiters Grounds North Turning Room Chest",
        lambda state: (state.has("Progressive Clawshot", player, 1)),
    )
    set_rule_if_exists(
        "Arbiters Grounds Spinner Room First Small Chest",
        lambda state: (
            state.has("Progressive Clawshot", player, 1)
            and state.has("Spinner", player)
            and can_defeat_Bubble(state, player)
            and can_defeat_Stalfos(state, player)
            and (
                state.has("Arbiters Grounds Small Key", player, 5)
                # Holdover from Keysy
                # or (
                #     state._tp_small_key_settings(player)
                #     == SmallKeySettings.option_anywhere
                # )
            )
        ),
        lambda state: (
            state.has("Progressive Clawshot", player, 1)
            and state.has("Spinner", player)
            and can_defeat_Bubble(state, player)
            and can_defeat_Stalfos(state, player)
            and (
                (
                    state.has("Arbiters Grounds Small Key", player, 5)
                    # Holdover from Keysy
                    # or (
                    #     state._tp_small_key_settings(player)
                    #     == SmallKeySettings.option_anywhere
                    # )
                )
                or (
                    state.has("Arbiters Grounds Small Key", player, 4)
                    and state.has("Shadow Crystal", player)
                )
            )
        ),
    )
    set_rule_if_exists(
        "Arbiters Grounds Spinner Room Lower Central Small Chest",
        lambda state: (
            state.has("Progressive Clawshot", player, 1)
            and state.has("Spinner", player)
            and can_defeat_Bubble(state, player)
            and can_defeat_Stalfos(state, player)
            and (
                state.has("Arbiters Grounds Small Key", player, 5)
                # Holdover from Keysy
                # or (
                #     state._tp_small_key_settings(player)
                #     == SmallKeySettings.option_anywhere
                # )
            )
        ),
        lambda state: (
            state.has("Progressive Clawshot", player, 1)
            and state.has("Spinner", player)
            and can_defeat_Bubble(state, player)
            and can_defeat_Stalfos(state, player)
            and (
                (
                    state.has("Arbiters Grounds Small Key", player, 5)
                    # Holdover from Keysy
                    # or (
                    #     state._tp_small_key_settings(player)
                    #     == SmallKeySettings.option_anywhere
                    # )
                )
                or (
                    state.has("Arbiters Grounds Small Key", player, 4)
                    and state.has("Shadow Crystal", player)
                )
            )
        ),
    )
    set_rule_if_exists(
        "Arbiters Grounds Spinner Room Lower North Chest",
        lambda state: (
            state.has("Progressive Clawshot", player, 1)
            and state.has("Spinner", player)
            and can_defeat_Bubble(state, player)
            and can_defeat_Stalfos(state, player)
            and (
                state.has("Arbiters Grounds Small Key", player, 5)
                # Holdover from Keysy
                # or (
                #     state._tp_small_key_settings(player)
                #     == SmallKeySettings.option_anywhere
                # )
            )
        ),
        lambda state: (
            state.has("Progressive Clawshot", player, 1)
            and state.has("Spinner", player)
            and can_defeat_Bubble(state, player)
            and can_defeat_Stalfos(state, player)
            and (
                (
                    state.has("Arbiters Grounds Small Key", player, 5)
                    # Holdover from Keysy
                    # or (
                    #     state._tp_small_key_settings(player)
                    #     == SmallKeySettings.option_anywhere
                    # )
                )
                or (
                    state.has("Arbiters Grounds Small Key", player, 4)
                    and state.has("Shadow Crystal", player)
                )
            )
        ),
    )
    set_rule_if_exists(
        "Arbiters Grounds Spinner Room Second Small Chest",
        lambda state: (
            state.has("Progressive Clawshot", player, 1)
            and state.has("Spinner", player)
            and can_defeat_Bubble(state, player)
            and can_defeat_Stalfos(state, player)
            and (
                state.has("Arbiters Grounds Small Key", player, 5)
                # Holdover from Keysy
                # or (
                #     state._tp_small_key_settings(player)
                #     == SmallKeySettings.option_anywhere
                # )
            )
        ),
        lambda state: (
            state.has("Progressive Clawshot", player, 1)
            and state.has("Spinner", player)
            and can_defeat_Bubble(state, player)
            and can_defeat_Stalfos(state, player)
            and (
                (
                    state.has("Arbiters Grounds Small Key", player, 5)
                    # Holdover from Keysy
                    # or (
                    #     state._tp_small_key_settings(player)
                    #     == SmallKeySettings.option_anywhere
                    # )
                )
                or (
                    state.has("Arbiters Grounds Small Key", player, 4)
                    and state.has("Shadow Crystal", player)
                )
            )
        ),
    )
    set_rule_if_exists(
        "Arbiters Grounds Spinner Room Stalfos Alcove Chest",
        lambda state: (
            state.has("Progressive Clawshot", player, 1)
            and state.has("Spinner", player)
            and can_defeat_Bubble(state, player)
            and can_defeat_Stalfos(state, player)
            and (
                state.has("Arbiters Grounds Small Key", player, 5)
                # Holdover from Keysy
                # or (
                #     state._tp_small_key_settings(player)
                #     == SmallKeySettings.option_anywhere
                # )
            )
        ),
        lambda state: (
            state.has("Progressive Clawshot", player, 1)
            and state.has("Spinner", player)
            and can_defeat_Bubble(state, player)
            and can_defeat_Stalfos(state, player)
            and (
                (
                    state.has("Arbiters Grounds Small Key", player, 5)
                    # Holdover from Keysy
                    # or (
                    #     state._tp_small_key_settings(player)
                    #     == SmallKeySettings.option_anywhere
                    # )
                )
                or (
                    state.has("Arbiters Grounds Small Key", player, 4)
                    and state.has("Shadow Crystal", player)
                )
            )
        ),
    )
    set_rule_if_exists(
        "Arbiters Grounds Stallord Heart Container",
        lambda state: (can_defeat_Stallord(state, player)),
    )
    set_rule_if_exists("Arbiters Grounds Torch Room East Chest", lambda state: (True))
    set_rule_if_exists(
        "Arbiters Grounds Torch Room Poe",
        lambda state: (state.has("Shadow Crystal", player)),
    )
    set_rule_if_exists("Arbiters Grounds Torch Room West Chest", lambda state: (True))
    set_rule_if_exists(
        "Arbiters Grounds West Chandelier Chest",
        lambda state: (
            (
                state.has("Arbiters Grounds Small Key", player, 4)
                # Holdover from Keysy
                # or (
                #     state._tp_small_key_settings(player)
                #     == SmallKeySettings.option_anywhere
                # )
            )
            and state.has("Shadow Crystal", player)
        ),
        lambda state: (
            (
                (
                    state.has("Arbiters Grounds Small Key", player, 4)
                    # Holdover from Keysy
                    # or (
                    #     state._tp_small_key_settings(player)
                    #     == SmallKeySettings.option_anywhere
                    # )
                )
                and state.has("Shadow Crystal", player)
            )
            or can_do_lja(state, player)
        ),
    )
    set_rule_if_exists(
        "Arbiters Grounds West Poe",
        lambda state: (
            state.has("Shadow Crystal", player)
            and can_smash(state, player)
            and (
                state.has("Arbiters Grounds Small Key", player, 4)
                # Holdover from Keysy
                # or (
                #     state._tp_small_key_settings(player)
                #     == SmallKeySettings.option_anywhere
                # )
            )
            and can_defeat_RedeadKnight(state, player)
            and can_defeat_Stalchild(state, player)
            and can_defeat_Bubble(state, player)
            and can_defeat_GhoulRat(state, player)
        ),
        lambda state: (
            state.has("Shadow Crystal", player)
            and can_smash(state, player)
            and (
                (
                    (
                        state.has("Arbiters Grounds Small Key", player, 4)
                        # Holdover from Keysy
                        # or (
                        #     state._tp_small_key_settings(player)
                        #     == SmallKeySettings.option_anywhere
                        # )
                    )
                    and can_defeat_RedeadKnight(state, player)
                    and can_defeat_Stalchild(state, player)
                    and can_defeat_Bubble(state, player)
                    and can_defeat_GhoulRat(state, player)
                )
                or can_do_lja(state, player)
            )
        ),
    )
    set_rule_if_exists(
        "Arbiters Grounds West Small Chest Behind Block", lambda state: (True)
    )
    set_rule_if_exists(
        "Arbiters Grounds West Stalfos Northeast Chest",
        lambda state: (
            can_break_wooden_door(state, player)
            and (
                state.has("Arbiters Grounds Small Key", player, 4)
                # Holdover from Keysy
                # or (
                #     state._tp_small_key_settings(player)
                #     == SmallKeySettings.option_anywhere
                # )
            )
            and can_defeat_RedeadKnight(state, player)
            and can_defeat_Stalchild(state, player)
            and can_defeat_Bubble(state, player)
            and can_defeat_GhoulRat(state, player)
        ),
        lambda state: (
            can_break_wooden_door(state, player)
            and (
                (
                    (
                        state.has("Arbiters Grounds Small Key", player, 4)
                        # Holdover from Keysy
                        # or (
                        #     state._tp_small_key_settings(player)
                        #     == SmallKeySettings.option_anywhere
                        # )
                    )
                    and can_defeat_RedeadKnight(state, player)
                    and can_defeat_Stalchild(state, player)
                    and can_defeat_Bubble(state, player)
                    and can_defeat_GhoulRat(state, player)
                )
                or can_do_lja(state, player)
            )
        ),
    )
    set_rule_if_exists(
        "Arbiters Grounds West Stalfos West Chest",
        lambda state: (
            can_break_wooden_door(state, player)
            and (
                state.has("Arbiters Grounds Small Key", player, 4)
                # Holdover from Keysy
                # or (
                #     state._tp_small_key_settings(player)
                #     == SmallKeySettings.option_anywhere
                # )
            )
            and can_defeat_RedeadKnight(state, player)
            and can_defeat_Stalchild(state, player)
            and can_defeat_Bubble(state, player)
            and can_defeat_GhoulRat(state, player)
        ),
        lambda state: (
            can_break_wooden_door(state, player)
            and (
                (
                    (
                        state.has("Arbiters Grounds Small Key", player, 4)
                        # Holdover from Keysy
                        # or (
                        #     state._tp_small_key_settings(player)
                        #     == SmallKeySettings.option_anywhere
                        # )
                    )
                    and can_defeat_RedeadKnight(state, player)
                    and can_defeat_Stalchild(state, player)
                    and can_defeat_Bubble(state, player)
                    and can_defeat_GhoulRat(state, player)
                )
                or can_do_lja(state, player)
            )
        ),
    )
    set_rule_if_exists(
        "City in The Sky Aeralfos Chest",
        lambda state: (
            can_defeat_Aeralfos(state, player)
            and state.has("Progressive Clawshot", player, 1)
            and state.has("Iron Boots", player)
            and can_defeat_Dinalfos(state, player)
            and can_defeat_TileWorm(state, player)
        ),
        lambda state: (
            can_defeat_Aeralfos(state, player)
            and state.has("Progressive Clawshot", player, 1)
            and state.has("Iron Boots", player)
            and can_defeat_Dinalfos(state, player)
        ),
    )
    set_rule_if_exists(
        "City in The Sky Argorok Heart Container",
        lambda state: (can_defeat_Argorok(state, player)),
    )
    set_rule_if_exists(
        "City in The Sky Baba Tower Alcove Chest",
        lambda state: (
            can_defeat_BabaSerpent(state, player)
            and can_defeat_BigBaba(state, player)
            and state.has("Progressive Clawshot", player, 2)
        ),
    )
    set_rule_if_exists(
        "City in The Sky Baba Tower Narrow Ledge Chest",
        lambda state: (
            can_defeat_BabaSerpent(state, player)
            and can_defeat_BigBaba(state, player)
            and state.has("Progressive Clawshot", player, 2)
        ),
    )
    set_rule_if_exists(
        "City in The Sky Baba Tower Top Small Chest",
        lambda state: (
            can_defeat_BabaSerpent(state, player)
            and can_defeat_BigBaba(state, player)
            and state.has("Progressive Clawshot", player, 2)
        ),
    )
    set_rule_if_exists(
        "City in The Sky Big Key Chest",
        lambda state: (
            can_defeat_Dinalfos(state, player)
            and can_defeat_Walltula(state, player)
            and can_defeat_Kargarok(state, player)
            and state.has("Shadow Crystal", player)
            and state.has("Progressive Clawshot", player, 1)
            and state.has("Iron Boots", player)
        ),
        lambda state: (
            (
                can_defeat_Dinalfos(state, player)
                and can_defeat_Walltula(state, player)
                and can_defeat_Kargarok(state, player)
                and state.has("Shadow Crystal", player)
            )
            or state.has("Progressive Clawshot", player, 1)
        ),
    )
    set_rule_if_exists(
        "City in The Sky Central Outside Ledge Chest",
        lambda state: (
            can_defeat_Dinalfos(state, player)
            and can_defeat_Walltula(state, player)
            and can_defeat_Kargarok(state, player)
            and state.has("Shadow Crystal", player)
        ),
        lambda state: (
            (
                can_defeat_Dinalfos(state, player)
                and can_defeat_Walltula(state, player)
                and can_defeat_Kargarok(state, player)
                and state.has("Shadow Crystal", player)
            )
            or state.has("Progressive Clawshot", player, 1)
        ),
    )
    set_rule_if_exists(
        "City in The Sky Central Outside Poe Island Chest",
        lambda state: (
            can_defeat_Dinalfos(state, player)
            and can_defeat_Walltula(state, player)
            and can_defeat_Kargarok(state, player)
            and state.has("Shadow Crystal", player)
        ),
        lambda state: (
            (
                (
                    can_defeat_Dinalfos(state, player)
                    and can_defeat_Walltula(state, player)
                    and can_defeat_Kargarok(state, player)
                )
                or state.has("Progressive Clawshot", player, 1)
            )
            and state.has("Shadow Crystal", player)
        ),
    )
    set_rule_if_exists(
        "City in The Sky Chest Behind North Fan",
        lambda state: (state.has("Progressive Clawshot", player, 2)),
        lambda state: (state.has("Progressive Clawshot", player, 1)),
    )
    set_rule_if_exists(
        "City in The Sky Chest Below Big Key Chest",
        lambda state: (can_defeat_Helmasaur(state, player)),
    )
    set_rule_if_exists(
        "City in The Sky Dungeon Reward",
        lambda state: (can_defeat_Argorok(state, player)),
    )
    set_rule_if_exists(
        "City in The Sky East First Wing Chest After Fans",
        lambda state: (state.has("Progressive Clawshot", player, 1)),
        lambda state: (
            state.has("Progressive Clawshot", player, 1) or can_do_lja(state, player)
        ),
    )
    set_rule_if_exists(
        "City in The Sky East Tile Worm Small Chest",
        lambda state: (state.has("Progressive Clawshot", player, 1)),
        lambda state: (
            state.has("Progressive Clawshot", player, 1) or can_do_lja(state, player)
        ),
    )
    set_rule_if_exists(
        "City in The Sky East Wing After Dinalfos Alcove Chest",
        lambda state: (
            state.has("Progressive Clawshot", player, 1)
            and can_defeat_TileWorm(state, player)
            and can_defeat_Dinalfos(state, player)
        ),
        lambda state: (
            state.has("Progressive Clawshot", player, 1)
            and (
                (
                    can_defeat_TileWorm(state, player)
                    and can_defeat_Dinalfos(state, player)
                )
                or state.has("Iron Boots", player)
            )
        ),
    )
    set_rule_if_exists(
        "City in The Sky East Wing After Dinalfos Ledge Chest",
        lambda state: (
            state.has("Progressive Clawshot", player, 1)
            and can_defeat_TileWorm(state, player)
            and can_defeat_Dinalfos(state, player)
        ),
        lambda state: (
            state.has("Progressive Clawshot", player, 1)
            and (
                (
                    can_defeat_TileWorm(state, player)
                    and can_defeat_Dinalfos(state, player)
                )
                or state.has("Iron Boots", player)
            )
        ),
    )
    set_rule_if_exists(
        "City in The Sky East Wing Lower Level Chest",
        lambda state: (
            state.has("Progressive Clawshot", player, 2)
            and can_defeat_Dinalfos(state, player)
            and can_defeat_TileWorm(state, player)
        ),
        lambda state: (state.has("Progressive Clawshot", player, 2)),
    )
    set_rule_if_exists(
        "City in The Sky Garden Island Poe",
        lambda state: (
            state.has("Shadow Crystal", player)
            and state.has("Progressive Clawshot", player, 2)
        ),
    )
    set_rule_if_exists(
        "City in The Sky Poe Above Central Fan",
        lambda state: (
            state.has("Shadow Crystal", player) and can_defeat_Walltula(state, player)
        ),
    )
    set_rule_if_exists(
        "City in The Sky Underwater East Chest",
        lambda state: (state.has("Iron Boots", player)),
    )
    set_rule_if_exists(
        "City in The Sky Underwater West Chest",
        lambda state: (state.has("Iron Boots", player)),
    )
    set_rule_if_exists(
        "City in The Sky West Garden Corner Chest",
        lambda state: (state.has("Progressive Clawshot", player, 2)),
    )
    set_rule_if_exists(
        "City in The Sky West Garden Ledge Chest",
        lambda state: (state.has("Progressive Clawshot", player, 2)),
    )
    set_rule_if_exists(
        "City in The Sky West Garden Lone Island Chest",
        lambda state: (state.has("Progressive Clawshot", player, 2)),
    )
    set_rule_if_exists(
        "City in The Sky West Garden Lower Chest",
        lambda state: (state.has("Progressive Clawshot", player, 2)),
    )
    set_rule_if_exists(
        "City in The Sky West Wing Baba Balcony Chest",
        lambda state: (state.has("Progressive Clawshot", player, 2)),
    )
    set_rule_if_exists("City in The Sky West Wing First Chest", lambda state: (True))
    set_rule_if_exists(
        "City in The Sky West Wing Narrow Ledge Chest",
        lambda state: (state.has("Progressive Clawshot", player, 2)),
    )
    set_rule_if_exists(
        "City in The Sky West Wing Tile Worm Chest",
        lambda state: (state.has("Progressive Clawshot", player, 2)),
    )
    set_rule_if_exists(
        "Forest Temple Big Baba Key",
        lambda state: (
            can_defeat_BigBaba(state, player) and can_defeat_Walltula(state, player)
        ),
        lambda state: (can_defeat_BigBaba(state, player)),
    )
    set_rule_if_exists(
        "Forest Temple Big Key Chest",
        lambda state: (state.has("Gale Boomerang", player)),
    )
    set_rule_if_exists(
        "Forest Temple Central Chest Behind Stairs",
        lambda state: (state.has("Gale Boomerang", player)),
        lambda state: (
            state.has("Gale Boomerang", player)
            and (can_defeat_Bombling(state, player) or can_smash(state, player))
        ),
    )
    set_rule_if_exists(
        "Forest Temple Central Chest Hanging From Web",
        lambda state: (can_cut_hanging_web(state, player)),
        lambda state: (
            can_cut_hanging_web(state, player) or can_do_js_moon_boots(state, player)
        ),
    )
    set_rule_if_exists(
        "Forest Temple Central North Chest",
        lambda state: (state.has("Lantern", player)),
        lambda state: (
            state.has("Lantern", player)
            or (
                can_do_lja(state, player)
                and state.can_reach_region("Forest Temple West Wing", player)
            )
        ),
    )
    set_rule_if_exists(
        "Forest Temple Diababa Heart Container",
        lambda state: (can_defeat_Diababa(state, player)),
    )
    set_rule_if_exists(
        "Forest Temple Dungeon Reward",
        lambda state: (can_defeat_Diababa(state, player)),
    )
    set_rule_if_exists(
        "Forest Temple East Tile Worm Chest",
        lambda state: (
            can_defeat_TileWorm(state, player)
            and can_defeat_Skulltula(state, player)
            and can_defeat_Walltula(state, player)
            and state.has("Gale Boomerang", player)
            and (
                state.has("Forest Temple Small Key", player, 4)
                # Holdover from Keysy
                # or (
                #     state._tp_small_key_settings(player)
                #     == SmallKeySettings.option_anywhere
                # )
            )
        ),
        lambda state: (
            (
                has_bombs(state, player)
                or can_do_bs_moon_boots(state, player)
                or can_do_js_moon_boots(state, player)
                or state.has("Gale Boomerang", player)
            )
            and (
                state.has("Forest Temple Small Key", player, 4)
                # Holdover from Keysy
                # or (
                #     state._tp_small_key_settings(player)
                #     == SmallKeySettings.option_anywhere
                # )
            )
        ),
    )
    set_rule_if_exists("Forest Temple East Water Cave Chest", lambda state: (True))
    set_rule_if_exists(
        "Forest Temple Entrance Vines Chest",
        lambda state: (can_defeat_Walltula(state, player)),
    )
    set_rule_if_exists(
        "Forest Temple Gale Boomerang",
        lambda state: (can_defeat_Ook(state, player)),
        lambda state: (can_defeat_Ook(state, player) or has_bombs(state, player)),
    )
    set_rule_if_exists(
        "Forest Temple North Deku Like Chest",
        lambda state: (state.has("Gale Boomerang", player)),
        lambda state: (
            state.has("Gale Boomerang", player)
            or (
                has_bombs(state, player)
                and has_sword(state, player)
                and state.has("Progressive Clawshot", player, 1)
            )
        ),
    )
    set_rule_if_exists(
        "Forest Temple Second Monkey Under Bridge Chest",
        lambda state: (
            state.has("Forest Temple Small Key", player, 4)
            # Holdover from Keysy
            # or (
            #     state._tp_small_key_settings(player) == SmallKeySettings.option_anywhere
            # )
        ),
    )
    set_rule_if_exists(
        "Forest Temple Totem Pole Chest",
        lambda state: (True),
        lambda state: (can_defeat_Bombling(state, player) or can_smash(state, player)),
    )
    set_rule_if_exists(
        "Forest Temple West Deku Like Chest",
        lambda state: (can_defeat_Walltula(state, player)),
        lambda state: (True),
    )
    set_rule_if_exists(
        "Forest Temple West Tile Worm Chest Behind Stairs",
        lambda state: (state.has("Gale Boomerang", player)),
        lambda state: (
            state.has("Gale Boomerang", player)
            and (can_defeat_Bombling(state, player) or can_smash(state, player))
        ),
    )
    set_rule_if_exists(
        "Forest Temple West Tile Worm Room Vines Chest",
        lambda state: (True),
        lambda state: (can_defeat_Bombling(state, player) or can_smash(state, player)),
    )
    set_rule_if_exists("Forest Temple Windless Bridge Chest", lambda state: (True))
    set_rule_if_exists(
        "Goron Mines After Crystal Switch Room Magnet Wall Chest",
        lambda state: (state.has("Iron Boots", player)),
    )
    set_rule_if_exists(
        "Goron Mines Beamos Room Chest",
        lambda state: (
            state.has("Iron Boots", player)
            and can_defeat_Dangoro(state, player)
            and state.has("Progressive Hero's Bow", player, 1)
        ),
        lambda state: (
            state.has("Iron Boots", player)
            and can_defeat_Dangoro(state, player)
            and can_defeat_Beamos(state, player)
        ),
    )
    set_rule_if_exists(
        "Goron Mines Chest Before Dangoro",
        lambda state: (state.has("Iron Boots", player)),
        lambda state: (state.has("Iron Boots", player) or can_do_lja(state, player)),
    )
    set_rule_if_exists(
        "Goron Mines Crystal Switch Room Small Chest",
        lambda state: (state.has("Iron Boots", player)),
    )
    set_rule_if_exists(
        "Goron Mines Crystal Switch Room Underwater Chest",
        lambda state: (state.has("Iron Boots", player)),
        lambda state: (has_heavy_mod(state, player)),
    )
    set_rule_if_exists(
        "Goron Mines Dangoro Chest",
        lambda state: (
            state.has("Iron Boots", player) and can_defeat_Dangoro(state, player)
        ),
    )
    set_rule_if_exists(
        "Goron Mines Dungeon Reward",
        lambda state: (can_defeat_Fyrus(state, player)),
    )
    set_rule_if_exists(
        "Goron Mines Entrance Chest",
        lambda state: (
            can_press_mines_switch(state, player)
            and can_break_wooden_door(state, player)
        ),
        lambda state: (
            can_do_bs_moon_boots(state, player) or can_break_wooden_door(state, player)
        ),
    )
    set_rule_if_exists(
        "Goron Mines Fyrus Heart Container",
        lambda state: (can_defeat_Fyrus(state, player)),
    )
    set_rule_if_exists(
        "Goron Mines Gor Amato Chest",
        lambda state: (state.has("Iron Boots", player)),
    )
    set_rule_if_exists(
        "Goron Mines Gor Amato Key Shard",
        lambda state: (state.has("Iron Boots", player)),
    )
    set_rule_if_exists(
        "Goron Mines Gor Amato Small Chest",
        lambda state: (state.has("Iron Boots", player)),
    )
    set_rule_if_exists("Goron Mines Gor Ebizo Chest", lambda state: (True))
    set_rule_if_exists("Goron Mines Gor Ebizo Key Shard", lambda state: (True))
    set_rule_if_exists(
        "Goron Mines Gor Liggs Chest",
        lambda state: (
            state.has("Iron Boots", player)
            and can_defeat_Dangoro(state, player)
            and state.has("Progressive Hero's Bow", player, 1)
        ),
        lambda state: (
            state.has("Iron Boots", player)
            and can_defeat_Dangoro(state, player)
            and can_defeat_Beamos(state, player)
        ),
    )
    set_rule_if_exists(
        "Goron Mines Gor Liggs Key Shard",
        lambda state: (
            state.has("Iron Boots", player)
            and can_defeat_Dangoro(state, player)
            and state.has("Progressive Hero's Bow", player, 1)
        ),
        lambda state: (
            state.has("Iron Boots", player)
            and can_defeat_Dangoro(state, player)
            and can_defeat_Beamos(state, player)
        ),
    )
    set_rule_if_exists(
        "Goron Mines Magnet Maze Chest",
        lambda state: (state.has("Iron Boots", player)),
    )
    set_rule_if_exists(
        "Goron Mines Main Magnet Room Bottom Chest", lambda state: (True)
    )
    set_rule_if_exists(
        "Goron Mines Main Magnet Room Top Chest",
        lambda state: (
            state.has("Progressive Hero's Bow", player, 1)
            and state.has("Iron Boots", player)
            and can_defeat_Dangoro(state, player)
            and (
                state.has("Goron Mines Small Key", player, 3)
                # Holdover from Keysy
                # or (
                #     state._tp_small_key_settings(player)
                #     == SmallKeySettings.option_anywhere
                # )
            )
        ),
        lambda state: (
            state.can_reach_region("Goron Mines Upper East Wing", player)
            and can_defeat_Dangoro(state, player)
            and can_defeat_Beamos(state, player)
        ),
    )
    set_rule_if_exists("Goron Mines Outside Beamos Chest", lambda state: (True))
    set_rule_if_exists(
        "Goron Mines Outside Clawshot Chest",
        lambda state: (
            state.has("Progressive Clawshot", player, 1)
            and (
                state.has("Progressive Hero's Bow", player, 1)
                or state.has("Slingshot", player)
            )
        ),
        lambda state: (state.has("Progressive Clawshot", player, 1)),
    )
    set_rule_if_exists(
        "Goron Mines Outside Underwater Chest",
        lambda state: (
            (has_sword(state, player) or can_use_water_bombs(state, player))
            and state.has("Iron Boots", player)
        ),
        lambda state: (has_heavy_mod(state, player)),
    )
    set_rule_if_exists("Hyrule Castle Big Key Chest", lambda state: (True))
    set_rule_if_exists(
        "Hyrule Castle East Wing Balcony Chest",
        lambda state: (state.has("Gale Boomerang", player)),
    )
    set_rule_if_exists(
        "Hyrule Castle East Wing Boomerang Puzzle Chest",
        lambda state: (state.has("Gale Boomerang", player)),
    )
    set_rule_if_exists(
        "Hyrule Castle Ganondorf", lambda state: (can_defeat_Ganondorf(state, player))
    )  # Technically reduntent
    set_rule_if_exists(
        "Hyrule Castle Graveyard Grave Switch Room Back Left Chest",
        lambda state: (can_smash(state, player)),
    )
    set_rule_if_exists(
        "Hyrule Castle Graveyard Grave Switch Room Front Left Chest",
        lambda state: (can_smash(state, player)),
    )
    set_rule_if_exists(
        "Hyrule Castle Graveyard Grave Switch Room Right Chest",
        lambda state: (can_smash(state, player)),
    )
    set_rule_if_exists(
        "Hyrule Castle Graveyard Owl Statue Chest",
        lambda state: (
            can_smash(state, player)
            and state.has("Lantern", player)
            and state.has("Progressive Dominion Rod", player, 2)
        ),
    )
    set_rule_if_exists(
        "Hyrule Castle King Bulblin Key",
        lambda state: (can_defeat_KingBulblinCastle(state, player)),
    )
    set_rule_if_exists(
        "Hyrule Castle Lantern Staircase Chest",
        lambda state: (
            can_defeat_Darknut(state, player)
            and state.has("Gale Boomerang", player)
            and can_defeat_Bokoblin(state, player)
            and can_defeat_Lizalfos(state, player)
            and state.has("Progressive Clawshot", player, 2)
        ),
        lambda state: (
            can_defeat_Darknut(state, player)
            and state.has("Gale Boomerang", player)
            and can_defeat_Bokoblin(state, player)
            and can_defeat_Lizalfos(state, player)
            and state.has("Progressive Clawshot", player)
        ),
    )
    set_rule_if_exists(
        "Hyrule Castle Main Hall Northeast Chest",
        lambda state: (
            can_defeat_Bokoblin(state, player)
            and can_defeat_Lizalfos(state, player)
            and state.has("Progressive Clawshot", player, 1)
        ),
        lambda state: (
            can_defeat_Bokoblin(state, player)
            and can_defeat_Lizalfos(state, player)
            and state.has("Progressive Clawshot", player)
        ),
    )
    set_rule_if_exists(
        "Hyrule Castle Main Hall Northwest Chest",
        lambda state: (
            can_knock_down_hc_painting(state, player)
            and can_defeat_Lizalfos(state, player)
            and can_defeat_Darknut(state, player)
            and state.has("Gale Boomerang", player)
            and state.has("Lantern", player)
            and state.has("Progressive Clawshot", player, 2)
        ),
        lambda state: (
            (
                can_knock_down_hc_painting(state, player)
                and can_defeat_Lizalfos(state, player)
                and can_defeat_Darknut(state, player)
                and state.has("Gale Boomerang", player)
                and state.has("Lantern", player)
                and state.has("Progressive Clawshot", player, 1)
            )
            or state.has("Progressive Clawshot", player, 2)
        ),
    )
    set_rule_if_exists(
        "Hyrule Castle Main Hall Southwest Chest",
        lambda state: (
            can_knock_down_hc_painting(state, player)
            and can_defeat_Lizalfos(state, player)
            and can_defeat_Darknut(state, player)
            and state.has("Gale Boomerang", player)
            and state.has("Lantern", player)
            and state.has("Progressive Clawshot", player, 2)
        ),
        lambda state: (
            (
                can_knock_down_hc_painting(state, player)
                and can_defeat_Lizalfos(state, player)
                and can_defeat_Darknut(state, player)
                and state.has("Gale Boomerang", player)
                and state.has("Lantern", player)
                and state.has("Progressive Clawshot", player, 1)
            )
            or state.has("Progressive Clawshot", player, 2)
        ),
    )
    set_rule_if_exists(
        "Hyrule Castle Southeast Balcony Tower Chest",
        lambda state: (can_defeat_Aeralfos(state, player)),
    )
    set_rule_if_exists(
        "Hyrule Castle Treasure Room Eighth Small Chest", lambda state: (True)
    )
    set_rule_if_exists("Hyrule Castle Treasure Room Fifth Chest", lambda state: (True))
    set_rule_if_exists(
        "Hyrule Castle Treasure Room Fifth Small Chest", lambda state: (True)
    )
    set_rule_if_exists("Hyrule Castle Treasure Room First Chest", lambda state: (True))
    set_rule_if_exists(
        "Hyrule Castle Treasure Room First Small Chest", lambda state: (True)
    )
    set_rule_if_exists("Hyrule Castle Treasure Room Fourth Chest", lambda state: (True))
    set_rule_if_exists(
        "Hyrule Castle Treasure Room Fourth Small Chest", lambda state: (True)
    )
    set_rule_if_exists("Hyrule Castle Treasure Room Second Chest", lambda state: (True))
    set_rule_if_exists(
        "Hyrule Castle Treasure Room Second Small Chest", lambda state: (True)
    )
    set_rule_if_exists(
        "Hyrule Castle Treasure Room Seventh Small Chest", lambda state: (True)
    )
    set_rule_if_exists(
        "Hyrule Castle Treasure Room Sixth Small Chest", lambda state: (True)
    )
    set_rule_if_exists("Hyrule Castle Treasure Room Third Chest", lambda state: (True))
    set_rule_if_exists(
        "Hyrule Castle Treasure Room Third Small Chest", lambda state: (True)
    )
    set_rule_if_exists(
        "Hyrule Castle West Courtyard Central Small Chest",
        lambda state: (can_defeat_Bokoblin(state, player)),
        lambda state: (True),
    )
    set_rule_if_exists(
        "Hyrule Castle West Courtyard North Small Chest",
        lambda state: (can_defeat_Bokoblin(state, player)),
        lambda state: (True),
    )
    set_rule_if_exists(
        "Lakebed Temple Before Deku Toad Alcove Chest",
        lambda state: (
            (
                (
                    state._tp_small_key_settings(player)
                    == SmallKeySettings.option_vanilla
                )
                and can_defeat_DekuToad(state, player)
                and state.has("Lakebed Temple Small Key", player, 2)
                and state.has("Zora Armor", player)
                and state.has("Iron Boots", player)
                and can_use_water_bombs(state, player)
                and state.has("Progressive Clawshot", player, 1)
            )
            or (
                (
                    state.has("Lakebed Temple Small Key", player, 3)
                    # Holdover from Keysy
                    # or (
                    #     state._tp_small_key_settings(player)
                    #     == SmallKeySettings.option_anywhere
                    # )
                )
                and (
                    can_launch_bombs(state, player)
                    or (
                        state.has("Progressive Clawshot", player, 1)
                        and can_smash(state, player)
                    )
                )
            )
        ),
        lambda state: (
            can_do_lja(state, player)
            or (
                (
                    state.has("Lakebed Temple Small Key", player, 2)
                    # Holdover from Keysy
                    # or (
                    #     state._tp_small_key_settings(player)
                    #     == SmallKeySettings.option_anywhere
                    # )
                )
                and (
                    can_launch_bombs(state, player)
                    or state.has("Progressive Clawshot", player, 1)
                )
            )
        ),
    )
    set_rule_if_exists(
        "Lakebed Temple Before Deku Toad Underwater Left Chest",
        lambda state: (
            state.has("Zora Armor", player)
            and state.has("Iron Boots", player)
            and (
                state.has("Lakebed Temple Small Key", player, 3)
                # Holdover from Keysy
                # or (
                #     state._tp_small_key_settings(player)
                #     == SmallKeySettings.option_anywhere
                # )
            )
            and (
                can_launch_bombs(state, player)
                or (
                    state.has("Progressive Clawshot", player, 1)
                    and can_smash(state, player)
                )
            )
        ),
        lambda state: (
            (
                (
                    can_do_lja(state, player)
                    and (
                        can_skip_key_to_deku_toad(state, player)
                        or state.has("Lakebed Temple Small Key", player, 1)
                    )
                )
            )
            or (
                (
                    can_skip_key_to_deku_toad(state, player)
                    or state.has("Lakebed Temple Small Key", player, 3)
                )
                and state.has("Progressive Clawshot", player, 1)
                and can_launch_bombs(state, player)
            )
            and has_heavy_mod(state, player)
        ),
    )
    set_rule_if_exists(
        "Lakebed Temple Before Deku Toad Underwater Right Chest",
        lambda state: (
            state.has("Zora Armor", player)
            and state.has("Iron Boots", player)
            and (
                state.has("Lakebed Temple Small Key", player, 3)
                # Holdover from Keysy
                # or (
                #     state._tp_small_key_settings(player)
                #     == SmallKeySettings.option_anywhere
                # )
            )
            and (
                can_launch_bombs(state, player)
                or (
                    state.has("Progressive Clawshot", player, 1)
                    and can_smash(state, player)
                )
            )
        ),
        lambda state: (
            (
                (
                    can_do_lja(state, player)
                    and (
                        can_skip_key_to_deku_toad(state, player)
                        or state.has("Lakebed Temple Small Key", player, 1)
                    )
                )
            )
            or (
                (
                    can_skip_key_to_deku_toad(state, player)
                    or state.has("Lakebed Temple Small Key", player, 3)
                )
                and state.has("Progressive Clawshot", player, 1)
                and can_launch_bombs(state, player)
            )
            and has_heavy_mod(state, player)
        ),
    )
    set_rule_if_exists(
        "Lakebed Temple Big Key Chest",
        lambda state: (
            state.has("Progressive Clawshot", player, 1)
            and can_use_water_bombs(state, player)
            and state.has("Zora Armor", player)
            and can_launch_bombs(state, player)
            and state.has("Iron Boots", player)
        ),
        lambda state: (
            state.has("Progressive Clawshot", player, 1)
            and (state.has("Zora Armor", player) or can_do_lja(state, player))
            and can_launch_bombs(state, player)
        ),
    )
    set_rule_if_exists("Lakebed Temple Central Room Chest", lambda state: (True))
    set_rule_if_exists("Lakebed Temple Central Room Small Chest", lambda state: (True))
    set_rule_if_exists(
        "Lakebed Temple Central Room Spire Chest",
        lambda state: (
            (
                state.has("Lakebed Temple Small Key", player, 3)
                # Holdover from Keysy
                # or (
                #     state._tp_small_key_settings(player)
                #     == SmallKeySettings.option_anywhere
                # )
            )
            and state.has("Iron Boots", player)
            and can_launch_bombs(state, player)
        ),
        lambda state: (
            (
                (
                    (
                        state.has("Lakebed Temple Small Key", player, 3)
                        # Holdover from Keysy
                        # or (
                        #     state._tp_small_key_settings(player)
                        #     == SmallKeySettings.option_anywhere
                        # )
                    )
                    and can_launch_bombs(state, player)
                )
                or (
                    state.has("Progressive Clawshot", player)
                    and has_sword(state, player)
                )
            )
            and state.has("Iron Boots", player)
        ),
    )
    set_rule_if_exists(
        "Lakebed Temple Chandelier Chest",
        lambda state: (state.has("Progressive Clawshot", player, 1)),
    )
    set_rule_if_exists(
        "Lakebed Temple Deku Toad Chest",
        lambda state: (
            can_defeat_DekuToad(state, player)
            and (
                state.has("Lakebed Temple Small Key", player, 3)
                # Holdover from Keysy
                # or (
                #     state._tp_small_key_settings(player)
                #     == SmallKeySettings.option_anywhere
                # )
            )
            and state.has("Zora Armor", player)
            and state.has("Iron Boots", player)
            and can_use_water_bombs(state, player)
            and (
                can_launch_bombs(state, player)
                or (
                    state.has("Progressive Clawshot", player, 1)
                    and can_smash(state, player)
                )
            )
        ),
        lambda state: (
            can_defeat_DekuToad(state, player)
            and (
                (
                    (
                        can_do_lja(state, player)
                        and (
                            can_skip_key_to_deku_toad(state, player)
                            or state.has("Lakebed Temple Small Key", player, 1)
                        )
                    )
                )
                or (
                    (
                        can_skip_key_to_deku_toad(state, player)
                        or state.has("Lakebed Temple Small Key", player, 3)
                    )
                    and state.has("Progressive Clawshot", player, 1)
                    and can_launch_bombs(state, player)
                )
            )
            and has_heavy_mod(state, player)
            and (can_use_water_bombs(state, player) or state.has("Zora Armor", player))
        ),
    )
    set_rule_if_exists(
        "Lakebed Temple Dungeon Reward",
        lambda state: (can_defeat_Morpheel(state, player)),
    )
    set_rule_if_exists(
        "Lakebed Temple East Lower Waterwheel Bridge Chest",
        lambda state: (
            state.has("Progressive Clawshot", player, 1)
            and (
                state.has("Lakebed Temple Small Key", player, 3)
                # Holdover from Keysy
                # or (
                #     state._tp_small_key_settings(player)
                #     == SmallKeySettings.option_anywhere
                # )
            )
            and can_launch_bombs(state, player)
        ),
        lambda state: (
            can_do_lja(state, player)
            or (
                state.has("Progressive Clawshot", player, 1)
                and has_bombs(state, player)
            )
            or (
                state.can_reach_region("Lakebed Temple East Wing Second Floor", player)
                and (
                    state.has("Progressive Clawshot", player, 1)
                    or can_launch_bombs(state, player)
                )
                and (
                    (
                        state.has("Shadow Crystal", player)
                        or (has_bombs(state, player) and has_sword(state, player))
                    )
                )
            )
            or (
                state.can_reach_region("Lakebed Temple West Wing", player)
                and can_launch_bombs(state, player)
            )
        ),
    )
    set_rule_if_exists(
        "Lakebed Temple East Lower Waterwheel Stalactite Chest",
        lambda state: (can_launch_bombs(state, player)),
        lambda state: (can_launch_bombs(state, player) or can_do_lja(state, player)),
    )
    set_rule_if_exists(
        "Lakebed Temple East Second Floor Southeast Chest",
        lambda state: (
            can_launch_bombs(state, player)
            or (
                state.has("Progressive Clawshot", player, 1)
                and can_smash(state, player)
            )
        ),
    )
    set_rule_if_exists(
        "Lakebed Temple East Second Floor Southwest Chest", lambda state: (True)
    )
    set_rule_if_exists(
        "Lakebed Temple East Water Supply Clawshot Chest",
        lambda state: (
            (
                state.has("Lakebed Temple Small Key", player, 3)
                # Holdover from Keysy
                # or (
                #     state._tp_small_key_settings(player)
                #     == SmallKeySettings.option_anywhere
                # )
            )
            and state.has("Progressive Clawshot", player, 1)
            and can_smash(state, player)
            and state.has("Iron Boots", player)
        ),
        lambda state: (
            (
                state.has("Lakebed Temple Small Key", player, 3)
                # Holdover from Keysy
                # or (
                #     state._tp_small_key_settings(player)
                #     == SmallKeySettings.option_anywhere
                # )
            )
            and state.has("Progressive Clawshot", player, 1)
            and can_smash(state, player)
        ),
    )
    set_rule_if_exists(
        "Lakebed Temple East Water Supply Small Chest",
        lambda state: (
            (
                state.has("Lakebed Temple Small Key", player, 3)
                # Holdover from Keysy
                # or (
                #     state._tp_small_key_settings(player)
                #     == SmallKeySettings.option_anywhere
                # )
            )
            and (
                state.has("Progressive Clawshot", player, 1)
                or can_launch_bombs(state, player)
            )
            and can_smash(state, player)
            and state.has("Iron Boots", player)
        ),
        lambda state: (
            (
                state.has("Lakebed Temple Small Key", player, 3)
                # Holdover from Keysy
                # or (
                #     state._tp_small_key_settings(player)
                #     == SmallKeySettings.option_anywhere
                # )
            )
            and (
                can_launch_bombs(state, player)
                or (
                    state.has("Progressive Clawshot", player)
                    and can_smash(state, player)
                )
            )
        ),
    )
    set_rule_if_exists(
        "Lakebed Temple Lobby Left Chest",
        lambda state: (state.has("Zora Armor", player)),
        lambda state: (
            state.has("Zora Armor", player) or can_do_air_refill(state, player)
        ),
    )
    set_rule_if_exists(
        "Lakebed Temple Lobby Rear Chest",
        lambda state: (state.has("Zora Armor", player)),
        lambda state: (
            state.has("Zora Armor", player) or can_do_air_refill(state, player)
        ),
    )
    set_rule_if_exists(
        "Lakebed Temple Morpheel Heart Container",
        lambda state: (can_defeat_Morpheel(state, player)),
    )
    set_rule_if_exists(
        "Lakebed Temple Stalactite Room Chest",
        lambda state: (can_launch_bombs(state, player)),
        lambda state: (can_launch_bombs(state, player) or can_do_lja(state, player)),
    )
    set_rule_if_exists(
        "Lakebed Temple Underwater Maze Small Chest",
        lambda state: (
            state.has("Zora Armor", player)
            and state.has("Progressive Clawshot", player, 1)
            and can_launch_bombs(state, player)
        ),
        lambda state: (
            state.has("Progressive Clawshot", player, 1)
            and (state.has("Zora Armor", player) or can_do_lja(state, player))
            and can_launch_bombs(state, player)
        ),
    )
    set_rule_if_exists(
        "Lakebed Temple West Lower Small Chest",
        lambda state: (state.has("Progressive Clawshot", player, 1)),
        lambda state: (
            state.has("Progressive Clawshot", player, 1) or can_do_lja(state, player)
        ),
    )
    set_rule_if_exists(
        "Lakebed Temple West Second Floor Central Small Chest",
        lambda state: (state.has("Progressive Clawshot", player, 1)),
    )
    set_rule_if_exists(
        "Lakebed Temple West Second Floor Northeast Chest",
        lambda state: (
            state.has("Progressive Clawshot", player, 1)
            and can_launch_bombs(state, player)
        ),
    )
    set_rule_if_exists(
        "Lakebed Temple West Second Floor Southeast Chest",
        lambda state: (
            state.has("Progressive Clawshot", player, 1)
            and can_launch_bombs(state, player)
        ),
    )
    set_rule_if_exists(
        "Lakebed Temple West Second Floor Southwest Underwater Chest",
        lambda state: (
            state.has("Progressive Clawshot", player, 1)
            and state.has("Iron Boots", player)
            and can_launch_bombs(state, player)
        ),
    )
    set_rule_if_exists(
        "Lakebed Temple West Water Supply Chest",
        lambda state: (
            state.has("Progressive Clawshot", player, 1)
            and can_launch_bombs(state, player)
            and state.has("Iron Boots", player)
        ),
        lambda state: (
            state.has("Progressive Clawshot", player, 1)
            and can_launch_bombs(state, player)
        ),
    )
    set_rule_if_exists(
        "Lakebed Temple West Water Supply Small Chest",
        lambda state: (
            state.has("Progressive Clawshot", player, 1)
            and can_launch_bombs(state, player)
            and state.has("Iron Boots", player)
        ),
        lambda state: (
            state.has("Progressive Clawshot", player, 1)
            and can_launch_bombs(state, player)
        ),
    )
    set_rule_if_exists(
        "Palace of Twilight Big Key Chest",
        lambda state: (
            state.has("Progressive Master Sword", player, 4)
            and state.has("Progressive Clawshot", player, 2)
            and can_defeat_ZantHead(state, player)
        ),
    )
    set_rule_if_exists(
        "Palace of Twilight Central First Room Chest",
        lambda state: (
            can_defeat_ZantHead(state, player)
            and state.has("Progressive Master Sword", player, 4)
        ),
    )
    set_rule_if_exists(
        "Palace of Twilight Central Outdoor Chest",
        lambda state: (can_defeat_ZantHead(state, player)),
    )
    set_rule_if_exists(
        "Palace of Twilight Central Tower Chest",
        lambda state: (
            can_defeat_ZantHead(state, player)
            and state.has("Progressive Master Sword", player, 4)
            and state.has("Progressive Clawshot", player, 1)
        ),
    )
    set_rule_if_exists(
        "Palace of Twilight Collect Both Sols",
        lambda state: (
            can_defeat_PhantomZant(state, player)
            and state.has("Progressive Clawshot", player, 1)
            and can_defeat_ZantHead(state, player)
            and (
                state.has("Palace of Twilight Small Key", player, 7)
                # Holdover from Keysy
                # or (
                #     state._tp_small_key_settings(player)
                #     == SmallKeySettings.option_anywhere
                # )
            )
            and can_defeat_ShadowBeast(state, player)
        ),
    )
    set_rule_if_exists(
        "Palace of Twilight East Wing First Room East Alcove Chest",
        lambda state: (
            state.has("Progressive Master Sword", player, 4)
            or (
                can_defeat_PhantomZant(state, player)
                and state.has("Progressive Clawshot", player, 1)
                and can_defeat_ZantHead(state, player)
                and (
                    state.has("Palace of Twilight Small Key", player, 6)
                    # Holdover from Keysy
                    # or (
                    #     state._tp_small_key_settings(player)
                    #     == SmallKeySettings.option_anywhere
                    # )
                )
                and can_defeat_ShadowBeast(state, player)
            )
        ),
    )
    set_rule_if_exists(
        "Palace of Twilight East Wing First Room North Small Chest",
        lambda state: (state.has("Progressive Clawshot", player, 1)),
    )
    set_rule_if_exists(
        "Palace of Twilight East Wing First Room West Alcove Chest",
        lambda state: (
            state.has("Progressive Master Sword", player, 4)
            or (
                can_defeat_PhantomZant(state, player)
                and state.has("Progressive Clawshot", player, 1)
                and can_defeat_ZantHead(state, player)
                and (
                    state.has("Palace of Twilight Small Key", player, 6)
                    # Holdover from Keysy
                    # or (
                    #     state._tp_small_key_settings(player)
                    #     == SmallKeySettings.option_anywhere
                    # )
                )
                and can_defeat_ShadowBeast(state, player)
            )
        ),
    )
    set_rule_if_exists(
        "Palace of Twilight East Wing First Room Zant Head Chest",
        lambda state: (
            can_defeat_ZantHead(state, player)
            and state.has("Progressive Clawshot", player, 1)
        ),
    )
    set_rule_if_exists(
        "Palace of Twilight East Wing Second Room Northeast Chest",
        lambda state: (
            can_defeat_ZantHead(state, player)
            and can_defeat_ShadowBeast(state, player)
            and state.has("Progressive Clawshot", player, 2)
            and (
                (
                    (
                        state.has("Palace of Twilight Small Key", player, 6)
                        or (
                            (
                                state._tp_small_key_settings(player)
                                == SmallKeySettings.option_vanilla
                            )
                            and state.has("Palace of Twilight Small Key", player, 3)
                        )
                    )
                    # Holdover from Keysy
                    # or (
                    #     state._tp_small_key_settings(player)
                    #     == SmallKeySettings.option_anywhere
                    # )
                )
            )
        ),
    )
    set_rule_if_exists(
        "Palace of Twilight East Wing Second Room Northwest Chest",
        lambda state: (
            can_defeat_ZantHead(state, player)
            and can_defeat_ShadowBeast(state, player)
            and state.has("Progressive Clawshot", player, 1)
            and (
                (
                    (
                        state.has("Palace of Twilight Small Key", player, 6)
                        or (
                            (
                                state._tp_small_key_settings(player)
                                == SmallKeySettings.option_vanilla
                            )
                            and state.has("Palace of Twilight Small Key", player, 3)
                        )
                    )
                    # Holdover from Keysy
                    # or (
                    #     state._tp_small_key_settings(player)
                    #     == SmallKeySettings.option_anywhere
                    # )
                )
            )
        ),
    )
    set_rule_if_exists(
        "Palace of Twilight East Wing Second Room Southeast Chest",
        lambda state: (
            can_defeat_ZantHead(state, player)
            and can_defeat_ShadowBeast(state, player)
            and state.has("Progressive Clawshot", player, 2)
            and (
                (
                    (
                        state.has("Palace of Twilight Small Key", player, 6)
                        or (
                            (
                                state._tp_small_key_settings(player)
                                == SmallKeySettings.option_vanilla
                            )
                            and state.has("Palace of Twilight Small Key", player, 3)
                        )
                    )
                    # Holdover from Keysy
                    # or (
                    #     state._tp_small_key_settings(player)
                    #     == SmallKeySettings.option_anywhere
                    # )
                )
            )
        ),
    )
    set_rule_if_exists(
        "Palace of Twilight East Wing Second Room Southwest Chest",
        lambda state: (
            can_defeat_ZantHead(state, player)
            and can_defeat_ShadowBeast(state, player)
            and state.has("Progressive Clawshot", player, 2)
            and (
                (
                    (
                        state.has("Palace of Twilight Small Key", player, 6)
                        or (
                            (
                                state._tp_small_key_settings(player)
                                == SmallKeySettings.option_vanilla
                            )
                            and state.has("Palace of Twilight Small Key", player, 3)
                        )
                    )
                    # Holdover from Keysy
                    # or (
                    #     state._tp_small_key_settings(player)
                    #     == SmallKeySettings.option_anywhere
                    # )
                )
            )
        ),
    )
    set_rule_if_exists(
        "Palace of Twilight West Wing Chest Behind Wall of Darkness",
        lambda state: (
            state.has("Progressive Master Sword", player, 4)
            and state.has("Progressive Clawshot", player, 1)
        ),
    )
    set_rule_if_exists(
        "Palace of Twilight West Wing First Room Central Chest",
        lambda state: (can_defeat_ZantHead(state, player)),
    )
    set_rule_if_exists(
        "Palace of Twilight West Wing Second Room Central Chest",
        lambda state: (
            (
                (
                    (
                        state.has("Palace of Twilight Small Key", player, 6)
                        or (
                            (
                                state._tp_small_key_settings(player)
                                == SmallKeySettings.option_vanilla
                            )
                            and state.has("Palace of Twilight Small Key", player, 3)
                        )
                    )
                    # Holdover from Keysy
                    # or (
                    #     state._tp_small_key_settings(player)
                    #     == SmallKeySettings.option_anywhere
                    # )
                )
            )
            and can_defeat_ZantHead(state, player)
            and state.has("Progressive Clawshot", player, 1)
        ),
    )
    set_rule_if_exists(
        "Palace of Twilight West Wing Second Room Lower South Chest",
        lambda state: (
            (
                (
                    (
                        state.has("Palace of Twilight Small Key", player, 6)
                        or (
                            (
                                state._tp_small_key_settings(player)
                                == SmallKeySettings.option_vanilla
                            )
                            and state.has("Palace of Twilight Small Key", player, 3)
                        )
                    )
                    # Holdover from Keysy
                    # or (
                    #     state._tp_small_key_settings(player)
                    #     == SmallKeySettings.option_anywhere
                    # )
                )
            )
            and can_defeat_ZantHead(state, player)
            and state.has("Progressive Clawshot", player, 1)
        ),
    )
    set_rule_if_exists(
        "Palace of Twilight West Wing Second Room Southeast Chest",
        lambda state: (
            (
                (
                    (
                        state.has("Palace of Twilight Small Key", player, 6)
                        or (
                            (
                                state._tp_small_key_settings(player)
                                == SmallKeySettings.option_vanilla
                            )
                            and state.has("Palace of Twilight Small Key", player, 3)
                        )
                    )
                    # Holdover from Keysy
                    # or (
                    #     state._tp_small_key_settings(player)
                    #     == SmallKeySettings.option_anywhere
                    # )
                )
            )
            and can_defeat_ZantHead(state, player)
            and state.has("Progressive Clawshot", player, 2)
        ),
    )
    set_rule_if_exists(
        "Palace of Twilight Zant Heart Container",
        lambda state: (can_defeat_Zant(state, player)),
    )
    set_rule_if_exists(
        "Snowpeak Ruins Ball and Chain",
        lambda state: (can_defeat_Darkhammer(state, player)),
    )
    set_rule_if_exists(
        "Snowpeak Ruins Blizzeta Heart Container",
        lambda state: (can_defeat_Blizzeta(state, player)),
    )
    set_rule_if_exists(
        "Snowpeak Ruins Broken Floor Chest",
        lambda state: (state.has("Ball and Chain", player)),
    )
    set_rule_if_exists(
        "Snowpeak Ruins Chapel Chest",
        lambda state: (can_defeat_Chilfos(state, player)),
    )
    set_rule_if_exists(
        "Snowpeak Ruins Chest After Darkhammer",
        lambda state: (
            can_defeat_Darkhammer(state, player) and state.has("Ball and Chain", player)
        ),
    )
    set_rule_if_exists(
        "Snowpeak Ruins Courtyard Central Chest",
        lambda state: (
            state.has("Ball and Chain", player)
            or (
                has_bombs(state, player)
                and (
                    (
                        state.has("Snowpeak Ruins Small Key", player, 2)
                        or state.has("Ordon Goat Cheese", player)
                    )
                    # Holdover from Keysy
                    # or (
                    #     state._tp_small_key_settings(player)
                    #     == SmallKeySettings.option_anywhere
                    # )
                )
            )
        ),
        lambda state: (
            state.has("Ball and Chain", player)
            or (
                has_bombs(state, player)
                and (
                    state.has("Snowpeak Ruins Small Key", player, 2)
                    # Holdover from Keysy
                    # or (
                    #     state._tp_small_key_settings(player)
                    #     == SmallKeySettings.option_anywhere
                    # )
                )
            )
        ),
    )
    set_rule_if_exists(
        "Snowpeak Ruins Dungeon Reward",
        lambda state: (can_defeat_Blizzeta(state, player)),
    )
    set_rule_if_exists(
        "Snowpeak Ruins East Courtyard Buried Chest",
        lambda state: (state.has("Shadow Crystal", player)),
    )
    set_rule_if_exists("Snowpeak Ruins East Courtyard Chest", lambda state: (True))
    set_rule_if_exists(
        "Snowpeak Ruins Ice Room Poe",
        lambda state: (state.has("Shadow Crystal", player)),
    )
    set_rule_if_exists(
        "Snowpeak Ruins Lobby Armor Poe",
        lambda state: (
            state.has("Shadow Crystal", player) and state.has("Ball and Chain", player)
        ),
    )
    set_rule_if_exists(
        "Snowpeak Ruins Lobby Chandelier Chest",
        lambda state: (
            (
                (
                    state.has("Snowpeak Ruins Small Key", player, 3)
                    and state.has("Ordon Goat Cheese", player)
                )
                # Holdover from Keysy
                # or (
                #     state._tp_small_key_settings(player)
                #     == SmallKeySettings.option_anywhere
                # )
            )
            and state.has("Ball and Chain", player)
        ),
        lambda state: (
            (
                (
                    (
                        state.has("Snowpeak Ruins Small Key", player, 3)
                        and state.has("Ordon Goat Cheese", player)
                    )
                    # Holdover from Keysy
                    # or (
                    #     state._tp_small_key_settings(player)
                    #     == SmallKeySettings.option_anywhere
                    # )
                )
                and state.has("Ball and Chain", player)
            )
            or (state.has("Shadow Crystal", player) and can_do_lja(state, player))
        ),
    )
    set_rule_if_exists(
        "Snowpeak Ruins Lobby East Armor Chest",
        lambda state: (state.has("Ball and Chain", player)),
    )
    set_rule_if_exists(
        "Snowpeak Ruins Lobby Poe",
        lambda state: (state.has("Shadow Crystal", player)),
    )
    set_rule_if_exists(
        "Snowpeak Ruins Lobby West Armor Chest",
        lambda state: (state.has("Ball and Chain", player)),
    )
    set_rule_if_exists("Snowpeak Ruins Mansion Map", lambda state: (True))
    set_rule_if_exists(
        "Snowpeak Ruins Northeast Chandelier Chest",
        lambda state: (
            can_defeat_Chilfos(state, player) and state.has("Ball and Chain", player)
        ),
    )
    set_rule_if_exists(
        "Snowpeak Ruins Ordon Pumpkin Chest",
        lambda state: (can_defeat_Chilfos(state, player)),
    )
    set_rule_if_exists(
        "Snowpeak Ruins West Cannon Room Central Chest",
        lambda state: (state.has("Ball and Chain", player)),
    )
    set_rule_if_exists(
        "Snowpeak Ruins West Cannon Room Corner Chest",
        lambda state: (can_smash(state, player)),
    )
    set_rule_if_exists(
        "Snowpeak Ruins West Courtyard Buried Chest",
        lambda state: (state.has("Shadow Crystal", player)),
    )
    set_rule_if_exists(
        "Snowpeak Ruins Wooden Beam Central Chest",
        lambda state: (can_defeat_IceKeese(state, player)),
    )
    set_rule_if_exists(
        "Snowpeak Ruins Wooden Beam Chandelier Chest",
        lambda state: (
            (
                state.has("Ordon Goat Cheese", player)
                # Holdover from Keysy
                # or (
                #     state._tp_small_key_settings(player)
                #     == SmallKeySettings.option_anywhere
                # )
            )
            and state.has("Ball and Chain", player)
        ),
        lambda state: (
            (
                state.has("Ordon Goat Cheese", player)
                # Holdover from Keysy
                # or (
                #     state._tp_small_key_settings(player)
                #     == SmallKeySettings.option_anywhere
                # )
            )
            and (state.has("Ball and Chain", player) or can_do_lja(state, player))
        ),
    )
    set_rule_if_exists(
        "Snowpeak Ruins Wooden Beam Northwest Chest",
        lambda state: (can_defeat_IceKeese(state, player)),
    )
    set_rule_if_exists(
        "Temple of Time Armogohma Heart Container",
        lambda state: (can_defeat_Armogohma(state, player)),
    )
    set_rule_if_exists(
        "Temple of Time Armos Antechamber East Chest",
        lambda state: (can_defeat_Armos(state, player)),
    )
    set_rule_if_exists(
        "Temple of Time Armos Antechamber North Chest", lambda state: (True)
    )
    set_rule_if_exists(
        "Temple of Time Armos Antechamber Statue Chest",
        lambda state: (state.has("Progressive Dominion Rod", player, 1)),
        lambda state: (True),
    )
    set_rule_if_exists(
        "Temple of Time Big Key Chest",
        lambda state: (
            can_defeat_Helmasaur(state, player)
            and state.has("Progressive Clawshot", player, 1)
        ),
    )
    set_rule_if_exists(
        "Temple of Time Chest Before Darknut",
        lambda state: (
            can_defeat_Armos(state, player)
            and can_defeat_BabyGohma(state, player)
            and can_defeat_YoungGohma(state, player)
        ),
    )
    set_rule_if_exists(
        "Temple of Time Darknut Chest",
        lambda state: (can_defeat_Darknut(state, player)),
    )
    set_rule_if_exists(
        "Temple of Time Dungeon Reward",
        lambda state: (can_defeat_Armogohma(state, player)),
    )
    set_rule_if_exists(
        "Temple of Time First Staircase Armos Chest",
        lambda state: (
            can_defeat_Armos(state, player) and has_ranged_item(state, player)
        ),
    )
    set_rule_if_exists(
        "Temple of Time First Staircase Gohma Gate Chest",
        lambda state: (can_defeat_YoungGohma(state, player)),
    )
    set_rule_if_exists(
        "Temple of Time First Staircase Window Chest",
        lambda state: (has_ranged_item(state, player)),
    )
    set_rule_if_exists(
        "Temple of Time Floor Switch Puzzle Room Upper Chest",
        lambda state: (state.has("Progressive Clawshot", player, 1)),
    )
    set_rule_if_exists("Temple of Time Gilloutine Chest", lambda state: (True))
    set_rule_if_exists(
        "Temple of Time Lobby Lantern Chest",
        lambda state: (state.has("Lantern", player)),
    )
    set_rule_if_exists(
        "Temple of Time Moving Wall Beamos Room Chest",
        lambda state: (state.has("Progressive Hero's Bow", player, 1)),
    )
    set_rule_if_exists(
        "Temple of Time Moving Wall Dinalfos Room Chest",
        lambda state: (
            can_defeat_Dinalfos(state, player)
            and state.has("Progressive Dominion Rod", player, 1)
            and state.has("Progressive Hero's Bow", player, 1)
        ),
        lambda state: (
            can_defeat_Dinalfos(state, player)
            and (
                state.has("Progressive Dominion Rod", player, 1)
                or (state.has("Spinner", player) and has_bombs(state, player))
            )
            and state.has("Progressive Hero's Bow", player, 1)
        ),
    )
    set_rule_if_exists(
        "Temple of Time Poe Above Scales",
        lambda state: (
            state.has("Shadow Crystal", player)
            and state.has("Progressive Clawshot", player, 1)
            and state.has("Spinner", player)
        ),
    )
    set_rule_if_exists(
        "Temple of Time Poe Behind Gate",
        lambda state: (
            state.has("Shadow Crystal", player)
            and state.has("Progressive Dominion Rod", player, 1)
        ),
        lambda state: (
            state.has("Shadow Crystal", player)
            and (
                state.has("Progressive Dominion Rod", player, 1)
                or state.has("Ball and Chain", player)
                or can_do_hs_moon_boots(state, player)
            )
        ),
    )
    set_rule_if_exists(
        "Temple of Time Scales Gohma Chest",
        lambda state: (
            can_defeat_YoungGohma(state, player) and can_defeat_BabyGohma(state, player)
        ),
    )
    set_rule_if_exists(
        "Temple of Time Scales Upper Chest",
        lambda state: (
            state.has("Progressive Clawshot", player, 1)
            and state.has("Spinner", player)
        ),
    )
    set_rule_if_exists("Barnes Bomb Bag", lambda state: (True))
    set_rule_if_exists(
        "Bridge of Eldin Female Phasmid",
        lambda state: (
            state.has("Progressive Clawshot", player, 1)
            or state.has("Gale Boomerang", player)
        ),
    )
    set_rule_if_exists(
        "Bridge of Eldin Male Phasmid",
        lambda state: (
            state.has("Progressive Clawshot", player, 1)
            or state.has("Gale Boomerang", player)
        ),
    )
    set_rule_if_exists(
        "Bridge of Eldin Owl Statue Chest",
        lambda state: (state.has("Progressive Dominion Rod", player, 2)),
        lambda state: (
            state.has("Progressive Dominion Rod", player, 2)
            or can_do_lja(state, player)
            or state.has("Shadow Crystal", player)
        ),
    )
    set_rule_if_exists(
        "Bridge of Eldin Owl Statue Sky Character",
        lambda state: (state.has("Progressive Dominion Rod", player, 2)),
    )
    set_rule_if_exists(
        "Cats Hide and Seek Minigame",
        lambda state: (
            state.has("Progressive Hero's Bow", player, 1)
            and state.can_reach_region("Kakariko Renados Sanctuary", player)
            and state.has("Ilias Charm", player)
            and state.has("Shadow Crystal", player)
            and state.has("Progressive Clawshot", player, 1)
        ),
        lambda state: (
            state.has("Ilias Charm", player)
            and state.has("Progressive Dominion Rod", player, 1)
            and can_do_hidden_village_glitched(state, player)
            and state.has("Shadow Crystal", player)
            and state.has("Progressive Clawshot", player, 1)
        ),
    )
    set_rule_if_exists(
        "Death Mountain Alcove Chest",
        lambda state: (
            (
                can_complete_goron_mines(state, player)
                # and (not state._tp_barren_dungeons(player))
            )
            or (
                state.has("Progressive Clawshot", player, 1)
                and (
                    state.has("Iron Boots", player)
                    or state.has("Shadow Crystal", player)
                )
            )
        ),
        lambda state: (
            (
                can_complete_goron_mines(state, player)
                # and (not state._tp_barren_dungeons(player))
            )
            or state.has("Progressive Clawshot", player, 1)
            or can_do_lja(state, player)
        ),
    )
    set_rule_if_exists(
        "Death Mountain Trail Poe",
        lambda state: (
            state.has("Shadow Crystal", player)
            and can_complete_goron_mines(state, player)
        ),
    )
    set_rule_if_exists(
        "Eldin Field Bomb Rock Chest",
        lambda state: (can_smash(state, player)),
        lambda state: (
            can_smash(state, player)
            or can_do_map_glitch(state, player)
            or (can_do_eb_moon_boots(state, player) and can_do_lja(state, player))
        ),
    )
    set_rule_if_exists(
        "Eldin Field Bomskit Grotto Lantern Chest",
        lambda state: (
            can_defeat_Bomskit(state, player) and state.has("Lantern", player)
        ),
    )
    set_rule_if_exists(
        "Eldin Field Bomskit Grotto Left Chest",
        lambda state: (can_defeat_Bomskit(state, player)),
    )
    set_rule_if_exists("Eldin Field Female Grasshopper", lambda state: (True))
    set_rule_if_exists("Eldin Field Male Grasshopper", lambda state: (True))
    set_rule_if_exists(
        "Eldin Field Stalfos Grotto Left Small Chest", lambda state: (True)
    )
    set_rule_if_exists(
        "Eldin Field Stalfos Grotto Right Small Chest", lambda state: (True)
    )
    set_rule_if_exists(
        "Eldin Field Stalfos Grotto Stalfos Chest",
        lambda state: (can_defeat_Stalfos(state, player)),
    )
    set_rule_if_exists("Eldin Field Water Bomb Fish Grotto Chest", lambda state: (True))
    set_rule_if_exists(
        "Eldin Lantern Cave First Chest",
        lambda state: (can_burn_webs(state, player)),
    )
    set_rule_if_exists(
        "Eldin Lantern Cave Lantern Chest",
        lambda state: (state.has("Lantern", player)),
    )
    set_rule_if_exists(
        "Eldin Lantern Cave Poe",
        lambda state: (
            state.has("Shadow Crystal", player) and can_burn_webs(state, player)
        ),
    )
    set_rule_if_exists(
        "Eldin Lantern Cave Second Chest",
        lambda state: (can_burn_webs(state, player)),
    )
    set_rule_if_exists(
        "Eldin Spring Underwater Chest",
        lambda state: (can_smash(state, player) and state.has("Iron Boots", player)),
        lambda state: (
            has_heavy_mod(state, player)
            and (can_smash(state, player) or can_do_map_glitch(state, player))
        ),
    )
    set_rule_if_exists(
        "Eldin Stockcave Lantern Chest",
        lambda state: (state.has("Lantern", player)),
        lambda state: (
            (state.has("Progressive Clawshot", player, 1) or can_do_lja(state, player))
            and state.has("Lantern", player)
        ),
    )
    set_rule_if_exists(
        "Eldin Stockcave Lowest Chest",
        lambda state: (True),
        lambda state: (
            (state.has("Progressive Clawshot", player, 1) or can_do_lja(state, player))
        ),
    )
    set_rule_if_exists(
        "Eldin Stockcave Upper Chest",
        lambda state: (state.has("Iron Boots", player)),
        lambda state: (state.has("Progressive Clawshot", player, 1)),
    )
    set_rule_if_exists(
        "Gift From Ralis",
        lambda state: (
            state.has("Ashei's Sketch", player)
            and (
                state.has("Gate Keys", player)
                # Holdover from Keysy
                # or (
                #     state._tp_small_key_settings(player)
                #     == SmallKeySettings.option_anywhere
                # )
            )
        ),
    )
    set_rule_if_exists(
        "Goron Springwater Rush",
        lambda state: (
            can_smash(state, player)
            or (
                (
                    True
                    # (state._tp_lanayru_twilight_cleared(player))
                    # or state.has("Shadow Crystal", player)
                )
                and (
                    state.has("Gate Keys", player)
                    # Holdover from Keysy
                    # or (
                    #     state._tp_small_key_settings(player)
                    #     == SmallKeySettings.option_anywhere
                    # )
                )
            )
        ),
    )
    set_rule_if_exists(
        "Hidden Village Poe",
        lambda state: (
            state.has("Progressive Hero's Bow", player, 1)
            and state.can_reach_region("Kakariko Renados Sanctuary", player)
            and state.has("Ilias Charm", player)
            and state.has("Shadow Crystal", player)
            and state.has("Progressive Clawshot", player, 1)
        ),
        lambda state: (
            state.has("Ilias Charm", player)
            and state.has("Progressive Dominion Rod", player, 1)
            and can_do_hidden_village_glitched(state, player)
            and state.has("Shadow Crystal", player)
        ),
    )
    set_rule_if_exists(
        "Ilias Charm",
        lambda state: (state.has("Progressive Hero's Bow", player, 1)),
        lambda state: (can_do_hidden_village_glitched(state, player)),
    )
    set_rule_if_exists(
        "Ilia Memory Reward",
        lambda state: (state.has("Ilias Charm", player)),
    )
    set_rule_if_exists(
        "Kakariko Gorge Double Clawshot Chest",
        lambda state: (state.has("Progressive Clawshot", player, 2)),
        lambda state: (
            state.has("Progressive Clawshot", player, 2)
            or can_do_lja(state, player)
            or state.has("Shadow Crystal", player)
        ),
    )
    set_rule_if_exists("Kakariko Gorge Female Pill Bug", lambda state: (True))
    set_rule_if_exists("Kakariko Gorge Male Pill Bug", lambda state: (True))
    set_rule_if_exists(
        "Kakariko Gorge Owl Statue Chest",
        lambda state: (state.has("Progressive Dominion Rod", player, 2)),
        lambda state: (
            state.has("Progressive Dominion Rod", player, 2)
            or can_do_lja(state, player)
            or can_do_storage(state, player)
            or can_do_eb_moon_boots(state, player)
        ),
    )
    set_rule_if_exists(
        "Kakariko Gorge Owl Statue Sky Character",
        lambda state: (state.has("Progressive Dominion Rod", player, 2)),
    )
    set_rule_if_exists(
        "Kakariko Gorge Poe",
        lambda state: (
            state.has("Shadow Crystal", player)
            # and can_complete_MDH(state, player)
            # and can_complete_all_twilight(state, player)
        ),
    )
    set_rule_if_exists(
        "Kakariko Gorge Spire Heart Piece",
        lambda state: (
            state.has("Progressive Clawshot", player, 1)
            or state.has("Gale Boomerang", player)
        ),
    )
    set_rule_if_exists(
        "Kakariko Graveyard Golden Wolf",
        lambda state: (
            state.has("Shadow Crystal", player)
            and state.can_reach_region("Snowpeak Climb Upper", player)
        ),
    )
    set_rule_if_exists(
        "Kakariko Graveyard Grave Poe",
        lambda state: (
            state.has("Shadow Crystal", player)
            and can_change_time(state, player)
            # redunant as with shadow crystal you can change time
        ),
        lambda state: (state.has("Shadow Crystal", player)),
    )
    set_rule_if_exists(
        "Kakariko Graveyard Lantern Chest",
        lambda state: (state.has("Lantern", player)),
    )
    set_rule_if_exists("Kakariko Graveyard Male Ant", lambda state: (True))
    set_rule_if_exists(
        "Kakariko Graveyard Open Poe",
        lambda state: (
            state.has("Shadow Crystal", player)
            and can_change_time(state, player)
            # redunant as with shadow crystal you can change time
        ),
        lambda state: (state.has("Shadow Crystal", player)),
    )
    set_rule_if_exists("Kakariko Inn Chest", lambda state: (True))
    set_rule_if_exists(
        "Kakariko Village Bomb Rock Spire Heart Piece",
        lambda state: (
            has_bombs(state, player) and state.has("Gale Boomerang", player)
        ),
        lambda state: (
            can_do_map_glitch(state, player)
            or (
                can_launch_bombs(state, player)
                and (
                    state.has("Gale Boomerang", player)
                    or state.has("Progressive Clawshot", player, 1)
                )
            )
        ),
    )
    set_rule_if_exists(
        "Kakariko Village Bomb Shop Poe",
        lambda state: (
            state.has("Shadow Crystal", player)
            and can_change_time(state, player)
            # redunant as with shadow crystal you can change time
        ),
        lambda state: (state.has("Shadow Crystal", player)),
    )
    set_rule_if_exists("Kakariko Village Female Ant", lambda state: (True))
    set_rule_if_exists(
        "Kakariko Village Malo Mart Hawkeye",
        lambda state: (
            can_complete_goron_mines(state, player)
            and state.can_reach_region("Kakariko Top of Watchtower", player)
            and state.has("Progressive Hero's Bow", player, 1)
        ),
        lambda state: (
            (
                can_complete_goron_mines(state, player)
                and state.has("Progressive Hero's Bow", player, 1)
            )
        ),
    )
    set_rule_if_exists("Kakariko Village Malo Mart Hylian Shield", lambda state: (True))
    set_rule_if_exists("Kakariko Village Malo Mart Red Potion", lambda state: (True))
    set_rule_if_exists("Kakariko Village Malo Mart Wooden Shield", lambda state: (True))
    set_rule_if_exists(
        "Kakariko Village Watchtower Poe",
        lambda state: (
            state.has("Shadow Crystal", player)
            and can_change_time(state, player)
            # redunant as with shadow crystal you can change time
        ),
        lambda state: (state.has("Shadow Crystal", player)),
    )
    set_rule_if_exists(
        "Kakariko Watchtower Alcove Chest",
        lambda state: (can_smash(state, player)),
        lambda state: (can_smash(state, player) or state.has("Shadow Crystal", player)),
    )
    set_rule_if_exists("Kakariko Watchtower Chest", lambda state: (True))
    set_rule_if_exists(
        "Renados Letter",
        lambda state: (can_complete_temple_of_time(state, player)),
    )
    set_rule_if_exists(
        "Rutelas Blessing",
        lambda state: (
            state.has("Gate Keys", player)
            # Holdover from Keysy
            # or (
            #     state._tp_small_key_settings(player) == SmallKeySettings.option_anywhere
            # )
        ),
    )
    set_rule_if_exists(
        "Skybook From Impaz",
        lambda state: (
            state.can_reach_region("Hidden Village", player)
            and state.has("Progressive Hero's Bow", player, 1)
            and state.has("Progressive Dominion Rod", player, 1)
        ),
        lambda state: (
            can_do_hidden_village_glitched(state, player)
            and state.has("Progressive Dominion Rod", player, 1)
        ),
    )
    set_rule_if_exists(
        "Talo Sharpshooting",
        lambda state: (
            can_complete_goron_mines(state, player)
            and state.has("Progressive Hero's Bow", player, 1)
            and can_change_time(state, player)
        ),
        lambda state: (
            can_complete_goron_mines(state, player)
            and state.has("Progressive Hero's Bow", player, 1)
        ),
    )
    set_rule_if_exists(
        "Coro Bottle", lambda state: True  # (can_complete_prologue(state, player))
    )
    set_rule_if_exists(
        "Faron Field Bridge Chest",
        lambda state: (state.has("Progressive Clawshot", player, 1)),
        lambda state: (
            state.has("Progressive Clawshot", player, 1)
            or can_do_storage(state, player)
        ),
    )
    set_rule_if_exists("Faron Field Corner Grotto Left Chest", lambda state: (True))
    set_rule_if_exists("Faron Field Corner Grotto Rear Chest", lambda state: (True))
    set_rule_if_exists("Faron Field Corner Grotto Right Chest", lambda state: (True))
    set_rule_if_exists(
        "Faron Field Female Beetle",
        lambda state: (
            state.has("Gale Boomerang", player)
            or state.has("Progressive Clawshot", player, 1)
        ),
        lambda state: (
            state.has("Gale Boomerang", player)
            or state.has("Progressive Clawshot", player, 1)
            or can_do_map_glitch(state, player)
            or can_do_eb_moon_boots(state, player)
        ),
    )
    set_rule_if_exists("Faron Field Male Beetle", lambda state: (True))
    set_rule_if_exists(
        "Faron Field Poe",
        lambda state: (
            state.has("Shadow Crystal", player)
            # and can_complete_MDH(state, player)
            # and can_complete_all_twilight(state, player)
        ),
    )
    set_rule_if_exists(
        "Faron Field Tree Heart Piece",
        lambda state: (
            state.has("Gale Boomerang", player)
            or state.has("Progressive Clawshot", player, 1)
        ),
        lambda state: (
            state.has("Gale Boomerang", player)
            or state.has("Progressive Clawshot", player, 1)
            or state.has("Ball and Chain", player)
        ),
    )
    set_rule_if_exists(
        "Faron Mist Cave Lantern Chest",
        lambda state: (state.has("Lantern", player)),
    )
    set_rule_if_exists("Faron Mist Cave Open Chest", lambda state: (True))
    set_rule_if_exists(
        "Faron Mist North Chest",
        lambda state: (
            state.has("Lantern", player)  # and can_complete_prologue(state, player)
        ),
        lambda state: (
            state.has("Lantern", player) or can_do_map_glitch(state, player)
        ),
    )
    set_rule_if_exists(
        "Faron Mist Poe",
        lambda state: (
            state.has(
                "Shadow Crystal", player
            )  # and can_complete_prologue(state, player)
        ),
        lambda state: (state.has("Shadow Crystal", player)),
    )
    set_rule_if_exists(
        "Faron Mist South Chest",
        lambda state: (
            state.has("Lantern", player)  # and can_complete_prologue(state, player)
        ),
        lambda state: (
            state.has("Lantern", player) or can_do_map_glitch(state, player)
        ),
    )
    set_rule_if_exists(
        "Faron Mist Stump Chest",
        lambda state: (
            state.has("Lantern", player)  # and can_complete_prologue(state, player)
        ),
        lambda state: (
            state.has("Lantern", player) or can_do_map_glitch(state, player)
        ),
    )
    set_rule_if_exists("Faron Woods Golden Wolf", lambda state: (True))
    set_rule_if_exists(
        "Faron Woods Owl Statue Chest",
        lambda state: (True),
        lambda state: (
            can_do_map_glitch(state, player)
            or (
                can_smash(state, player)
                and state.has("Progressive Dominion Rod", player, 2)
                and state.has("Shadow Crystal", player)
                and can_clear_forest(state, player)
            )
        ),
    )
    set_rule_if_exists(
        "Faron Woods Owl Statue Sky Character",
        lambda state: (
            can_clear_forest(state, player)
            and state.has("Progressive Dominion Rod", player, 2)
        ),
        lambda state: (
            state.has("Progressive Dominion Rod", player, 2)
            and (
                can_do_map_glitch(state, player)
                or (can_smash(state, player) and can_clear_forest(state, player))
            )
        ),
    )
    set_rule_if_exists(
        "Lost Woods Boulder Poe",
        lambda state: (
            state.has("Shadow Crystal", player)
            and (
                can_defeat_SkullKid(state, player)
                or (state._tp_tot_entrance(player) == TotEntrance.option_open)
                or (state._tp_tot_entrance(player) == TotEntrance.option_open_grove)
            )
            and can_smash(state, player)
        ),
    )
    set_rule_if_exists(
        "Lost Woods Lantern Chest",
        lambda state: (state.has("Lantern", player)),
    )
    set_rule_if_exists(
        "Lost Woods Waterfall Poe",
        lambda state: (state.has("Shadow Crystal", player)),
    )
    set_rule_if_exists("North Faron Woods Deku Baba Chest", lambda state: (True))
    set_rule_if_exists(
        "Sacred Grove Baba Serpent Grotto Chest",
        lambda state: (
            can_defeat_BabaSerpent(state, player)
            and can_knock_down_HangingBaba(state, player)
        ),
        lambda state: (
            can_defeat_BabaSerpent(state, player)
            and (
                can_knock_down_HangingBaba(state, player)
                or has_sword(state, player)
                or state.has("Shadow Crystal", player)
                or state.has("Slingshot", player)
                or state.has("Ball and Chain", player)
                or has_bombs(state, player)
            )
        ),
    )
    set_rule_if_exists(
        "Sacred Grove Female Snail",
        lambda state: (
            state.has("Progressive Clawshot", player, 1)
            or state.has("Gale Boomerang", player)
        ),
    )
    set_rule_if_exists(
        "Sacred Grove Male Snail",
        lambda state: (
            state.has("Progressive Clawshot", player, 1)
            or state.has("Gale Boomerang", player)
        ),
    )
    set_rule_if_exists(
        "Sacred Grove Master Sword Poe",
        lambda state: (state.has("Shadow Crystal", player)),
    )
    set_rule_if_exists(
        "Sacred Grove Past Owl Statue Chest",
        lambda state: (state.has("Progressive Dominion Rod", player, 1)),
        lambda state: (
            state.has("Progressive Dominion Rod", player, 1)
            or state.has("Shadow Crystal", player)
        ),
    )
    set_rule_if_exists("Sacred Grove Pedestal Master Sword", lambda state: (True))
    set_rule_if_exists("Sacred Grove Pedestal Shadow Crystal", lambda state: (True))
    set_rule_if_exists(
        "Sacred Grove Spinner Chest",
        lambda state: (state.has("Spinner", player)),
        lambda state: (state.has("Spinner", player) or can_do_lja(state, player)),
    )
    set_rule_if_exists(
        "Sacred Grove Temple of Time Owl Statue Poe",
        lambda state: (
            state.has("Shadow Crystal", player)
            and state.has("Progressive Dominion Rod", player, 1)
        ),
    )
    set_rule_if_exists("South Faron Cave Chest", lambda state: (True))
    set_rule_if_exists(
        "Bulblin Camp First Chest Under Tower At Entrance", lambda state: (True)
    )
    set_rule_if_exists(
        "Bulblin Camp Poe",
        lambda state: (
            state.has("Shadow Crystal", player)
            and (
                state.has("Gerudo Desert Bublin Camp Key", player)
                # Holdover from Keysy
                # or (
                #     state._tp_small_key_settings(player)
                #     == SmallKeySettings.option_anywhere
                # )
                or (state._tp_skip_arbiters_entrance(player))
            )
        ),
        lambda state: (
            (
                state.has("Shadow Crystal", player)
                and (
                    state.has("Gerudo Desert Bublin Camp Key", player)
                    or (
                        (can_do_map_glitch(state, player) and has_sword(state, player))
                        # Holdover from Keysy
                        # or (
                        #     state._tp_small_key_settings(player)
                        #     == SmallKeySettings.option_anywhere
                        # )
                    )
                )
            )
            or (state._tp_skip_arbiters_entrance(player))
        ),
    )
    set_rule_if_exists(
        "Bulblin Camp Roasted Boar",
        lambda state: (has_damaging_item(state, player)),
    )
    set_rule_if_exists("Bulblin Camp Small Chest in Back of Camp", lambda state: (True))
    set_rule_if_exists(
        "Bulblin Guard Key", lambda state: (can_defeat_Bulblin(state, player))
    )
    set_rule_if_exists(
        "Cave of Ordeals Floor 17 Poe",
        lambda state: (
            state.has("Spinner", player)
            and state.has("Shadow Crystal", player)
            and can_defeat_Helmasaur(state, player)
            and can_defeat_Rat(state, player)
            and can_defeat_Chu(state, player)
            and can_defeat_ChuWorm(state, player)
            and can_defeat_Bubble(state, player)
            and can_defeat_Keese(state, player)
            and can_defeat_Stalhound(state, player)
        ),
        lambda state: (
            (
                state.has("Spinner", player)
                or (
                    (state.has("Progressive Clawshot", player, 1))
                    and can_do_lja(state, player)
                )
            )
            and state.has("Shadow Crystal", player)
            and can_defeat_Helmasaur(state, player)
            and can_defeat_Rat(state, player)
            and can_defeat_Chu(state, player)
            and can_defeat_ChuWorm(state, player)
            and can_defeat_Bubble(state, player)
            and can_defeat_Keese(state, player)
            and can_defeat_Stalhound(state, player)
        ),
    )
    set_rule_if_exists(
        "Cave of Ordeals Floor 33 Poe",
        lambda state: (
            state.has("Shadow Crystal", player)
            and state.has("Progressive Dominion Rod", player, 2)
            and can_defeat_Beamos(state, player)
            and can_defeat_Keese(state, player)
            and can_defeat_Dodongo(state, player)
            and can_defeat_Bubble(state, player)
            and can_defeat_RedeadKnight(state, player)
        ),
    )
    set_rule_if_exists(
        "Cave of Ordeals Floor 44 Poe",
        lambda state: (
            state.has("Shadow Crystal", player)
            and state.has("Progressive Clawshot", player, 2)
            and can_defeat_Armos(state, player)
            and can_defeat_BabaSerpent(state, player)
            and can_defeat_Lizalfos(state, player)
            and can_defeat_Dinalfos(state, player)
            and (
                state.has("Progressive Hero's Bow", player, 1)
                or state.has("Ball and Chain", player)
            )
        ),
        lambda state: (
            state.has("Shadow Crystal", player)
            and (
                state.has("Progressive Clawshot", player, 2)
                or (
                    state.has("Progressive Clawshot", player, 1)
                    and can_do_lja(state, player)
                )
            )
            and can_defeat_Armos(state, player)
            and can_defeat_BabaSerpent(state, player)
            and can_defeat_Lizalfos(state, player)
            and can_defeat_Dinalfos(state, player)
            and (
                state.has("Progressive Hero's Bow", player, 1)
                or state.has("Ball and Chain", player)
            )
        ),
    )
    set_rule_if_exists(
        "Cave of Ordeals Great Fairy Reward",
        lambda state: (
            can_defeat_Armos(state, player)
            and can_defeat_Bokoblin(state, player)
            and can_defeat_BabaSerpent(state, player)
            and can_defeat_Lizalfos(state, player)
            and can_defeat_Bulblin(state, player)
            and can_defeat_Dinalfos(state, player)
            and can_defeat_Poe(state, player)
            and can_defeat_RedeadKnight(state, player)
            and can_defeat_Chu(state, player)
            and can_defeat_Freezard(state, player)
            and can_defeat_Chilfos(state, player)
            and can_defeat_GhoulRat(state, player)
            and can_defeat_Rat(state, player)
            and can_defeat_Stalchild(state, player)
            and can_defeat_Aeralfos(state, player)
            and can_defeat_Darknut(state, player)
        ),
    )
    set_rule_if_exists(
        "Gerudo Desert Campfire East Chest",
        lambda state: (can_defeat_Bulblin(state, player)),
    )
    set_rule_if_exists("Gerudo Desert Campfire North Chest", lambda state: (True))
    set_rule_if_exists(
        "Gerudo Desert Campfire West Chest",
        lambda state: (can_defeat_Bulblin(state, player)),
    )
    set_rule_if_exists("Gerudo Desert East Canyon Chest", lambda state: (True))
    set_rule_if_exists(
        "Gerudo Desert East Poe",
        lambda state: (state.has("Shadow Crystal", player)),
    )
    set_rule_if_exists("Gerudo Desert Female Dayfly", lambda state: (True))
    set_rule_if_exists(
        "Gerudo Desert Golden Wolf",
        lambda state: (
            state.has("Shadow Crystal", player)
            and state.can_reach_region("Lake Hylia", player)
        ),
    )
    set_rule_if_exists("Gerudo Desert Lone Small Chest", lambda state: (True))
    set_rule_if_exists("Gerudo Desert Male Dayfly", lambda state: (True))
    set_rule_if_exists(
        "Gerudo Desert North Peahat Poe",
        lambda state: (state.has("Shadow Crystal", player)),
        lambda state: (
            state.has("Shadow Crystal", player)
            and state.has("Progressive Clawshot", player, 1)
        ),
    )
    set_rule_if_exists(
        "Gerudo Desert North Small Chest Before Bulblin Camp",
        lambda state: (True),
        lambda state: (can_defeat_Bulblin(state, player)),
    )
    set_rule_if_exists(
        "Gerudo Desert Northeast Chest Behind Gates",
        lambda state: (can_defeat_Bulblin(state, player)),
    )
    set_rule_if_exists(
        "Gerudo Desert Northwest Chest Behind Gates",
        lambda state: (can_defeat_Bulblin(state, player)),
    )
    set_rule_if_exists(
        "Gerudo Desert Owl Statue Chest",
        lambda state: (state.has("Progressive Dominion Rod", player, 2)),
        lambda state: (
            state.has("Progressive Dominion Rod", player, 2)
            or can_do_lja(state, player)
        ),
    )
    set_rule_if_exists(
        "Gerudo Desert Owl Statue Sky Character",
        lambda state: (state.has("Progressive Dominion Rod", player, 2)),
    )
    set_rule_if_exists(
        "Gerudo Desert Peahat Ledge Chest",
        lambda state: (state.has("Progressive Clawshot", player, 1)),
    )
    set_rule_if_exists(
        "Gerudo Desert Poe Above Cave of Ordeals",
        lambda state: (state.has("Shadow Crystal", player)),
        lambda state: (
            state.has("Shadow Crystal", player)
            and state.has("Progressive Clawshot", player, 1)
            and can_defeat_ShadowBeast(state, player)
        ),
    )
    set_rule_if_exists(
        "Gerudo Desert Rock Grotto First Poe",
        lambda state: (
            state.has("Shadow Crystal", player) and can_smash(state, player)
        ),
    )
    set_rule_if_exists(
        "Gerudo Desert Rock Grotto Lantern Chest",
        lambda state: (can_smash(state, player) and state.has("Lantern", player)),
    )
    set_rule_if_exists(
        "Gerudo Desert Rock Grotto Second Poe",
        lambda state: (
            state.has("Shadow Crystal", player) and can_smash(state, player)
        ),
    )
    set_rule_if_exists(
        "Gerudo Desert Skulltula Grotto Chest",
        lambda state: (can_defeat_Skulltula(state, player)),
    )
    set_rule_if_exists(
        "Gerudo Desert South Chest Behind Wooden Gates",
        lambda state: (can_defeat_Bulblin(state, player)),
    )
    set_rule_if_exists(
        "Gerudo Desert West Canyon Chest",
        lambda state: (state.has("Progressive Clawshot", player, 1)),
        lambda state: (
            state.has("Progressive Clawshot", player, 1)
            or can_do_lja(state, player)
            or (state.has("Shadow Crystal", player) and has_bombs(state, player))
        ),
    )
    set_rule_if_exists(
        "Outside Arbiters Grounds Lantern Chest",
        lambda state: (state.has("Lantern", player)),
    )
    set_rule_if_exists(
        "Outside Arbiters Grounds Poe",
        lambda state: (state.has("Shadow Crystal", player)),
    )
    set_rule_if_exists(
        "Outside Bulblin Camp Poe",
        lambda state: (state.has("Shadow Crystal", player)),
    )
    set_rule_if_exists(
        "Agitha Female Ant Reward",
        lambda state: (state.has("Female Ant", player)),
    )
    set_rule_if_exists(
        "Agitha Female Beetle Reward",
        lambda state: (state.has("Female Beetle", player)),
    )
    set_rule_if_exists(
        "Agitha Female Butterfly Reward",
        lambda state: (state.has("Female Butterfly", player)),
    )
    set_rule_if_exists(
        "Agitha Female Dayfly Reward",
        lambda state: (state.has("Female Dayfly", player)),
    )
    set_rule_if_exists(
        "Agitha Female Dragonfly Reward",
        lambda state: (state.has("Female Dragonfly", player)),
    )
    set_rule_if_exists(
        "Agitha Female Grasshopper Reward",
        lambda state: (state.has("Female Grasshopper", player)),
    )
    set_rule_if_exists(
        "Agitha Female Ladybug Reward",
        lambda state: (state.has("Female Ladybug", player)),
    )
    set_rule_if_exists(
        "Agitha Female Mantis Reward",
        lambda state: (state.has("Female Mantis", player)),
    )
    set_rule_if_exists(
        "Agitha Female Phasmid Reward",
        lambda state: (state.has("Female Phasmid", player)),
    )
    set_rule_if_exists(
        "Agitha Female Pill Bug Reward",
        lambda state: (state.has("Female Pill Bug", player)),
    )
    set_rule_if_exists(
        "Agitha Female Snail Reward",
        lambda state: (state.has("Female Snail", player)),
    )
    set_rule_if_exists(
        "Agitha Female Stag Beetle Reward",
        lambda state: (state.has("Female Stag Beetle", player)),
    )
    set_rule_if_exists(
        "Agitha Male Ant Reward",
        lambda state: (state.has("Male Ant", player)),
    )
    set_rule_if_exists(
        "Agitha Male Beetle Reward",
        lambda state: (state.has("Male Beetle", player)),
    )
    set_rule_if_exists(
        "Agitha Male Butterfly Reward",
        lambda state: (state.has("Male Butterfly", player)),
    )
    set_rule_if_exists(
        "Agitha Male Dayfly Reward",
        lambda state: (state.has("Male Dayfly", player)),
    )
    set_rule_if_exists(
        "Agitha Male Dragonfly Reward",
        lambda state: (state.has("Male Dragonfly", player)),
    )
    set_rule_if_exists(
        "Agitha Male Grasshopper Reward",
        lambda state: (state.has("Male Grasshopper", player)),
    )
    set_rule_if_exists(
        "Agitha Male Ladybug Reward",
        lambda state: (state.has("Male Ladybug", player)),
    )
    set_rule_if_exists(
        "Agitha Male Mantis Reward",
        lambda state: (state.has("Male Mantis", player)),
    )
    set_rule_if_exists(
        "Agitha Male Phasmid Reward",
        lambda state: (state.has("Male Phasmid", player)),
    )
    set_rule_if_exists(
        "Agitha Male Pill Bug Reward",
        lambda state: (state.has("Male Pill Bug", player)),
    )
    set_rule_if_exists(
        "Agitha Male Snail Reward",
        lambda state: (state.has("Male Snail", player)),
    )
    set_rule_if_exists(
        "Agitha Male Stag Beetle Reward",
        lambda state: (state.has("Male Stag Beetle", player)),
    )
    set_rule_if_exists("Auru Gift To Fyer", lambda state: (True))
    set_rule_if_exists(
        "Castle Town Malo Mart Magic Armor",
        lambda state: (
            state.can_reach_region("Kakariko Malo Mart", player)
            and state.can_reach_region("Lower Kakariko Village", player)
            and (
                (state._tp_increase_wallet(player))
                or state.has("Progressive Wallet", player, 1)
            )
        ),
        lambda state: (
            (state._tp_increase_wallet(player))
            or state.has("Progressive Wallet", player, 1)
            # or ((false) and has_bug(state, player)) # NPC not shuffled and has bugs
        ),
    )
    set_rule_if_exists("Charlo Donation Blessing", lambda state: (True))
    set_rule_if_exists(
        "Doctors Office Balcony Chest",
        lambda state: (True),
        lambda state: (
            state.has("Invoice", player) and state.has("Shadow Crystal", player)
        ),
    )
    set_rule_if_exists(
        "East Castle Town Bridge Poe",
        lambda state: (state.has("Shadow Crystal", player)),
    )
    set_rule_if_exists(
        "Fishing Hole Bottle",
        lambda state: (state.has("Progressive Fishing Rod", player, 1)),
    )
    set_rule_if_exists(
        "Fishing Hole Heart Piece",
        lambda state: (
            state.can_reach_region("Fishing Hole House", player)
            or state.has("Progressive Clawshot", player, 1)
        ),
        lambda state: (True),
    )
    set_rule_if_exists("Flight By Fowl Fifth Platform Chest", lambda state: (True))
    set_rule_if_exists("Flight By Fowl Fourth Platform Chest", lambda state: (True))
    set_rule_if_exists(
        "Flight By Fowl Ledge Poe",
        lambda state: (state.has("Shadow Crystal", player)),
    )
    set_rule_if_exists("Flight By Fowl Second Platform Chest", lambda state: (True))
    set_rule_if_exists("Flight By Fowl Third Platform Chest", lambda state: (True))
    set_rule_if_exists("Flight By Fowl Top Platform Reward", lambda state: (True))
    set_rule_if_exists(
        "Hyrule Field Amphitheater Owl Statue Chest",
        lambda state: (state.has("Progressive Dominion Rod", player, 2)),
        lambda state: (
            state.has("Progressive Dominion Rod", player, 2)
            or can_do_lja(state, player)
            or can_do_map_glitch(state, player)
            or can_do_eb_moon_boots(state, player)
        ),
    )
    set_rule_if_exists(
        "Hyrule Field Amphitheater Owl Statue Sky Character",
        lambda state: (state.has("Progressive Dominion Rod", player, 2)),
    )
    set_rule_if_exists(
        "Hyrule Field Amphitheater Poe",
        lambda state: (state.has("Shadow Crystal", player)),
    )
    set_rule_if_exists(
        "Isle of Riches Poe",
        lambda state: (state.has("Shadow Crystal", player)),
    )
    set_rule_if_exists(
        "Iza Helping Hand",
        lambda state: (
            state.can_reach_region("Upper Zoras River", player)
            and (
                has_sword(state, player)
                or (
                    can_defeat_ShadowBeast(state, player)
                    and (state._tp_transform_anywhere(player))
                )
            )
            and state.has("Progressive Hero's Bow", player, 1)
        ),
        lambda state: (
            state.has("Progressive Hero's Bow", player, 1)
            and state.can_reach_region("Zoras Domain", player)
            and (
                has_sword(state, player)
                or (
                    can_defeat_ShadowBeast(state, player)
                    and (state._tp_transform_anywhere(player))
                )
            )
        ),
    )
    set_rule_if_exists(
        "Iza Raging Rapids Minigame",
        lambda state: (
            state.can_reach_region("Upper Zoras River", player)
            and (
                has_sword(state, player)
                or (
                    can_defeat_ShadowBeast(state, player)
                    and (state._tp_transform_anywhere(player))
                )
            )
            and state.has("Progressive Hero's Bow", player, 1)
        ),
        lambda state: (
            state.has("Progressive Hero's Bow", player, 1)
            and state.can_reach_region("Zoras Domain", player)
            and (
                has_sword(state, player)
                or (
                    can_defeat_ShadowBeast(state, player)
                    and (state._tp_transform_anywhere(player))
                )
            )
        ),
    )
    set_rule_if_exists(
        "Jovani 20 Poe Soul Reward",
        lambda state: (state.has("Poe Soul", player, 20)),
    )
    set_rule_if_exists(
        "Jovani 60 Poe Soul Reward",
        lambda state: (state.has("Poe Soul", player, 60)),
    )
    set_rule_if_exists(
        "Jovani House Poe",
        lambda state: (state.has("Shadow Crystal", player)),
    )
    set_rule_if_exists(
        "Lake Hylia Alcove Poe",
        lambda state: (state.has("Shadow Crystal", player)),
    )
    set_rule_if_exists(
        "Lake Hylia Bridge Bubble Grotto Chest",
        lambda state: (
            can_defeat_Bubble(state, player)
            and can_defeat_FireBubble(state, player)
            and can_defeat_IceBubble(state, player)
        ),
    )
    set_rule_if_exists(
        "Lake Hylia Bridge Cliff Chest",
        lambda state: (True),
        lambda state: (
            (
                can_launch_bombs(state, player)
                and state.has("Progressive Clawshot", player, 1)
            )
        ),
    )
    set_rule_if_exists(
        "Lake Hylia Bridge Cliff Poe",
        lambda state: (
            # can_complete_MDH(state, player) and
            state.has("Shadow Crystal", player)
            # and can_complete_all_twilight(state, player)
        ),
        lambda state: (
            state.has("Shadow Crystal", player)
            and (
                can_launch_bombs(state, player)
                and state.has("Progressive Clawshot", player, 1)
            )
            # and can_complete_MDH(state, player)
            # and can_complete_all_twilight(state, player)
        ),
    )
    set_rule_if_exists(
        "Lake Hylia Bridge Female Mantis",
        lambda state: (
            state.has("Progressive Clawshot", player, 1)
            or state.has("Gale Boomerang", player)
        ),
        lambda state: (
            state.has("Progressive Clawshot", player, 1)
            or state.has("Gale Boomerang", player)
            or can_get_bug_with_lantern(state, player)
        ),
    )
    set_rule_if_exists(
        "Lake Hylia Bridge Male Mantis",
        lambda state: (
            state.has("Progressive Clawshot", player, 1)
            or state.has("Gale Boomerang", player)
        ),
        lambda state: (
            state.has("Progressive Clawshot", player, 1)
            or state.has("Gale Boomerang", player)
            or can_get_bug_with_lantern(state, player)
        ),
    )
    set_rule_if_exists(
        "Lake Hylia Bridge Owl Statue Chest",
        lambda state: (
            state.has("Progressive Dominion Rod", player, 2)
            and state.has("Progressive Clawshot", player, 1)
        ),
        lambda state: (
            can_do_map_glitch(state, player)
            or (
                state.has("Progressive Clawshot", player, 1)
                and state.has("Progressive Dominion Rod", player, 2)
            )
        ),
    )
    set_rule_if_exists(
        "Lake Hylia Bridge Owl Statue Sky Character",
        lambda state: (
            state.has("Progressive Dominion Rod", player, 2)
            and state.has("Progressive Clawshot", player, 1)
        ),
        lambda state: (
            state.has("Progressive Dominion Rod", player, 2)
            and (
                state.has("Progressive Clawshot", player, 1)
                or can_do_map_glitch(state, player)
            )
        ),
    )
    set_rule_if_exists(
        "Lake Hylia Bridge Vines Chest",
        lambda state: (state.has("Progressive Clawshot", player, 1)),
    )
    set_rule_if_exists(
        "Lake Hylia Dock Poe",
        lambda state: (state.has("Shadow Crystal", player)),
    )
    set_rule_if_exists(
        "Lake Hylia Shell Blade Grotto Chest",
        lambda state: (can_defeat_ShellBlade(state, player)),
    )
    set_rule_if_exists(
        "Lake Hylia Tower Poe",
        lambda state: (state.has("Shadow Crystal", player)),
    )
    set_rule_if_exists(
        "Lake Hylia Underwater Chest",
        lambda state: (state.has("Iron Boots", player)),
        lambda state: (has_heavy_mod(state, player)),
    )
    set_rule_if_exists(
        "Lake Hylia Water Toadpoli Grotto Chest",
        lambda state: (can_defeat_WaterToadpoli(state, player)),
    )
    set_rule_if_exists(
        "Lake Lantern Cave Eighth Chest",
        lambda state: (can_smash(state, player) and state.has("Lantern", player)),
        lambda state: (can_smash(state, player)),
    )
    set_rule_if_exists(
        "Lake Lantern Cave Eleventh Chest",
        lambda state: (can_smash(state, player) and state.has("Lantern", player)),
        lambda state: (can_smash(state, player)),
    )
    set_rule_if_exists(
        "Lake Lantern Cave End Lantern Chest",
        lambda state: (can_smash(state, player) and state.has("Lantern", player)),
    )
    set_rule_if_exists(
        "Lake Lantern Cave Fifth Chest",
        lambda state: (can_smash(state, player) and state.has("Lantern", player)),
        lambda state: (can_smash(state, player)),
    )
    set_rule_if_exists(
        "Lake Lantern Cave Final Poe",
        lambda state: (
            state.has("Shadow Crystal", player)
            and can_smash(state, player)
            and state.has("Lantern", player)
        ),
        lambda state: (
            state.has("Shadow Crystal", player) and can_smash(state, player)
        ),
    )
    set_rule_if_exists(
        "Lake Lantern Cave First Chest",
        lambda state: (can_smash(state, player) and state.has("Lantern", player)),
        lambda state: (can_smash(state, player)),
    )
    set_rule_if_exists(
        "Lake Lantern Cave First Poe",
        lambda state: (
            state.has("Shadow Crystal", player)
            and can_smash(state, player)
            and state.has("Lantern", player)
        ),
        lambda state: (
            state.has("Shadow Crystal", player) and can_smash(state, player)
        ),
    )
    set_rule_if_exists(
        "Lake Lantern Cave Fourteenth Chest",
        lambda state: (can_smash(state, player) and state.has("Lantern", player)),
        lambda state: (can_smash(state, player)),
    )
    set_rule_if_exists(
        "Lake Lantern Cave Fourth Chest",
        lambda state: (can_smash(state, player) and state.has("Lantern", player)),
        lambda state: (can_smash(state, player)),
    )
    set_rule_if_exists(
        "Lake Lantern Cave Ninth Chest",
        lambda state: (can_smash(state, player) and state.has("Lantern", player)),
        lambda state: (can_smash(state, player)),
    )
    set_rule_if_exists(
        "Lake Lantern Cave Second Chest",
        lambda state: (can_smash(state, player) and state.has("Lantern", player)),
        lambda state: (can_smash(state, player)),
    )
    set_rule_if_exists(
        "Lake Lantern Cave Second Poe",
        lambda state: (
            state.has("Shadow Crystal", player)
            and can_smash(state, player)
            and state.has("Lantern", player)
        ),
        lambda state: (
            state.has("Shadow Crystal", player) and can_smash(state, player)
        ),
    )
    set_rule_if_exists(
        "Lake Lantern Cave Seventh Chest",
        lambda state: (can_smash(state, player) and state.has("Lantern", player)),
        lambda state: (can_smash(state, player)),
    )
    set_rule_if_exists(
        "Lake Lantern Cave Sixth Chest",
        lambda state: (can_smash(state, player) and state.has("Lantern", player)),
    )
    set_rule_if_exists(
        "Lake Lantern Cave Tenth Chest",
        lambda state: (can_smash(state, player) and state.has("Lantern", player)),
        lambda state: (can_smash(state, player)),
    )
    set_rule_if_exists(
        "Lake Lantern Cave Third Chest",
        lambda state: (can_smash(state, player) and state.has("Lantern", player)),
        lambda state: (can_smash(state, player)),
    )
    set_rule_if_exists(
        "Lake Lantern Cave Thirteenth Chest",
        lambda state: (can_smash(state, player) and state.has("Lantern", player)),
        lambda state: (can_smash(state, player)),
    )
    set_rule_if_exists(
        "Lake Lantern Cave Twelfth Chest",
        lambda state: (can_smash(state, player) and state.has("Lantern", player)),
        lambda state: (can_smash(state, player)),
    )
    set_rule_if_exists(
        "Lanayru Field Behind Gate Underwater Chest",
        lambda state: (state.has("Iron Boots", player)),
        lambda state: (has_heavy_mod(state, player)),
    )
    set_rule_if_exists(
        "Lanayru Field Bridge Poe",
        lambda state: (
            state.has("Shadow Crystal", player)
            # and can_complete_MDH(state, player)
            # and can_complete_all_twilight(state, player)
        ),
    )
    set_rule_if_exists(
        "Lanayru Field Female Stag Beetle",
        lambda state: (
            state.has("Progressive Clawshot", player, 1)
            or state.has("Gale Boomerang", player)
        ),
        lambda state: (
            state.has("Progressive Clawshot", player, 1)
            or state.has("Gale Boomerang", player)
            or can_get_bug_with_lantern(state, player)
        ),
    )
    set_rule_if_exists(
        "Lanayru Field Male Stag Beetle",
        lambda state: (
            state.has("Progressive Clawshot", player, 1)
            or state.has("Gale Boomerang", player)
        ),
        lambda state: (
            state.has("Progressive Clawshot", player, 1)
            or state.has("Gale Boomerang", player)
            or can_get_bug_with_lantern(state, player)
        ),
    )
    set_rule_if_exists(
        "Lanayru Field Poe Grotto Left Poe",
        lambda state: (state.has("Shadow Crystal", player)),
    )
    set_rule_if_exists(
        "Lanayru Field Poe Grotto Right Poe",
        lambda state: (state.has("Shadow Crystal", player)),
    )
    set_rule_if_exists(
        "Lanayru Field Skulltula Grotto Chest",
        lambda state: (
            can_defeat_Skulltula(state, player)
            and state.has("Lantern", player)
            and can_break_wooden_door(state, player)
        ),
        lambda state: (
            state.has("Lantern", player) and can_break_wooden_door(state, player)
        ),
    )
    set_rule_if_exists(
        "Lanayru Field Spinner Track Chest",
        lambda state: (state.has("Spinner", player)),
        lambda state: (
            can_do_map_glitch(state, player)
            or (can_smash(state, player) and state.has("Spinner", player))
        ),
    )
    set_rule_if_exists(
        "Lanayru Ice Block Puzzle Cave Chest",
        lambda state: (state.has("Ball and Chain", player)),
    )
    set_rule_if_exists(
        "Lanayru Spring Back Room Lantern Chest",
        lambda state: (
            state.has("Progressive Clawshot", player, 1)
            and state.has("Lantern", player)
        ),
        lambda state: (
            state.has("Lantern", player)
            and (
                state.has("Progressive Clawshot", player, 1)
                or can_do_bs_moon_boots(state, player)
            )
        ),
    )
    set_rule_if_exists(
        "Lanayru Spring Back Room Left Chest",
        lambda state: (state.has("Progressive Clawshot", player, 1)),
        lambda state: (
            state.has("Progressive Clawshot", player, 1)
            or can_do_bs_moon_boots(state, player)
        ),
    )
    set_rule_if_exists(
        "Lanayru Spring Back Room Right Chest",
        lambda state: (state.has("Progressive Clawshot", player, 1)),
        lambda state: (
            state.has("Progressive Clawshot", player, 1)
            or can_do_bs_moon_boots(state, player)
        ),
    )
    set_rule_if_exists(
        "Lanayru Spring East Double Clawshot Chest",
        lambda state: (state.has("Progressive Clawshot", player, 2)),
    )
    set_rule_if_exists(
        "Lanayru Spring Underwater Left Chest",
        lambda state: (state.has("Iron Boots", player)),
        lambda state: (has_heavy_mod(state, player)),
    )
    set_rule_if_exists(
        "Lanayru Spring Underwater Right Chest",
        lambda state: (state.has("Iron Boots", player)),
        lambda state: (has_heavy_mod(state, player)),
    )
    set_rule_if_exists(
        "Lanayru Spring West Double Clawshot Chest",
        lambda state: (state.has("Progressive Clawshot", player, 2)),
    )
    set_rule_if_exists(
        "North Castle Town Golden Wolf",
        lambda state: (
            state.has("Shadow Crystal", player)
            and state.can_reach_region("Hidden Village", player)
            # and can_complete_MDH(state, player)
        ),
    )
    set_rule_if_exists("Outside Lanayru Spring Left Statue Chest", lambda state: (True))
    set_rule_if_exists(
        "Outside Lanayru Spring Right Statue Chest", lambda state: (True)
    )
    set_rule_if_exists(
        "Outside South Castle Town Double Clawshot Chasm Chest",
        lambda state: (state.has("Progressive Clawshot", player, 2)),
        lambda state: (
            state.has("Progressive Clawshot", player, 2)
            or (
                has_sword(state, player)
                and (
                    (
                        (
                            state._tp_damage_magnification(player)
                            == DamageMagnification.option_vanilla
                        )
                        or (
                            state._tp_damage_magnification(player)
                            == DamageMagnification.option_double
                        )
                    )
                    or can_use_bottled_fairy(state, player)
                )
            )
            or has_bombs(state, player)
            or state.has("Spinner", player)
            or state.has("Shadow Crystal", player)
        ),
    )
    set_rule_if_exists("Outside South Castle Town Female Ladybug", lambda state: (True))
    set_rule_if_exists(
        "Outside South Castle Town Fountain Chest",
        lambda state: (
            state.has("Spinner", player)
            and state.has("Progressive Clawshot", player, 1)
        ),
        lambda state: (
            (
                state.has("Spinner", player)
                and state.has("Progressive Clawshot", player, 1)
            )
            or (can_do_map_glitch(state, player) and has_bottle(state, player))
            or can_do_moon_boots(state, player)
            or can_do_bs_moon_boots(state, player)
            or can_do_lja(state, player)
            or (
                has_sword(state, player)
                and (
                    state.has("Progressive Hidden Skill", player, 3)
                    or has_bombs(state, player)
                )
            )
        ),
    )
    set_rule_if_exists(
        "Outside South Castle Town Golden Wolf",
        lambda state: (
            state.has("Shadow Crystal", player)
            and state.can_reach_region("North Faron Woods", player)
        ),
    )
    set_rule_if_exists("Outside South Castle Town Male Ladybug", lambda state: (True))
    set_rule_if_exists(
        "Outside South Castle Town Poe",
        lambda state: (state.has("Shadow Crystal", player)),
    )
    set_rule_if_exists(
        "Outside South Castle Town Tektite Grotto Chest",
        lambda state: (can_defeat_Tektite(state, player)),
    )
    set_rule_if_exists(
        "Outside South Castle Town Tightrope Chest",
        lambda state: (
            state.has("Progressive Clawshot", player, 1)
            and state.has("Shadow Crystal", player)
        ),
    )
    set_rule_if_exists(
        "Plumm Fruit Balloon Minigame",
        lambda state: (state.has("Shadow Crystal", player)),
    )
    set_rule_if_exists(
        "STAR Prize 1",
        lambda state: (state.has("Progressive Clawshot", player, 1)),
    )
    set_rule_if_exists(
        "STAR Prize 2",
        lambda state: (state.has("Progressive Clawshot", player, 2)),
    )
    set_rule_if_exists(
        "Telma Invoice",
        lambda state: (state.has("Renado's Letter", player)),
    )
    set_rule_if_exists("Upper Zoras River Female Dragonfly", lambda state: (True))
    set_rule_if_exists(
        "Upper Zoras River Poe",
        lambda state: (state.has("Shadow Crystal", player)),
    )
    set_rule_if_exists(
        "West Hyrule Field Female Butterfly",
        lambda state: (
            state.has("Progressive Clawshot", player, 1)
            or state.has("Gale Boomerang", player)
            or state.can_reach_region("Outside Castle Town West Grotto Ledge", player)
        ),
        lambda state: (
            state.has("Progressive Clawshot", player, 1)
            or state.has("Gale Boomerang", player)
            or can_do_map_glitch(state, player)
            or can_get_bug_with_lantern(state, player)
        ),
    )
    set_rule_if_exists(
        "West Hyrule Field Golden Wolf",
        lambda state: (
            state.has("Shadow Crystal", player)
            and state.can_reach_region("Upper Zoras River", player)
        ),
        lambda state: (
            state.has("Shadow Crystal", player)
            and state.can_reach_region("Zoras Domain", player)
        ),
    )
    set_rule_if_exists(
        "West Hyrule Field Helmasaur Grotto Chest",
        lambda state: (can_defeat_Helmasaur(state, player)),
    )
    set_rule_if_exists("West Hyrule Field Male Butterfly", lambda state: (True))
    set_rule_if_exists(
        "Wooden Statue",
        lambda state: (
            state.can_reach_region("Castle Town Doctors Office Lower", player)
            and state.has("Shadow Crystal", player)
            and state.can_reach_region("Castle Town South", player)
        ),
        lambda state: (state.has("Invoice", player)),
    )
    set_rule_if_exists(
        "Zoras Domain Chest Behind Waterfall",
        lambda state: (state.has("Shadow Crystal", player)),
        lambda state: (
            state.has("Shadow Crystal", player)
            or can_do_bs_moon_boots(state, player)
            or state.has("Spinner", player)
            or (has_bombs(state, player) and has_sword(state, player))
            or can_do_lja(state, player)
        ),
    )
    set_rule_if_exists(
        "Zoras Domain Chest By Mother and Child Isles", lambda state: (True)
    )
    set_rule_if_exists(
        "Zoras Domain Extinguish All Torches Chest",
        lambda state: (
            state.has("Gale Boomerang", player) and state.has("Iron Boots", player)
        ),
        lambda state: (
            state.has("Gale Boomerang", player) and has_heavy_mod(state, player)
        ),
    )
    set_rule_if_exists(
        "Zoras Domain Light All Torches Chest",
        lambda state: (
            state.has("Lantern", player) and state.has("Iron Boots", player)
        ),
        lambda state: (state.has("Lantern", player) and has_heavy_mod(state, player)),
    )
    set_rule_if_exists("Zoras Domain Male Dragonfly", lambda state: (True))
    set_rule_if_exists(
        "Zoras Domain Mother and Child Isle Poe",
        lambda state: (state.has("Shadow Crystal", player)),
    )
    set_rule_if_exists(
        "Zoras Domain Underwater Goron",
        lambda state: (
            can_use_water_bombs(state, player)
            and state.has("Iron Boots", player)
            and state.has("Zora Armor", player)
        ),
        lambda state: (
            can_use_water_bombs(state, player) and state.has("Iron Boots", player)
        ),
    )
    set_rule_if_exists(
        "Zoras Domain Waterfall Poe",
        lambda state: (state.has("Shadow Crystal", player)),
    )
    set_rule_if_exists(
        "Herding Goats Reward",
        lambda state: (
            # can_complete_prologue(state, player) and
            can_change_time(state, player)
        ),
        lambda state: True,  # (can_complete_prologue(state, player)),
    )
    set_rule_if_exists(
        "Links Basement Chest",
        lambda state: (state.has("Lantern", player)),
    )
    set_rule_if_exists(
        "Ordon Cat Rescue",
        lambda state: (
            state.can_reach_region("Ordon Village", player)
            and state.has("Progressive Fishing Rod", player, 1)
            and can_change_time(state, player)
        ),
        lambda state: (state.has("Progressive Fishing Rod", player, 1)),
    )
    set_rule_if_exists(
        "Ordon Ranch Grotto Lantern Chest",
        lambda state: (state.has("Lantern", player)),
    )
    set_rule_if_exists(
        "Ordon Shield",
        lambda state: (
            (
                # (
                #     (not state._tp_faron_twilight_cleared(player))
                #     and can_complete_prologue(state, player)
                # )
                # or (
                #     (state._tp_faron_twilight_cleared(player))
                #    and
                state.has("Shadow Crystal", player)
                # )
            )
            and (
                (not state._tp_bonks_do_damage(player))
                or (
                    (state._tp_bonks_do_damage(player))
                    and (
                        (
                            state._tp_damage_magnification(player)
                            != DamageMagnification.option_ohko
                        )
                        or can_use_bottled_fairies(state, player)
                    )
                )
            )
        ),
    )
    set_rule_if_exists(
        "Ordon Spring Golden Wolf",
        lambda state: (
            state.has("Shadow Crystal", player)
            and state.can_reach_region("Death Mountain Trail", player)
        ),
    )
    set_rule_if_exists(
        "Ordon Sword",
        lambda state: (
            True
            # can_complete_prologue(state, player)
            # or (state._tp_faron_twilight_cleared(player))
        ),
    )
    set_rule_if_exists("Sera Shop Slingshot", lambda state: (True))
    set_rule_if_exists(
        "Uli Cradle Delivery",
        lambda state: (can_change_time(state, player)),
        lambda state: (True),
    )
    set_rule_if_exists("Wooden Sword Chest", lambda state: (True))
    set_rule_if_exists("Wrestling With Bo", lambda state: (True))
    set_rule_if_exists("Ashei Sketch", lambda state: (True))
    set_rule_if_exists(
        "Snowboard Racing Prize",
        lambda state: (
            can_complete_snowpeak_ruins(state, player)
            and can_defeat_ShadowBeast(state, player)
        ),
        lambda state: (can_complete_snowpeak_ruins(state, player)),
    )
    set_rule_if_exists(
        "Snowpeak Above Freezard Grotto Poe",
        lambda state: (state.has("Shadow Crystal", player)),
        lambda state: (
            state.has("Shadow Crystal", player)
            and (
                state.has("Progressive Fishing Rod", player, 2)
                or (state._tp_skip_snowpeak_entrance(player))
                or can_do_map_glitch(state, player)
            )
        ),
    )
    set_rule_if_exists(
        "Snowpeak Blizzard Poe",
        lambda state: (state.has("Shadow Crystal", player)),
        lambda state: (
            state.has("Shadow Crystal", player)
            and (
                state.has("Progressive Fishing Rod", player, 2)
                or (state._tp_skip_snowpeak_entrance(player))
                or can_do_map_glitch(state, player)
            )
        ),
    )
    set_rule_if_exists(
        "Snowpeak Cave Ice Lantern Chest",
        lambda state: (
            state.has("Lantern", player) and state.has("Ball and Chain", player)
        ),
    )
    set_rule_if_exists(
        "Snowpeak Cave Ice Poe",
        lambda state: (
            state.has("Shadow Crystal", player) and state.has("Ball and Chain", player)
        ),
    )
    set_rule_if_exists(
        "Snowpeak Freezard Grotto Chest",
        lambda state: (state.has("Ball and Chain", player)),
        lambda state: (
            can_defeat_Freezard(state, player) and state.has("Ball and Chain", player)
        ),
    )
    set_rule_if_exists(
        "Snowpeak Icy Summit Poe",
        lambda state: (
            state.has("Shadow Crystal", player)
            and can_defeat_ShadowBeast(state, player)
            and (
                (not state._tp_bonks_do_damage(player))
                or (
                    (state._tp_bonks_do_damage(player))
                    and (
                        (
                            state._tp_damage_magnification(player)
                            != DamageMagnification.option_ohko
                        )
                        or can_use_bottled_fairy(state, player)
                    )
                )
            )
        ),
    )
    set_rule_if_exists(
        "Snowpeak Poe Among Trees",
        lambda state: (state.has("Shadow Crystal", player)),
        lambda state: (
            state.has("Shadow Crystal", player)
            and (
                state.has("Progressive Fishing Rod", player, 2)
                or (state._tp_skip_snowpeak_entrance(player))
                or can_do_map_glitch(state, player)
            )
        ),
    )
