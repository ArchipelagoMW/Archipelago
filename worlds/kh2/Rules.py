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

    def level_locking_unlock(self, state: CollectionState, amount):
        if self.world.options.Promise_Charm and state.has(ItemName.PromiseCharm, self.player):
            return True
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
            add_rule(location, lambda state: state.has(exclusion_table["WeaponSlots"][location.name], self.player))
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
            # could get the location of each of these, but I feel like that would be less optimal
            region = self.multiworld.get_region(region_name, self.player)
            # if region_name in form_region_rules
            if region_name != RegionName.Summon:
                for entrance in region.entrances:
                    entrance.access_rule = self.form_region_rules[region_name]
            for loc in region.locations:
                loc.access_rule = self.form_rules[loc.name]


class KH2PuzzlePiecesRules(KH2Rules):
    player: int
    world: KH2World
    region_rules: Dict[str, Callable[[CollectionState], bool]]
    location_rules: Dict[str, Callable[[CollectionState], bool]]

    def __init__(self, world: KH2World) -> None:
        super().__init__(world)
        self.puzzle_pieces_location_rules = {
            LocationName.DaylightPuzzleTT2MarketStreet:       lambda state: self.has_vertical(state, 2) and self.has_glide(state),  # af
            LocationName.SunsetPuzzleTT3TSunsetTerrace1:      lambda state: self.has_vertical(state) and self.has_glide(state),  # one over the water fall #af
            LocationName.SunsetPuzzleTT3OldMansion:           lambda state: self.has_vertical(state, 2) and self.has_glide(state),  # af
            LocationName.DaylightPuzzleTT3MansionFoyer2:      lambda state: self.has_vertical(state) and self.has_glide(state, 3),  # one over the door #af
            LocationName.HeartPuzzleHB1MarketplaceItem:       lambda state: self.has_vertical(state),  # hj2 or ad 1 or any has final,master,limit,valor
            LocationName.SunsetPuzzleHB1Borough:              lambda state: self.has_vertical(state, 2) and self.has_glide(state, 2),
            LocationName.SunsetPuzzleHB2Corridors:            lambda state: self.has_vertical(state) and self.has_glide(state),
            LocationName.FrontierPuzzleHB2PosternDoorway:     lambda state: self.has_vertical(state) and self.has_glide(state),
            LocationName.SunsetPuzzleHB2BaileyDancers:        lambda state: self.has_vertical(state, 2) and self.has_glide(state, 2),
            LocationName.SunsetPuzzleEncampmentAwayFromStand: lambda state: self.has_vertical(state, 2) and self.has_glide(state, 2),
            LocationName.FrontierPuzzleMountainTrail:         lambda state: self.has_vertical(state) and self.has_glide(state),
            LocationName.HeartPuzzleVillageHome:              lambda state: self.has_vertical(state, 1),
            LocationName.DaylightPuzzleVillageBell:           lambda state: self.has_vertical(state, 2) and self.has_glide(state, 2),
            LocationName.DaylightPuzzleThroneRoomClose:       lambda state: self.has_vertical(state, 2) and self.has_glide(state, 2),
            LocationName.DaylightPuzzleRoomFar:               lambda state: self.has_vertical(state, 3) and self.has_glide(state, 3),
            LocationName.SunsetPuzzleEntranceHall:            lambda state: self.has_vertical(state, 2) and self.has_glide(state, 2),
            LocationName.DaylightPuzzleWestHall:              lambda state: self.has_vertical(state) and self.has_glide(state, 2),
            LocationName.DaylightPuzzleCaveDeadPassage:       lambda state: self.has_vertical(state, 2) and self.has_glide(state, 2),
            LocationName.DaylightPuzzleLostRoadOne:           lambda state: self.has_vertical(state, 2),
            LocationName.DaylightPuzzleLostRoadTwo:           lambda state: self.has_vertical(state, 2),
            LocationName.DualityPuzzleGummiHangar:            lambda state: self.has_vertical(state) and self.has_glide(state),
            LocationName.HeartPuzzleCourtyardOne:             lambda state: self.has_vertical(state) or self.has_magic_buffer(state),
            LocationName.DaylightPuzzleCollannade:            lambda state: self.has_vertical(state) or self.has_glide(state),
            LocationName.DualityPuzzlePierTree:               lambda state: self.has_vertical(state) or self.has_magic_buffer(state),
            LocationName.SunsetPuzzleHarbor:                  lambda state: self.has_vertical(state, 2) and self.has_glide(state, 2),
            LocationName.DaylightPuzzleBlackPearlFlags:       lambda state: self.has_vertical(state, 2) and self.has_glide(state, 2),
            LocationName.FrontierPuzzleAgrabah:               lambda state: self.stand_break(state),
            LocationName.FrontierPuzzleBazaar:                lambda state: self.stand_break(state),
            LocationName.SunsetPuzzleBazaar:                  lambda state: self.has_vertical(state, 2) and self.has_glide(state, 2),  # only need aerial dodge
            LocationName.SunsetPuzzleCurlyHill:               lambda state: self.has_vertical(state, 3) and self.has_glide(state, 3),
            LocationName.SunsetPuzzleToyFactory:              lambda state: self.has_vertical(state) and self.has_glide(state),
            LocationName.SunsetPuzzleCanyon:                  lambda state: self.has_vertical(state, 3) and self.has_glide(state, 3),
            LocationName.SunsetPuzzleTwilightView:            lambda state: self.has_vertical(state, 2) and self.has_glide(state, 2),
            LocationName.DaylightPuzzleNaughts:               lambda state: self.has_vertical(state, 2) and self.has_glide(state, 2),
            LocationName.SunsetPuzzleRuinPassageOne:          lambda state: self.has_vertical(state, 3) and self.has_glide(state, 3),
            LocationName.SunsetPuzzleRuinPassageTwo:          lambda state: self.has_vertical(state, 3) and self.has_glide(state, 3),
            LocationName.DaylightPuzzlePooh:                  lambda state: self.has_vertical(state),  # only needs aerial dodge,
        }

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

    def stand_break(self, state: CollectionState) -> bool:
        return state.has_any({ItemName.FireElement,
                              ItemName.BlizzardElement,
                              ItemName.ThunderElement,
                              ItemName.ValorForm,
                              ItemName.WisdomForm,
                              ItemName.LimitForm,
                              ItemName.MasterForm,
                              ItemName.FinalForm,
                              ItemName.FlareForce}, self.player)

    def set_kh2_puzzle_pieces_rules(self) -> None:
        for loc_name, rule in self.puzzle_pieces_location_rules.items():
            location = self.multiworld.get_location(loc_name, self.player)
            location.access_rule = rule


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
            RegionName.Terra:             lambda state: self.get_terra_rules(state) and state.has(ItemName.ProofofConnection, self.player),
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
        if self.fight_logic == "Easy":
            self.fight_region_rules[RegionName.ShanYu] = lambda state: self.get_easy_shanyu_rules(state),
            self.fight_region_rules[RegionName.AnsemRiku] = lambda state: self.get_easy_ansemriku_rules(state),
            self.fight_region_rules[RegionName.StormRider] = lambda state: self.get_easy_stormrider_rules(state),
            self.fight_region_rules[RegionName.DataXigbar] = lambda state: self.get_easy_dataxigbar_rules(state),
            self.fight_region_rules[RegionName.TwinLords] = lambda state: self.get_easy_twinlords_rules(state),
            self.fight_region_rules[RegionName.GenieJafar] = lambda state: self.get_easy_geniejafar_rules(state),
            self.fight_region_rules[RegionName.DataLexaeus] = lambda state: self.get_easy_datalexaeus_rules(state),
            self.fight_region_rules[RegionName.OldPete] = lambda state: self.get_easy_oldpete_rules(state),
            self.fight_region_rules[RegionName.FuturePete] = lambda state: self.get_easy_futurepete_rules(state),
            self.fight_region_rules[RegionName.Terra] = lambda state: self.get_easy_terra_rules(state),
            self.fight_region_rules[RegionName.DataMarluxia] = lambda state: self.get_easy_datamarluxia_rules(state),
            self.fight_region_rules[RegionName.Barbosa] = lambda state: self.get_easy_barbosa_rules(state),
            self.fight_region_rules[RegionName.GrimReaper1] = lambda state: self.get_easy_grimreaper1_rules(state),
            self.fight_region_rules[RegionName.GrimReaper2] = lambda state: self.get_easy_grimreaper2_rules(state),
            self.fight_region_rules[RegionName.DataLuxord] = lambda state: self.get_easy_dataluxord_rules(state),
            self.fight_region_rules[RegionName.Cerberus] = lambda state: self.get_easy_cerberus_rules(state),
            self.fight_region_rules[RegionName.OlympusPete] = lambda state: self.get_easy_olympuspete_rules(state),
            self.fight_region_rules[RegionName.Hydra] = lambda state: self.get_easy_hydra_rules(state),
            self.fight_region_rules[RegionName.Hades] = lambda state: self.get_easy_hades_rules(state),
            self.fight_region_rules[RegionName.DataZexion] = lambda state: self.get_easy_datazexion_rules(state),
            self.fight_region_rules[RegionName.OcPainAndPanicCup] = lambda state: self.get_easy_ocpainandpaniccup_rules(state),
            self.fight_region_rules[RegionName.OcCerberusCup] = lambda state: self.get_easy_occerberuscup_rules(state),
            self.fight_region_rules[RegionName.Oc2TitanCup] = lambda state: self.get_easy_oc2titancup_rules(state),
            self.fight_region_rules[RegionName.Oc2GofCup] = lambda state: self.get_easy_oc2gofcup_rules(state),
            self.fight_region_rules[RegionName.HadesCups] = lambda state: self.get_easy_hadescups_rules(state),
            self.fight_region_rules[RegionName.Thresholder] = lambda state: self.get_easy_thresholder_rules(state),
            self.fight_region_rules[RegionName.Beast] = lambda state: self.get_easy_beast_rules(state),
            self.fight_region_rules[RegionName.DarkThorn] = lambda state: self.get_easy_darkthorn_rules(state),
            self.fight_region_rules[RegionName.Xaldin] = lambda state: self.get_easy_xaldin_rules(state),
            self.fight_region_rules[RegionName.DataXaldin] = lambda state: self.get_easy_dataxaldin_rules(state),
            self.fight_region_rules[RegionName.HostileProgram] = lambda state: self.get_easy_hostileprogram_rules(state),
            self.fight_region_rules[RegionName.Mcp] = lambda state: self.get_easy_mcp_rules(state),
            self.fight_region_rules[RegionName.DataLarxene] = lambda state: self.get_easy_datalarxene_rules(state),
            self.fight_region_rules[RegionName.PrisonKeeper] = lambda state: self.get_easy_prisonkeeper_rules(state),
            self.fight_region_rules[RegionName.OogieBoogie] = lambda state: self.get_easy_oogieboogie_rules(state),
            self.fight_region_rules[RegionName.Experiment] = lambda state: self.get_easy_experiment_rules(state),
            self.fight_region_rules[RegionName.DataVexen] = lambda state: self.get_easy_datavexen_rules(state),
            self.fight_region_rules[RegionName.HBDemyx] = lambda state: self.get_easy_hbdemyx_rules(state),
            self.fight_region_rules[RegionName.ThousandHeartless] = lambda state: self.get_easy_thousandheartless_rules(state),
            self.fight_region_rules[RegionName.DataDemyx] = lambda state: self.get_easy_datademyx_rules(state),
            self.fight_region_rules[RegionName.Sephi] = lambda state: self.get_easy_sephi_rules(state),
            self.fight_region_rules[RegionName.CorFirstFight] = lambda state: self.get_easy_corfirstfight_rules(state),
            self.fight_region_rules[RegionName.CorSecondFight] = lambda state: self.get_easy_corsecondfight_rules(state),
            self.fight_region_rules[RegionName.Transport] = lambda state: self.get_easy_transport_rules(state),
            self.fight_region_rules[RegionName.Scar] = lambda state: self.get_easy_scar_rules(state),
            self.fight_region_rules[RegionName.GroundShaker] = lambda state: self.get_easy_groundshaker_rules(state),
            self.fight_region_rules[RegionName.DataSaix] = lambda state: self.get_easy_datasaix_rules(state),
            self.fight_region_rules[RegionName.TwilightThorn] = lambda state: self.get_easy_twilightthorn_rules(state),
            self.fight_region_rules[RegionName.Axel1] = lambda state: self.get_easy_axel1_rules(state),
            self.fight_region_rules[RegionName.Axel2] = lambda state: self.get_easy_axel2_rules(state),
            self.fight_region_rules[RegionName.DataRoxas] = lambda state: self.get_easy_dataroxas_rules(state),
            self.fight_region_rules[RegionName.DataAxel] = lambda state: self.get_easy_dataaxel_rules(state),
            self.fight_region_rules[RegionName.Roxas] = lambda state: self.get_easy_roxas_rules(state),
            self.fight_region_rules[RegionName.Xigbar] = lambda state: self.get_easy_xigbar_rules(state),
            self.fight_region_rules[RegionName.Luxord] = lambda state: self.get_easy_luxord_rules(state),
            self.fight_region_rules[RegionName.Saix] = lambda state: self.get_easy_saix_rules(state),
            self.fight_region_rules[RegionName.Xemnas] = lambda state: self.get_easy_xemnas_rules(state),
            self.fight_region_rules[RegionName.ArmoredXemnas] = lambda state: self.get_easy_armoredxemnas_rules(state),
            self.fight_region_rules[RegionName.ArmoredXemnas2] = lambda state: self.get_easy_armoredxemnas2_rules(state),
            self.fight_region_rules[RegionName.FinalXemnas] = lambda state: self.get_easy_finalxemnas_rules(state),
            self.fight_region_rules[RegionName.DataXemnas] = lambda state: self.get_easy_dataxemnas_rules(state),

        elif self.fight_logic == "Normal":
            self.fight_region_rules[RegionName.ShanYu] = lambda state: self.get_normal_shanyu_rules(state),
            self.fight_region_rules[RegionName.AnsemRiku] = lambda state: self.get_normal_ansemriku_rules(state),
            self.fight_region_rules[RegionName.StormRider] = lambda state: self.get_normal_stormrider_rules(state),
            self.fight_region_rules[RegionName.DataXigbar] = lambda state: self.get_normal_dataxigbar_rules(state),
            self.fight_region_rules[RegionName.TwinLords] = lambda state: self.get_normal_twinlords_rules(state),
            self.fight_region_rules[RegionName.GenieJafar] = lambda state: self.get_normal_geniejafar_rules(state),
            self.fight_region_rules[RegionName.DataLexaeus] = lambda state: self.get_normal_datalexaeus_rules(state),
            self.fight_region_rules[RegionName.OldPete] = lambda state: self.get_normal_oldpete_rules(state),
            self.fight_region_rules[RegionName.FuturePete] = lambda state: self.get_normal_futurepete_rules(state),
            self.fight_region_rules[RegionName.Terra] = lambda state: self.get_normal_terra_rules(state),
            self.fight_region_rules[RegionName.DataMarluxia] = lambda state: self.get_normal_datamarluxia_rules(state),
            self.fight_region_rules[RegionName.Barbosa] = lambda state: self.get_normal_barbosa_rules(state),
            self.fight_region_rules[RegionName.GrimReaper1] = lambda state: self.get_normal_grimreaper1_rules(state),
            self.fight_region_rules[RegionName.GrimReaper2] = lambda state: self.get_normal_grimreaper2_rules(state),
            self.fight_region_rules[RegionName.DataLuxord] = lambda state: self.get_normal_dataluxord_rules(state),
            self.fight_region_rules[RegionName.Cerberus] = lambda state: self.get_normal_cerberus_rules(state),
            self.fight_region_rules[RegionName.OlympusPete] = lambda state: self.get_normal_olympuspete_rules(state),
            self.fight_region_rules[RegionName.Hydra] = lambda state: self.get_normal_hydra_rules(state),
            self.fight_region_rules[RegionName.Hades] = lambda state: self.get_normal_hades_rules(state),
            self.fight_region_rules[RegionName.DataZexion] = lambda state: self.get_normal_datazexion_rules(state),
            self.fight_region_rules[RegionName.OcPainAndPanicCup] = lambda state: self.get_normal_ocpainandpaniccup_rules(state),
            self.fight_region_rules[RegionName.OcCerberusCup] = lambda state: self.get_normal_occerberuscup_rules(state),
            self.fight_region_rules[RegionName.Oc2TitanCup] = lambda state: self.get_normal_oc2titancup_rules(state),
            self.fight_region_rules[RegionName.Oc2GofCup] = lambda state: self.get_normal_oc2gofcup_rules(state),
            self.fight_region_rules[RegionName.HadesCups] = lambda state: self.get_normal_hadescups_rules(state),
            self.fight_region_rules[RegionName.Thresholder] = lambda state: self.get_normal_thresholder_rules(state),
            self.fight_region_rules[RegionName.Beast] = lambda state: self.get_normal_beast_rules(state),
            self.fight_region_rules[RegionName.DarkThorn] = lambda state: self.get_normal_darkthorn_rules(state),
            self.fight_region_rules[RegionName.Xaldin] = lambda state: self.get_normal_xaldin_rules(state),
            self.fight_region_rules[RegionName.DataXaldin] = lambda state: self.get_normal_dataxaldin_rules(state),
            self.fight_region_rules[RegionName.HostileProgram] = lambda state: self.get_normal_hostileprogram_rules(state),
            self.fight_region_rules[RegionName.Mcp] = lambda state: self.get_normal_mcp_rules(state),
            self.fight_region_rules[RegionName.DataLarxene] = lambda state: self.get_normal_datalarxene_rules(state),
            self.fight_region_rules[RegionName.PrisonKeeper] = lambda state: self.get_normal_prisonkeeper_rules(state),
            self.fight_region_rules[RegionName.OogieBoogie] = lambda state: self.get_normal_oogieboogie_rules(state),
            self.fight_region_rules[RegionName.Experiment] = lambda state: self.get_normal_experiment_rules(state),
            self.fight_region_rules[RegionName.DataVexen] = lambda state: self.get_normal_datavexen_rules(state),
            self.fight_region_rules[RegionName.HBDemyx] = lambda state: self.get_normal_hbdemyx_rules(state),
            self.fight_region_rules[RegionName.ThousandHeartless] = lambda state: self.get_normal_thousandheartless_rules(state),
            self.fight_region_rules[RegionName.DataDemyx] = lambda state: self.get_normal_datademyx_rules(state),
            self.fight_region_rules[RegionName.Sephi] = lambda state: self.get_normal_sephi_rules(state),
            self.fight_region_rules[RegionName.CorFirstFight] = lambda state: self.get_normal_corfirstfight_rules(state),
            self.fight_region_rules[RegionName.CorSecondFight] = lambda state: self.get_normal_corsecondfight_rules(state),
            self.fight_region_rules[RegionName.Transport] = lambda state: self.get_normal_transport_rules(state),
            self.fight_region_rules[RegionName.Scar] = lambda state: self.get_normal_scar_rules(state),
            self.fight_region_rules[RegionName.GroundShaker] = lambda state: self.get_normal_groundshaker_rules(state),
            self.fight_region_rules[RegionName.DataSaix] = lambda state: self.get_normal_datasaix_rules(state),
            self.fight_region_rules[RegionName.TwilightThorn] = lambda state: self.get_normal_twilightthorn_rules(state),
            self.fight_region_rules[RegionName.Axel1] = lambda state: self.get_normal_axel1_rules(state),
            self.fight_region_rules[RegionName.Axel2] = lambda state: self.get_normal_axel2_rules(state),
            self.fight_region_rules[RegionName.DataRoxas] = lambda state: self.get_normal_dataroxas_rules(state),
            self.fight_region_rules[RegionName.DataAxel] = lambda state: self.get_normal_dataaxel_rules(state),
            self.fight_region_rules[RegionName.Roxas] = lambda state: self.get_normal_roxas_rules(state),
            self.fight_region_rules[RegionName.Xigbar] = lambda state: self.get_normal_xigbar_rules(state),
            self.fight_region_rules[RegionName.Luxord] = lambda state: self.get_normal_luxord_rules(state),
            self.fight_region_rules[RegionName.Saix] = lambda state: self.get_normal_saix_rules(state),
            self.fight_region_rules[RegionName.Xemnas] = lambda state: self.get_normal_xemnas_rules(state),
            self.fight_region_rules[RegionName.ArmoredXemnas] = lambda state: self.get_normal_armoredxemnas_rules(state),
            self.fight_region_rules[RegionName.ArmoredXemnas2] = lambda state: self.get_normal_armoredxemnas2_rules(state),
            self.fight_region_rules[RegionName.FinalXemnas] = lambda state: self.get_normal_finalxemnas_rules(state),
            self.fight_region_rules[RegionName.DataXemnas] = lambda state: self.get_normal_dataxemnas_rules(state),
        else:
            self.fight_region_rules[RegionName.ShanYu] = lambda state: self.get_hard_shanyu_rules(state),
            self.fight_region_rules[RegionName.AnsemRiku] = lambda state: self.get_hard_ansemriku_rules(state),
            self.fight_region_rules[RegionName.StormRider] = lambda state: self.get_hard_stormrider_rules(state),
            self.fight_region_rules[RegionName.DataXigbar] = lambda state: self.get_hard_dataxigbar_rules(state),
            self.fight_region_rules[RegionName.TwinLords] = lambda state: self.get_hard_twinlords_rules(state),
            self.fight_region_rules[RegionName.GenieJafar] = lambda state: self.get_hard_geniejafar_rules(state),
            self.fight_region_rules[RegionName.DataLexaeus] = lambda state: self.get_hard_datalexaeus_rules(state),
            self.fight_region_rules[RegionName.OldPete] = lambda state: self.get_hard_oldpete_rules(state),
            self.fight_region_rules[RegionName.FuturePete] = lambda state: self.get_hard_futurepete_rules(state),
            self.fight_region_rules[RegionName.Terra] = lambda state: self.get_hard_terra_rules(state),
            self.fight_region_rules[RegionName.DataMarluxia] = lambda state: self.get_hard_datamarluxia_rules(state),
            self.fight_region_rules[RegionName.Barbosa] = lambda state: self.get_hard_barbosa_rules(state),
            self.fight_region_rules[RegionName.GrimReaper1] = lambda state: self.get_hard_grimreaper1_rules(state),
            self.fight_region_rules[RegionName.GrimReaper2] = lambda state: self.get_hard_grimreaper2_rules(state),
            self.fight_region_rules[RegionName.DataLuxord] = lambda state: self.get_hard_dataluxord_rules(state),
            self.fight_region_rules[RegionName.Cerberus] = lambda state: self.get_hard_cerberus_rules(state),
            self.fight_region_rules[RegionName.OlympusPete] = lambda state: self.get_hard_olympuspete_rules(state),
            self.fight_region_rules[RegionName.Hydra] = lambda state: self.get_hard_hydra_rules(state),
            self.fight_region_rules[RegionName.Hades] = lambda state: self.get_hard_hades_rules(state),
            self.fight_region_rules[RegionName.DataZexion] = lambda state: self.get_hard_datazexion_rules(state),
            self.fight_region_rules[RegionName.OcPainAndPanicCup] = lambda state: self.get_hard_ocpainandpaniccup_rules(state),
            self.fight_region_rules[RegionName.OcCerberusCup] = lambda state: self.get_hard_occerberuscup_rules(state),
            self.fight_region_rules[RegionName.Oc2TitanCup] = lambda state: self.get_hard_oc2titancup_rules(state),
            self.fight_region_rules[RegionName.Oc2GofCup] = lambda state: self.get_hard_oc2gofcup_rules(state),
            self.fight_region_rules[RegionName.HadesCups] = lambda state: self.get_hard_hadescups_rules(state),
            self.fight_region_rules[RegionName.Thresholder] = lambda state: self.get_hard_thresholder_rules(state),
            self.fight_region_rules[RegionName.Beast] = lambda state: self.get_hard_beast_rules(state),
            self.fight_region_rules[RegionName.DarkThorn] = lambda state: self.get_hard_darkthorn_rules(state),
            self.fight_region_rules[RegionName.Xaldin] = lambda state: self.get_hard_xaldin_rules(state),
            self.fight_region_rules[RegionName.DataXaldin] = lambda state: self.get_hard_dataxaldin_rules(state),
            self.fight_region_rules[RegionName.HostileProgram] = lambda state: self.get_hard_hostileprogram_rules(state),
            self.fight_region_rules[RegionName.Mcp] = lambda state: self.get_hard_mcp_rules(state),
            self.fight_region_rules[RegionName.DataLarxene] = lambda state: self.get_hard_datalarxene_rules(state),
            self.fight_region_rules[RegionName.PrisonKeeper] = lambda state: self.get_hard_prisonkeeper_rules(state),
            self.fight_region_rules[RegionName.OogieBoogie] = lambda state: self.get_hard_oogieboogie_rules(state),
            self.fight_region_rules[RegionName.Experiment] = lambda state: self.get_hard_experiment_rules(state),
            self.fight_region_rules[RegionName.DataVexen] = lambda state: self.get_hard_datavexen_rules(state),
            self.fight_region_rules[RegionName.HBDemyx] = lambda state: self.get_hard_hbdemyx_rules(state),
            self.fight_region_rules[RegionName.ThousandHeartless] = lambda state: self.get_hard_thousandheartless_rules(state),
            self.fight_region_rules[RegionName.DataDemyx] = lambda state: self.get_hard_datademyx_rules(state),
            self.fight_region_rules[RegionName.Sephi] = lambda state: self.get_hard_sephi_rules(state),
            self.fight_region_rules[RegionName.CorFirstFight] = lambda state: self.get_hard_corfirstfight_rules(state),
            self.fight_region_rules[RegionName.CorSecondFight] = lambda state: self.get_hard_corsecondfight_rules(state),
            self.fight_region_rules[RegionName.Transport] = lambda state: self.get_hard_transport_rules(state),
            self.fight_region_rules[RegionName.Scar] = lambda state: self.get_hard_scar_rules(state),
            self.fight_region_rules[RegionName.GroundShaker] = lambda state: self.get_hard_groundshaker_rules(state),
            self.fight_region_rules[RegionName.DataSaix] = lambda state: self.get_hard_datasaix_rules(state),
            self.fight_region_rules[RegionName.TwilightThorn] = lambda state: self.get_hard_twilightthorn_rules(state),
            self.fight_region_rules[RegionName.Axel1] = lambda state: self.get_hard_axel1_rules(state),
            self.fight_region_rules[RegionName.Axel2] = lambda state: self.get_hard_axel2_rules(state),
            self.fight_region_rules[RegionName.DataRoxas] = lambda state: self.get_hard_dataroxas_rules(state),
            self.fight_region_rules[RegionName.DataAxel] = lambda state: self.get_hard_dataaxel_rules(state),
            self.fight_region_rules[RegionName.Roxas] = lambda state: self.get_hard_roxas_rules(state),
            self.fight_region_rules[RegionName.Xigbar] = lambda state: self.get_hard_xigbar_rules(state),
            self.fight_region_rules[RegionName.Luxord] = lambda state: self.get_hard_luxord_rules(state),
            self.fight_region_rules[RegionName.Saix] = lambda state: self.get_hard_saix_rules(state),
            self.fight_region_rules[RegionName.Xemnas] = lambda state: self.get_hard_xemnas_rules(state),
            self.fight_region_rules[RegionName.ArmoredXemnas] = lambda state: self.get_hard_armoredxemnas_rules(state),
            self.fight_region_rules[RegionName.ArmoredXemnas2] = lambda state: self.get_hard_armoredxemnas2_rules(state),
            self.fight_region_rules[RegionName.FinalXemnas] = lambda state: self.get_hard_finalxemnas_rules(state),
            self.fight_region_rules[RegionName.DataXemnas] = lambda state: self.get_hard_dataxemnas_rules(state),

    def set_kh2_fight_rules(self) -> None:
        for region_name, rules in self.fight_region_rules.items():
            region = self.multiworld.get_region(region_name, self.player)
            for entrance in region.entrances:
                entrance.access_rule = rules

        for loc_name in [LocationName.TransportEventLocation, LocationName.TransporttoRemembrance]:
            location = self.multiworld.get_location(loc_name, self.player)
            add_rule(location, lambda state: self.get_transport_fight_rules(state))

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
        # easy:scom,gap closers,explosion,2 combo pluses,final 7,firaga, donald limits,reflect,guard,3 dodge roll,3 aerial dodge and 3glide
        return self.kh2_dict_count(easy_terra_tools, state) and self.kh2_has_final_form(state) and self.get_form_level_max(state, 5),

    def get_normal_terra_rules(self, state: CollectionState) -> bool:
        # normal:gap closers,explosion,2 combo pluses,2 dodge roll,2 aerial dodge and lvl 2glide,guard,donald limit, guard
        return self.kh2_dict_count(normal_terra_tools, state) and self.kh2_list_any_sum([donald_limit], state) >= 1

    def get_hard_terra_rules(self, state: CollectionState) -> bool:
        # hard:1 gap closer,explosion,2 combo pluses,2 dodge roll,2 aerial dodge and lvl 2glide,guard
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

    def get_cerberus_cup_rules(self, state: CollectionState) -> bool:
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

    def get_goddess_of_fate_cup_rules(self, state: CollectionState) -> bool:
        # can beat all the other cups+xemnas 1
        for loc_name in [LocationName.ProtectBeltPainandPanicCup, LocationName.RisingDragonCerberusCup, LocationName.GenjiShieldTitanCup, LocationName.Xemnas1GetBonus]:
            loc = self.world.get_location(loc_name)
            if not loc.can_reach(state):
                return False
        return True

    def get_hades_cup_rules(self, state: CollectionState) -> bool:
        # can beat goddess of fate cup
        return self.world.get_location(LocationName.FatalCrestGoddessofFateCup).can_reach(state)

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
            "easy":   self.kh2_dict_count(easy_data_larxene, state) and self.kh2_has_final_form(state) and self.get_form_level_max(state, 5),
            "normal": self.kh2_dict_count(normal_data_larxene, state) and self.kh2_list_any_sum([gap_closer, ground_finisher, donald_limit], state) >= 3 and self.kh2_has_final_form(state) and self.get_form_level_max(state, 5),
            "hard":   self.kh2_dict_count(hard_data_larxene, state) and self.kh2_list_any_sum([gap_closer, donald_limit], state) >= 2 and self.kh2_has_final_form(state) and self.get_form_level_max(state, 3),
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
            "easy":   self.kh2_dict_count(easy_data_vexen, state) and self.kh2_has_final_form(state) and self.get_form_level_max(state, 5),
            "normal": self.kh2_dict_count(normal_data_vexen, state) and self.kh2_list_any_sum([gap_closer, ground_finisher, donald_limit], state) >= 3 and self.kh2_has_final_form(state) and self.get_form_level_max(state, 5),
            "hard":   self.kh2_dict_count(hard_data_vexen, state) and self.kh2_list_any_sum([gap_closer, donald_limit], state) >= 2 and self.kh2_has_final_form(state) and self.get_form_level_max(state, 3),
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
            "easy":   self.kh2_dict_count(easy_data_demyx, state) and self.kh2_has_wisdom_form(state) and self.get_form_level_max(state, 5),
            "normal": self.kh2_dict_count(normal_data_demyx, state) and self.kh2_has_wisdom_form(state) and self.get_form_level_max(state, 5),
            "hard":   self.kh2_dict_count(hard_data_demyx, state) and self.kh2_has_wisdom_form(state) and self.get_form_level_max(state, 4),
        }
        return data_demyx_rules[self.fight_logic]

    def get_sephiroth_rules(self, state: CollectionState) -> bool:
        # easy:both gap closers,limit 5,reflega,guard,both 2 ground finishers,3 dodge roll,finishing plus,scom
        # normal:both gap closers,limit 5,reflera,guard,both 2 ground finishers,3 dodge roll,finishing plus
        # hard:1 gap closers,reflect, guard,both 1 ground finisher,2 dodge roll,finishing plus
        sephiroth_rules = {
            "easy":   self.kh2_dict_count(easy_sephiroth_tools, state) and self.kh2_has_limit_form(state) and self.get_form_level_max(state, 3) and self.kh2_list_any_sum([donald_limit], state) >= 1,
            "normal": self.kh2_dict_count(normal_sephiroth_tools, state) and self.kh2_has_limit_form(state) and self.get_form_level_max(state, 3) and self.kh2_list_any_sum([donald_limit, gap_closer], state) >= 2,
            "hard":   self.kh2_dict_count(hard_sephiroth_tools, state) and self.kh2_list_any_sum([gap_closer, ground_finisher], state) >= 2,
        }
        return sephiroth_rules[self.fight_logic]

    def get_cor_first_fight_movement_rules(self, state: CollectionState) -> bool:
        # easy: quick run 3 or wisdom 5 (wisdom has qr 3)
        # normal: quick run 2 and aerial dodge 1 or wisdom 5 (wisdom has qr 3)
        # hard: (quick run 1, aerial dodge 1) or (wisdom form and aerial dodge 1)
        cor_first_fight_movement_rules = {
            "easy":   state.has(ItemName.QuickRun, self.player, 3) or (self.kh2_has_wisdom_form(state) and self.get_form_level_max(state, 3)),
            "normal": self.kh2_dict_count({ItemName.QuickRun: 2, ItemName.AerialDodge: 1}, state) or (self.kh2_has_wisdom_form(state) and self.get_form_level_max(state, 5)),
            "hard":   self.kh2_has_all([ItemName.AerialDodge, ItemName.QuickRun], state) or self.kh2_has_all([ItemName.AerialDodge, ItemName.WisdomForm], state),
        }
        return cor_first_fight_movement_rules[self.fight_logic]

    def get_cor_first_fight_rules(self, state: CollectionState) -> bool:
        # easy:have 5 of these things (reflega,stitch and chicken,final form,magnera,explosion,thundara)
        # normal:have 3 of these things (reflega,stitch and chicken,final form,magnera,explosion,thundara)
        # hard: reflect,stitch or chicken,final form
        cor_first_fight_rules = {
            "easy":   self.kh2_dict_one_count(not_hard_cor_tools_dict, state) >= 5 or (self.kh2_dict_one_count(not_hard_cor_tools_dict, state) >= 4 and self.kh2_has_final_form(state)),
            "normal": self.kh2_dict_one_count(not_hard_cor_tools_dict, state) >= 3 or (self.kh2_dict_one_count(not_hard_cor_tools_dict, state) >= 2 and self.kh2_has_final_form(state)),
            "hard":   state.has(ItemName.ReflectElement, self.player) and self.kh2_has_any([ItemName.Stitch, ItemName.ChickenLittle], state) and self.kh2_has_final_form(state),
        }
        return cor_first_fight_rules[self.fight_logic]

    def get_cor_skip_first_rules(self, state: CollectionState) -> bool:
        # if option is not allow skips return false else run rules
        if not self.world.options.CorSkipToggle:
            return False
        # easy: aerial dodge 3,master form,fire
        # normal: aerial dodge 2, master form,fire
        # hard:void cross(quick run 3,aerial dodge 1)
        # or (quick run 2,aerial dodge 2 and magic)
        # or (final form and (magic or combo master))
        # or (master form and (reflect or fire or thunder or combo master)
        # wall rise(aerial dodge 1 and (final form lvl 5 or glide 2) or (master form and (1 of black magic or combo master)
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
            "hard":   state.has(ItemName.AerialDodge, self.player) and self.kh2_has_final_form(state) and self.get_form_level_max(state, 3) or state.has(ItemName.Glide, self.player, 2)
        }
        return void_cross_rules[self.fight_logic] and wall_rise_rules[self.fight_logic]

    def get_cor_second_fight_movement_rules(self, state: CollectionState) -> bool:
        # easy: quick run 2, aerial dodge 3 or master form 5
        # normal: quick run 2, aerial dodge 2 or master 5
        # hard: (glide 1,aerial dodge 1 any magic) or (master 3 any magic) or glide 1 and aerial dodge 2

        cor_second_fight_movement_rules = {
            "easy":   self.kh2_dict_count({ItemName.QuickRun: 2, ItemName.AerialDodge: 3}, state) or self.kh2_has_master_form(state) and self.get_form_level_max(state, 3),
            "normal": self.kh2_dict_count({ItemName.QuickRun: 2, ItemName.AerialDodge: 2}, state) or self.kh2_has_master_form(state) and self.get_form_level_max(state, 3),
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
            "easy":   self.kh2_dict_count(easy_data_saix, state) and self.kh2_has_final_form(state) and self.get_form_level_max(state, 5),
            "normal": self.kh2_dict_count(normal_data_saix, state) and self.kh2_list_any_sum([gap_closer, ground_finisher, donald_limit], state) >= 3 and self.kh2_has_final_form(state) and self.get_form_level_max(state, 5),
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
            "easy":   self.kh2_dict_count(easy_data_roxas_tools, state) and self.kh2_has_limit_form(state) and self.get_form_level_max(state, 3) and self.kh2_list_any_sum([donald_limit], state) >= 1,
            "normal": self.kh2_dict_count(normal_data_roxas_tools, state) and self.kh2_has_limit_form(state) and self.get_form_level_max(state, 3) and self.kh2_list_any_sum([donald_limit, gap_closer], state) >= 2,
            "hard":   self.kh2_dict_count(hard_data_roxas_tools, state) and self.kh2_list_any_sum([gap_closer, ground_finisher], state) >= 2
        }
        return data_roxas_rules[self.fight_logic]

    def get_data_axel_rules(self, state: CollectionState) -> bool:
        # easy:both gap closers,limit 5,reflega,guard,both 2 ground finishers,3 dodge roll,finishing plus,scom,blizzaga
        # normal:both gap closers,limit 5,reflera,guard,both 2 ground finishers,3 dodge roll,finishing plus,blizzaga
        # hard:1 gap closers,reflect, guard,both 1 ground finisher,2 dodge roll,finishing plus,blizzara
        data_axel_rules = {
            "easy":   self.kh2_dict_count(easy_data_axel_tools, state) and self.kh2_has_limit_form(state) and self.get_form_level_max(state, 3) and self.kh2_list_any_sum([donald_limit], state) >= 1,
            "normal": self.kh2_dict_count(normal_data_axel_tools, state) and self.kh2_has_limit_form(state) and self.get_form_level_max(state, 3) and self.kh2_list_any_sum([donald_limit, gap_closer], state) >= 2,
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
            "easy":   self.kh2_dict_count(easy_xigbar_tools, state) and self.kh2_has_final_form(state) and self.get_form_level_max(state, 2),
            "normal": self.kh2_dict_count(normal_xigbar_tools, state) and self.kh2_has_final_form(state) and self.get_form_level_max(state, 2),
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
            "easy":   self.kh2_dict_count(easy_data_xemnas, state) and self.kh2_list_count_sum(ground_finisher, state) >= 2 and self.kh2_has_limit_form(state) and self.get_form_level_max(state, 3),
            "normal": self.kh2_dict_count(normal_data_xemnas, state) and self.kh2_list_count_sum(ground_finisher, state) >= 2 and self.kh2_has_limit_form(state) and self.get_form_level_max(state, 3),
            "hard":   self.kh2_dict_count(hard_data_xemnas, state) and self.kh2_list_any_sum([ground_finisher, gap_closer], state) >= 2
        }
        return data_xemnas_rules[self.fight_logic]
