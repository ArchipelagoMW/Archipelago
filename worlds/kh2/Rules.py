from typing import Dict, Callable, TYPE_CHECKING

from BaseClasses import MultiWorld, CollectionState
from logic import *
from .Items import exclusionItem_table
from .Locations import STT_Checks, exclusion_table
from .Names import LocationName, ItemName, RegionName
from ..generic.Rules import add_rule, forbid_items, set_rule

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

        # These Rules are Always in effect
        self.region_rules = {
            RegionName.LoD:        lambda state: self.lod_unlocked(state, 1),
            RegionName.LoD2:       lambda state: self.lod_unlocked(state, 2),

            RegionName.Oc:         lambda state: self.oc_unlocked(state, 1),
            RegionName.Oc2:        lambda state: self.oc_unlocked(state, 2),

            RegionName.Twtnw2:     lambda state: self.twtnw_unlocked(state, 1),
            # These will be swapped and First Visit lock for twtnw is in development.
            # RegionName.Twtnw1: lambda state: self.lod_unlocked(state, 2),

            RegionName.Ht:         lambda state: self.ht_unlocked(state, 1),
            RegionName.Ht2:        lambda state: self.ht_unlocked(state, 2),

            RegionName.Tt:         lambda state: self.tt_unlocked(state, 1),
            RegionName.Tt2:        lambda state: self.tt_unlocked(state, 2),
            RegionName.Tt3:        lambda state: self.tt_unlocked(state, 3),

            RegionName.Pr:         lambda state: self.pr_unlocked(state, 1),
            RegionName.Pr2:        lambda state: self.pr_unlocked(state, 2),

            RegionName.Sp:         lambda state: self.sp_unlocked(state, 1),
            RegionName.Sp2:        lambda state: self.sp_unlocked(state, 2),

            RegionName.Stt:        lambda state: self.stt_unlocked(state, 1),

            RegionName.Dc:         lambda state: self.dc_unlocked(state, 1),
            RegionName.Tr:         lambda state: self.dc_unlocked(state, 2),
            #  Terra is a fight and can have more than just this requirement.
            # RegionName.Terra:      lambda state:state.has(ItemName.ProofofConnection,self.player),

            RegionName.Hb:         lambda state: self.hb_unlocked(state, 1),
            RegionName.Hb2:        lambda state: self.hb_unlocked(state, 2),
            RegionName.Mushroom13: lambda state: state.has(ItemName.ProofofPeace, self.player),

            RegionName.Pl:         lambda state: self.pl_unlocked(state, 1),
            RegionName.Pl2:        lambda state: self.pl_unlocked(state, 2),

            RegionName.Ag:         lambda state: self.ag_unlocked(state, 1),
            RegionName.Ag2:        lambda state: self.ag_unlocked(state, 2),

            RegionName.Bc:         lambda state: self.bc_unlocked(state, 1),
            RegionName.Bc2:        lambda state: self.bc_unlocked(state, 2),

            RegionName.Valor:      lambda state: self.multi_form_region_access(state),
            RegionName.Wisdom:     lambda state: self.multi_form_region_access(state),
            RegionName.Limit:      lambda state: self.limit_form_region_access(state),
            RegionName.Master:     lambda state: self.multi_form_region_access(state),
            RegionName.Final:      lambda state: self.final_form_region_access(state)
        }

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

    def final_form_region_access(self, state: CollectionState) -> bool:
        """
        Can reach one of TT3,Twtnw post Roxas, BC2, LoD2 or PR2
        """
        # tt3 start, can beat roxas, can beat gr2, can beat xaldin, can beat storm rider.
        final_leveling_access = [LocationName.MemorysSkyscaperMythrilCrystal, LocationName.GrimReaper2,
                                 LocationName.Xaldin, LocationName.StormRider, LocationName.SunsetTerraceAbilityRing]
        return any(self.world.multiworld.get_location(location, self.player).can_reach(state) for location in
                   final_leveling_access)

    def limit_form_region_access(self, state: CollectionState) -> bool:
        """
        multi_form_region_access + namine sketches for leveling
        """
        multi_form_region_access = {
            ItemName.CastleKey,
            ItemName.BattlefieldsofWar,
            ItemName.SwordoftheAncestor,
            ItemName.BeastsClaw,
            ItemName.BoneFist,
            ItemName.SkillandCrossbones,
            ItemName.Scimitar,
            ItemName.MembershipCard,
            ItemName.IceCream,
            ItemName.WaytotheDawn,
            ItemName.IdentityDisk,
            ItemName.NamineSketches
        }
        return state.has_any(multi_form_region_access, self.player)

    def multi_form_region_access(self, state: CollectionState) -> bool:
        """
        Valor, Wisdom and Master Form region access.
        Note: This does not account for having the drive form. See drive_form_unlock
        """
        # todo: if boss enemy start the player with oc stone because of cerb
        multi_form_region_access = {
            ItemName.CastleKey,
            ItemName.BattlefieldsofWar,
            ItemName.SwordoftheAncestor,
            ItemName.BeastsClaw,
            ItemName.BoneFist,
            ItemName.SkillandCrossbones,
            ItemName.Scimitar,
            ItemName.MembershipCard,
            ItemName.IceCream,
            ItemName.WaytotheDawn,
            ItemName.IdentityDisk,
        }
        return state.has_any(multi_form_region_access, self.player)

    def set_kh2_rules(self) -> None:
        world = self.world.multiworld
        player = self.player
        for region in world.get_regions(self.player):
            if region.name in self.region_rules:
                for entrance in region.entrances:
                    entrance.access_rule = self.region_rules[region.name]

        self.set_kh2_goal()

        for slot, weapon in exclusion_table["WeaponSlots"].items():
            add_rule(world.get_location(slot, player), lambda state: state.has(weapon, player))

        #  Forbid Abilities on popups due to game limitations
        for location in exclusion_table["Popups"]:
            forbid_items(world.get_location(location, player), exclusionItem_table["Ability"])
            forbid_items(world.get_location(location, player), exclusionItem_table["StatUps"])

        for location in STT_Checks:
            forbid_items(world.get_location(location, player), exclusionItem_table["StatUps"])

        # Santa's house also breaks with stat ups
        for location in {LocationName.SantasHouseChristmasTownMap, LocationName.SantasHouseAPBoost}:
            forbid_items(world.get_location(location, player), exclusionItem_table["StatUps"])

    def set_kh2_goal(self):
        if self.world.multiworld.Goal[self.player] == "three_proofs":
            add_rule(self.world.multiworld.get_location(LocationName.FinalXemnas, self.player),
                     lambda state: state.kh_three_proof_unlocked(self.player))
            if self.world.multiworld.FinalXemnas[self.player]:
                self.world.multiworld.completion_condition[self.player] = lambda state: state.kh_victory(self.player)
            else:
                self.world.multiworld.completion_condition[self.player] = lambda state: state.kh_three_proof_unlocked(
                        self.player)
        # lucky emblem hunt
        elif self.world.multiworld.Goal[self.player] == "lucky_emblem_hunt":
            add_rule(self.world.multiworld.get_location(LocationName.FinalXemnas, self.player),
                     lambda state: state.kh_lucky_emblem_unlocked(self.player,
                                                                  self.world.multiworld.LuckyEmblemsRequired[
                                                                      self.player].value))
            if self.world.multiworld.FinalXemnas[self.player]:
                self.world.multiworld.completion_condition[self.player] = lambda state: state.kh_victory(self.player)
            else:
                self.world.multiworld.completion_condition[self.player] = lambda state: state.kh_lucky_emblem_unlocked(
                        self.player,
                        self.world.multiworld.LuckyEmblemsRequired[
                            self.player].value)
        # hitlist if == 2
        else:
            add_rule(self.world.multiworld.get_location(LocationName.FinalXemnas, self.player),
                     lambda state: state.kh_hitlist(self.player,
                                                    self.world.multiworld.BountyRequired[self.player].value))
            if self.world.multiworld.FinalXemnas[self.player]:
                self.world.multiworld.completion_condition[self.player] = lambda state: state.kh_victory(self.player)
            else:
                self.world.multiworld.completion_condition[self.player] = lambda state: state.kh_hitlist(self.player,
                                                                                                         self.world.multiworld.BountyRequired[
                                                                                                             self.player].value)

    def kh2_set_count(self, item_name_set: set, state: CollectionState) -> int:
        """
        Returns the sum of all the items in the set.
        """
        return sum([state.count(item_name, self.player) for item_name in item_name_set if
                    state.count(item_name, self.player)])

    def kh2_dict_count(self, item_name_to_count: dict, state: CollectionState) -> bool:
        """
        simplifies count to a dictionary.
        """
        return all([state.count(item_name, self.player) >= item_name_to_count[item_name] for item_name in
                    item_name_to_count.keys() if state.count(item_name, self.player)])

    def kh2_can_reach_any(self, loc_set: set, state: CollectionState):
        """
        Can reach any locations in the set.
        """
        return any([self.kh2_can_reach(location, state) for location in
                    loc_set])

    def kh2_can_reach_all(self, loc_set: set, state: CollectionState):
        """
        Can reach all locations in the set.
        """
        return all([self.kh2_can_reach(location, state) for location in
                    loc_set])

    def kh2_can_reach(self, loc: str, state: CollectionState):
        """
        Returns bool instead of collection state.
        """
        if self.world.multiworld.get_location(loc, self.player).can_reach(state):
            return True
        else:
            return False

    def kh2_has_all(self, items: set, state: CollectionState):
        return state.has_all(items, self.player)

    def kh2_has_any(self, items: set, state: CollectionState):
        return state.has_any(items, self.player)


