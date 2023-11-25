from typing import Dict, Callable, TYPE_CHECKING

from BaseClasses import CollectionState
from .Items import exclusion_item_table, visit_locking_dict, DonaldAbility_Table, GoofyAbility_Table
from .Locations import exclusion_table, popups_set, Goofy_Checks, Donald_Checks
from .Names import LocationName, ItemName, RegionName
from worlds.generic.Rules import add_rule, forbid_items, add_item_rule
from .Logic import *

# I don't know what is going on here, but it works.
if TYPE_CHECKING:
    from . import KH2World
else:
    KH2World = object


# Shamelessly Stolen from Messanger


class KH2Rules:
    player: int
    world: KH2World
    # World Rules: Rules for the visit locks
    # Location Rules: Deterministic of player settings.
    # Form Rules: Rules for Drive Forms and Summon levels. These Are Locations
    # Fight Rules: Rules for fights. These are regions in the worlds.
    world_rules: Dict[str, Callable[[CollectionState], bool]]
    location_rules: Dict[str, Callable[[CollectionState], bool]]

    fight_rules: Dict[str, Callable[[CollectionState], bool]]

    def __init__(self, world: KH2World) -> None:
        self.player = world.player
        self.world = world
        self.multiworld = world.multiworld

    def lod_unlocked(self, state: CollectionState, Amount) -> bool:
        return state.has(ItemName.SwordoftheAncestor, self.player, Amount)

    def oc_unlocked(self, state: CollectionState, Amount) -> bool:
        return state.has(ItemName.BattlefieldsofWar, self.player, Amount)

    def twtnw_unlocked(self, state: CollectionState, Amount) -> bool:
        return state.has(ItemName.WaytotheDawn, self.player, Amount)

    def ht_unlocked(self, state: CollectionState, Amount) -> bool:
        return state.has(ItemName.BoneFist, self.player, Amount)

    def tt_unlocked(self, state: CollectionState, Amount) -> bool:
        return state.has(ItemName.IceCream, self.player, Amount)

    def pr_unlocked(self, state: CollectionState, Amount) -> bool:
        return state.has(ItemName.SkillandCrossbones, self.player, Amount)

    def sp_unlocked(self, state: CollectionState, Amount) -> bool:
        return state.has(ItemName.IdentityDisk, self.player, Amount)

    def stt_unlocked(self, state: CollectionState, Amount) -> bool:
        return state.has(ItemName.NamineSketches, self.player, Amount)

    def dc_unlocked(self, state: CollectionState, Amount) -> bool:
        return state.has(ItemName.CastleKey, self.player, Amount)  # Using Dummy 13 for this

    def hb_unlocked(self, state: CollectionState, Amount) -> bool:
        return state.has(ItemName.MembershipCard, self.player, Amount)

    def pl_unlocked(self, state: CollectionState, Amount) -> bool:
        return state.has(ItemName.ProudFang, self.player, Amount)

    def ag_unlocked(self, state: CollectionState, Amount) -> bool:
        return state.has(ItemName.Scimitar, self.player, Amount)

    def bc_unlocked(self, state: CollectionState, Amount) -> bool:
        return state.has(ItemName.BeastsClaw, self.player, Amount)

    def at_three_unlocked(self, state: CollectionState) -> bool:
        return state.has(ItemName.MagnetElement, self.player, 2)

    def at_four_unlocked(self, state: CollectionState) -> bool:
        return state.has(ItemName.ThunderElement, self.player, 3)

    def hundred_acre_unlocked(self, state: CollectionState, amount) -> bool:
        return state.has(ItemName.TornPages, self.player, amount)

    def level_locking_unlock(self, state: CollectionState, amount):
        return amount <= sum([state.count(item_name, self.player) for item_name in visit_locking_dict["2VisitLocking"]])

    def summon_levels_unlocked(self, state: CollectionState, amount) -> bool:
        return amount <= sum([state.count(item_name, self.player) for item_name in summons])

    def kh2_list_count_sum(self, item_name_set: list, state: CollectionState) -> int:
        """
        Returns the sum of state.count() for each item in the list.
        """
        return sum(
                [state.count(item_name, self.player) for item_name in item_name_set]
        )

    def kh2_list_any_sum(self, list_of_item_name_list: list, state: CollectionState) -> int:
        """
        Returns sum that increments by 1 if state.has_any
        """
        return sum(
                [1 for item_list in list_of_item_name_list if
                 state.has_any(set(item_list), self.player)]
        )

    def kh2_dict_count(self, item_name_to_count: dict, state: CollectionState) -> bool:
        """
        simplifies count to a dictionary.
        """
        return all(
                [state.count(item_name, self.player) >= item_amount for item_name, item_amount in
                 item_name_to_count.items()]
        )

    def kh2_dict_one_count(self, item_name_to_count: dict, state: CollectionState) -> int:
        """
        simplifies count to a dictionary.
        """
        return sum(
                [1 for item_name, item_amount in
                 item_name_to_count.items() if state.count(item_name, self.player) >= item_amount]
        )

    def kh2_can_reach_any(self, loc_set: list, state: CollectionState):
        """
        Can reach any locations in the set.
        """
        return any(
                [self.kh2_can_reach(location, state) for location in
                 loc_set]
        )

    def kh2_can_reach_all(self, loc_list: list, state: CollectionState):
        """
        Can reach all locations in the set.
        """
        return all(
                [self.kh2_can_reach(location, state) for location in loc_list]
        )

    def kh2_can_reach(self, loc: str, state: CollectionState):
        """
        Returns bool instead of collection state.
        """
        return state.can_reach(self.multiworld.get_location(loc, self.player), "location", self.player)

    def kh2_has_all(self, items: list, state: CollectionState):
        """If state has at least one of all."""
        return state.has_all(set(items), self.player)

    def kh2_has_any(self, items: list, state: CollectionState):
        return state.has_any(set(items), self.player)

    def form_list_unlock(self, state: CollectionState, parent_form_list, level_required, fight_logic=False) -> bool:
        form_access = {parent_form_list}
        if self.multiworld.AutoFormLogic[self.player] and state.has(ItemName.SecondChance, self.player) and not fight_logic:
            if parent_form_list == ItemName.MasterForm:
                if state.has(ItemName.DriveConverter, self.player):
                    form_access.add(auto_form_dict[parent_form_list])
            else:
                form_access.add(auto_form_dict[parent_form_list])
        return state.has_any(form_access, self.player) \
            and self.get_form_level_requirement(state, level_required)

    def get_form_level_requirement(self, state, amount):
        forms_available = 0
        form_list = [ItemName.ValorForm, ItemName.WisdomForm, ItemName.LimitForm, ItemName.MasterForm,
                     ItemName.FinalForm]
        if self.world.multiworld.FinalFormLogic[self.player] != "no_light_and_darkness":
            if self.world.multiworld.FinalFormLogic[self.player] == "light_and_darkness":
                if state.has(ItemName.LightDarkness, self.player) and state.has_any(set(form_list), self.player):
                    forms_available += 1
                    form_list.remove(ItemName.FinalForm)
            else:  # self.multiworld.FinalFormLogic=="just a form"
                form_list.remove(ItemName.FinalForm)
                if state.has_any(form_list, self.player):
                    forms_available += 1
        forms_available += sum([1 for form in form_list if state.has(form, self.player)])
        return forms_available >= amount


