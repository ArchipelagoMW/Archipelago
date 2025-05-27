from typing import Dict, Callable, TYPE_CHECKING

from BaseClasses import CollectionState
from .Items import visit_locking_dict, DonaldAbility_Table, GoofyAbility_Table, SupportAbility_Table
from .Locations import exclusion_table, Goofy_Checks, Donald_Checks
from worlds.generic.Rules import add_rule, add_item_rule
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

    def cor_unlocked(self, state: CollectionState) -> bool:
        return self.kh2_has_final_form(state) or \
            (self.kh2_has_master_form(state) and self.has_magic_buffer(state)) \
            or self.has_vertical(state, 1) \
            or (self.kh2_has_valor_form(state) and self.get_form_level_max(state, 3))  #level 5

    def level_locking_unlock(self, state: CollectionState, amount):
        if self.world.options.Promise_Charm and state.has(ItemName.PromiseCharm, self.player):
            return True
        return amount <= sum([state.count(item_name, self.player) for item_name in visit_locking_dict["2VisitLocking"]])

    def summon_levels_unlocked(self, state: CollectionState, amount) -> bool:
        return amount <= sum([1 for item_name in summons if state.has(item_name,self.player)])

    def kh2_list_count_sum(self, item_name_list: list, state: CollectionState) -> int:
        """
        Returns the sum of state.count() for each item in the list.
        """
        return sum(
                [state.count(item_name, self.player) for item_name in item_name_list]
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
        Returns all the count for the items in the dictionary.
        """
        return all(
                [state.count(item_name, self.player) >= item_amount for item_name, item_amount in
                 item_name_to_count.items()]
        )

    def kh2_dict_one_count(self, item_name_to_count: dict, state: CollectionState) -> int:
        """
        returns the sum of the dict count
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

    def kh2_has_valor_form(self, state: CollectionState):
        return state.has(ItemName.ValorForm, self.player)

    def kh2_has_wisdom_form(self, state: CollectionState):
        return state.has(ItemName.WisdomForm, self.player)

    def kh2_has_limit_form(self, state: CollectionState):
        return state.has(ItemName.LimitForm, self.player)

    def kh2_has_master_form(self, state: CollectionState):
        return state.has(ItemName.MasterForm, self.player)

    def kh2_has_final_form(self, state: CollectionState):
        if self.world.options.FinalFormLogic == "light_and_darkness":
            return (state.has_any({ItemName.ValorForm, ItemName.WisdomForm, ItemName.LimitForm, ItemName.MasterForm}, self.player) and state.has(ItemName.LightDarkness, self.player)) \
                or state.has(ItemName.FinalForm, self.player)
        elif self.world.options.FinalFormLogic == "no_light_and_darkness":
            return state.has(ItemName.FinalForm, self.player)
        else:  # just a form
            return state.has_any(set(form_list), self.player)

    def kh2_has_auto_valor(self, state: CollectionState):
        if self.world.options.AutoFormLogic:
            return state.has(ItemName.AutoValor, self.player) and state.has(ItemName.SecondChance, self.player)
        return False

    def kh2_has_auto_wisdom(self, state: CollectionState):
        if self.world.options.AutoFormLogic:
            return state.has(ItemName.AutoWisdom, self.player) and state.has(ItemName.SecondChance, self.player)
        return False

    def kh2_has_auto_limit(self, state: CollectionState):
        if self.world.options.AutoFormLogic:
            return state.has(ItemName.AutoLimit, self.player) and state.has(ItemName.SecondChance, self.player)
        return False

    def kh2_has_auto_master(self, state: CollectionState):
        if self.world.options.AutoFormLogic:
            return state.has(ItemName.AutoMaster, self.player) and state.has(ItemName.SecondChance, self.player) and state.has(ItemName.DriveConverter, self.player)
        return False

    def kh2_has_auto_final(self, state: CollectionState):
        if self.world.options.AutoFormLogic:
            return state.has(ItemName.AutoFinal, self.player) and state.has(ItemName.SecondChance, self.player)
        return False

    def get_form_level_max(self, state, amount):
        forms_available = 0
        forms = [
            self.kh2_has_valor_form,
            self.kh2_has_wisdom_form,
            self.kh2_has_limit_form,
            self.kh2_has_master_form,
            self.kh2_has_final_form,
        ]
        for form in forms:
            forms_available += form(state)
            if forms_available >= amount:
                return True
        return False

    #movement stuff
    def has_vertical(self, state: CollectionState, amount=1) -> bool:
        # amount_to_vertical = {
        #    1: self.kh2_dict_count({ItemName.HighJump: 1, ItemName.AerialDodge: 1}, state),
        #    2: self.kh2_dict_count({ItemName.HighJump: 2, ItemName.AerialDodge: 2}, state),
        #    3: self.kh2_dict_count({ItemName.HighJump: 3, ItemName.AerialDodge: 3}, state),
        #    4: self.kh2_dict_count({ItemName.HighJump: 4, ItemName.AerialDodge: 4}, state),
        # }
        return self.kh2_dict_count({ItemName.HighJump: amount, ItemName.AerialDodge: amount}, state)

    def has_glide(self, state: CollectionState, amount=1) -> bool:
        return state.has(ItemName.Glide, self.player, amount)

    def has_high_jump(self, state: CollectionState, amount=1):
        return state.has(ItemName.HighJump, self.player, amount)

    def has_aerial_dodge(self, state: CollectionState, amount=1):
        return state.has(ItemName.AerialDodge, self.player, amount)

    def has_magic_buffer(self, state: CollectionState) -> bool:
        return self.kh2_has_any(magic, state)


class KH2LocationRules(KH2Rules):
    def __init__(self, kh2world: KH2World) -> None:
        # These Rules are Always in effect
        super().__init__(kh2world)
        self.location_rules = {
            LocationName.CoRDepthsManifestIllusion: lambda state: self.get_cor_depths_illusion_rules(state),
            LocationName.CoRDepthsAPBoost2:         lambda state: self.get_cor_depths_ap_boost_two_rules(state),
        }

    def get_cor_depths_illusion_rules(self, state: CollectionState):
        # high jump,aerial dodge and glide 2
        return (self.has_vertical(state) and self.has_glide(state, 2)) or \
            (self.kh2_has_final_form(state), self.get_form_level_max(state, 3))  #final 5

    def get_cor_depths_ap_boost_two_rules(self, state: CollectionState):
        # high jump,aerial dodge and glide 1
        return (self.has_vertical(state) and self.has_glide(state, 1)) or \
            self.kh2_has_final_form(state) or self.kh2_has_master_form(state)

    def set_kh2_location_rules(self):
        for location_name, loc_rule in self.location_rules.items():
            location = self.multiworld.get_location(location_name, self.player)
            location.access_rule = loc_rule


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
            RegionName.CoR:                lambda state: self.cor_unlocked(state),
            RegionName.Mushroom13:         lambda state: state.has(ItemName.ProofofPeace, self.player),

            RegionName.Pl:                 lambda state: self.pl_unlocked(state, 1),
            RegionName.Pl2:                lambda state: self.pl_unlocked(state, 2),

            RegionName.Ag:                 lambda state: self.ag_unlocked(state, 1),
            RegionName.Ag2:                lambda state: self.ag_unlocked(state, 2) and self.kh2_has_all([ItemName.FireElement, ItemName.BlizzardElement, ItemName.ThunderElement], state),

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
            if location.name in exclusion_table["WeaponSlots"]:  # shop items and starting items are not in this list
                exclusion_item = exclusion_table["WeaponSlots"][location.name]
                add_rule(location, lambda state, e_item=exclusion_item: state.has(e_item, self.player))

            if location.name in Goofy_Checks:
                add_item_rule(location, lambda item: item.player == self.player and item.name in GoofyAbility_Table.keys())
            elif location.name in Donald_Checks:
                add_item_rule(location, lambda item: item.player == self.player and item.name in DonaldAbility_Table.keys())
            else:
                add_item_rule(location, lambda item: item.player == self.player and item.name in SupportAbility_Table.keys())

    def set_kh2_goal(self):
        final_xemnas_location = self.multiworld.get_location(LocationName.FinalXemnasEventLocation, self.player)
        if self.world.options.Goal == "three_proofs":
            final_xemnas_location.access_rule = lambda state: self.kh2_has_all(three_proofs, state)
            if self.world.options.FinalXemnas:
                self.multiworld.completion_condition[self.player] = lambda state: state.has(ItemName.Victory, self.player, 1)
            else:
                self.multiworld.completion_condition[self.player] = lambda state: self.kh2_has_all(three_proofs, state)
        # lucky emblem hunt
        elif self.world.options.Goal == "lucky_emblem_hunt":
            final_xemnas_location.access_rule = lambda state: state.has(ItemName.LuckyEmblem, self.player, self.world.options.LuckyEmblemsRequired.value)
            if self.world.options.FinalXemnas:
                self.multiworld.completion_condition[self.player] = lambda state: state.has(ItemName.Victory, self.player, 1)
            else:
                self.multiworld.completion_condition[self.player] = lambda state: state.has(ItemName.LuckyEmblem, self.player, self.world.options.LuckyEmblemsRequired.value)
        # hitlist if == 2
        elif self.world.options.Goal == "hitlist":
            final_xemnas_location.access_rule = lambda state: state.has(ItemName.Bounty, self.player, self.world.options.BountyRequired.value)
            if self.world.options.FinalXemnas:
                self.multiworld.completion_condition[self.player] = lambda state: state.has(ItemName.Victory, self.player, 1)
            else:
                self.multiworld.completion_condition[self.player] = lambda state: state.has(ItemName.Bounty, self.player, self.world.options.BountyRequired.value)
        else:
            final_xemnas_location.access_rule = lambda state: state.has(ItemName.Bounty, self.player, self.world.options.BountyRequired.value) and \
                                                              state.has(ItemName.LuckyEmblem, self.player, self.world.options.LuckyEmblemsRequired.value)
            if self.world.options.FinalXemnas:
                self.multiworld.completion_condition[self.player] = lambda state: state.has(ItemName.Victory, self.player, 1)
            else:
                self.multiworld.completion_condition[self.player] = lambda state: state.has(ItemName.Bounty, self.player, self.world.options.BountyRequired.value) and \
                                                                                  state.has(ItemName.LuckyEmblem, self.player, self.world.options.LuckyEmblemsRequired.value)


class KH2FormRules(KH2Rules):
    #: Dict[str, Callable[[CollectionState], bool]]
    def __init__(self, world: KH2World) -> None:
        super().__init__(world)
        # access rules on where you can level a form.

        self.form_rules = {
            LocationName.Valorlvl2:  lambda state: (self.kh2_has_valor_form(state) or self.kh2_has_auto_valor(state)) and self.get_form_level_max(state, 0),
            LocationName.Valorlvl3:  lambda state: (self.kh2_has_valor_form(state) or self.kh2_has_auto_valor(state)) and self.get_form_level_max(state, 1),
            LocationName.Valorlvl4:  lambda state: (self.kh2_has_valor_form(state) or self.kh2_has_auto_valor(state)) and self.get_form_level_max(state, 2),
            LocationName.Valorlvl5:  lambda state: (self.kh2_has_valor_form(state) or self.kh2_has_auto_valor(state)) and self.get_form_level_max(state, 3),
            LocationName.Valorlvl6:  lambda state: (self.kh2_has_valor_form(state) or self.kh2_has_auto_valor(state)) and self.get_form_level_max(state, 4),
            LocationName.Valorlvl7:  lambda state: (self.kh2_has_valor_form(state) or self.kh2_has_auto_valor(state)) and self.get_form_level_max(state, 5),
            LocationName.Wisdomlvl2: lambda state: (self.kh2_has_wisdom_form(state) or self.kh2_has_auto_wisdom(state)) and self.get_form_level_max(state, 0),
            LocationName.Wisdomlvl3: lambda state: (self.kh2_has_wisdom_form(state) or self.kh2_has_auto_wisdom(state)) and self.get_form_level_max(state, 1),
            LocationName.Wisdomlvl4: lambda state: (self.kh2_has_wisdom_form(state) or self.kh2_has_auto_wisdom(state)) and self.get_form_level_max(state, 2),
            LocationName.Wisdomlvl5: lambda state: (self.kh2_has_wisdom_form(state) or self.kh2_has_auto_wisdom(state)) and self.get_form_level_max(state, 3),
            LocationName.Wisdomlvl6: lambda state: (self.kh2_has_wisdom_form(state) or self.kh2_has_auto_wisdom(state)) and self.get_form_level_max(state, 4),
            LocationName.Wisdomlvl7: lambda state: (self.kh2_has_wisdom_form(state) or self.kh2_has_auto_wisdom(state)) and self.get_form_level_max(state, 5),
            LocationName.Limitlvl2:  lambda state: (self.kh2_has_limit_form(state) or self.kh2_has_auto_limit(state)) and self.get_form_level_max(state, 0),
            LocationName.Limitlvl3:  lambda state: (self.kh2_has_limit_form(state) or self.kh2_has_auto_limit(state)) and self.get_form_level_max(state, 1),
            LocationName.Limitlvl4:  lambda state: (self.kh2_has_limit_form(state) or self.kh2_has_auto_limit(state)) and self.get_form_level_max(state, 2),
            LocationName.Limitlvl5:  lambda state: (self.kh2_has_limit_form(state) or self.kh2_has_auto_limit(state)) and self.get_form_level_max(state, 3),
            LocationName.Limitlvl6:  lambda state: (self.kh2_has_limit_form(state) or self.kh2_has_auto_limit(state)) and self.get_form_level_max(state, 4),
            LocationName.Limitlvl7:  lambda state: (self.kh2_has_limit_form(state) or self.kh2_has_auto_limit(state)) and self.get_form_level_max(state, 5),
            LocationName.Masterlvl2: lambda state: (self.kh2_has_master_form(state) or self.kh2_has_auto_master(state)) and self.get_form_level_max(state, 0),
            LocationName.Masterlvl3: lambda state: (self.kh2_has_master_form(state) or self.kh2_has_auto_master(state)) and self.get_form_level_max(state, 1),
            LocationName.Masterlvl4: lambda state: (self.kh2_has_master_form(state) or self.kh2_has_auto_master(state)) and self.get_form_level_max(state, 2),
            LocationName.Masterlvl5: lambda state: (self.kh2_has_master_form(state) or self.kh2_has_auto_master(state)) and self.get_form_level_max(state, 3),
            LocationName.Masterlvl6: lambda state: (self.kh2_has_master_form(state) or self.kh2_has_auto_master(state)) and self.get_form_level_max(state, 4),
            LocationName.Masterlvl7: lambda state: (self.kh2_has_master_form(state) or self.kh2_has_auto_master(state)) and self.get_form_level_max(state, 5),
            LocationName.Finallvl2:  lambda state: (self.kh2_has_final_form(state) or self.kh2_has_auto_final(state)) and self.get_form_level_max(state, 0),
            LocationName.Finallvl3:  lambda state: (self.kh2_has_final_form(state) or self.kh2_has_auto_final(state)) and self.get_form_level_max(state, 1),
            LocationName.Finallvl4:  lambda state: (self.kh2_has_final_form(state) or self.kh2_has_auto_final(state)) and self.get_form_level_max(state, 2),
            LocationName.Finallvl5:  lambda state: (self.kh2_has_final_form(state) or self.kh2_has_auto_final(state)) and self.get_form_level_max(state, 3),
            LocationName.Finallvl6:  lambda state: (self.kh2_has_final_form(state) or self.kh2_has_auto_final(state)) and self.get_form_level_max(state, 4),
            LocationName.Finallvl7:  lambda state: (self.kh2_has_final_form(state) or self.kh2_has_auto_final(state)) and self.get_form_level_max(state, 5),
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

        self.form_region_indirect_condition_regions = {
            RegionName.Final: {
                self.world.get_location(location).parent_region for location in final_leveling_access
            }
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
        Note: This does not account for having the drive form. See get_form_level_max
        """
        # todo: if boss enemy start the player with oc stone because of cerb
        return True

    def set_kh2_form_rules(self):
        for region_name in drive_form_list:
            if region_name == RegionName.Summon and not self.world.options.SummonLevelLocationToggle:
                continue
            indirect_condition_regions = self.form_region_indirect_condition_regions.get(region_name, ())
            # could get the location of each of these, but I feel like that would be less optimal
            region = self.multiworld.get_region(region_name, self.player)
            # if region_name in form_region_rules
            if region_name != RegionName.Summon:
                for entrance in region.entrances:
                    entrance.access_rule = self.form_region_rules[region_name]
                    for indirect_condition_region in indirect_condition_regions:
                        self.multiworld.register_indirect_condition(indirect_condition_region, entrance)
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
        self.fight_logic = world.options.FightLogic.current_key
        self.fight_region_rules = {}
        if self.fight_logic == "Easy":
            self.fight_region_rules[RegionName.ShanYu] = lambda state: self.get_easy_shanyu_rules(state)
            self.fight_region_rules[RegionName.AnsemRiku] = lambda state: self.get_easy_ansemriku_rules(state)
            self.fight_region_rules[RegionName.StormRider] = lambda state: self.get_easy_stormrider_rules(state)
            self.fight_region_rules[RegionName.DataXigbar] = lambda state: self.get_easy_dataxigbar_rules(state)
            self.fight_region_rules[RegionName.TwinLords] = lambda state: self.get_easy_firelord_rules(state) and self.get_easy_blizzardlord_rules(state)
            self.fight_region_rules[RegionName.GenieJafar] = lambda state: self.get_easy_geniejafar_rules(state)
            self.fight_region_rules[RegionName.DataLexaeus] = lambda state: self.get_easy_datalexaeus_rules(state)
            self.fight_region_rules[RegionName.OldPete] = lambda state: self.get_old_pete_rules(),
            self.fight_region_rules[RegionName.FuturePete] = lambda state: self.get_easy_futurepete_rules(state)
            self.fight_region_rules[RegionName.Terra] = lambda state: self.get_easy_terra_rules(state)
            self.fight_region_rules[RegionName.DataMarluxia] = lambda state: self.get_easy_datamarluxia_rules(state)
            self.fight_region_rules[RegionName.Barbosa] = lambda state: self.get_easy_barbosa_rules(state)
            self.fight_region_rules[RegionName.GrimReaper1] = lambda state: self.get_grim_reaper1_rules(),
            self.fight_region_rules[RegionName.GrimReaper2] = lambda state: self.get_easy_grimreaper2_rules(state)
            self.fight_region_rules[RegionName.DataLuxord] = lambda state: self.get_easy_dataluxord_rules(state)
            self.fight_region_rules[RegionName.Cerberus] = lambda state: self.get_easy_cerberus_rules(state)
            self.fight_region_rules[RegionName.OlympusPete] = lambda state: self.get_easy_olympus_pete_rules(state)
            self.fight_region_rules[RegionName.Hydra] = lambda state: self.get_easy_hydra_rules(state)
            self.fight_region_rules[RegionName.Hades] = lambda state: self.get_easy_hades_rules(state)
            self.fight_region_rules[RegionName.DataZexion] = lambda state: self.get_easy_data_zexion_rules(state)
            self.fight_region_rules[RegionName.OcPainAndPanicCup] = lambda state: self.get_pain_and_panic_cup_rules(state)
            self.fight_region_rules[RegionName.OcCerberusCup] = lambda state: self.get_easy_cerberus_cup_rules(state)
            self.fight_region_rules[RegionName.Oc2TitanCup] = lambda state: self.get_easy_titan_cup_rules(state)
            self.fight_region_rules[RegionName.Oc2GofCup] = lambda state: self.get_goddess_of_fate_cup_entrance_rules(state)
            self.fight_region_rules[RegionName.HadesCups] = lambda state: self.get_hades_cup_rules(state)
            self.fight_region_rules[RegionName.Thresholder] = lambda state: self.get_easy_thresholder_rules(state)
            self.fight_region_rules[RegionName.Beast] = lambda state: self.get_beast_rules()
            self.fight_region_rules[RegionName.DarkThorn] = lambda state: self.get_easy_dark_thorn_rules(state)
            self.fight_region_rules[RegionName.Xaldin] = lambda state: self.get_easy_xaldin_rules(state)
            self.fight_region_rules[RegionName.DataXaldin] = lambda state: self.get_easy_data_xaldin_rules(state)
            self.fight_region_rules[RegionName.HostileProgram] = lambda state: self.get_easy_hostile_program_rules(state)
            self.fight_region_rules[RegionName.Mcp] = lambda state: self.get_mcp_rules(state)
            self.fight_region_rules[RegionName.DataLarxene] = lambda state: self.get_easy_data_larxene_rules(state)
            self.fight_region_rules[RegionName.PrisonKeeper] = lambda state: self.get_easy_prison_keeper_rules(state)
            self.fight_region_rules[RegionName.OogieBoogie] = lambda state: self.get_oogie_rules()
            self.fight_region_rules[RegionName.Experiment] = lambda state: self.get_easy_experiment_rules(state)
            self.fight_region_rules[RegionName.DataVexen] = lambda state: self.get_easy_data_vexen_rules(state)
            self.fight_region_rules[RegionName.Hb2Corridors]= lambda state:self.get_easy_corridors_fight_rules(state)
            self.fight_region_rules[RegionName.HBDemyx] = lambda state: self.get_easy_demyx_rules(state)
            self.fight_region_rules[RegionName.ThousandHeartless] = lambda state: self.get_easy_thousand_heartless_rules(state)
            self.fight_region_rules[RegionName.DataDemyx] = lambda state: self.get_easy_data_demyx_rules(state)
            self.fight_region_rules[RegionName.Sephi] = lambda state: self.get_easy_sephiroth_rules(state)
            self.fight_region_rules[RegionName.CorFirstFight] = lambda state: self.get_easy_cor_first_fight_movement_rules(state) and (self.get_easy_cor_first_fight_rules(state) or self.get_easy_cor_skip_first_rules(state))
            self.fight_region_rules[RegionName.CorSecondFight] = lambda state: self.get_easy_cor_second_fight_movement_rules(state)
            self.fight_region_rules[RegionName.Transport] = lambda state: self.get_easy_transport_fight_rules(state) and self.get_easy_transport_movement_rules(state)
            self.fight_region_rules[RegionName.Scar] = lambda state: self.get_easy_scar_rules(state)
            self.fight_region_rules[RegionName.GroundShaker] = lambda state: self.get_easy_groundshaker_rules(state)
            self.fight_region_rules[RegionName.DataSaix] = lambda state: self.get_easy_data_saix_rules(state)
            self.fight_region_rules[RegionName.TwilightThorn] = lambda state: self.get_twilight_thorn_rules()
            self.fight_region_rules[RegionName.Axel1] = lambda state: self.get_axel_one_rules()
            self.fight_region_rules[RegionName.Axel2] = lambda state: self.get_axel_two_rules()
            self.fight_region_rules[RegionName.DataRoxas] = lambda state: self.get_easy_data_roxas_rules(state)
            self.fight_region_rules[RegionName.DataAxel] = lambda state: self.get_easy_data_axel_rules(state)
            self.fight_region_rules[RegionName.Roxas] = lambda state: self.get_easy_roxas_rules(state)
            self.fight_region_rules[RegionName.Xigbar] = lambda state: self.get_easy_xigbar_rules(state)
            self.fight_region_rules[RegionName.Luxord] = lambda state: self.get_easy_luxord_rules(state)
            self.fight_region_rules[RegionName.Saix] = lambda state: self.get_easy_saix_rules(state)
            self.fight_region_rules[RegionName.Xemnas] = lambda state: self.get_easy_xemnas_rules(state)
            self.fight_region_rules[RegionName.ArmoredXemnas] = lambda state: self.get_easy_armored_xemnas_one_rules(state)
            self.fight_region_rules[RegionName.ArmoredXemnas2] = lambda state: self.get_normal_armored_xemnas_one_rules(state)
            self.fight_region_rules[RegionName.FinalXemnas] = lambda state: self.get_easy_final_xemnas_rules(state)
            self.fight_region_rules[RegionName.DataXemnas] = lambda state: self.get_easy_data_xemnas_rules(state)

        elif self.fight_logic == "Normal":
            self.fight_region_rules[RegionName.ShanYu] = lambda state: self.get_normal_shanyu_rules(state)
            self.fight_region_rules[RegionName.AnsemRiku] = lambda state: self.get_normal_ansemriku_rules(state)
            self.fight_region_rules[RegionName.StormRider] = lambda state: self.get_normal_stormrider_rules(state)
            self.fight_region_rules[RegionName.DataXigbar] = lambda state: self.get_normal_dataxigbar_rules(state)
            self.fight_region_rules[RegionName.TwinLords] = lambda state: self.get_normal_firelord_rules(state) and self.get_normal_blizzardlord_rules(state)
            self.fight_region_rules[RegionName.GenieJafar] = lambda state: self.get_normal_geniejafar_rules(state)
            self.fight_region_rules[RegionName.DataLexaeus] = lambda state: self.get_normal_datalexaeus_rules(state)
            self.fight_region_rules[RegionName.OldPete] = lambda state: self.get_old_pete_rules()
            self.fight_region_rules[RegionName.FuturePete] = lambda state: self.get_normal_futurepete_rules(state)
            self.fight_region_rules[RegionName.Terra] = lambda state: self.get_normal_terra_rules(state)
            self.fight_region_rules[RegionName.DataMarluxia] = lambda state: self.get_normal_datamarluxia_rules(state)
            self.fight_region_rules[RegionName.Barbosa] = lambda state: self.get_normal_barbosa_rules(state)
            self.fight_region_rules[RegionName.GrimReaper1] = lambda state: self.get_grim_reaper1_rules()
            self.fight_region_rules[RegionName.GrimReaper2] = lambda state: self.get_normal_grimreaper2_rules(state)
            self.fight_region_rules[RegionName.DataLuxord] = lambda state: self.get_normal_dataluxord_rules(state)
            self.fight_region_rules[RegionName.Cerberus] = lambda state: self.get_normal_cerberus_rules(state)
            self.fight_region_rules[RegionName.OlympusPete] = lambda state: self.get_normal_olympus_pete_rules(state)
            self.fight_region_rules[RegionName.Hydra] = lambda state: self.get_normal_hydra_rules(state)
            self.fight_region_rules[RegionName.Hades] = lambda state: self.get_normal_hades_rules(state)
            self.fight_region_rules[RegionName.DataZexion] = lambda state: self.get_normal_data_zexion_rules(state)
            self.fight_region_rules[RegionName.OcPainAndPanicCup] = lambda state: self.get_pain_and_panic_cup_rules(state)
            self.fight_region_rules[RegionName.OcCerberusCup] = lambda state: self.get_normal_cerberus_cup_rules(state)
            self.fight_region_rules[RegionName.Oc2TitanCup] = lambda state: self.get_normal_titan_cup_rules(state)
            self.fight_region_rules[RegionName.Oc2GofCup] = lambda state: self.get_goddess_of_fate_cup_entrance_rules(state),
            self.fight_region_rules[RegionName.HadesCups] = lambda state: self.get_hades_cup_rules(state)
            self.fight_region_rules[RegionName.Thresholder] = lambda state: self.get_normal_thresholder_rules(state)
            self.fight_region_rules[RegionName.Beast] = lambda state: self.get_beast_rules()
            self.fight_region_rules[RegionName.DarkThorn] = lambda state: self.get_normal_dark_thorn_rules(state)
            self.fight_region_rules[RegionName.Xaldin] = lambda state: self.get_normal_xaldin_rules(state)
            self.fight_region_rules[RegionName.DataXaldin] = lambda state: self.get_normal_data_xaldin_rules(state)
            self.fight_region_rules[RegionName.HostileProgram] = lambda state: self.get_normal_hostile_program_rules(state)
            self.fight_region_rules[RegionName.Mcp] = lambda state: self.get_mcp_rules(state)
            self.fight_region_rules[RegionName.DataLarxene] = lambda state: self.get_normal_data_larxene_rules(state)
            self.fight_region_rules[RegionName.PrisonKeeper] = lambda state: self.get_normal_prison_keeper_rules(state)
            self.fight_region_rules[RegionName.OogieBoogie] = lambda state: self.get_oogie_rules()
            self.fight_region_rules[RegionName.Experiment] = lambda state: self.get_normal_experiment_rules(state)
            self.fight_region_rules[RegionName.DataVexen] = lambda state: self.get_normal_data_vexen_rules(state)
            self.fight_region_rules[RegionName.Hb2Corridors] = lambda state: self.get_normal_corridors_fight_rules(state)
            self.fight_region_rules[RegionName.HBDemyx] = lambda state: self.get_normal_demyx_rules(state)
            self.fight_region_rules[RegionName.ThousandHeartless] = lambda state: self.get_normal_thousand_heartless_rules(state)
            self.fight_region_rules[RegionName.DataDemyx] = lambda state: self.get_normal_data_demyx_rules(state)
            self.fight_region_rules[RegionName.Sephi] = lambda state: self.get_normal_sephiroth_rules(state)
            self.fight_region_rules[RegionName.CorFirstFight] = lambda state: self.get_normal_cor_first_fight_movement_rules(state) and (self.get_normal_cor_first_fight_rules(state) or self.get_normal_cor_skip_first_rules(state))
            self.fight_region_rules[RegionName.CorSecondFight] = lambda state: self.get_normal_cor_second_fight_movement_rules(state)
            self.fight_region_rules[RegionName.Transport] = lambda state: self.get_normal_transport_fight_rules(state) and self.get_normal_transport_movement_rules(state)
            self.fight_region_rules[RegionName.Scar] = lambda state: self.get_normal_scar_rules(state)
            self.fight_region_rules[RegionName.GroundShaker] = lambda state: self.get_normal_groundshaker_rules(state)
            self.fight_region_rules[RegionName.DataSaix] = lambda state: self.get_normal_data_saix_rules(state)
            self.fight_region_rules[RegionName.TwilightThorn] = lambda state: self.get_twilight_thorn_rules()
            self.fight_region_rules[RegionName.Axel1] = lambda state: self.get_axel_one_rules()
            self.fight_region_rules[RegionName.Axel2] = lambda state: self.get_axel_two_rules()
            self.fight_region_rules[RegionName.DataRoxas] = lambda state: self.get_normal_data_roxas_rules(state)
            self.fight_region_rules[RegionName.DataAxel] = lambda state: self.get_normal_data_axel_rules(state)
            self.fight_region_rules[RegionName.Roxas] = lambda state: self.get_normal_roxas_rules(state)
            self.fight_region_rules[RegionName.Xigbar] = lambda state: self.get_normal_xigbar_rules(state)
            self.fight_region_rules[RegionName.Luxord] = lambda state: self.get_normal_luxord_rules(state)
            self.fight_region_rules[RegionName.Saix] = lambda state: self.get_normal_saix_rules(state)
            self.fight_region_rules[RegionName.Xemnas] = lambda state: self.get_normal_xemnas_rules(state)
            self.fight_region_rules[RegionName.ArmoredXemnas] = lambda state: self.get_normal_armored_xemnas_one_rules(state)
            self.fight_region_rules[RegionName.ArmoredXemnas2] = lambda state: self.get_normal_armored_xemnas_one_rules(state)
            self.fight_region_rules[RegionName.FinalXemnas] = lambda state: self.get_normal_final_xemnas_rules(state)
            self.fight_region_rules[RegionName.DataXemnas] = lambda state: self.get_normal_data_xemnas_rules(state)
        else:
            self.fight_region_rules[RegionName.ShanYu] = lambda state: self.get_hard_shanyu_rules(state)
            self.fight_region_rules[RegionName.AnsemRiku] = lambda state: self.get_hard_ansemriku_rules(state)
            self.fight_region_rules[RegionName.StormRider] = lambda state: self.get_hard_stormrider_rules(state)
            self.fight_region_rules[RegionName.DataXigbar] = lambda state: self.get_hard_dataxigbar_rules(state)
            self.fight_region_rules[RegionName.TwinLords] = lambda state: self.get_hard_firelord_rules(state) and self.get_hard_blizzardlord_rules(state)
            self.fight_region_rules[RegionName.GenieJafar] = lambda state: self.get_hard_geniejafar_rules(state)
            self.fight_region_rules[RegionName.DataLexaeus] = lambda state: self.get_hard_datalexaeus_rules(state)
            self.fight_region_rules[RegionName.OldPete] = lambda state: self.get_old_pete_rules()
            self.fight_region_rules[RegionName.FuturePete] = lambda state: self.get_hard_futurepete_rules(state)
            self.fight_region_rules[RegionName.Terra] = lambda state: self.get_hard_terra_rules(state)
            self.fight_region_rules[RegionName.DataMarluxia] = lambda state: self.get_hard_datamarluxia_rules(state)
            self.fight_region_rules[RegionName.Barbosa] = lambda state: self.get_hard_barbosa_rules(state)
            self.fight_region_rules[RegionName.GrimReaper1] = lambda state: self.get_grim_reaper1_rules()
            self.fight_region_rules[RegionName.GrimReaper2] = lambda state: self.get_hard_grimreaper2_rules(state)
            self.fight_region_rules[RegionName.DataLuxord] = lambda state: self.get_hard_dataluxord_rules(state)
            self.fight_region_rules[RegionName.Cerberus] = lambda state: self.get_hard_cerberus_rules(state)
            self.fight_region_rules[RegionName.OlympusPete] = lambda state: self.get_hard_olympus_pete_rules(state)
            self.fight_region_rules[RegionName.Hydra] = lambda state: self.get_hard_hydra_rules(state)
            self.fight_region_rules[RegionName.Hades] = lambda state: self.get_hard_hades_rules(state)
            self.fight_region_rules[RegionName.DataZexion] = lambda state: self.get_hard_data_zexion_rules(state)
            self.fight_region_rules[RegionName.OcPainAndPanicCup] = lambda state: self.get_pain_and_panic_cup_rules(state)
            self.fight_region_rules[RegionName.OcCerberusCup] = lambda state: self.get_hard_cerberus_cup_rules(state)
            self.fight_region_rules[RegionName.Oc2TitanCup] = lambda state: self.get_hard_titan_cup_rules(state)
            self.fight_region_rules[RegionName.Oc2GofCup] = lambda state: self.get_goddess_of_fate_cup_entrance_rules(state)
            self.fight_region_rules[RegionName.HadesCups] = lambda state: self.get_hades_cup_rules(state)
            self.fight_region_rules[RegionName.Thresholder] = lambda state: self.get_hard_thresholder_rules(state)
            self.fight_region_rules[RegionName.Beast] = lambda state: self.get_beast_rules()
            self.fight_region_rules[RegionName.DarkThorn] = lambda state: self.get_hard_dark_thorn_rules(state)
            self.fight_region_rules[RegionName.Xaldin] = lambda state: self.get_hard_xaldin_rules(state)
            self.fight_region_rules[RegionName.DataXaldin] = lambda state: self.get_hard_data_xaldin_rules(state)
            self.fight_region_rules[RegionName.HostileProgram] = lambda state: self.get_hard_hostile_program_rules(state)
            self.fight_region_rules[RegionName.Mcp] = lambda state: self.get_mcp_rules(state)
            self.fight_region_rules[RegionName.DataLarxene] = lambda state: self.get_hard_data_larxene_rules(state)
            self.fight_region_rules[RegionName.PrisonKeeper] = lambda state: self.get_hard_prison_keeper_rules(state)
            self.fight_region_rules[RegionName.OogieBoogie] = lambda state: self.get_oogie_rules()
            self.fight_region_rules[RegionName.Experiment] = lambda state: self.get_hard_experiment_rules(state)
            self.fight_region_rules[RegionName.DataVexen] = lambda state: self.get_hard_data_vexen_rules(state)
            self.fight_region_rules[RegionName.Hb2Corridors] = lambda state: self.get_hard_corridors_fight_rules(state)
            self.fight_region_rules[RegionName.HBDemyx] = lambda state: self.get_hard_demyx_rules(state)
            self.fight_region_rules[RegionName.ThousandHeartless] = lambda state: self.get_hard_thousand_heartless_rules(state)
            self.fight_region_rules[RegionName.DataDemyx] = lambda state: self.get_hard_data_demyx_rules(state)
            self.fight_region_rules[RegionName.Sephi] = lambda state: self.get_hard_sephiroth_rules(state)
            self.fight_region_rules[RegionName.CorFirstFight] = lambda state: self.get_hard_cor_first_fight_movement_rules(state) and (self.get_hard_cor_first_fight_rules(state) or self.get_hard_cor_skip_first_rules(state))
            self.fight_region_rules[RegionName.CorSecondFight] = lambda state: self.get_hard_cor_second_fight_movement_rules(state)
            self.fight_region_rules[RegionName.Transport] = lambda state: self.get_hard_transport_fight_rules(state) and self.get_hard_transport_movement_rules(state)
            self.fight_region_rules[RegionName.Scar] = lambda state: self.get_hard_scar_rules(state)
            self.fight_region_rules[RegionName.GroundShaker] = lambda state: self.get_hard_groundshaker_rules(state)
            self.fight_region_rules[RegionName.DataSaix] = lambda state: self.get_hard_data_saix_rules(state)
            self.fight_region_rules[RegionName.TwilightThorn] = lambda state: self.get_twilight_thorn_rules()
            self.fight_region_rules[RegionName.Axel1] = lambda state: self.get_axel_one_rules()
            self.fight_region_rules[RegionName.Axel2] = lambda state: self.get_axel_two_rules()
            self.fight_region_rules[RegionName.DataRoxas] = lambda state: self.get_hard_data_roxas_rules(state)
            self.fight_region_rules[RegionName.DataAxel] = lambda state: self.get_hard_data_axel_rules(state)
            self.fight_region_rules[RegionName.Roxas] = lambda state: self.get_hard_roxas_rules(state)
            self.fight_region_rules[RegionName.Xigbar] = lambda state: self.get_hard_xigbar_rules(state)
            self.fight_region_rules[RegionName.Luxord] = lambda state: self.get_hard_luxord_rules(state)
            self.fight_region_rules[RegionName.Saix] = lambda state: self.get_hard_saix_rules(state)
            self.fight_region_rules[RegionName.Xemnas] = lambda state: self.get_hard_xemnas_rules(state)
            self.fight_region_rules[RegionName.ArmoredXemnas] = lambda state: self.get_hard_armored_xemnas_one_rules(state)
            self.fight_region_rules[RegionName.ArmoredXemnas2] = lambda state: self.get_hard_armored_xemnas_one_rules(state)
            self.fight_region_rules[RegionName.FinalXemnas] = lambda state: self.get_hard_final_xemnas_rules(state)
            self.fight_region_rules[RegionName.DataXemnas] = lambda state: self.get_hard_data_xemnas_rules(state)

    def set_kh2_fight_rules(self) -> None:
        for region_name, rules in self.fight_region_rules.items():
            region = self.multiworld.get_region(region_name, self.player)
            for entrance in region.entrances:
                entrance.access_rule = rules

    def get_easy_shanyu_rules(self, state: CollectionState) -> bool:
        # easy: gap closer, defensive tool,drive form
        return self.kh2_list_any_sum([gap_closer, defensive_tool, form_list], state) >= 3

    def get_normal_shanyu_rules(self, state: CollectionState) -> bool:
        # normal: 2 out of easy
        return self.kh2_list_any_sum([gap_closer, defensive_tool, form_list], state) >= 2

    def get_hard_shanyu_rules(self, state: CollectionState) -> bool:
        # hard: defensive tool or drive form
        return self.kh2_list_any_sum([defensive_tool, form_list], state) >= 1

    def get_easy_ansemriku_rules(self, state: CollectionState) -> bool:
        # easy: gap closer,defensive tool,ground finisher/limit form
        return self.kh2_list_any_sum([gap_closer, defensive_tool, [ItemName.LimitForm], ground_finisher], state) >= 3

    def get_normal_ansemriku_rules(self, state: CollectionState) -> bool:
        # normal: defensive tool and (gap closer/ground finisher/limit form)
        return self.kh2_list_any_sum([gap_closer, defensive_tool, [ItemName.LimitForm], ground_finisher], state) >= 2

    def get_hard_ansemriku_rules(self, state: CollectionState) -> bool:
        # hard: defensive tool or limit form
        return self.kh2_has_any([ItemName.ReflectElement, ItemName.Guard, ItemName.LimitForm], state)

    def get_easy_stormrider_rules(self, state: CollectionState) -> bool:
        # easy: has defensive tool,drive form, party limit,aerial move
        return self.kh2_list_any_sum([defensive_tool, party_limit, aerial_move, form_list], state) >= 4

    def get_normal_stormrider_rules(self, state: CollectionState) -> bool:
        # normal: 3 of easy
        return self.kh2_list_any_sum([defensive_tool, party_limit, aerial_move, form_list], state) >= 3

    def get_hard_stormrider_rules(self, state: CollectionState) -> bool:
        # hard: 2 of easy
        return self.kh2_list_any_sum([defensive_tool, party_limit, aerial_move, form_list], state) >= 2

    def get_easy_dataxigbar_rules(self, state: CollectionState) -> bool:
        # easy:final 7,firaga,2 air combo plus,air gap closer, finishing plus,guard,reflega,horizontal slash,donald limit
        return self.kh2_dict_count(easy_data_xigbar_tools, state) and self.kh2_has_final_form(state) and self.get_form_level_max(state, 5) and \
            self.kh2_has_any(donald_limit, state)

    def get_normal_dataxigbar_rules(self, state: CollectionState) -> bool:
        # normal:final 7,firaga,finishing plus,guard,reflect horizontal slash,donald limit
        return self.kh2_dict_count(normal_data_xigbar_tools, state) and self.kh2_has_final_form(state) and self.get_form_level_max(state, 5) and \
            self.kh2_has_any(donald_limit, state)

    def get_hard_dataxigbar_rules(self, state: CollectionState) -> bool:
        # hard:((final 5, fira) or donald limit), finishing plus,guard/reflect
        return ((self.kh2_has_final_form(state) and self.get_form_level_max(state, 3) and state.has(ItemName.FireElement, self.player, 2))
                or self.kh2_has_any(donald_limit, state)) and state.has(ItemName.FinishingPlus, self.player) and self.kh2_has_any(defensive_tool, state)

    def get_easy_firelord_rules(self, state: CollectionState) -> bool:
        # easy: drive form,defensive tool,one black magic,party limit
        return self.kh2_list_any_sum([form_list, defensive_tool, black_magic, party_limit], state) >= 4

    def get_normal_firelord_rules(self, state: CollectionState) -> bool:
        # normal: 3 of easy
        return self.kh2_list_any_sum([form_list, defensive_tool, black_magic, party_limit], state) >= 3

    def get_hard_firelord_rules(self, state: CollectionState) -> bool:
        # hard:2 of easy
        return self.kh2_list_any_sum([form_list, defensive_tool, black_magic, party_limit], state) >= 2

    def get_easy_blizzardlord_rules(self, state: CollectionState) -> bool:
        # easy: drive form,defensive tool,one black magic,party limit
        return self.kh2_list_any_sum([form_list, defensive_tool, black_magic, party_limit], state) >= 4

    def get_normal_blizzardlord_rules(self, state: CollectionState) -> bool:
        # normal: 3 of easy
        return self.kh2_list_any_sum([form_list, defensive_tool, black_magic, party_limit], state) >= 3

    def get_hard_blizzardlord_rules(self, state: CollectionState) -> bool:
        # hard: 2 of easy
        return self.kh2_list_any_sum([form_list, defensive_tool, black_magic, party_limit], state) >= 2

    def get_easy_geniejafar_rules(self, state: CollectionState) -> bool:
        # easy: defensive tool,black magic,ground finisher,finishing plus
        return self.kh2_list_any_sum([defensive_tool, black_magic, ground_finisher, {ItemName.FinishingPlus}], state) >= 4

    def get_normal_geniejafar_rules(self, state: CollectionState) -> bool:
        # normal: defensive tool, ground finisher,finishing plus
        return self.kh2_list_any_sum([defensive_tool, ground_finisher, {ItemName.FinishingPlus}], state) >= 3

    def get_hard_geniejafar_rules(self, state: CollectionState) -> bool:
        # hard: defensive tool,finishing plus
        return self.kh2_list_any_sum([defensive_tool, {ItemName.FinishingPlus}], state) >= 2

    def get_easy_datalexaeus_rules(self, state: CollectionState) -> bool:
        # easy:both gap closers,final 7,firaga,reflera,donald limit, guard
        return self.kh2_dict_count(easy_data_lex_tools, state) and self.kh2_has_final_form(state) and self.get_form_level_max(state, 5) and \
            self.kh2_list_any_sum([donald_limit], state) >= 1

    def get_normal_datalexaeus_rules(self, state: CollectionState) -> bool:
        # normal:one gap closer,final 5,fira,reflect, donald limit,guard
        return self.kh2_dict_count(normal_data_lex_tools, state) and self.kh2_has_final_form(state) and self.get_form_level_max(state, 5) and \
            self.kh2_list_any_sum([donald_limit, gap_closer], state) >= 2

    def get_hard_datalexaeus_rules(self, state: CollectionState) -> bool:
        # hard:defensive tool,gap closer
        return self.kh2_list_any_sum([defensive_tool, gap_closer], state) >= 2

    @staticmethod
    def get_old_pete_rules():
        # fight is free.
        return True

    def get_easy_futurepete_rules(self, state: CollectionState) -> bool:
        # easy:defensive option,gap closer,drive form
        return self.kh2_list_any_sum([defensive_tool, gap_closer, form_list], state) >= 3

    def get_normal_futurepete_rules(self, state: CollectionState) -> bool:
        # normal:2 of easy
        return self.kh2_list_any_sum([defensive_tool, gap_closer, form_list], state) >= 2

    def get_hard_futurepete_rules(self, state: CollectionState) -> bool:
        # hard 1 of easy
        return self.kh2_list_any_sum([defensive_tool, gap_closer, form_list], state) >= 1

    def get_easy_datamarluxia_rules(self, state: CollectionState) -> bool:
        # easy:both gap closers,final 7,firaga,reflera,donald limit, guard
        return self.kh2_dict_count(easy_data_marluxia_tools, state) and self.kh2_has_final_form(state) and self.get_form_level_max(state, 5) and self.kh2_list_any_sum([donald_limit], state) >= 1

    def get_normal_datamarluxia_rules(self, state: CollectionState) -> bool:
        # normal:one gap closer,final 5,fira,reflect, donald limit,guard
        return self.kh2_dict_count(normal_data_marluxia_tools, state) and self.kh2_has_final_form(state) and self.get_form_level_max(state, 3) and self.kh2_list_any_sum([donald_limit, gap_closer], state) >= 2

    def get_hard_datamarluxia_rules(self, state: CollectionState) -> bool:
        # hard:defensive tool,gap closer and aerial recovery
        return self.kh2_list_any_sum([defensive_tool, gap_closer, [ItemName.AerialRecovery]], state) >= 3

    def get_easy_terra_rules(self, state: CollectionState) -> bool:
        # easy:scom,gap closers,explosion,2 combo pluses,final 7,firaga, donald limits,reflect,guard,3 dodge roll,3 aerial dodge and 3glide,aerial recovery
        return self.kh2_dict_count(easy_terra_tools, state) and self.kh2_has_final_form(state) and self.get_form_level_max(state, 5),

    def get_normal_terra_rules(self, state: CollectionState) -> bool:
        # normal:gap closers,explosion,2 combo pluses,2 dodge roll,2 aerial dodge and lvl 2glide,guard,donald limit, guard,aerial recovery
        return self.kh2_dict_count(normal_terra_tools, state) and self.kh2_list_any_sum([donald_limit], state) >= 1

    def get_hard_terra_rules(self, state: CollectionState) -> bool:
        # hard:1 gap closer,explosion,2 combo pluses,2 dodge roll,2 aerial dodge and lvl 2glide,guard,aerial recovery
        return self.kh2_dict_count(hard_terra_tools, state) and self.kh2_list_any_sum([gap_closer], state) >= 1

    def get_easy_barbosa_rules(self, state: CollectionState) -> bool:
        # easy:blizzara and thundara or one of each,defensive tool
        return self.kh2_list_count_sum([ItemName.BlizzardElement, ItemName.ThunderElement], state) >= 2 and self.kh2_list_any_sum([defensive_tool], state) >= 1

    def get_normal_barbosa_rules(self, state: CollectionState) -> bool:
        # normal:(blizzard or thunder) and defensive tool
        return self.kh2_list_any_sum([defensive_tool, {ItemName.BlizzardElement, ItemName.ThunderElement}], state) >= 2

    def get_hard_barbosa_rules(self, state: CollectionState) -> bool:
        # hard: defensive tool
        return self.kh2_list_any_sum([defensive_tool], state) >= 1

    @staticmethod
    def get_grim_reaper1_rules():
        # fight is free.
        return True

    def get_easy_grimreaper2_rules(self, state: CollectionState) -> bool:
        # easy:master form,thunder,defensive option
        return self.kh2_list_any_sum([defensive_tool, {ItemName.MasterForm, ItemName.ThunderElement}], state) >= 2

    def get_normal_grimreaper2_rules(self, state: CollectionState) -> bool:
        # normal:master form/stitch,thunder,defensive option
        return self.kh2_list_any_sum([defensive_tool, {ItemName.MasterForm, ItemName.Stitch}, {ItemName.ThunderElement}], state) >= 3

    def get_hard_grimreaper2_rules(self, state: CollectionState) -> bool:
        # hard:any black magic,defensive option.
        return self.kh2_list_any_sum([black_magic, defensive_tool], state) >= 2

    def get_easy_dataluxord_rules(self, state: CollectionState) -> bool:
        # easy:gap closers,reflega,aerial dodge lvl 2,glide lvl 2,guard
        return self.kh2_dict_count(easy_data_luxord_tools, state)

    def get_normal_dataluxord_rules(self, state: CollectionState) -> bool:
        # normal:1 gap closer,reflect,aerial dodge lvl 1,glide lvl 1,guard
        return self.kh2_has_all([ItemName.ReflectElement, ItemName.AerialDodge, ItemName.Glide, ItemName.Guard], state) and self.kh2_has_any(defensive_tool, state)

    def get_hard_dataluxord_rules(self, state: CollectionState) -> bool:
        # hard:quick run,defensive option
        return self.kh2_list_any_sum([{ItemName.QuickRun}, defensive_tool], state)

    def get_easy_cerberus_rules(self, state: CollectionState) -> bool:
        # easy:defensive option, offensive magic
        return self.kh2_list_any_sum([defensive_tool, black_magic], state) >= 2

    def get_normal_cerberus_rules(self, state: CollectionState) -> bool:
        # normal:defensive option, offensive magic
        # return self.kh2_list_any_sum([defensive_tool, black_magic], state) >= 2
        return self.kh2_list_any_sum([defensive_tool, black_magic], state) >= 2

    def get_hard_cerberus_rules(self, state: CollectionState) -> bool:
        # Hard: defensive option
        return self.kh2_has_any(defensive_tool, state)

    def get_pain_and_panic_cup_rules(self, state: CollectionState) -> bool:
        # easy:2 party limit,reflect
        return self.kh2_list_count_sum(party_limit, state) >= 2 and state.has(ItemName.ReflectElement, self.player) and (self.kh2_has_all([ItemName.FuturePeteEvent], state) or state.has(ItemName.HadesCupTrophy, self.player))

    def get_normal_pain_and_panic_cup_rules(self, state: CollectionState) -> bool:
        # normal:1 party limit,reflect
        return self.kh2_list_count_sum(party_limit, state) >= 1 and state.has(ItemName.ReflectElement, self.player) and (self.kh2_has_all([ItemName.FuturePeteEvent], state) or state.has(ItemName.HadesCupTrophy, self.player))

    def get_hard_pain_and_panic_cup_rules(self, state: CollectionState) -> bool:
        # hard:reflect
        return state.has(ItemName.ReflectElement, self.player) and (self.kh2_has_all([ItemName.FuturePeteEvent], state) or state.has(ItemName.HadesCupTrophy, self.player))

    def get_easy_cerberus_cup_rules(self, state: CollectionState) -> bool:
        # easy:3 drive forms,reflect
        return self.get_form_level_max(state, 3) and state.has(ItemName.ReflectElement, self.player) and (self.kh2_has_all([ItemName.ScarEvent, ItemName.OogieBoogieEvent, ItemName.TwinLordsEvent], state) or state.has(ItemName.HadesCupTrophy, self.player))

    def get_normal_cerberus_cup_rules(self, state: CollectionState) -> bool:
        # normal:2 drive forms,reflect
        return self.get_form_level_max(state, 2) and state.has(ItemName.ReflectElement, self.player) and (self.kh2_has_all([ItemName.ScarEvent, ItemName.OogieBoogieEvent, ItemName.TwinLordsEvent], state) or state.has(ItemName.HadesCupTrophy, self.player))

    def get_hard_cerberus_cup_rules(self, state: CollectionState) -> bool:
        # hard:reflect
        return state.has(ItemName.ReflectElement, self.player) and (self.kh2_has_all([ItemName.ScarEvent, ItemName.OogieBoogieEvent, ItemName.TwinLordsEvent], state) or state.has(ItemName.HadesCupTrophy, self.player))

    # easy:3 drive forms,reflect
    def get_easy_titan_cup_rules(self, state: CollectionState) -> bool:
        # easy:4 summons,reflera
        return self.kh2_list_count_sum(summons, state) >= 4 and state.has(ItemName.ReflectElement, self.player, 2) and (state.has(ItemName.HadesEvent, self.player) or state.has(ItemName.HadesCupTrophy, self.player))

    def get_normal_titan_cup_rules(self, state: CollectionState) -> bool:
        # normal:4 summons,reflera
        return self.kh2_list_count_sum(summons, state) >= 3 and state.has(ItemName.ReflectElement, self.player, 2) and (state.has(ItemName.HadesEvent, self.player) or state.has(ItemName.HadesCupTrophy, self.player))

    def get_hard_titan_cup_rules(self, state: CollectionState) -> bool:
        # hard:2 summons,reflera
        return self.kh2_list_count_sum(summons, state) >= 2 and state.has(ItemName.ReflectElement, self.player, 2) and (state.has(ItemName.HadesEvent, self.player) or state.has(ItemName.HadesCupTrophy, self.player))

    def get_goddess_of_fate_cup_entrance_rules(self, state: CollectionState) -> bool:
        # can beat all the other cups+xemnas 1
        return self.kh2_has_all([ItemName.OcPainAndPanicCupEvent, ItemName.OcCerberusCupEvent, ItemName.Oc2TitanCupEvent, ItemName.XemnasEvent], state)

    def get_hades_cup_rules(self, state: CollectionState) -> bool:
        # can beat goddess of fate cup
        return state.has(ItemName.Oc2GofCupEvent, self.player)

    def get_easy_olympus_pete_rules(self, state: CollectionState) -> bool:
        # easy:gap closer,defensive option,drive form
        return self.kh2_list_any_sum([gap_closer, defensive_tool, form_list], state) >= 3

    def get_normal_olympus_pete_rules(self, state: CollectionState) -> bool:
        # normal:2 of those things
        return self.kh2_list_any_sum([gap_closer, defensive_tool, form_list], state) >= 2

    def get_hard_olympus_pete_rules(self, state: CollectionState) -> bool:
        # hard:1 of those things
        return self.kh2_list_any_sum([gap_closer, defensive_tool, form_list], state) >= 1

    def get_easy_hydra_rules(self, state: CollectionState) -> bool:
        # easy:drive form,defensive option,offensive magic
        return self.kh2_list_any_sum([black_magic, defensive_tool, form_list], state) >= 3

    def get_normal_hydra_rules(self, state: CollectionState) -> bool:
        # normal 2 of those things
        return self.kh2_list_any_sum([black_magic, defensive_tool, form_list], state) >= 2

    def get_hard_hydra_rules(self, state: CollectionState) -> bool:
        # hard: one of those things
        return self.kh2_list_any_sum([black_magic, defensive_tool, form_list], state) >= 1

    def get_easy_hades_rules(self, state: CollectionState) -> bool:
        # easy:drive form,summon,gap closer,defensive option
        return self.kh2_list_any_sum([gap_closer, summons, defensive_tool, form_list], state) >= 4

    def get_normal_hades_rules(self, state: CollectionState) -> bool:
        # normal:3 of those things
        return self.kh2_list_any_sum([gap_closer, summons, defensive_tool, form_list], state) >= 3

    def get_hard_hades_rules(self, state: CollectionState) -> bool:
        # hard:2 of those things
        return self.kh2_list_any_sum([gap_closer, summons, defensive_tool, form_list], state) >= 2

    def get_easy_data_zexion_rules(self, state: CollectionState) -> bool:
        # easy: final 7,firaga,scom,both donald limits, Reflega ,guard,2 gap closers,quick run level 3
        return self.kh2_dict_count(easy_data_zexion, state) and self.kh2_has_final_form(state) and self.get_form_level_max(state, 5)

    def get_normal_data_zexion_rules(self, state: CollectionState) -> bool:
        # normal:final 7,firaga, donald limit, Reflega ,guard,1 gap closers,quick run level 3
        return self.kh2_dict_count(normal_data_zexion, state) and self.kh2_has_final_form(state) and self.get_form_level_max(state, 5) and self.kh2_list_any_sum([donald_limit, gap_closer], state) >= 2,

    def get_hard_data_zexion_rules(self, state: CollectionState) -> bool:
        # hard:final 5,fira, donald limit, reflect,gap closer,quick run level 2
        return self.kh2_dict_count(hard_data_zexion, state) and self.kh2_has_final_form(state) and self.get_form_level_max(state, 3) and self.kh2_list_any_sum([donald_limit, gap_closer], state) >= 2,

    def get_easy_thresholder_rules(self, state: CollectionState) -> bool:
        # easy:drive form,black magic,defensive tool
        return self.kh2_list_any_sum([form_list, black_magic, defensive_tool], state) >= 3

    def get_normal_thresholder_rules(self, state: CollectionState) -> bool:
        # normal:2 of those things
        return self.kh2_list_any_sum([form_list, black_magic, defensive_tool], state) >= 2

    def get_hard_thresholder_rules(self, state: CollectionState) -> bool:
        # hard:defensive tool or drive form
        return self.kh2_list_any_sum([form_list, defensive_tool], state) >= 1

    @staticmethod
    def get_beast_rules():
        # fight is free
        return True

    def get_easy_dark_thorn_rules(self, state: CollectionState) -> bool:
        # easy:drive form,defensive tool,gap closer
        return self.kh2_list_any_sum([form_list, gap_closer, defensive_tool], state) >= 3

    def get_normal_dark_thorn_rules(self, state: CollectionState) -> bool:
        # normal:drive form,defensive tool

        return self.kh2_list_any_sum([form_list, defensive_tool], state) >= 2

    def get_hard_dark_thorn_rules(self, state: CollectionState) -> bool:
        # hard:defensive tool
        return self.kh2_list_any_sum([defensive_tool], state) >= 1

    def get_easy_xaldin_rules(self, state: CollectionState) -> bool:
        # easy:guard,2 aerial modifier,valor/master/final
        return self.kh2_list_any_sum([[ItemName.Guard], [ItemName.ValorForm, ItemName.MasterForm, ItemName.FinalForm]], state) >= 2 and self.kh2_list_count_sum(aerial_move, state) >= 2,

    def get_normal_xaldin_rules(self, state: CollectionState) -> bool:
        # normal:guard,1 aerial modifier
        return self.kh2_list_any_sum([aerial_move], state) >= 1 and state.has(ItemName.Guard, self.player)

    def get_hard_xaldin_rules(self, state: CollectionState) -> bool:
        # hard:guard
        return state.has(ItemName.Guard, self.player)

    def get_easy_data_xaldin_rules(self, state: CollectionState) -> bool:
        # easy:final 7,firaga,2 air combo plus, finishing plus,guard,reflega,donald limit,high jump aerial dodge glide lvl 3,magnet,aerial dive,aerial spiral,hori slash,berserk charge
        return self.kh2_dict_count(easy_data_xaldin, state) and self.kh2_has_final_form(state) and self.get_form_level_max(state, 5)

    def get_normal_data_xaldin_rules(self, state: CollectionState) -> bool:
        # normal:final 7,firaga, finishing plus,guard,reflega,donald limit,high jump aerial dodge glide lvl 3,magnet,aerial dive,aerial spiral,hori slash
        return self.kh2_dict_count(normal_data_xaldin, state) and self.kh2_has_final_form(state) and self.get_form_level_max(state, 5)

    def get_hard_data_xaldin_rules(self, state: CollectionState) -> bool:
        # hard:final 5, fira, party limit, finishing plus,guard,high jump aerial dodge glide lvl 2,magnet,aerial dive
        return self.kh2_dict_count(hard_data_xaldin, state) and self.kh2_has_final_form(state) and self.get_form_level_max(state, 3) and self.kh2_has_any(party_limit, state)

    def get_easy_hostile_program_rules(self, state: CollectionState) -> bool:
        # easy:donald limit,reflect,drive form,summon

        return self.kh2_list_any_sum([donald_limit, form_list, summons, {ItemName.ReflectElement}], state) >= 4

    def get_normal_hostile_program_rules(self, state: CollectionState) -> bool:
        # normal:3 of those things
        return self.kh2_list_any_sum([donald_limit, form_list, summons, {ItemName.ReflectElement}], state) >= 3

    def get_hard_hostile_program_rules(self, state: CollectionState) -> bool:
        # hard: 2 of those things

        return self.kh2_list_any_sum([donald_limit, form_list, summons, {ItemName.ReflectElement}], state) >= 2

    def get_mcp_rules(self, state: CollectionState) -> bool:
        # same fight rules. Change this if boss enemy
        return state.has(ItemName.HostileProgramEvent, self.player)

    def get_easy_data_larxene_rules(self, state: CollectionState) -> bool:
        # easy: final 7,firaga,scom,both donald limits, Reflega,guard,2 gap closers,2 ground finishers,aerial dodge 3,glide 3

        return self.kh2_dict_count(easy_data_larxene, state) and self.kh2_has_final_form(state) and self.get_form_level_max(state, 5),

    def get_normal_data_larxene_rules(self, state: CollectionState) -> bool:
        # normal:final 7,firaga, donald limit, Reflega ,guard,1 gap closers,1 ground finisher,aerial dodge 3,glide 3
        return self.kh2_dict_count(easy_data_larxene, state) and self.kh2_has_final_form(state) and self.get_form_level_max(state, 5),

    def get_hard_data_larxene_rules(self, state: CollectionState) -> bool:
        # hard:final 5,fira, donald limit, reflect,gap closer,aerial dodge 2,glide 2

        return self.kh2_dict_count(hard_data_larxene, state) and self.kh2_list_any_sum([gap_closer, donald_limit], state) >= 2 and self.kh2_has_final_form(state) and self.get_form_level_max(state, 3),

    def get_easy_prison_keeper_rules(self, state: CollectionState) -> bool:
        # easy:defensive tool,drive form, party limit

        return self.kh2_list_any_sum([defensive_tool, form_list, party_limit], state) >= 3

    def get_normal_prison_keeper_rules(self, state: CollectionState) -> bool:
        # normal:two of those things

        return self.kh2_list_any_sum([defensive_tool, form_list, party_limit], state) >= 2

    def get_hard_prison_keeper_rules(self, state: CollectionState) -> bool:
        # hard:one of those things

        return self.kh2_list_any_sum([defensive_tool, form_list, party_limit], state) >= 1

    @staticmethod
    def get_oogie_rules():
        # fight is free
        return True

    def get_easy_experiment_rules(self, state: CollectionState) -> bool:
        # easy:drive form,defensive tool,summon,party limit
        return self.kh2_list_any_sum([form_list, defensive_tool, party_limit, summons], state) >= 4

    def get_normal_experiment_rules(self, state: CollectionState) -> bool:
        # normal:3 of those things
        return self.kh2_list_any_sum([form_list, defensive_tool, party_limit, summons], state) >= 3

    def get_hard_experiment_rules(self, state: CollectionState) -> bool:
        # hard 2 of those things
        return self.kh2_list_any_sum([form_list, defensive_tool, party_limit, summons], state) >= 2

    def get_easy_data_vexen_rules(self, state: CollectionState) -> bool:
        # easy: final 7,firaga,scom,both donald limits, Reflega,guard,2 gap closers,2 ground finishers,aerial dodge 3,glide 3,dodge roll 3,quick run 3

        return self.kh2_dict_count(easy_data_vexen, state) and self.kh2_has_final_form(state) and self.get_form_level_max(state, 5),

    def get_normal_data_vexen_rules(self, state: CollectionState) -> bool:
        # normal:final 7,firaga, donald limit, Reflega,guard,1 gap closers,1 ground finisher,aerial dodge 3,glide 3,dodge roll 3,quick run 3

        return self.kh2_dict_count(normal_data_vexen, state) and self.kh2_list_any_sum([gap_closer, ground_finisher, donald_limit], state) >= 3 and self.kh2_has_final_form(state) and self.get_form_level_max(state, 5),

    def get_hard_data_vexen_rules(self, state: CollectionState) -> bool:
        # hard:final 5,fira, donald limit, reflect,gap closer,aerial dodge 2,glide 2,dodge roll 2,quick run 2

        return self.kh2_dict_count(hard_data_vexen, state) and self.kh2_list_any_sum([gap_closer, donald_limit], state) >= 2 and self.kh2_has_final_form(state) and self.get_form_level_max(state, 3),

    def get_easy_corridors_fight_rules(self, state: CollectionState) -> bool:
        # chicken little,magnera,magnet burst,defensive tool,form and party limit
        return self.kh2_dict_count({ItemName.ChickenLittle: 1, ItemName.MagnetElement: 2, ItemName.MagnetBurst: 1}, state) and self.kh2_list_any_sum([defensive_tool, form_list, party_limit], state) >= 3

    def get_normal_corridors_fight_rules(self, state: CollectionState) -> bool:
        # has 3 total of defensive tool,drive form,party limit,magnet,chicken,magnetburst
        # such as 3 reflects would count here or 3 party limits.
        return self.kh2_list_any_sum([defensive_tool, form_list, party_limit, [ItemName.ChickenLittle, ItemName.MagnetElement, ItemName.MagnetBurst]], state) >= 3

    def get_hard_corridors_fight_rules(self, state: CollectionState) -> bool:
        # 2 of normal's rules
        return self.kh2_list_any_sum([defensive_tool, form_list, party_limit, [ItemName.ChickenLittle, ItemName.MagnetElement, ItemName.MagnetBurst]], state) >= 2

    def get_easy_demyx_rules(self, state: CollectionState) -> bool:
        # defensive option,drive form,party limit
        return self.kh2_list_any_sum([defensive_tool, form_list, party_limit], state) >= 3

    def get_normal_demyx_rules(self, state: CollectionState) -> bool:
        # defensive option,drive form

        return self.kh2_list_any_sum([defensive_tool, form_list], state) >= 2

    def get_hard_demyx_rules(self, state: CollectionState) -> bool:
        # defensive option

        return self.kh2_list_any_sum([defensive_tool], state) >= 1

    def get_easy_thousand_heartless_rules(self, state: CollectionState) -> bool:
        # easy:scom,limit form,guard,magnera

        return self.kh2_dict_count(easy_thousand_heartless_rules, state)

    def get_normal_thousand_heartless_rules(self, state: CollectionState) -> bool:
        # normal:limit form, guard

        return self.kh2_dict_count(normal_thousand_heartless_rules, state)

    def get_hard_thousand_heartless_rules(self, state: CollectionState) -> bool:
        # hard:guard

        return state.has(ItemName.Guard, self.player)

    def get_easy_data_demyx_rules(self, state: CollectionState) -> bool:
        # easy:wisdom 7,1 form boosts,reflera,firaga,duck flare,guard,scom,finishing plus

        return self.kh2_dict_count(easy_data_demyx, state) and self.kh2_has_wisdom_form(state) and self.get_form_level_max(state, 5)

    def get_normal_data_demyx_rules(self, state: CollectionState) -> bool:
        # normal:remove form boost and scom

        return self.kh2_dict_count(normal_data_demyx, state) and self.kh2_has_wisdom_form(state) and self.get_form_level_max(state, 5)

    def get_hard_data_demyx_rules(self, state: CollectionState) -> bool:
        # hard:wisdom 6,reflect,guard,duck flare,fira,finishing plus
        return self.kh2_dict_count(hard_data_demyx, state) and self.kh2_has_wisdom_form(state) and self.get_form_level_max(state, 4)

    def get_easy_sephiroth_rules(self, state: CollectionState) -> bool:
        # easy:both gap closers,limit 5,reflega,guard,both 2 ground finishers,3 dodge roll,finishing plus,scom,aerial recovery
        return self.kh2_dict_count(easy_sephiroth_tools, state) and self.kh2_has_limit_form(state) and self.get_form_level_max(state, 3)

    def get_normal_sephiroth_rules(self, state: CollectionState) -> bool:
        # normal:both gap closers,limit 5,reflera,guard,both 2 ground finishers,3 dodge roll,finishing plus,aerial recovery
        return self.kh2_dict_count(normal_sephiroth_tools, state) and self.kh2_has_limit_form(state) and self.get_form_level_max(state, 3)

    def get_hard_sephiroth_rules(self, state: CollectionState) -> bool:
        # hard:1 gap closers,reflect, guard,both 1 ground finisher,2 dodge roll,finishing plus ,aerial recovery
        return self.kh2_dict_count(hard_sephiroth_tools, state) and self.kh2_list_any_sum([gap_closer, ground_finisher], state) >= 2

    def get_easy_cor_first_fight_movement_rules(self, state: CollectionState) -> bool:
        # easy: quick run 3 or wisdom 5 (wisdom has qr 3)
        return state.has(ItemName.QuickRun, self.player, 3) or (self.kh2_has_wisdom_form(state) and self.get_form_level_max(state, 3))

    def get_normal_cor_first_fight_movement_rules(self, state: CollectionState) -> bool:
        # normal: quick run 2 and aerial dodge 1 or wisdom 5 (wisdom has qr 3)
        return self.kh2_dict_count({ItemName.QuickRun: 2, ItemName.AerialDodge: 1}, state) or (self.kh2_has_wisdom_form(state) and self.get_form_level_max(state, 5)),

    def get_hard_cor_first_fight_movement_rules(self, state: CollectionState) -> bool:
        # hard: (quick run 1, aerial dodge 1) or (wisdom form and aerial dodge 1)
        return self.kh2_has_all([ItemName.AerialDodge, ItemName.QuickRun], state) or self.kh2_has_all([ItemName.AerialDodge, ItemName.WisdomForm], state)

    def get_easy_cor_first_fight_rules(self, state: CollectionState) -> bool:
        # easy:have 5 of these things (reflega,stitch and chicken,final form,magnera,explosion,thundara)
        return self.kh2_dict_one_count(not_hard_cor_tools_dict, state) >= 5 or (self.kh2_dict_one_count(not_hard_cor_tools_dict, state) >= 4 and self.kh2_has_final_form(state))

    def get_normal_cor_first_fight_rules(self, state: CollectionState) -> bool:
        # normal:have 3 of these things (reflega,stitch and chicken,final form,magnera,explosion,thundara)
        return self.kh2_dict_one_count(not_hard_cor_tools_dict, state) >= 3 or (self.kh2_dict_one_count(not_hard_cor_tools_dict, state) >= 2 and self.kh2_has_final_form(state))

    def get_hard_cor_first_fight_rules(self, state: CollectionState) -> bool:
        # hard: reflect,stitch or chicken,final form
        return state.has(ItemName.ReflectElement, self.player) and self.kh2_has_any([ItemName.Stitch, ItemName.ChickenLittle], state) and self.kh2_has_final_form(state)

    def get_easy_cor_skip_first_rules(self, state: CollectionState) -> bool:
        # if option is not allow skips return false else run rules
        if not self.world.options.CorSkipToggle:
            return False
        # easy: aerial dodge 3,master form,fire
        return state.has(ItemName.AerialDodge, self.player, 3) and self.kh2_has_all([ItemName.MasterForm, ItemName.FireElement], state)

    def get_normal_cor_skip_first_rules(self, state: CollectionState) -> bool:
        # if option is not allow skips return false else run rules
        if not self.world.options.CorSkipToggle:
            return False
        # normal: aerial dodge 2, master form,fire
        return state.has(ItemName.AerialDodge, self.player, 2) and self.kh2_has_all([ItemName.MasterForm, ItemName.FireElement], state)

    def get_hard_cor_skip_first_rules(self, state: CollectionState) -> bool:
        # if option is not allow skips return false else run rules
        if not self.world.options.CorSkipToggle:
            return False
        # hard:void cross(quick run 3,aerial dodge 1)
        # or (quick run 2,aerial dodge 2 and magic)
        # or (final form and (magic or combo master))
        # or (master form and (reflect or fire or thunder or combo master)
        # wall rise(aerial dodge 1 and (final form lvl 5 or glide 2) or (master form and (1 of black magic or combo master)
        return (self.kh2_dict_count({ItemName.QuickRun: 3, ItemName.AerialDodge: 1}, state)) \
            or (self.kh2_dict_count({ItemName.QuickRun: 2, ItemName.AerialDodge: 2}, state) and self.kh2_has_any(magic, state)) \
            or (state.has(ItemName.FinalForm, self.player) and (self.kh2_has_any(magic, state) or state.has(ItemName.ComboMaster, self.player))) \
            or (state.has(ItemName.MasterForm, self.player) and (self.kh2_has_any([ItemName.ReflectElement, ItemName.FireElement, ItemName.ComboMaster], state))) and state.has(ItemName.AerialDodge, self.player) and self.kh2_has_final_form(state) and self.get_form_level_max(state, 3) or state.has(ItemName.Glide, self.player, 2)

    def get_easy_cor_second_fight_movement_rules(self, state: CollectionState) -> bool:
        # easy: quick run 2, aerial dodge 3 or master form 5
        return self.kh2_dict_count({ItemName.QuickRun: 2, ItemName.AerialDodge: 3}, state) or self.kh2_has_master_form(state) and self.get_form_level_max(state, 3)

    def get_normal_cor_second_fight_movement_rules(self, state: CollectionState) -> bool:
        # normal: quick run 2, aerial dodge 2 or master 5
        return self.kh2_dict_count({ItemName.QuickRun: 2, ItemName.AerialDodge: 2}, state) or self.kh2_has_master_form(state) and self.get_form_level_max(state, 3)

    def get_hard_cor_second_fight_movement_rules(self, state: CollectionState) -> bool:
        # hard: (glide 1,aerial dodge 1 any magic) or (master 3 any magic) or glide 1 and aerial dodge 2
        return (self.kh2_has_all([ItemName.Glide, ItemName.AerialDodge], state) and self.kh2_has_any(magic, state)) \
            or (state.has(ItemName.MasterForm, self.player) and self.kh2_has_any(magic, state)) \
            or (state.has(ItemName.Glide, self.player) and state.has(ItemName.AerialDodge, self.player, 2))

    def get_easy_transport_fight_rules(self, state: CollectionState) -> bool:
        # easy: reflega,stitch and chicken,final form,magnera,explosion,finishing leap,thundaga,2 donald limits

        return self.kh2_dict_count(transport_tools_dict, state)

    def get_normal_transport_fight_rules(self, state: CollectionState) -> bool:
        # normal: 7 of those things
        return self.kh2_dict_one_count(transport_tools_dict, state) >= 7

    def get_hard_transport_fight_rules(self, state: CollectionState) -> bool:
        # hard: 5 of those things
        return self.kh2_dict_one_count(transport_tools_dict, state) >= 5

    def get_easy_transport_movement_rules(self, state: CollectionState) -> bool:
        # easy:high jump 3,aerial dodge 3,glide 3
        return self.kh2_dict_count({ItemName.HighJump: 3, ItemName.AerialDodge: 3, ItemName.Glide: 3}, state)

    def get_normal_transport_movement_rules(self, state: CollectionState) -> bool:
        # normal: high jump 2,glide 3,aerial dodge 2
        return self.kh2_dict_count({ItemName.HighJump: 2, ItemName.AerialDodge: 2, ItemName.Glide: 3}, state)

    def get_hard_transport_movement_rules(self, state: CollectionState) -> bool:
        # hard: (hj 2,glide 2,ad 1,any magic) or hj 1,glide 2,ad 3 any magic or (any magic master form,ad) or hj lvl 1,glide 3,ad 1
        return (self.kh2_dict_count({ItemName.HighJump: 2, ItemName.AerialDodge: 1, ItemName.Glide: 2}, state) and self.kh2_has_any(magic, state)) \
            or (self.kh2_dict_count({ItemName.HighJump: 1, ItemName.Glide: 2, ItemName.AerialDodge: 3}, state) and self.kh2_has_any(magic, state)) \
            or (self.kh2_dict_count({ItemName.HighJump: 1, ItemName.Glide: 3, ItemName.AerialDodge: 1}, state)) \
            or (self.kh2_has_all([ItemName.MasterForm, ItemName.AerialDodge], state) and self.kh2_has_any(magic, state))

    def get_easy_scar_rules(self, state: CollectionState) -> bool:
        # easy: reflect,thunder,fire
        return self.kh2_has_all([ItemName.ReflectElement, ItemName.ThunderElement, ItemName.FireElement], state)

    def get_normal_scar_rules(self, state: CollectionState) -> bool:
        # normal:reflect,fire
        return self.kh2_has_all([ItemName.ReflectElement, ItemName.FireElement], state)

    def get_hard_scar_rules(self, state: CollectionState) -> bool:
        # hard:reflect
        return state.has(ItemName.ReflectElement, self.player)

    def get_easy_groundshaker_rules(self, state: CollectionState) -> bool:
        # easy:berserk charge,cure,2 air combo plus,reflect
        return state.has(ItemName.AirComboPlus, self.player, 2) and self.kh2_has_all([ItemName.BerserkCharge, ItemName.CureElement, ItemName.ReflectElement], state)

    def get_normal_groundshaker_rules(self, state: CollectionState) -> bool:
        # normal:berserk charge,reflect,cure
        return self.kh2_has_all([ItemName.BerserkCharge, ItemName.ReflectElement, ItemName.CureElement], state)

    def get_hard_groundshaker_rules(self, state: CollectionState) -> bool:
        # hard:berserk charge or 2 air combo plus. reflect
        return (state.has(ItemName.BerserkCharge, self.player) or state.has(ItemName.AirComboPlus, self.player, 2)) and state.has(ItemName.ReflectElement, self.player)

    def get_easy_data_saix_rules(self, state: CollectionState) -> bool:
        # easy:guard,2 gap closers,thunder,blizzard,2 donald limit,reflega,2 ground finisher,aerial dodge 3,glide 3,final 7,firaga,scom
        return self.kh2_dict_count(easy_data_saix, state) and self.kh2_has_final_form(state) and self.get_form_level_max(state, 5)

    def get_normal_data_saix_rules(self, state: CollectionState) -> bool:
        # normal:guard,1 gap closers,thunder,blizzard,1 donald limit,reflega,1 ground finisher,aerial dodge 3,glide 3,final 7,firaga
        return self.kh2_dict_count(normal_data_saix, state) and self.kh2_list_any_sum([gap_closer, ground_finisher, donald_limit], state) >= 3 and self.kh2_has_final_form(state) and self.get_form_level_max(state, 5)

    def get_hard_data_saix_rules(self, state: CollectionState) -> bool:
        # hard:aerial dodge 3,glide 3,guard,reflect,blizzard,1 gap closer,1 ground finisher
        return self.kh2_dict_count(hard_data_saix, state) and self.kh2_list_any_sum([gap_closer, ground_finisher], state) >= 2

    @staticmethod
    def get_twilight_thorn_rules() -> bool:
        return True

    @staticmethod
    def get_axel_one_rules() -> bool:
        return True

    @staticmethod
    def get_axel_two_rules() -> bool:
        return True

    def get_easy_data_roxas_rules(self, state: CollectionState) -> bool:
        # easy:both gap closers,limit 5,reflega,guard,both 2 ground finishers,3 dodge roll,finishing plus,scom,aerial recovery
        return self.kh2_dict_count(easy_data_roxas_tools, state) and \
            self.kh2_has_limit_form(state) and self.get_form_level_max(state, 5)

    def get_normal_data_roxas_rules(self, state: CollectionState) -> bool:
        # normal:both gap closers,limit 5,reflera,guard,both 2 ground finishers,3 dodge roll,finishing plus, one of scom, aerial recovery

        return self.kh2_dict_count(normal_data_roxas_tools, state) and \
            self.kh2_has_limit_form(state) and self.get_form_level_max(state, 3) and \
            self.kh2_has_any(scom, state)

    def get_hard_data_roxas_rules(self, state: CollectionState) -> bool:
        # hard:1 gap closers,reflect, guard,both 1 ground finisher,2 dodge roll,finishing plus

        return self.kh2_dict_count(hard_data_roxas_tools, state) and self.kh2_list_any_sum([gap_closer, ground_finisher], state) >= 2

    def get_easy_data_axel_rules(self, state: CollectionState) -> bool:
        # easy:both gap closers,limit 5,reflega,guard,both 2 ground finishers,3 dodge roll,finishing plus,scom,blizzaga and 1 thunder
        return self.kh2_dict_count(easy_data_axel_tools, state) and self.kh2_has_limit_form(state) and self.get_form_level_max(state, 3)

    def get_normal_data_axel_rules(self, state: CollectionState) -> bool:
        # normal:1 gap closers,limit 5,reflera,guard,both 2 ground finishers,3 dodge roll,finishing plus,blizzaga and 1 thunder
        return self.kh2_dict_count(normal_data_axel_tools, state) and self.kh2_has_limit_form(state) and self.get_form_level_max(state, 3) and self.kh2_has_any([gap_closer], state)

    def get_hard_data_axel_rules(self, state: CollectionState) -> bool:
        # hard:1 gap closers,reflect, guard,both 1 ground finisher,2 dodge roll,finishing plus,blizzara,thunder

        return self.kh2_dict_count(hard_data_axel_tools, state) and self.kh2_list_any_sum([gap_closer, ground_finisher], state) >= 2

    def get_easy_roxas_rules(self, state: CollectionState) -> bool:
        # easy:aerial dodge 1,glide 1, limit form,thunder,reflera,guard break,2 gap closers,finishing plus,blizzard
        return self.kh2_dict_count(easy_roxas_tools, state)

    def get_normal_roxas_rules(self, state: CollectionState) -> bool:
        # normal:thunder,reflera,guard break,2 gap closers,finishing plus,blizzard
        return self.kh2_dict_count(normal_roxas_tools, state)

    def get_hard_roxas_rules(self, state: CollectionState) -> bool:
        # hard:guard
        return state.has(ItemName.Guard, self.player)

    def get_easy_xigbar_rules(self, state: CollectionState) -> bool:
        # easy:final 4,horizontal slash,fira,finishing plus,glide 2,aerial dodge 2,quick run 2,guard,reflect
        return self.kh2_dict_count(easy_xigbar_tools, state) and self.kh2_has_final_form(state) and self.get_form_level_max(state, 2)

    def get_normal_xigbar_rules(self, state: CollectionState) -> bool:
        # normal:final 4,fira,finishing plus,glide 2,aerial dodge 2,quick run 2,guard,reflect
        return self.kh2_dict_count(normal_xigbar_tools, state) and self.kh2_has_final_form(state) and self.get_form_level_max(state, 2)

    def get_hard_xigbar_rules(self, state: CollectionState) -> bool:
        # hard:guard,quick run,finishing plus
        return self.kh2_has_all([ItemName.Guard, ItemName.QuickRun, ItemName.FinishingPlus], state)

    def get_easy_luxord_rules(self, state: CollectionState) -> bool:
        # easy:aerial dodge 1,glide 1,quickrun 2,guard,reflera,2 gap closers,ground finisher,limit form
        return self.kh2_dict_count(easy_luxord_tools, state) and self.kh2_has_any(ground_finisher, state)

    def get_normal_luxord_rules(self, state: CollectionState) -> bool:
        # normal:aerial dodge 1,glide 1,quickrun 2,guard,reflera,1 gap closers,ground finisher
        return self.kh2_dict_count(normal_luxord_tools, state) and self.kh2_list_any_sum([gap_closer, ground_finisher], state) >= 2

    def get_hard_luxord_rules(self, state: CollectionState) -> bool:
        # hard:quick run,guard
        return self.kh2_has_all([ItemName.Guard, ItemName.QuickRun], state)

    def get_easy_saix_rules(self, state: CollectionState) -> bool:
        return self.kh2_dict_count(easy_saix_tools, state) and self.kh2_has_any(ground_finisher, state)

    def get_normal_saix_rules(self, state: CollectionState) -> bool:
        return self.kh2_dict_count(normal_saix_tools, state) and self.kh2_list_any_sum([gap_closer, ground_finisher], state) >= 2

    def get_hard_saix_rules(self, state: CollectionState) -> bool:
        return self.kh2_has_all([ItemName.Guard], state)

    def get_easy_xemnas_rules(self, state: CollectionState) -> bool:
        # easy:aerial dodge 1,glide 1,quickrun 2,guard,reflera,2 gap closers,ground finisher,limit form
        return self.kh2_dict_count(easy_xemnas_tools, state) and self.kh2_has_any(ground_finisher, state)

    def get_normal_xemnas_rules(self, state: CollectionState) -> bool:
        # normal:aerial dodge 1,glide 1,quickrun 2,guard,reflera,1 gap closers,ground finisher
        return self.kh2_dict_count(normal_xemnas_tools, state) and self.kh2_list_any_sum([gap_closer, ground_finisher], state) >= 2

    def get_hard_xemnas_rules(self, state: CollectionState) -> bool:
        return self.kh2_has_all([ItemName.Guard], state)

    def get_easy_armored_xemnas_one_rules(self, state: CollectionState) -> bool:
        # easy:donald limit,reflect,1 gap closer,ground finisher
        return self.kh2_list_any_sum([donald_limit, gap_closer, ground_finisher, {ItemName.ReflectElement}], state) >= 4

    def get_normal_armored_xemnas_one_rules(self, state: CollectionState) -> bool:
        # easy:donald limit,reflect,1 gap closer,ground finisher
        #
        return self.kh2_list_any_sum([gap_closer, ground_finisher, {ItemName.ReflectElement}], state) >= 3

    def get_hard_armored_xemnas_one_rules(self, state: CollectionState) -> bool:
        return state.has(ItemName.ReflectElement, self.player)

    def get_easy_armored_xemnas_two_rules(self, state: CollectionState) -> bool:
        return self.kh2_list_any_sum([gap_closer, ground_finisher, {ItemName.ReflectElement}, {ItemName.ThunderElement}], state) >= 4

    def get_normal_armored_xemnas_two_rules(self, state: CollectionState) -> bool:
        return self.kh2_list_any_sum([gap_closer, ground_finisher, {ItemName.ReflectElement}], state) >= 3

    def get_hard_armored_xemnas_two_rules(self, state: CollectionState) -> bool:
        return state.has(ItemName.ReflectElement, self.player)

    def get_easy_final_xemnas_rules(self, state: CollectionState) -> bool:
        # easy:reflera,limit form,finishing plus,gap closer,guard
        return self.kh2_has_all([ItemName.LimitForm, ItemName.FinishingPlus, ItemName.Guard], state) and state.has(ItemName.ReflectElement, self.player, 2) and self.kh2_has_any(gap_closer, state),

    def get_normal_final_xemnas_rules(self, state: CollectionState) -> bool:
        # normal:reflect,finishing plus,guard
        return self.kh2_has_all([ItemName.ReflectElement, ItemName.FinishingPlus, ItemName.Guard], state)

    def get_hard_final_xemnas_rules(self, state: CollectionState) -> bool:
        return state.has(ItemName.Guard, self.player)

    def get_easy_data_xemnas_rules(self, state: CollectionState) -> bool:
        # easy:combo master,slapshot,reflega,2 ground finishers,both gap closers,finishing plus,guard,limit 5,scom,trinity limit
        return self.kh2_dict_count(easy_data_xemnas, state) and self.kh2_list_count_sum(ground_finisher, state) >= 2 and self.kh2_has_limit_form(state) and self.get_form_level_max(state, 3)

    def get_normal_data_xemnas_rules(self, state: CollectionState) -> bool:
        # normal:combo master,slapshot,reflega,2 ground finishers,both gap closers,finishing plus,guard,limit 5,
        return self.kh2_dict_count(normal_data_xemnas, state) and self.kh2_list_count_sum(ground_finisher, state) >= 2 and self.kh2_has_limit_form(state) and self.get_form_level_max(state, 3)

    def get_hard_data_xemnas_rules(self, state: CollectionState) -> bool:
        # hard:combo master,slapshot,reflera,1 ground finishers,1 gap closers,finishing plus,guard,limit form
        return self.kh2_dict_count(hard_data_xemnas, state) and self.kh2_list_any_sum([ground_finisher, gap_closer], state) >= 2