class KH2FormRules(KH2Rules):
    #: Dict[str, Callable[[CollectionState], bool]]
    def __init__(self, world: KH2World) -> None:
        super().__init__(world)
        # access rules on where you can level a form.
        self.auto_form_dict = {
            ItemName.FinalForm:  ItemName.AutoFinal,
            ItemName.MasterForm: ItemName.AutoMaster,
            ItemName.LimitForm:  ItemName.AutoLimit,
            ItemName.WisdomForm: ItemName.AutoWisdom,
            ItemName.ValorForm:  ItemName.AutoValor,
        }

        self.form_rules = {
            LocationName.Valorlvl2:  lambda state: self.drive_form_unlock(state, ItemName.ValorForm, 0),
            LocationName.Valorlvl3:  lambda state: self.drive_form_unlock(state, ItemName.ValorForm, 1),
            LocationName.Valorlvl4:  lambda state: self.drive_form_unlock(state, ItemName.ValorForm, 2),
            LocationName.Valorlvl5:  lambda state: self.drive_form_unlock(state, ItemName.ValorForm, 3),
            LocationName.Valorlvl6:  lambda state: self.drive_form_unlock(state, ItemName.ValorForm, 4),
            LocationName.Valorlvl7:  lambda state: self.drive_form_unlock(state, ItemName.ValorForm, 5),
            LocationName.Wisdomlvl2: lambda state: self.drive_form_unlock(state, ItemName.WisdomForm, 0),
            LocationName.Wisdomlvl3: lambda state: self.drive_form_unlock(state, ItemName.WisdomForm, 1),
            LocationName.Wisdomlvl4: lambda state: self.drive_form_unlock(state, ItemName.WisdomForm, 2),
            LocationName.Wisdomlvl5: lambda state: self.drive_form_unlock(state, ItemName.WisdomForm, 3),
            LocationName.Wisdomlvl6: lambda state: self.drive_form_unlock(state, ItemName.WisdomForm, 4),
            LocationName.Wisdomlvl7: lambda state: self.drive_form_unlock(state, ItemName.WisdomForm, 5),
            LocationName.Limitlvl2:  lambda state: self.drive_form_unlock(state, ItemName.LimitForm, 0),
            LocationName.Limitlvl3:  lambda state: self.drive_form_unlock(state, ItemName.LimitForm, 1),
            LocationName.Limitlvl4:  lambda state: self.drive_form_unlock(state, ItemName.LimitForm, 2),
            LocationName.Limitlvl5:  lambda state: self.drive_form_unlock(state, ItemName.LimitForm, 3),
            LocationName.Limitlvl6:  lambda state: self.drive_form_unlock(state, ItemName.LimitForm, 4),
            LocationName.Limitlvl7:  lambda state: self.drive_form_unlock(state, ItemName.LimitForm, 5),
            LocationName.Masterlvl2: lambda state: self.drive_form_unlock(state, ItemName.MasterForm, 0),
            LocationName.Masterlvl3: lambda state: self.drive_form_unlock(state, ItemName.MasterForm, 1),
            LocationName.Masterlvl4: lambda state: self.drive_form_unlock(state, ItemName.MasterForm, 2),
            LocationName.Masterlvl5: lambda state: self.drive_form_unlock(state, ItemName.MasterForm, 3),
            LocationName.Masterlvl6: lambda state: self.drive_form_unlock(state, ItemName.MasterForm, 4),
            LocationName.Masterlvl7: lambda state: self.drive_form_unlock(state, ItemName.MasterForm, 5),
            LocationName.Finallvl2:  lambda state: self.drive_form_unlock(state, ItemName.FinalForm, 0),
            LocationName.Finallvl3:  lambda state: self.drive_form_unlock(state, ItemName.FinalForm, 1),
            LocationName.Finallvl4:  lambda state: self.drive_form_unlock(state, ItemName.FinalForm, 2),
            LocationName.Finallvl5:  lambda state: self.drive_form_unlock(state, ItemName.FinalForm, 3),
            LocationName.Finallvl6:  lambda state: self.drive_form_unlock(state, ItemName.FinalForm, 4),
            LocationName.Finallvl7:  lambda state: self.drive_form_unlock(state, ItemName.FinalForm, 5),
        }

    def drive_form_unlock(self, state: CollectionState, drive_form, level_required) -> bool:
        form_access = {drive_form}
        if self.world.multiworld.AutoFormLogic[self.player] and state.has(ItemName.SecondChance, self.player):
            form_access.add(self.auto_form_dict[drive_form])
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

    def set_kh2_form_rules(self):
        # could use comprehension for getting a list of the region objects
        drive_form_set = {RegionName.Valor, RegionName.Wisdom, RegionName.Limit, RegionName.Master,
                          RegionName.Final}
        for region in self.world.multiworld.get_regions(self.player):
            if region.name in drive_form_set:
                for loc in region.locations:
                    if loc.name in self.form_rules:
                        loc.access_rule = self.form_rules[loc.name]