class KH2WorldRules(KH2Rules):
    def __init__(self, kh2world: KH2World) -> None:
        # These Rules are Always in effect
        super().__init__(kh2world)
        self.region_rules = {
            RegionName.LoD:                lambda state: self.lod_unlocked(state, 1),
            RegionName.LoD2:               lambda state: self.lod_unlocked(state, 2),

            RegionName.Oc:                 lambda state: self.oc_unlocked(state, 1),
            RegionName.Oc2:                lambda state: self.oc_unlocked(state, 2),

            RegionName.Twtnw2:             lambda state: self.twtnw_unlocked(state, 2),
            # These will be swapped and First Visit lock for twtnw is in development.
            # RegionName.Twtnw1: lambda state: self.lod_unlocked(state, 2),

            RegionName.Ht:                 lambda state: self.ht_unlocked(state, 1),
            RegionName.Ht2:                lambda state: self.ht_unlocked(state, 2),

            RegionName.Tt:                 lambda state: self.tt_unlocked(state, 1),
            RegionName.Tt2:                lambda state: self.tt_unlocked(state, 2),
            RegionName.Tt3:                lambda state: self.tt_unlocked(state, 3),

            RegionName.Pr:                 lambda state: self.pr_unlocked(state, 1),
            RegionName.Pr2:                lambda state: self.pr_unlocked(state, 2),

            RegionName.Sp:                 lambda state: self.sp_unlocked(state, 1),
            RegionName.Sp2:                lambda state: self.sp_unlocked(state, 2),

            RegionName.Stt:                lambda state: self.stt_unlocked(state, 1),

            RegionName.Dc:                 lambda state: self.dc_unlocked(state, 1),
            RegionName.Tr:                 lambda state: self.dc_unlocked(state, 2),
            #  Terra is a fight and can have more than just this requirement.
            # RegionName.Terra:      lambda state:state.has(ItemName.ProofofConnection,self.player),

            RegionName.Hb:                 lambda state: self.hb_unlocked(state, 1),
            RegionName.Hb2:                lambda state: self.hb_unlocked(state, 2),
            RegionName.Mushroom13:         lambda state: state.has(ItemName.ProofofPeace, self.player),

            RegionName.Pl:                 lambda state: self.pl_unlocked(state, 1),
            RegionName.Pl2:                lambda state: self.pl_unlocked(state, 2),

            RegionName.Ag:                 lambda state: self.ag_unlocked(state, 1),
            RegionName.Ag2:                lambda state: self.ag_unlocked(state, 2),

            RegionName.Bc:                 lambda state: self.bc_unlocked(state, 1),
            RegionName.Bc2:                lambda state: self.bc_unlocked(state, 2),

            RegionName.AtlanticaSongThree: lambda state: self.at_three_unlocked(state),
            RegionName.AtlanticaSongFour:  lambda state: self.at_four_unlocked(state),

            RegionName.Ha1:                lambda state: True,
            RegionName.Ha2:                lambda state: self.hundred_acre_unlocked(state, 1),
            RegionName.Ha3:                lambda state: self.hundred_acre_unlocked(state, 2),
            RegionName.Ha4:                lambda state: self.hundred_acre_unlocked(state, 3),
            RegionName.Ha5:                lambda state: self.hundred_acre_unlocked(state, 4),
            RegionName.Ha6:                lambda state: self.hundred_acre_unlocked(state, 5),

            RegionName.LevelsVS1:          lambda state: self.level_locking_unlock(state, 1),
            RegionName.LevelsVS3:          lambda state: self.level_locking_unlock(state, 3),
            RegionName.LevelsVS6:          lambda state: self.level_locking_unlock(state, 6),
            RegionName.LevelsVS9:          lambda state: self.level_locking_unlock(state, 9),
            RegionName.LevelsVS12:         lambda state: self.level_locking_unlock(state, 12),
            RegionName.LevelsVS15:         lambda state: self.level_locking_unlock(state, 15),
            RegionName.LevelsVS18:         lambda state: self.level_locking_unlock(state, 18),
            RegionName.LevelsVS21:         lambda state: self.level_locking_unlock(state, 21),
            RegionName.LevelsVS24:         lambda state: self.level_locking_unlock(state, 24),
            RegionName.LevelsVS26:         lambda state: self.level_locking_unlock(state, 26),
        }

    def set_kh2_rules(self) -> None:
        for region_name, rules in self.region_rules.items():
            region = self.multiworld.get_region(region_name, self.player)
            for entrance in region.entrances:
                entrance.access_rule = rules

        self.set_kh2_goal()

        weapon_region = self.multiworld.get_region(RegionName.Keyblade, self.player)
        for location in weapon_region.locations:
            add_rule(location, lambda state: state.has(exclusion_table["WeaponSlots"][location.name], self.player))
            if location.name in Goofy_Checks:
                add_item_rule(location, lambda item: item.player == self.player and item.name in GoofyAbility_Table.keys())
            elif location.name in Donald_Checks:
                add_item_rule(location, lambda item: item.player == self.player and item.name in DonaldAbility_Table.keys())

    def set_kh2_goal(self):

        final_xemnas_location = self.multiworld.get_location(LocationName.FinalXemnas, self.player)
        if self.multiworld.Goal[self.player] == "three_proofs":
            final_xemnas_location.access_rule = lambda state: self.kh2_has_all(three_proofs, state)
            if self.multiworld.FinalXemnas[self.player]:
                self.multiworld.completion_condition[self.player] = lambda state: state.has(ItemName.Victory, self.player, 1)
            else:
                self.multiworld.completion_condition[self.player] = lambda state: self.kh2_has_all(three_proofs, state)
        # lucky emblem hunt
        elif self.multiworld.Goal[self.player] == "lucky_emblem_hunt":
            final_xemnas_location.access_rule = lambda state: state.has(ItemName.LuckyEmblem, self.player, self.multiworld.LuckyEmblemsRequired[self.player].value)
            if self.multiworld.FinalXemnas[self.player]:
                self.multiworld.completion_condition[self.player] = lambda state: state.has(ItemName.Victory, self.player, 1)
            else:
                self.multiworld.completion_condition[self.player] = lambda state: state.has(ItemName.LuckyEmblem, self.player, self.multiworld.LuckyEmblemsRequired[self.player].value)
        # hitlist if == 2
        elif self.multiworld.Goal[self.player] == "hitlist":
            final_xemnas_location.access_rule = lambda state: state.has(ItemName.Bounty, self.player, self.multiworld.BountyRequired[self.player].value)
            if self.multiworld.FinalXemnas[self.player]:
                self.multiworld.completion_condition[self.player] = lambda state: state.has(ItemName.Victory, self.player, 1)
            else:
                self.multiworld.completion_condition[self.player] = lambda state: state.has(ItemName.Bounty, self.player, self.multiworld.BountyRequired[self.player].value)
        else:
            final_xemnas_location.access_rule = lambda state: state.has(ItemName.Bounty, self.player, self.multiworld.BountyRequired[self.player].value) and\
                                  state.has(ItemName.LuckyEmblem, self.player, self.multiworld.LuckyEmblemsRequired[self.player].value)
            if self.multiworld.FinalXemnas[self.player]:
                self.multiworld.completion_condition[self.player] = lambda state: state.has(ItemName.Victory, self.player, 1)
            else:
                self.multiworld.completion_condition[self.player] = lambda state: state.has(ItemName.Bounty, self.player, self.multiworld.BountyRequired[self.player].value) and \
                                                                                  state.has(ItemName.LuckyEmblem, self.player, self.multiworld.LuckyEmblemsRequired[self.player].value)


class KH2FormRules(KH2Rules):
    #: Dict[str, Callable[[CollectionState], bool]]
    def __init__(self, world: KH2World) -> None:
        super().__init__(world)
        # access rules on where you can level a form.

        self.form_rules = {
            LocationName.Valorlvl2:  lambda state: self.form_list_unlock(state, ItemName.ValorForm, 0),
            LocationName.Valorlvl3:  lambda state: self.form_list_unlock(state, ItemName.ValorForm, 1),
            LocationName.Valorlvl4:  lambda state: self.form_list_unlock(state, ItemName.ValorForm, 2),
            LocationName.Valorlvl5:  lambda state: self.form_list_unlock(state, ItemName.ValorForm, 3),
            LocationName.Valorlvl6:  lambda state: self.form_list_unlock(state, ItemName.ValorForm, 4),
            LocationName.Valorlvl7:  lambda state: self.form_list_unlock(state, ItemName.ValorForm, 5),
            LocationName.Wisdomlvl2: lambda state: self.form_list_unlock(state, ItemName.WisdomForm, 0),
            LocationName.Wisdomlvl3: lambda state: self.form_list_unlock(state, ItemName.WisdomForm, 1),
            LocationName.Wisdomlvl4: lambda state: self.form_list_unlock(state, ItemName.WisdomForm, 2),
            LocationName.Wisdomlvl5: lambda state: self.form_list_unlock(state, ItemName.WisdomForm, 3),
            LocationName.Wisdomlvl6: lambda state: self.form_list_unlock(state, ItemName.WisdomForm, 4),
            LocationName.Wisdomlvl7: lambda state: self.form_list_unlock(state, ItemName.WisdomForm, 5),
            LocationName.Limitlvl2:  lambda state: self.form_list_unlock(state, ItemName.LimitForm, 0),
            LocationName.Limitlvl3:  lambda state: self.form_list_unlock(state, ItemName.LimitForm, 1),
            LocationName.Limitlvl4:  lambda state: self.form_list_unlock(state, ItemName.LimitForm, 2),
            LocationName.Limitlvl5:  lambda state: self.form_list_unlock(state, ItemName.LimitForm, 3),
            LocationName.Limitlvl6:  lambda state: self.form_list_unlock(state, ItemName.LimitForm, 4),
            LocationName.Limitlvl7:  lambda state: self.form_list_unlock(state, ItemName.LimitForm, 5),
            LocationName.Masterlvl2: lambda state: self.form_list_unlock(state, ItemName.MasterForm, 0),
            LocationName.Masterlvl3: lambda state: self.form_list_unlock(state, ItemName.MasterForm, 1),
            LocationName.Masterlvl4: lambda state: self.form_list_unlock(state, ItemName.MasterForm, 2),
            LocationName.Masterlvl5: lambda state: self.form_list_unlock(state, ItemName.MasterForm, 3),
            LocationName.Masterlvl6: lambda state: self.form_list_unlock(state, ItemName.MasterForm, 4),
            LocationName.Masterlvl7: lambda state: self.form_list_unlock(state, ItemName.MasterForm, 5),
            LocationName.Finallvl2:  lambda state: self.form_list_unlock(state, ItemName.FinalForm, 0),
            LocationName.Finallvl3:  lambda state: self.form_list_unlock(state, ItemName.FinalForm, 1),
            LocationName.Finallvl4:  lambda state: self.form_list_unlock(state, ItemName.FinalForm, 2),
            LocationName.Finallvl5:  lambda state: self.form_list_unlock(state, ItemName.FinalForm, 3),
            LocationName.Finallvl6:  lambda state: self.form_list_unlock(state, ItemName.FinalForm, 4),
            LocationName.Finallvl7:  lambda state: self.form_list_unlock(state, ItemName.FinalForm, 5),
            LocationName.Summonlvl2: lambda state: self.summon_levels_unlocked(state, 1),
            LocationName.Summonlvl3: lambda state: self.summon_levels_unlocked(state, 1),
            LocationName.Summonlvl4: lambda state: self.summon_levels_unlocked(state, 2),
            LocationName.Summonlvl5: lambda state: self.summon_levels_unlocked(state, 3),
            LocationName.Summonlvl6: lambda state: self.summon_levels_unlocked(state, 4),
            LocationName.Summonlvl7: lambda state: self.summon_levels_unlocked(state, 4),
        }
        self.form_region_rules = {
            RegionName.Valor:  lambda state: self.multi_form_region_access(),
            RegionName.Wisdom: lambda state: self.multi_form_region_access(),
            RegionName.Limit:  lambda state: self.limit_form_region_access(),
            RegionName.Master: lambda state: self.multi_form_region_access(),
            RegionName.Final:  lambda state: self.final_form_region_access(state)
        }

    def final_form_region_access(self, state: CollectionState) -> bool:
        """
        Can reach one of TT3,Twtnw post Roxas, BC2, LoD2 or PR2
        """
        # tt3 start, can beat roxas, can beat gr2, can beat xaldin, can beat storm rider.

        return any(
                self.multiworld.get_location(location, self.player).can_reach(state) for location in
                final_leveling_access
        )

    @staticmethod
    def limit_form_region_access() -> bool:
        """
        returns true since twtnw always is open and has enemies
        """
        return True

    @staticmethod
    def multi_form_region_access() -> bool:
        """
        returns true since twtnw always is open and has enemies
        Valor, Wisdom and Master Form region access.
        Note: This does not account for having the drive form. See form_list_unlock
        """
        # todo: if boss enemy start the player with oc stone because of cerb
        return True

    def set_kh2_form_rules(self):
        for region_name in drive_form_list:
            if region_name == RegionName.Summon and not self.world.options.SummonLevelLocationToggle:
                continue
            # could get the location of each of these, but I feel like that would be less optimal
            region = self.multiworld.get_region(region_name, self.player)
            # if region_name in form_region_rules
            if region_name != RegionName.Summon:
                for entrance in region.entrances:
                    entrance.access_rule = self.form_region_rules[region_name]
            for loc in region.locations:
                loc.access_rule = self.form_rules[loc.name]


class KH2FightRules(KH2Rules):
    player: int
    world: KH2World
    region_rules: Dict[str, Callable[[CollectionState], bool]]
    location_rules: Dict[str, Callable[[CollectionState], bool]]

    # cor logic
    # have 3 things for the logic
    # region:movement_rules and (fight_rules or skip rules)
    # if skip rules are of return false
    def __init__(self, world: KH2World) -> None:
        super().__init__(world)
        self.fight_logic = self.multiworld.FightLogic[self.player].current_key

        self.fight_region_rules = {
            RegionName.ShanYu:            lambda state: self.get_shan_yu_rules(state),
            RegionName.AnsemRiku:         lambda state: self.get_ansem_riku_rules(state),
            RegionName.StormRider:        lambda state: self.get_storm_rider_rules(state),
            RegionName.DataXigbar:        lambda state: self.get_data_xigbar_rules(state),
            RegionName.TwinLords:         lambda state: self.get_fire_lord_rules(state) and self.get_blizzard_lord_rules(state),
            RegionName.GenieJafar:        lambda state: self.get_genie_jafar_rules(state),
            RegionName.DataLexaeus:       lambda state: self.get_data_lexaeus_rules(state),
            RegionName.OldPete:           lambda state: self.get_old_pete_rules(),
            RegionName.FuturePete:        lambda state: self.get_future_pete_rules(state),
            RegionName.Terra:             lambda state: self.get_terra_rules(state),
            RegionName.DataMarluxia:      lambda state: self.get_data_marluxia_rules(state),
            RegionName.Barbosa:           lambda state: self.get_barbosa_rules(state),
            RegionName.GrimReaper1:       lambda state: self.get_grim_reaper1_rules(),
            RegionName.GrimReaper2:       lambda state: self.get_grim_reaper2_rules(state),
            RegionName.DataLuxord:        lambda state: self.get_data_luxord_rules(state),
            RegionName.Cerberus:          lambda state: self.get_cerberus_rules(state),
            RegionName.OlympusPete:       lambda state: self.get_olympus_pete_rules(state),
            RegionName.Hydra:             lambda state: self.get_hydra_rules(state),
            RegionName.Hades:             lambda state: self.get_hades_rules(state),
            RegionName.DataZexion:        lambda state: self.get_data_zexion_rules(state),
            RegionName.OcPainAndPanicCup: lambda state: self.get_pain_and_panic_cup_rules(state),
            RegionName.OcCerberusCup:     lambda state: self.get_cerberus_cup_rules(state),
            RegionName.Oc2TitanCup:       lambda state: self.get_titan_cup_rules(state),
            RegionName.Oc2GofCup:         lambda state: self.get_goddess_of_fate_cup_rules(state),
            RegionName.HadesCups:         lambda state: self.get_hades_cup_rules(state),
            RegionName.Thresholder:       lambda state: self.get_thresholder_rules(state),
            RegionName.Beast:             lambda state: self.get_beast_rules(),
            RegionName.DarkThorn:         lambda state: self.get_dark_thorn_rules(state),
            RegionName.Xaldin:            lambda state: self.get_xaldin_rules(state),
            RegionName.DataXaldin:        lambda state: self.get_data_xaldin_rules(state),
            RegionName.HostileProgram:    lambda state: self.get_hostile_program_rules(state),
            RegionName.Mcp:               lambda state: self.get_mcp_rules(state),
            RegionName.DataLarxene:       lambda state: self.get_data_larxene_rules(state),
            RegionName.PrisonKeeper:      lambda state: self.get_prison_keeper_rules(state),
            RegionName.OogieBoogie:       lambda state: self.get_oogie_rules(),
            RegionName.Experiment:        lambda state: self.get_experiment_rules(state),
            RegionName.DataVexen:         lambda state: self.get_data_vexen_rules(state),
            RegionName.HBDemyx:           lambda state: self.get_demyx_rules(state),
            RegionName.ThousandHeartless: lambda state: self.get_thousand_heartless_rules(state),
            RegionName.DataDemyx:         lambda state: self.get_data_demyx_rules(state),
            RegionName.Sephi:             lambda state: self.get_sephiroth_rules(state),
            RegionName.CorFirstFight:     lambda state: self.get_cor_first_fight_movement_rules(state) and (self.get_cor_first_fight_rules(state) or self.get_cor_skip_first_rules(state)),
            RegionName.CorSecondFight:    lambda state: self.get_cor_second_fight_movement_rules(state),
            RegionName.Transport:         lambda state: self.get_transport_movement_rules(state),
            RegionName.Scar:              lambda state: self.get_scar_rules(state),
            RegionName.GroundShaker:      lambda state: self.get_groundshaker_rules(state),
            RegionName.DataSaix:          lambda state: self.get_data_saix_rules(state),
            RegionName.TwilightThorn:     lambda state: self.get_twilight_thorn_rules(),
            RegionName.Axel1:             lambda state: self.get_axel_one_rules(),
            RegionName.Axel2:             lambda state: self.get_axel_two_rules(),
            RegionName.DataRoxas:         lambda state: self.get_data_roxas_rules(state),
            RegionName.DataAxel:          lambda state: self.get_data_axel_rules(state),
            RegionName.Roxas:             lambda state: self.get_roxas_rules(state) and self.twtnw_unlocked(state, 1),
            RegionName.Xigbar:            lambda state: self.get_xigbar_rules(state),
            RegionName.Luxord:            lambda state: self.get_luxord_rules(state),
            RegionName.Saix:              lambda state: self.get_saix_rules(state),
            RegionName.Xemnas:            lambda state: self.get_xemnas_rules(state),
            RegionName.ArmoredXemnas:     lambda state: self.get_armored_xemnas_one_rules(state),
            RegionName.ArmoredXemnas2:    lambda state: self.get_armored_xemnas_two_rules(state),
            RegionName.FinalXemnas:       lambda state: self.get_final_xemnas_rules(state),
            RegionName.DataXemnas:        lambda state: self.get_data_xemnas_rules(state),
        }

    def set_kh2_fight_rules(self) -> None:
        for region_name, rules in self.fight_region_rules.items():
            region = self.multiworld.get_region(region_name, self.player)
            for entrance in region.entrances:
                entrance.access_rule = rules

        for loc_name in [LocationName.TransportEventLocation, LocationName.TransporttoRemembrance]:
            location = self.multiworld.get_location(loc_name, self.player)
            add_rule(location, lambda state: self.get_transport_fight_rules(state))

    def get_shan_yu_rules(self, state: CollectionState) -> bool:
        # easy: gap closer, defensive tool,drive form
        # normal: 2 out of easy
        # hard: defensive tool or drive form
        shan_yu_rules = {
            "easy":   self.kh2_list_any_sum([gap_closer, defensive_tool, form_list], state) >= 3,
            "normal": self.kh2_list_any_sum([gap_closer, defensive_tool, form_list], state) >= 2,
            "hard":   self.kh2_list_any_sum([defensive_tool, form_list], state) >= 1
        }
        return shan_yu_rules[self.fight_logic]

    def get_ansem_riku_rules(self, state: CollectionState) -> bool:
        # easy: gap closer,defensive tool,ground finisher/limit form 
        # normal: defensive tool and (gap closer/ground finisher/limit form)
        # hard: defensive tool or limit form
        ansem_riku_rules = {
            "easy":   self.kh2_list_any_sum([gap_closer, defensive_tool, [ItemName.LimitForm], ground_finisher], state) >= 3,
            "normal": self.kh2_list_any_sum([gap_closer, defensive_tool, [ItemName.LimitForm], ground_finisher], state) >= 2,
            "hard":   self.kh2_has_any([ItemName.ReflectElement, ItemName.Guard, ItemName.LimitForm], state),
        }
        return ansem_riku_rules[self.fight_logic]

    def get_storm_rider_rules(self, state: CollectionState) -> bool:
        # easy: has defensive tool,drive form, party limit,aerial move
        # normal: has 3 of those things
        # hard: has 2 of those things 
        storm_rider_rules = {
            "easy":   self.kh2_list_any_sum([defensive_tool, party_limit, aerial_move, form_list], state) >= 4,
            "normal": self.kh2_list_any_sum([defensive_tool, party_limit, aerial_move, form_list], state) >= 3,
            "hard":   self.kh2_list_any_sum([defensive_tool, party_limit, aerial_move, form_list], state) >= 2,
        }
        return storm_rider_rules[self.fight_logic]

    def get_data_xigbar_rules(self, state: CollectionState) -> bool:
        # easy:final 7,firaga,2 air combo plus,air gap closer, finishing plus,guard,reflega,horizontal slash,donald limit
        # normal:final 7,firaga,finishing plus,guard,reflect horizontal slash,donald limit
        # hard:((final 5, fira) or donald limit), finishing plus,guard/reflect
        data_xigbar_rules = {
            "easy":   self.kh2_dict_count(easy_data_xigbar_tools, state) and self.form_list_unlock(state, ItemName.FinalForm, 5, True) and self.kh2_has_any(donald_limit, state),
            "normal": self.kh2_dict_count(normal_data_xigbar_tools, state) and self.form_list_unlock(state, ItemName.FinalForm, 5, True) and self.kh2_has_any(donald_limit, state),
            "hard":   ((self.form_list_unlock(state, ItemName.FinalForm, 3, True) and state.has(ItemName.FireElement, self.player, 2)) or self.kh2_has_any(donald_limit, state))
                      and state.has(ItemName.FinishingPlus, self.player) and self.kh2_has_any(defensive_tool, state)
        }
        return data_xigbar_rules[self.fight_logic]

    def get_fire_lord_rules(self, state: CollectionState) -> bool:
        # easy: drive form,defensive tool,one black magic,party limit
        # normal: 3 of those things
        # hard:2 of those things
        # duplicate of the other because in boss rando there will be to bosses in arena and these bosses can be split.
        fire_lords_rules = {
            "easy":   self.kh2_list_any_sum([form_list, defensive_tool, black_magic, party_limit], state) >= 4,
            "normal": self.kh2_list_any_sum([form_list, defensive_tool, black_magic, party_limit], state) >= 3,
            "hard":   self.kh2_list_any_sum([form_list, defensive_tool, black_magic, party_limit], state) >= 2,
        }
        return fire_lords_rules[self.fight_logic]

    def get_blizzard_lord_rules(self, state: CollectionState) -> bool:
        # easy: drive form,defensive tool,one black magic,party limit
        # normal: 3 of those things
        # hard:2 of those things
        # duplicate of the other because in boss rando there will be to bosses in arena and these bosses can be split.
        blizzard_lords_rules = {
            "easy":   self.kh2_list_any_sum([form_list, defensive_tool, black_magic, party_limit], state) >= 4,
            "normal": self.kh2_list_any_sum([form_list, defensive_tool, black_magic, party_limit], state) >= 3,
            "hard":   self.kh2_list_any_sum([form_list, defensive_tool, black_magic, party_limit], state) >= 2,
        }
        return blizzard_lords_rules[self.fight_logic]

    def get_genie_jafar_rules(self, state: CollectionState) -> bool:
        # easy: defensive tool,black magic,ground finisher,finishing plus
        # normal: defensive tool, ground finisher,finishing plus
        # hard: defensive tool,finishing plus
        genie_jafar_rules = {
            "easy":   self.kh2_list_any_sum([defensive_tool, black_magic, ground_finisher, {ItemName.FinishingPlus}], state) >= 4,
            "normal": self.kh2_list_any_sum([defensive_tool, ground_finisher, {ItemName.FinishingPlus}], state) >= 3,
            "hard":   self.kh2_list_any_sum([defensive_tool, {ItemName.FinishingPlus}], state) >= 2,
        }
        return genie_jafar_rules[self.fight_logic]

    def get_data_lexaeus_rules(self, state: CollectionState) -> bool:
        # easy:both gap closers,final 7,firaga,reflera,donald limit, guard
        # normal:one gap closer,final 5,fira,reflect, donald limit,guard
        # hard:defensive tool,gap closer
        data_lexaues_rules = {
            "easy":   self.kh2_dict_count(easy_data_lex_tools, state) and self.form_list_unlock(state, ItemName.FinalForm, 5, True) and self.kh2_list_any_sum([donald_limit], state) >= 1,
            "normal": self.kh2_dict_count(normal_data_lex_tools, state) and self.form_list_unlock(state, ItemName.FinalForm, 3, True) and self.kh2_list_any_sum([donald_limit, gap_closer], state) >= 2,
            "hard":   self.kh2_list_any_sum([defensive_tool, gap_closer], state) >= 2,
        }
        return data_lexaues_rules[self.fight_logic]

    @staticmethod
    def get_old_pete_rules():
        # fight is free.
        return True

    def get_future_pete_rules(self, state: CollectionState) -> bool:
        # easy:defensive option,gap closer,drive form
        # norma:2 of those things
        # hard 1 of those things
        future_pete_rules = {
            "easy":   self.kh2_list_any_sum([defensive_tool, gap_closer, form_list], state) >= 3,
            "normal": self.kh2_list_any_sum([defensive_tool, gap_closer, form_list], state) >= 2,
            "hard":   self.kh2_list_any_sum([defensive_tool, gap_closer, form_list], state) >= 1,
        }
        return future_pete_rules[self.fight_logic]

    def get_data_marluxia_rules(self, state: CollectionState) -> bool:
        # easy:both gap closers,final 7,firaga,reflera,donald limit, guard
        # normal:one gap closer,final 5,fira,reflect, donald limit,guard
        # hard:defensive tool,gap closer
        data_marluxia_rules = {
            "easy":   self.kh2_dict_count(easy_data_marluxia_tools, state) and self.form_list_unlock(state, ItemName.FinalForm, 5, True) and self.kh2_list_any_sum([donald_limit], state) >= 1,
            "normal": self.kh2_dict_count(normal_data_marluxia_tools, state) and self.form_list_unlock(state, ItemName.FinalForm, 3, True) and self.kh2_list_any_sum([donald_limit, gap_closer], state) >= 2,
            "hard":   self.kh2_list_any_sum([defensive_tool, gap_closer, [ItemName.AerialRecovery]], state) >= 3,
        }
        return data_marluxia_rules[self.fight_logic]

    def get_terra_rules(self, state: CollectionState) -> bool:
        # easy:scom,gap closers,explosion,2 combo pluses,final 7,firaga, donald limits,reflect,guard,3 dodge roll,3 aerial dodge and 3glide
        # normal:gap closers,explosion,2 combo pluses,2 dodge roll,2 aerial dodge and lvl 2glide,guard,donald limit, guard
        # hard:1 gap closer,explosion,2 combo pluses,2 dodge roll,2 aerial dodge and lvl 2glide,guard
        terra_rules = {
            "easy":   self.kh2_dict_count(easy_terra_tools, state) and self.form_list_unlock(state, ItemName.FinalForm, 5, True),
            "normal": self.kh2_dict_count(normal_terra_tools, state) and self.kh2_list_any_sum([donald_limit], state) >= 1,
            "hard":   self.kh2_dict_count(hard_terra_tools, state) and self.kh2_list_any_sum([gap_closer], state) >= 1,
        }
        return terra_rules[self.fight_logic]

    def get_barbosa_rules(self, state: CollectionState) -> bool:
        # easy:blizzara and thundara or one of each,defensive tool
        # normal:(blizzard or thunder) and defensive tool
        # hard: defensive tool
        barbosa_rules = {
            "easy":   self.kh2_list_count_sum([ItemName.BlizzardElement, ItemName.ThunderElement], state) >= 2 and self.kh2_list_any_sum([defensive_tool], state) >= 1,
            "normal": self.kh2_list_any_sum([defensive_tool, {ItemName.BlizzardElement, ItemName.ThunderElement}], state) >= 2,
            "hard":   self.kh2_list_any_sum([defensive_tool], state) >= 1,
        }
        return barbosa_rules[self.fight_logic]

    @staticmethod
    def get_grim_reaper1_rules():
        # fight is free.
        return True

    def get_grim_reaper2_rules(self, state: CollectionState) -> bool:
        # easy:master form,thunder,defensive option
        # normal:master form/stitch,thunder,defensive option
        # hard:any black magic,defensive option.
        gr2_rules = {
            "easy":   self.kh2_list_any_sum([defensive_tool, {ItemName.MasterForm, ItemName.ThunderElement}], state) >= 2,
            "normal": self.kh2_list_any_sum([defensive_tool, {ItemName.MasterForm, ItemName.Stitch}, {ItemName.ThunderElement}], state) >= 3,
            "hard":   self.kh2_list_any_sum([black_magic, defensive_tool], state) >= 2
        }
        return gr2_rules[self.fight_logic]

    def get_data_luxord_rules(self, state: CollectionState) -> bool:
        # easy:gap closers,reflega,aerial dodge lvl 2,glide lvl 2,guard
        # normal:1 gap closer,reflect,aerial dodge lvl 1,glide lvl 1,guard
        # hard:quick run,defensive option
        data_luxord_rules = {
            "easy":   self.kh2_dict_count(easy_data_luxord_tools, state),
            "normal": self.kh2_has_all([ItemName.ReflectElement, ItemName.AerialDodge, ItemName.Glide, ItemName.Guard], state) and self.kh2_has_any(defensive_tool, state),
            "hard":   self.kh2_list_any_sum([{ItemName.QuickRun}, defensive_tool], state)
        }
        return data_luxord_rules[self.fight_logic]

    def get_cerberus_rules(self, state: CollectionState) -> bool:
        # easy,normal:defensive option, offensive magic
        # hard:defensive option
        cerberus_rules = {
            "easy":   self.kh2_list_any_sum([defensive_tool, black_magic], state) >= 2,
            "normal": self.kh2_list_any_sum([defensive_tool, black_magic], state) >= 2,
            "hard":   self.kh2_has_any(defensive_tool, state),
        }
        return cerberus_rules[self.fight_logic]

    def get_pain_and_panic_cup_rules(self, state: CollectionState) -> bool:
        # easy:2 party limit,reflect
        # normal:1 party limit,reflect
        # hard:reflect
        pain_and_panic_rules = {
            "easy":   self.kh2_list_count_sum(party_limit, state) >= 2 and state.has(ItemName.ReflectElement, self.player),
            "normal": self.kh2_list_count_sum(party_limit, state) >= 1 and state.has(ItemName.ReflectElement, self.player),
            "hard":   state.has(ItemName.ReflectElement, self.player)
        }
        return pain_and_panic_rules[self.fight_logic] and (self.kh2_has_all([ItemName.FuturePeteEvent], state) or state.has(ItemName.HadesCupTrophy, self.player))

    def get_cerberus_cup_rules(self, state: CollectionState) -> bool:
        # easy:3 drive forms,reflect
        # normal:2 drive forms,reflect
        # hard:reflect
        cerberus_cup_rules = {
            "easy":   self.kh2_can_reach_any([LocationName.Valorlvl5, LocationName.Wisdomlvl5, LocationName.Limitlvl5, LocationName.Masterlvl5, LocationName.Finallvl5], state) and state.has(ItemName.ReflectElement, self.player),
            "normal": self.kh2_can_reach_any([LocationName.Valorlvl4, LocationName.Wisdomlvl4, LocationName.Limitlvl4, LocationName.Masterlvl4, LocationName.Finallvl4], state) and state.has(ItemName.ReflectElement, self.player),
            "hard":   state.has(ItemName.ReflectElement, self.player)
        }
        return cerberus_cup_rules[self.fight_logic] and (self.kh2_has_all([ItemName.ScarEvent, ItemName.OogieBoogieEvent, ItemName.TwinLordsEvent], state) or state.has(ItemName.HadesCupTrophy, self.player))

    def get_titan_cup_rules(self, state: CollectionState) -> bool:
        # easy:4 summons,reflera
        # normal:4 summons,reflera
        # hard:2 summons,reflera
        titan_cup_rules = {
            "easy":   self.kh2_list_count_sum(summons, state) >= 4 and state.has(ItemName.ReflectElement, self.player, 2),
            "normal": self.kh2_list_count_sum(summons, state) >= 3 and state.has(ItemName.ReflectElement, self.player, 2),
            "hard":   self.kh2_list_count_sum(summons, state) >= 2 and state.has(ItemName.ReflectElement, self.player, 2),
        }
        return titan_cup_rules[self.fight_logic] and (state.has(ItemName.HadesEvent, self.player) or state.has(ItemName.HadesCupTrophy, self.player))

    def get_goddess_of_fate_cup_rules(self, state: CollectionState) -> bool:
        # can beat all the other cups+xemnas 1
        return self.kh2_has_all([ItemName.OcPainAndPanicCupEvent, ItemName.OcCerberusCupEvent, ItemName.Oc2TitanCupEvent], state)

    def get_hades_cup_rules(self, state: CollectionState) -> bool:
        # can beat goddess of fate cup
        return state.has(ItemName.Oc2GofCupEvent, self.player)

    def get_olympus_pete_rules(self, state: CollectionState) -> bool:
        # easy:gap closer,defensive option,drive form
        # normal:2 of those things
        # hard:1 of those things
        olympus_pete_rules = {
            "easy":   self.kh2_list_any_sum([gap_closer, defensive_tool, form_list], state) >= 3,
            "normal": self.kh2_list_any_sum([gap_closer, defensive_tool, form_list], state) >= 2,
            "hard":   self.kh2_list_any_sum([gap_closer, defensive_tool, form_list], state) >= 1,
        }
        return olympus_pete_rules[self.fight_logic]

    def get_hydra_rules(self, state: CollectionState) -> bool:
        # easy:drive form,defensive option,offensive magic
        # normal 2 of those things
        # hard: one of those things
        hydra_rules = {
            "easy":   self.kh2_list_any_sum([black_magic, defensive_tool, form_list], state) >= 3,
            "normal": self.kh2_list_any_sum([black_magic, defensive_tool, form_list], state) >= 2,
            "hard":   self.kh2_list_any_sum([black_magic, defensive_tool, form_list], state) >= 1,
        }
        return hydra_rules[self.fight_logic]

    def get_hades_rules(self, state: CollectionState) -> bool:
        # easy:drive form,summon,gap closer,defensive option
        # normal:3 of those things
        # hard:2 of those things
        hades_rules = {
            "easy":   self.kh2_list_any_sum([gap_closer, summons, defensive_tool, form_list], state) >= 4,
            "normal": self.kh2_list_any_sum([gap_closer, summons, defensive_tool, form_list], state) >= 3,
            "hard":   self.kh2_list_any_sum([gap_closer, summons, defensive_tool, form_list], state) >= 2,
        }
        return hades_rules[self.fight_logic]

    def get_data_zexion_rules(self, state: CollectionState) -> bool:
        # easy: final 7,firaga,scom,both donald limits, Reflega ,guard,2 gap closers,quick run level 3
        # normal:final 7,firaga, donald limit, Reflega ,guard,1 gap closers,quick run level 3
        # hard:final 5,fira, donald limit, reflect,gap closer,quick run level 2
        data_zexion_rules = {
            "easy":   self.kh2_dict_count(easy_data_zexion, state) and self.form_list_unlock(state, ItemName.FinalForm, 5, True),
            "normal": self.kh2_dict_count(normal_data_zexion, state) and self.form_list_unlock(state, ItemName.FinalForm, 5, True) and self.kh2_list_any_sum([donald_limit, gap_closer], state) >= 2,
            "hard":   self.kh2_dict_count(hard_data_zexion, state) and self.form_list_unlock(state, ItemName.FinalForm, 3, True) and self.kh2_list_any_sum([donald_limit, gap_closer], state) >= 2,
        }
        return data_zexion_rules[self.fight_logic]

    def get_thresholder_rules(self, state: CollectionState) -> bool:
        # easy:drive form,black magic,defensive tool
        # normal:2 of those things
        # hard:defensive tool or drive form
        thresholder_rules = {
            "easy":   self.kh2_list_any_sum([form_list, black_magic, defensive_tool], state) >= 3,
            "normal": self.kh2_list_any_sum([form_list, black_magic, defensive_tool], state) >= 2,
            "hard":   self.kh2_list_any_sum([form_list, defensive_tool], state) >= 1,
        }
        return thresholder_rules[self.fight_logic]

    @staticmethod
    def get_beast_rules():
        # fight is free
        return True

    def get_dark_thorn_rules(self, state: CollectionState) -> bool:
        # easy:drive form,defensive tool,gap closer
        # normal:drive form,defensive tool
        # hard:defensive tool
        dark_thorn_rules = {
            "easy":   self.kh2_list_any_sum([form_list, gap_closer, defensive_tool], state) >= 3,
            "normal": self.kh2_list_any_sum([form_list, defensive_tool], state) >= 2,
            "hard":   self.kh2_list_any_sum([defensive_tool], state) >= 1,
        }
        return dark_thorn_rules[self.fight_logic]

    def get_xaldin_rules(self, state: CollectionState) -> bool:
        # easy:guard,2 aerial modifier,valor/master/final
        # normal:guard,1 aerial modifier
        # hard:guard
        xaldin_rules = {
            "easy":   self.kh2_list_any_sum([[ItemName.Guard], [ItemName.ValorForm, ItemName.MasterForm, ItemName.FinalForm]], state) >= 2 and self.kh2_list_count_sum(aerial_move, state) >= 2,
            "normal": self.kh2_list_any_sum([aerial_move], state) >= 1 and state.has(ItemName.Guard, self.player),
            "hard":   state.has(ItemName.Guard, self.player),
        }
        return xaldin_rules[self.fight_logic]

    def get_data_xaldin_rules(self, state: CollectionState) -> bool:
        # easy:final 7,firaga,2 air combo plus, finishing plus,guard,reflega,donald limit,high jump aerial dodge glide lvl 3,magnet,aerial dive,aerial spiral,hori slash,berserk charge
        # normal:final 7,firaga, finishing plus,guard,reflega,donald limit,high jump aerial dodge glide lvl 3,magnet,aerial dive,aerial spiral,hori slash
        # hard:final 5, fira, party limit, finishing plus,guard,high jump aerial dodge glide lvl 2,magnet,aerial dive
        data_xaldin_rules = {
            "easy":   self.kh2_dict_count(easy_data_xaldin, state) and self.form_list_unlock(state, ItemName.FinalForm, 5, True),
            "normal": self.kh2_dict_count(normal_data_xaldin, state) and self.form_list_unlock(state, ItemName.FinalForm, 5, True),
            "hard":   self.kh2_dict_count(hard_data_xaldin, state) and self.form_list_unlock(state, ItemName.FinalForm, 3, True) and self.kh2_has_any(party_limit, state),
        }
        return data_xaldin_rules[self.fight_logic]

    def get_hostile_program_rules(self, state: CollectionState) -> bool:
        # easy:donald limit,reflect,drive form,summon
        # normal:3 of those things
        # hard: 2 of those things
        hostile_program_rules = {
            "easy":   self.kh2_list_any_sum([donald_limit, form_list, summons, {ItemName.ReflectElement}], state) >= 4,
            "normal": self.kh2_list_any_sum([donald_limit, form_list, summons, {ItemName.ReflectElement}], state) >= 3,
            "hard":   self.kh2_list_any_sum([donald_limit, form_list, summons, {ItemName.ReflectElement}], state) >= 2,
        }
        return hostile_program_rules[self.fight_logic]

    def get_mcp_rules(self, state: CollectionState) -> bool:
        # easy:donald limit,reflect,drive form,summon
        # normal:3 of those things
        # hard: 2 of those things
        mcp_rules = {
            "easy":   self.kh2_list_any_sum([donald_limit, form_list, summons, {ItemName.ReflectElement}], state) >= 4,
            "normal": self.kh2_list_any_sum([donald_limit, form_list, summons, {ItemName.ReflectElement}], state) >= 3,
            "hard":   self.kh2_list_any_sum([donald_limit, form_list, summons, {ItemName.ReflectElement}], state) >= 2,
        }
        return mcp_rules[self.fight_logic]

    def get_data_larxene_rules(self, state: CollectionState) -> bool:
        # easy: final 7,firaga,scom,both donald limits, Reflega,guard,2 gap closers,2 ground finishers,aerial dodge 3,glide 3
        # normal:final 7,firaga, donald limit, Reflega ,guard,1 gap closers,1 ground finisher,aerial dodge 3,glide 3
        # hard:final 5,fira, donald limit, reflect,gap closer,aerial dodge 2,glide 2
        data_larxene_rules = {
            "easy":   self.kh2_dict_count(easy_data_larxene, state) and self.form_list_unlock(state, ItemName.FinalForm, 5, True),
            "normal": self.kh2_dict_count(normal_data_larxene, state) and self.kh2_list_any_sum([gap_closer, ground_finisher, donald_limit], state) >= 3 and self.form_list_unlock(state, ItemName.FinalForm, 5, True),
            "hard":   self.kh2_dict_count(hard_data_larxene, state) and self.kh2_list_any_sum([gap_closer, donald_limit], state) >= 2 and self.form_list_unlock(state, ItemName.FinalForm, 3, True),
        }
        return data_larxene_rules[self.fight_logic]

    def get_prison_keeper_rules(self, state: CollectionState) -> bool:
        # easy:defensive tool,drive form, party limit
        # normal:two of those things
        # hard:one of those things
        prison_keeper_rules = {
            "easy":   self.kh2_list_any_sum([defensive_tool, form_list, party_limit], state) >= 3,
            "normal": self.kh2_list_any_sum([defensive_tool, form_list, party_limit], state) >= 2,
            "hard":   self.kh2_list_any_sum([defensive_tool, form_list, party_limit], state) >= 1,
        }
        return prison_keeper_rules[self.fight_logic]

    @staticmethod
    def get_oogie_rules():
        # fight is free
        return True

    def get_experiment_rules(self, state: CollectionState) -> bool:
        # easy:drive form,defensive tool,summon,party limit
        # normal:3 of those things
        # hard 2 of those things
        experiment_rules = {
            "easy":   self.kh2_list_any_sum([form_list, defensive_tool, party_limit, summons], state) >= 4,
            "normal": self.kh2_list_any_sum([form_list, defensive_tool, party_limit, summons], state) >= 3,
            "hard":   self.kh2_list_any_sum([form_list, defensive_tool, party_limit, summons], state) >= 2,
        }
        return experiment_rules[self.fight_logic]

    def get_data_vexen_rules(self, state: CollectionState) -> bool:
        # easy: final 7,firaga,scom,both donald limits, Reflega,guard,2 gap closers,2 ground finishers,aerial dodge 3,glide 3,dodge roll 3,quick run 3
        # normal:final 7,firaga, donald limit, Reflega,guard,1 gap closers,1 ground finisher,aerial dodge 3,glide 3,dodge roll 3,quick run 3
        # hard:final 5,fira, donald limit, reflect,gap closer,aerial dodge 2,glide 2,dodge roll 2,quick run 2
        data_vexen_rules = {
            "easy":   self.kh2_dict_count(easy_data_vexen, state) and self.form_list_unlock(state, ItemName.FinalForm, 5, True),
            "normal": self.kh2_dict_count(normal_data_vexen, state) and self.kh2_list_any_sum([gap_closer, ground_finisher, donald_limit], state) >= 3 and self.form_list_unlock(state, ItemName.FinalForm, 5, True),
            "hard":   self.kh2_dict_count(hard_data_vexen, state) and self.kh2_list_any_sum([gap_closer, donald_limit], state) >= 2 and self.form_list_unlock(state, ItemName.FinalForm, 3, True),
        }
        return data_vexen_rules[self.fight_logic]

    def get_demyx_rules(self, state: CollectionState) -> bool:
        # defensive option,drive form,party limit
        # defensive option,drive form
        # defensive option
        demyx_rules = {
            "easy":   self.kh2_list_any_sum([defensive_tool, form_list, party_limit], state) >= 3,
            "normal": self.kh2_list_any_sum([defensive_tool, form_list], state) >= 2,
            "hard":   self.kh2_list_any_sum([defensive_tool], state) >= 1,
        }
        return demyx_rules[self.fight_logic]

    def get_thousand_heartless_rules(self, state: CollectionState) -> bool:
        # easy:scom,limit form,guard,magnera
        # normal:limit form, guard
        # hard:guard
        thousand_heartless_rules = {
            "easy":   self.kh2_dict_count(easy_thousand_heartless_rules, state),
            "normal": self.kh2_dict_count(normal_thousand_heartless_rules, state),
            "hard":   state.has(ItemName.Guard, self.player),
        }
        return thousand_heartless_rules[self.fight_logic]

    def get_data_demyx_rules(self, state: CollectionState) -> bool:
        # easy:wisdom 7,1 form boosts,reflera,firaga,duck flare,guard,scom,finishing plus
        # normal:remove form boost and scom
        # hard:wisdom 6,reflect,guard,duck flare,fira,finishing plus
        data_demyx_rules = {
            "easy":   self.kh2_dict_count(easy_data_demyx, state) and self.form_list_unlock(state, ItemName.WisdomForm, 5, True),
            "normal": self.kh2_dict_count(normal_data_demyx, state) and self.form_list_unlock(state, ItemName.WisdomForm, 5, True),
            "hard":   self.kh2_dict_count(hard_data_demyx, state) and self.form_list_unlock(state, ItemName.WisdomForm, 4, True),
        }
        return data_demyx_rules[self.fight_logic]

    def get_sephiroth_rules(self, state: CollectionState) -> bool:
        # easy:both gap closers,limit 5,reflega,guard,both 2 ground finishers,3 dodge roll,finishing plus,scom
        # normal:both gap closers,limit 5,reflera,guard,both 2 ground finishers,3 dodge roll,finishing plus
        # hard:1 gap closers,reflect, guard,both 1 ground finisher,2 dodge roll,finishing plus
        sephiroth_rules = {
            "easy":   self.kh2_dict_count(easy_sephiroth_tools, state) and self.kh2_can_reach(LocationName.Limitlvl5, state) and self.kh2_list_any_sum([donald_limit], state) >= 1,
            "normal": self.kh2_dict_count(normal_sephiroth_tools, state) and self.kh2_can_reach(LocationName.Limitlvl5, state) and self.kh2_list_any_sum([donald_limit, gap_closer], state) >= 2,
            "hard":   self.kh2_dict_count(hard_sephiroth_tools, state) and self.kh2_list_any_sum([gap_closer, ground_finisher], state) >= 2,
        }
        return sephiroth_rules[self.fight_logic]

    def get_cor_first_fight_movement_rules(self, state: CollectionState) -> bool:
        # easy: quick run 3 or wisdom 5 (wisdom has qr 3)
        # normal: quick run 2 and aerial dodge 1 or wisdom 5 (wisdom has qr 3)
        # hard: (quick run 1, aerial dodge 1) or (wisdom form and aerial dodge 1)
        cor_first_fight_movement_rules = {
            "easy":   state.has(ItemName.QuickRun, self.player, 3) or self.form_list_unlock(state, ItemName.WisdomForm, 3, True),
            "normal": self.kh2_dict_count({ItemName.QuickRun: 2, ItemName.AerialDodge: 1}, state) or self.form_list_unlock(state, ItemName.WisdomForm, 3, True),
            "hard":   self.kh2_has_all([ItemName.AerialDodge, ItemName.QuickRun], state) or self.kh2_has_all([ItemName.AerialDodge, ItemName.WisdomForm], state),
        }
        return cor_first_fight_movement_rules[self.fight_logic]

    def get_cor_first_fight_rules(self, state: CollectionState) -> bool:
        # easy:have 5 of these things (reflega,stitch and chicken,final form,magnera,explosion,thundara)
        # normal:have 3 of these things (reflega,stitch and chicken,final form,magnera,explosion,thundara)
        # hard: reflect,stitch or chicken,final form
        cor_first_fight_rules = {
            "easy":   self.kh2_dict_one_count(not_hard_cor_tools_dict, state) >= 5 or self.kh2_dict_one_count(not_hard_cor_tools_dict, state) >= 4 and self.form_list_unlock(state, ItemName.FinalForm, 1, True),
            "normal": self.kh2_dict_one_count(not_hard_cor_tools_dict, state) >= 3 or self.kh2_dict_one_count(not_hard_cor_tools_dict, state) >= 2 and self.form_list_unlock(state, ItemName.FinalForm, 1, True),
            "hard":   state.has(ItemName.ReflectElement, self.player) and self.kh2_has_any([ItemName.Stitch, ItemName.ChickenLittle], state) and self.form_list_unlock(state, ItemName.FinalForm, 1, True),
        }
        return cor_first_fight_rules[self.fight_logic]

    def get_cor_skip_first_rules(self, state: CollectionState) -> bool:
        # if option is not allow skips return false else run rules
        if not self.multiworld.CorSkipToggle[self.player]:
            return False
        # easy: aerial dodge 3,master form,fire
        # normal: aerial dodge 2, master form,fire
        # hard:void cross(quick run 3,aerial dodge 1)
        # or (quick run 2,aerial dodge 2 and magic)
        # or (final form and (magic or combo master))
        # or (master form and (reflect or fire or thunder or combo master)
        # wall rise(aerial dodge 1 and (final form lvl 3 or glide 2) or (master form and (1 of black magic or combo master)
        void_cross_rules = {
            "easy":   state.has(ItemName.AerialDodge, self.player, 3) and self.kh2_has_all([ItemName.MasterForm, ItemName.FireElement], state),
            "normal": state.has(ItemName.AerialDodge, self.player, 2) and self.kh2_has_all([ItemName.MasterForm, ItemName.FireElement], state),
            "hard":   (self.kh2_dict_count({ItemName.QuickRun: 3, ItemName.AerialDodge: 1}, state)) \
                      or (self.kh2_dict_count({ItemName.QuickRun: 2, ItemName.AerialDodge: 2}, state) and self.kh2_has_any(magic, state)) \
                      or (state.has(ItemName.FinalForm, self.player) and (self.kh2_has_any(magic, state) or state.has(ItemName.ComboMaster, self.player))) \
                      or (state.has(ItemName.MasterForm, self.player) and (self.kh2_has_any([ItemName.ReflectElement, ItemName.FireElement, ItemName.ComboMaster], state)))
        }
        wall_rise_rules = {
            "easy":   True,
            "normal": True,
            "hard":   state.has(ItemName.AerialDodge, self.player) and (self.form_list_unlock(state, ItemName.FinalForm, 1, True) or state.has(ItemName.Glide, self.player, 2))
        }
        return void_cross_rules[self.fight_logic] and wall_rise_rules[self.fight_logic]

    def get_cor_second_fight_movement_rules(self, state: CollectionState) -> bool:
        # easy: quick run 2, aerial dodge 3 or master form 5
        # normal: quick run 2, aerial dodge 2 or master 5
        # hard: (glide 1,aerial dodge 1 any magic) or (master 3 any magic) or glide 1 and aerial dodge 2

        cor_second_fight_movement_rules = {
            "easy":   self.kh2_dict_count({ItemName.QuickRun: 2, ItemName.AerialDodge: 3}, state) or self.form_list_unlock(state, ItemName.MasterForm, 3, True),
            "normal": self.kh2_dict_count({ItemName.QuickRun: 2, ItemName.AerialDodge: 2}, state) or self.form_list_unlock(state, ItemName.MasterForm, 3, True),
            "hard":   (self.kh2_has_all([ItemName.Glide, ItemName.AerialDodge], state) and self.kh2_has_any(magic, state)) \
                      or (state.has(ItemName.MasterForm, self.player) and self.kh2_has_any(magic, state)) \
                      or (state.has(ItemName.Glide, self.player) and state.has(ItemName.AerialDodge, self.player, 2)),
        }
        return cor_second_fight_movement_rules[self.fight_logic]

    def get_transport_fight_rules(self, state: CollectionState) -> bool:
        # easy: reflega,stitch and chicken,final form,magnera,explosion,finishing leap,thundaga,2 donald limits
        # normal: 7 of those things
        # hard: 5 of those things
        transport_fight_rules = {
            "easy":   self.kh2_dict_count(transport_tools_dict, state),
            "normal": self.kh2_dict_one_count(transport_tools_dict, state) >= 7,
            "hard":   self.kh2_dict_one_count(transport_tools_dict, state) >= 5,
        }
        return transport_fight_rules[self.fight_logic]

    def get_transport_movement_rules(self, state: CollectionState) -> bool:
        # easy:high jump 3,aerial dodge 3,glide 3
        # normal: high jump 2,glide 3,aerial dodge 2
        # hard: (hj 2,glide 2,ad 1,any magic) or hj 1,glide 2,ad 3 any magic or (any magic master form,ad) or hj lvl 1,glide 3,ad 1
        transport_movement_rules = {
            "easy":   self.kh2_dict_count({ItemName.HighJump: 3, ItemName.AerialDodge: 3, ItemName.Glide: 3}, state),
            "normal": self.kh2_dict_count({ItemName.HighJump: 2, ItemName.AerialDodge: 2, ItemName.Glide: 3}, state),
            "hard":   (self.kh2_dict_count({ItemName.HighJump: 2, ItemName.AerialDodge: 1, ItemName.Glide: 2}, state) and self.kh2_has_any(magic, state)) \
                      or (self.kh2_dict_count({ItemName.HighJump: 1, ItemName.Glide: 2, ItemName.AerialDodge: 3}, state) and self.kh2_has_any(magic, state)) \
                      or (self.kh2_dict_count({ItemName.HighJump: 1, ItemName.Glide: 3, ItemName.AerialDodge: 1}, state)) \
                      or (self.kh2_has_all([ItemName.MasterForm, ItemName.AerialDodge], state) and self.kh2_has_any(magic, state)),
        }
        return transport_movement_rules[self.fight_logic]

    def get_scar_rules(self, state: CollectionState) -> bool:
        # easy: reflect,thunder,fire
        # normal:reflect,fire
        # hard:reflect
        scar_rules = {
            "easy":   self.kh2_has_all([ItemName.ReflectElement, ItemName.ThunderElement, ItemName.FireElement], state),
            "normal": self.kh2_has_all([ItemName.ReflectElement, ItemName.FireElement], state),
            "hard":   state.has(ItemName.ReflectElement, self.player),
        }
        return scar_rules[self.fight_logic]

    def get_groundshaker_rules(self, state: CollectionState) -> bool:
        # easy:berserk charge,cure,2 air combo plus,reflect
        # normal:berserk charge,reflect,cure
        # hard:berserk charge or 2 air combo plus. reflect
        groundshaker_rules = {
            "easy":   state.has(ItemName.AirComboPlus, self.player, 2) and self.kh2_has_all([ItemName.BerserkCharge, ItemName.CureElement, ItemName.ReflectElement], state),
            "normal": self.kh2_has_all([ItemName.BerserkCharge, ItemName.ReflectElement, ItemName.CureElement], state),
            "hard":   (state.has(ItemName.BerserkCharge, self.player) or state.has(ItemName.AirComboPlus, self.player, 2)) and state.has(ItemName.ReflectElement, self.player),
        }
        return groundshaker_rules[self.fight_logic]

    def get_data_saix_rules(self, state: CollectionState) -> bool:
        # easy:guard,2 gap closers,thunder,blizzard,2 donald limit,reflega,2 ground finisher,aerial dodge 3,glide 3,final 7,firaga,scom
        # normal:guard,1 gap closers,thunder,blizzard,1 donald limit,reflega,1 ground finisher,aerial dodge 3,glide 3,final 7,firaga
        # hard:aerial dodge 3,glide 3,guard,reflect,blizzard,1 gap closer,1 ground finisher
        easy_data_rules = {
            "easy":   self.kh2_dict_count(easy_data_saix, state) and self.form_list_unlock(state, ItemName.FinalForm, 5),
            "normal": self.kh2_dict_count(normal_data_saix, state) and self.kh2_list_any_sum([gap_closer, ground_finisher, donald_limit], state) >= 3 and self.form_list_unlock(state, ItemName.FinalForm, 5),
            "hard":   self.kh2_dict_count(hard_data_saix, state) and self.kh2_list_any_sum([gap_closer, ground_finisher], state) >= 2
        }
        return easy_data_rules[self.fight_logic]

    @staticmethod
    def get_twilight_thorn_rules() -> bool:
        return True

    @staticmethod
    def get_axel_one_rules() -> bool:
        return True

    @staticmethod
    def get_axel_two_rules() -> bool:
        return True

    def get_data_roxas_rules(self, state: CollectionState) -> bool:
        # easy:both gap closers,limit 5,reflega,guard,both 2 ground finishers,3 dodge roll,finishing plus,scom
        # normal:both gap closers,limit 5,reflera,guard,both 2 ground finishers,3 dodge roll,finishing plus
        # hard:1 gap closers,reflect, guard,both 1 ground finisher,2 dodge roll,finishing plus
        data_roxas_rules = {
            "easy":   self.kh2_dict_count(easy_data_roxas_tools, state) and self.kh2_can_reach(LocationName.Limitlvl5, state) and self.kh2_list_any_sum([donald_limit], state) >= 1,
            "normal": self.kh2_dict_count(normal_data_roxas_tools, state) and self.kh2_can_reach(LocationName.Limitlvl5, state) and self.kh2_list_any_sum([donald_limit, gap_closer], state) >= 2,
            "hard":   self.kh2_dict_count(hard_data_roxas_tools, state) and self.kh2_list_any_sum([gap_closer, ground_finisher], state) >= 2
        }
        return data_roxas_rules[self.fight_logic]

    def get_data_axel_rules(self, state: CollectionState) -> bool:
        # easy:both gap closers,limit 5,reflega,guard,both 2 ground finishers,3 dodge roll,finishing plus,scom,blizzaga
        # normal:both gap closers,limit 5,reflera,guard,both 2 ground finishers,3 dodge roll,finishing plus,blizzaga
        # hard:1 gap closers,reflect, guard,both 1 ground finisher,2 dodge roll,finishing plus,blizzara
        data_axel_rules = {
            "easy":   self.kh2_dict_count(easy_data_axel_tools, state) and self.kh2_can_reach(LocationName.Limitlvl5, state) and self.kh2_list_any_sum([donald_limit], state) >= 1,
            "normal": self.kh2_dict_count(normal_data_axel_tools, state) and self.kh2_can_reach(LocationName.Limitlvl5, state) and self.kh2_list_any_sum([donald_limit, gap_closer], state) >= 2,
            "hard":   self.kh2_dict_count(hard_data_axel_tools, state) and self.kh2_list_any_sum([gap_closer, ground_finisher], state) >= 2
        }
        return data_axel_rules[self.fight_logic]

    def get_roxas_rules(self, state: CollectionState) -> bool:
        # easy:aerial dodge 1,glide 1, limit form,thunder,reflera,guard break,2 gap closers,finishing plus,blizzard
        # normal:thunder,reflera,guard break,2 gap closers,finishing plus,blizzard
        # hard:guard
        roxas_rules = {
            "easy":   self.kh2_dict_count(easy_roxas_tools, state),
            "normal": self.kh2_dict_count(normal_roxas_tools, state),
            "hard":   state.has(ItemName.Guard, self.player),
        }
        return roxas_rules[self.fight_logic]

    def get_xigbar_rules(self, state: CollectionState) -> bool:
        # easy:final 4,horizontal slash,fira,finishing plus,glide 2,aerial dodge 2,quick run 2,guard,reflect
        # normal:final 4,fira,finishing plus,glide 2,aerial dodge 2,quick run 2,guard,reflect
        # hard:guard,quick run,finishing plus
        xigbar_rules = {
            "easy":   self.kh2_dict_count(easy_xigbar_tools, state) and self.form_list_unlock(state, ItemName.FinalForm, 1) and self.kh2_has_any([ItemName.LightDarkness, ItemName.FinalForm], state),
            "normal": self.kh2_dict_count(normal_xigbar_tools, state) and self.form_list_unlock(state, ItemName.FinalForm, 1),
            "hard":   self.kh2_has_all([ItemName.Guard, ItemName.QuickRun, ItemName.FinishingPlus], state),
        }
        return xigbar_rules[self.fight_logic]

    def get_luxord_rules(self, state: CollectionState) -> bool:
        # easy:aerial dodge 1,glide 1,quickrun 2,guard,reflera,2 gap closers,ground finisher,limit form
        # normal:aerial dodge 1,glide 1,quickrun 2,guard,reflera,1 gap closers,ground finisher
        # hard:quick run,guard
        luxord_rules = {
            "easy":   self.kh2_dict_count(easy_luxord_tools, state) and self.kh2_has_any(ground_finisher, state),
            "normal": self.kh2_dict_count(normal_luxord_tools, state) and self.kh2_list_any_sum([gap_closer, ground_finisher], state) >= 2,
            "hard":   self.kh2_has_all([ItemName.Guard, ItemName.QuickRun], state)
        }
        return luxord_rules[self.fight_logic]

    def get_saix_rules(self, state: CollectionState) -> bool:
        # easy:aerial dodge 1,glide 1,quickrun 2,guard,reflera,2 gap closers,ground finisher,limit form
        # normal:aerial dodge 1,glide 1,quickrun 2,guard,reflera,1 gap closers,ground finisher
        # hard:,guard

        saix_rules = {
            "easy":   self.kh2_dict_count(easy_saix_tools, state) and self.kh2_has_any(ground_finisher, state),
            "normal": self.kh2_dict_count(normal_saix_tools, state) and self.kh2_list_any_sum([gap_closer, ground_finisher], state) >= 2,
            "hard":   self.kh2_has_all([ItemName.Guard], state)
        }
        return saix_rules[self.fight_logic]

    def get_xemnas_rules(self, state: CollectionState) -> bool:
        # easy:aerial dodge 1,glide 1,quickrun 2,guard,reflera,2 gap closers,ground finisher,limit form
        # normal:aerial dodge 1,glide 1,quickrun 2,guard,reflera,1 gap closers,ground finisher
        # hard:,guard
        xemnas_rules = {
            "easy":   self.kh2_dict_count(easy_xemnas_tools, state) and self.kh2_has_any(ground_finisher, state),
            "normal": self.kh2_dict_count(normal_xemnas_tools, state) and self.kh2_list_any_sum([gap_closer, ground_finisher], state) >= 2,
            "hard":   self.kh2_has_all([ItemName.Guard], state)
        }
        return xemnas_rules[self.fight_logic]

    def get_armored_xemnas_one_rules(self, state: CollectionState) -> bool:
        # easy:donald limit,reflect,1 gap closer,ground finisher
        # normal:reflect,gap closer,ground finisher
        # hard:reflect
        armored_xemnas_one_rules = {
            "easy":   self.kh2_list_any_sum([donald_limit, gap_closer, ground_finisher, {ItemName.ReflectElement}], state) >= 4,
            "normal": self.kh2_list_any_sum([gap_closer, ground_finisher, {ItemName.ReflectElement}], state) >= 3,
            "hard":   state.has(ItemName.ReflectElement, self.player),
        }
        return armored_xemnas_one_rules[self.fight_logic]

    def get_armored_xemnas_two_rules(self, state: CollectionState) -> bool:
        # easy:donald limit,reflect,1 gap closer,ground finisher
        # normal:reflect,gap closer,ground finisher
        # hard:reflect
        armored_xemnas_two_rules = {
            "easy":   self.kh2_list_any_sum([gap_closer, ground_finisher, {ItemName.ReflectElement}, {ItemName.ThunderElement}], state) >= 4,
            "normal": self.kh2_list_any_sum([gap_closer, ground_finisher, {ItemName.ReflectElement}], state) >= 3,
            "hard":   state.has(ItemName.ReflectElement, self.player),
        }
        return armored_xemnas_two_rules[self.fight_logic]

    def get_final_xemnas_rules(self, state: CollectionState) -> bool:
        # easy:reflera,limit form,finishing plus,gap closer,guard
        # normal:reflect,finishing plus,guard
        # hard:guard
        final_xemnas_rules = {
            "easy":   self.kh2_has_all([ItemName.LimitForm, ItemName.FinishingPlus, ItemName.Guard], state) and state.has(ItemName.ReflectElement, self.player, 2) and self.kh2_has_any(gap_closer, state),
            "normal": self.kh2_has_all([ItemName.ReflectElement, ItemName.FinishingPlus, ItemName.Guard], state),
            "hard":   state.has(ItemName.Guard, self.player),
        }
        return final_xemnas_rules[self.fight_logic]

    def get_data_xemnas_rules(self, state: CollectionState) -> bool:
        # easy:combo master,slapshot,reflega,2 ground finishers,both gap closers,finishing plus,guard,limit 5,scom,trinity limit
        # normal:combo master,slapshot,reflega,2 ground finishers,both gap closers,finishing plus,guard,limit 5,
        # hard:combo master,slapshot,reflera,1 ground finishers,1 gap closers,finishing plus,guard,limit form
        data_xemnas_rules = {
            "easy":   self.kh2_dict_count(easy_data_xemnas, state) and self.kh2_list_count_sum(ground_finisher, state) >= 2 and self.kh2_can_reach(LocationName.Limitlvl5, state),
            "normal": self.kh2_dict_count(normal_data_xemnas, state) and self.kh2_list_count_sum(ground_finisher, state) >= 2 and self.kh2_can_reach(LocationName.Limitlvl5, state),
            "hard":   self.kh2_dict_count(hard_data_xemnas, state) and self.kh2_list_any_sum([ground_finisher, gap_closer], state) >= 2
        }
        return data_xemnas_rules[self.fight_logic]