class KH2FightRules(KH2Rules):
    player: int
    world: KH2World
    region_rules: Dict[str, Callable[[CollectionState], bool]]
    location_rules: Dict[str, Callable[[CollectionState], bool]]

    def __init__(self, world: KH2World) -> None:
        super().__init__(world)
        self.fight_logic = self.world.multiworld.FightLogic[self.player].current_key
        self.player = world.player
        self.world = world
        self.final_leveling_access = {
            LocationName.MemorysSkyscaperMythrilCrystal,
            LocationName.GrimReaper2,
            LocationName.Xaldin,
            LocationName.StormRider,
            LocationName.SunsetTerraceAbilityRing
        }
        self.fight_region_rules = {
            RegionName.ShanYu:                lambda state: self.get_shan_yu_rules(state),
            RegionName.AnsemRiku:             lambda state: self.get_ansem_riku_rules(state),
            RegionName.StormRider:            lambda state: self.get_storm_rider_rules(state),
            RegionName.DataXigbar:            lambda state: self.get_data_xigbar_rules(state),
            RegionName.TwinLords:             lambda state: self.get_twin_lords_rules(state),
            RegionName.GenieJafar:            lambda state: self.get_genie_jafar_rules(state),
            RegionName.DataLexaeus:           lambda state: self.get_data_lexaeus_rules(state),
            RegionName.OldPete:               lambda state: self.get_old_pete_rules(),
            RegionName.FuturePete:            lambda state: self.get_future_pete_rules(state),
            RegionName.Terra:                 lambda state: self.get_terra_rules(state),
            RegionName.DataMarluxia:          lambda state: self.get_data_marluxia_rules(state),
            RegionName.Barbosa:               lambda state: self.get_barbosa_rules(state),
            RegionName.GrimReaper1:           lambda state: self.get_grim_reaper1_rules(state),
            RegionName.GrimReaper2:           lambda state: self.get_grim_reaper2_rules(state),
            RegionName.DataLuxord:            lambda state: self.get_data_luxord_rules(state),
            RegionName.Cerberus:              lambda state: self.get_cerberus_rules(state),
            RegionName.OlympusPete:           lambda state: self.get_olympus_pete_rules(state),
            RegionName.Hydra:                 lambda state: self.get_hydra_rules(state),
            RegionName.Hades:                 lambda state: self.get_hades_rules(state),
            RegionName.DataZexion:            lambda state: self.get_data_zexion_rules(state),
            RegionName.Oc_pain_and_panic_cup: lambda state: self.get_genie_jafar_rules(state),
            RegionName.Oc_cerberus_cup:       lambda state: self.get_genie_jafar_rules(state),
            RegionName.Oc2_titan_cup:         lambda state: self.get_genie_jafar_rules(state),
            RegionName.Oc2_gof_cup:           lambda state: self.get_genie_jafar_rules(state),
            RegionName.HadesCups:             lambda state: self.get_genie_jafar_rules(state),
            RegionName.Thresholder:           lambda state: self.get_genie_jafar_rules(state),
            RegionName.Beast:                 lambda state: self.get_genie_jafar_rules(state),
            RegionName.DarkThorn:             lambda state: self.get_genie_jafar_rules(state),
            RegionName.Xaldin:                lambda state: self.get_genie_jafar_rules(state),
            RegionName.DataXaldin:            lambda state: self.get_genie_jafar_rules(state),
            RegionName.HostileProgram:        lambda state: self.get_genie_jafar_rules(state),
            RegionName.Mcp:                   lambda state: self.get_genie_jafar_rules(state),
            RegionName.DataLarxene:           lambda state: self.get_genie_jafar_rules(state),
            RegionName.PrisonKeeper:          lambda state: self.get_genie_jafar_rules(state),
            RegionName.OogieBoogie:           lambda state: self.get_genie_jafar_rules(state),
            RegionName.Experiment:            lambda state: self.get_genie_jafar_rules(state),
            RegionName.DataVexen:             lambda state: self.get_genie_jafar_rules(state),
            RegionName.HBDemyx:               lambda state: self.get_genie_jafar_rules(state),
            RegionName.ThousandHeartless:     lambda state: self.get_genie_jafar_rules(state),
            RegionName.DataDemyx:             lambda state: self.get_genie_jafar_rules(state),
            RegionName.Sephi:                 lambda state: self.get_genie_jafar_rules(state),
            RegionName.CorFirstFight:         lambda state: self.get_genie_jafar_rules(state),
            RegionName.CorSecondFight:        lambda state: self.get_genie_jafar_rules(state),
            RegionName.Transport:             lambda state: self.get_genie_jafar_rules(state),
            RegionName.Scar:                  lambda state: self.get_genie_jafar_rules(state),
            RegionName.GroundShaker:          lambda state: self.get_genie_jafar_rules(state),
            RegionName.DataSaix:              lambda state: self.get_genie_jafar_rules(state),
            RegionName.TwilightThorn:         lambda state: self.get_genie_jafar_rules(state),
            RegionName.Axel1:                 lambda state: self.get_genie_jafar_rules(state),
            RegionName.Axel2:                 lambda state: self.get_genie_jafar_rules(state),
            RegionName.DataRoxas:             lambda state: self.get_genie_jafar_rules(state),
            RegionName.DataAxel:              lambda state: self.get_genie_jafar_rules(state),
            RegionName.Roxas:                 lambda state: self.get_genie_jafar_rules(state),
            RegionName.Xigbar:                lambda state: self.get_genie_jafar_rules(state),
            RegionName.Luxord:                lambda state: self.get_genie_jafar_rules(state),
            RegionName.Saix:                  lambda state: self.get_genie_jafar_rules(state),
            RegionName.Xemnas:                lambda state: self.get_genie_jafar_rules(state),
            RegionName.ArmoredXemnas:         lambda state: self.get_genie_jafar_rules(state),
            RegionName.ArmoredXemnas2:        lambda state: self.get_genie_jafar_rules(state),
            RegionName.FinalXemnas:           lambda state: self.get_genie_jafar_rules(state),
            RegionName.DataXemnas:            lambda state: self.get_genie_jafar_rules(state),
        }

    def set_kh2_fight_rules(self) -> None:
        world = self.world.multiworld
        player = self.player
        for region in world.get_regions(player):
            if region.name == RegionName.AnsemRiku:
                for entrance in region.entrances:
                    entrance.access_rule = self.fight_region_rules[region.name]

    def get__rules(self, state: CollectionState) -> bool:
        _rules = {
            "easy":   self,
            "normal": self,
            "hard":   self,
        }
        return _rules[self.fight_logic]

    def get_shan_yu_rules(self, state: CollectionState) -> bool:
        shan_yu_rules = {
            "easy":   state.has_all(easy_shan_yu_tools, self.player),
            "normal": self,
            "hard":   self,
        }
        return shan_yu_rules[self.fight_logic]

    def get_ansem_riku_rules(self, state: CollectionState) -> bool:
        ansem_riku_rules = {
            "easy":   self.kh2_has_all(easy_ansem_riku_tools, state),
            "normal": state.has_all(self.ansem_riku_tools, self.player),
            "hard":   state.has_all(self.ansem_riku_tools, self.player),
        }
        return ansem_riku_rules[self.fight_logic]

    def get_storm_rider_rules(self, state: CollectionState) -> bool:
        storm_rider_rules = {
            "easy":   self.kh2_has_all(easy_storm_rider_tools, state),
            "normal": self,
            "hard":   self,
        }
        return storm_rider_rules[self.fight_logic]

    def get_data_xigbar_rules(self, state: CollectionState) -> bool:
        data_xigbar_rules = {
            "easy":   self.kh2_dict_count(easy_data_xigbar_tools, state),
            "normal": self,
            "hard":   self,
        }

        return data_xigbar_rules[self.fight_logic] and self.kh2_can_reach_any(self.final_leveling_access, state)

    def get_twin_lords_rules(self, state: CollectionState) -> bool:
        twin_lords_rules = {
            "easy":   self.kh2_has_all(easy_twin_lords_tools, state),
            "normal": self,
            "hard":   self,
        }
        return twin_lords_rules[self.fight_logic]

    def get_genie_jafar_rules(self, state: CollectionState) -> bool:
        genie_jafar_rules = {
            "easy":   self.kh2_has_all(easy_genie_jafar_tools, state),
            "normal": self,
            "hard":   self,
        }
        return genie_jafar_rules[self.fight_logic]

    def get_data_lexaeus_rules(self, state: CollectionState) -> bool:
        data_lexaues_rules = {
            "easy":   self.kh2_dict_count(easy_data_lexaeus_rules, state),
            "normal": self,
            "hard":   self,
        }
        return data_lexaues_rules[self.fight_logic]

    @staticmethod
    def get_old_pete_rules():
        return True

    def get_future_pete_rules(self, state: CollectionState) -> bool:
        future_pete_rules = {
            "easy":   self.kh2_has_all(easy_future_pete_tools, state),
            "normal": self,
            "hard":   self,
        }
        return future_pete_rules[self.fight_logic]

    def get_data_marluxia_rules(self, state: CollectionState) -> bool:
        data_marluxia_rules = {
            "easy":   self.kh2_dict_count(easy_data_marluxia_tools, state),
            "normal": self,
            "hard":   self,
        }
        return data_marluxia_rules[self.fight_logic]

    def get_terra_rules(self, state: CollectionState) -> bool:
        terra_rules = {
            "easy":   self.kh2_dict_count(easy_terra_tools, state),
            "normal": self,
            "hard":   self,
        }
        return terra_rules[self.fight_logic]

    def get_barbosa_rules(self, state: CollectionState) -> bool:
        barbosa_rules = {
            "easy":   self.kh2_has_all(easy_barbosa_tools, state),
            "normal": self,
            "hard":   self,
        }
        return barbosa_rules[self.fight_logic]

    def get_grim_reaper1_rules(self, state: CollectionState) -> bool:
        gr1_rules = {
            "easy":   self.kh2_has_all(easy_gr1_tools, state),
            "normal": self,
            "hard":   self,
        }
        return gr1_rules[self.fight_logic]

    def get_grim_reaper2_rules(self, state: CollectionState) -> bool:
        gr2_rules = {
            "easy":   self.kh2_has_all(easy_gr2_tools, state),
            "normal": self,
            "hard":   self,
        }
        return gr2_rules[self.fight_logic]

    def get_data_luxord_rules(self, state: CollectionState) -> bool:
        data_luxord_rules = {
            "easy":   self.kh2_dict_count(easy_data_luxord_tools, state),
            "normal": self,
            "hard":   self,
        }
        return data_luxord_rules[self.fight_logic]

    def get_cerberus_rules(self, state: CollectionState) -> bool:
        cerberus_rules = {
            "easy":   self.kh2_has_all(easy_cerberus_tools, state),
            "normal": self,
            "hard":   self,
        }
        return cerberus_rules[self.fight_logic]

    def get_olympus_pete_rules(self, state: CollectionState) -> bool:
        olympus_pete_rules = {
            "easy":   self.kh2_has_all(easy_olympus_pete_tools, state),
            "normal": self,
            "hard":   self,
        }
        return olympus_pete_rules[self.fight_logic]

    def get_hydra_rules(self, state: CollectionState) -> bool:
        hydra_rules = {
            "easy":   self.kh2_has_all(easy_hydra_tools, state),
            "normal": self,
            "hard":   self,
        }
        return hydra_rules[self.fight_logic]

    def get_hades_rules(self, state: CollectionState) -> bool:
        hades_rules = {
            "easy":   self.kh2_dict_count(easy_hades_tools, state),
            "normal": self,
            "hard":   self,
        }
        return hades_rules[self.fight_logic]

    def get_data_zexion_rules(self, state: CollectionState) -> bool:
        data_zexion_rules = {
            "easy":   self.kh2_dict_count(easy_data_zexion, state) and self.kh2_can_reach(LocationName.Finallvl7,
                                                                                          state),
            "normal": self,
            "hard":   self,
        }
        return data_zexion_rules[self.fight_logic]

    def get_thresholder_rules(self, state: CollectionState) -> bool:
        thresholder_rules = {
            "easy":   self.kh2_has_all(easy_thresholder, state),
            "normal": self,
            "hard":   self,
        }
        return thresholder_rules[self.fight_logic]

    @staticmethod
    def get_beast_rules():
        return True

    def get_dark_thorn_rules(self, state: CollectionState) -> bool:
        dark_thorn_rules = {
            "easy":   self.kh2_has_all(easy_dark_thorn, state),
            "normal": self,
            "hard":   self,
        }
        return dark_thorn_rules[self.fight_logic]

    def get__rules(self, state: CollectionState) -> bool:
        _rules = {
            "easy":   self,
            "normal": self,
            "hard":   self,
        }
        return _rules[self.fight_logic]

    def get__rules(self, state: CollectionState) -> bool:
        _rules = {
            "easy":   self,
            "normal": self,
            "hard":   self,
        }
        return _rules[self.fight_logic]

    def get__rules(self, state: CollectionState) -> bool:
        _rules = {
            "easy":   self,
            "normal": self,
            "hard":   self,
        }
        return _rules[self.fight_logic]

    def get__rules(self, state: CollectionState) -> bool:
        _rules = {
            "easy":   self,
            "normal": self,
            "hard":   self,
        }
        return _rules[self.fight_logic]

    def get__rules(self, state: CollectionState) -> bool:
        _rules = {
            "easy":   self,
            "normal": self,
            "hard":   self,
        }
        return _rules[self.fight_logic]

    def get__rules(self, state: CollectionState) -> bool:
        _rules = {
            "easy":   self,
            "normal": self,
            "hard":   self,
        }
        return _rules[self.fight_logic]

    def get__rules(self, state: CollectionState) -> bool:
        _rules = {
            "easy":   self,
            "normal": self,
            "hard":   self,
        }
        return _rules[self.fight_logic]

    def get__rules(self, state: CollectionState) -> bool:
        _rules = {
            "easy":   self,
            "normal": self,
            "hard":   self,
        }
        return _rules[self.fight_logic]

    def get__rules(self, state: CollectionState) -> bool:
        _rules = {
            "easy":   self,
            "normal": self,
            "hard":   self,
        }
        return _rules[self.fight_logic]

    def get__rules(self, state: CollectionState) -> bool:
        _rules = {
            "easy":   self,
            "normal": self,
            "hard":   self,
        }
        return _rules[self.fight_logic]

    def get__rules(self, state: CollectionState) -> bool:
        _rules = {
            "easy":   self,
            "normal": self,
            "hard":   self,
        }
        return _rules[self.fight_logic]

    def get__rules(self, state: CollectionState) -> bool:
        _rules = {
            "easy":   self,
            "normal": self,
            "hard":   self,
        }
        return _rules[self.fight_logic]

    def get__rules(self, state: CollectionState) -> bool:
        _rules = {
            "easy":   self,
            "normal": self,
            "hard":   self,
        }
        return _rules[self.fight_logic]

    def get__rules(self, state: CollectionState) -> bool:
        _rules = {
            "easy":   self,
            "normal": self,
            "hard":   self,
        }
        return _rules[self.fight_logic]
