from typing import Dict, Callable, TYPE_CHECKING

from BaseClasses import MultiWorld, CollectionState

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
            # RegionName.Final:      lambda state: self.drive_form_unlock(state, "Final Form", 1),
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

    def set_kh2_rules(self) -> None:
        multiworld = self.world.multiworld

        for region in multiworld.get_regions(self.player):
            if region.name in self.region_rules:
                for entrance in region.entrances:
                    entrance.access_rule = self.region_rules[region.name]
            # for loc in region.locations:
            #    if loc.name in self.location_rules:
            #        loc.access_rule = self.location_rules[loc.name]

        multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)


class KH2FormRules(KH2Rules):
    #: Dict[str, Callable[[CollectionState], bool]]

    def __init__(self, world: KH2World) -> None:
        super().__init__(world)

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

    def drive_form_unlock(self, state: CollectionState, driveForm, levelRequired) -> bool:
        formLogic = {driveForm}
        if self.world.multiworld.AutoFormLogic[self.player] and state.has(ItemName.SecondChance, self.player):
            autoFormDict = {
                ItemName.FinalForm:  ItemName.AutoFinal,
                ItemName.MasterForm: ItemName.AutoMaster,
                ItemName.LimitForm:  ItemName.AutoLimit,
                ItemName.WisdomForm: ItemName.AutoWisdom,
                ItemName.ValorForm:  ItemName.AutoValor,
            }
            formLogic.add(autoFormDict[driveForm])
        return state.has_any(formLogic, self.player) and self.getLevelRequirement(state, levelRequired)

    def getLevelRequirement(self, state, amount):
        formsAvailable = 0
        formList = [ItemName.ValorForm, ItemName.WisdomForm, ItemName.LimitForm, ItemName.MasterForm,
                    ItemName.FinalForm]
        if self.world.multiworld.FinalFormLogic[self.player] != "no_light_and_darkness":
            if self.world.multiworld.FinalFormLogic[self.player] == "light_and_darkness":
                if state.has(ItemName.LightDarkness, self.player) and state.has_any(set(formList), self.player):
                    formsAvailable += 1
                    formList.remove(ItemName.FinalForm)
            else:  # self.multiworld.FirmFormLogic=="just a form"
                formList.remove(ItemName.FinalForm)
                if state.has_any(formList, self.player):
                    formsAvailable += 1
        formsAvailable += sum([1 for form in formList if state.has(form, self.player)])
        return formsAvailable >= amount

    def set_kh2_form_rules(self):
        for region in self.world.multiworld.get_regions(self.player):
            if region.name in {RegionName.Valor, RegionName.Wisdom, RegionName.Limit, RegionName.Master,
                               RegionName.Final}:
                for loc in region.locations:
                    if loc.name in self.form_rules:
                        loc.access_rule = self.form_rules[loc.name]


def set_rules(world: MultiWorld, player: int):
    add_rule(world.get_location(LocationName.RoxasDataMagicBoost, player),
             lambda state: state.kh_dataroxas(player))
    add_rule(world.get_location(LocationName.DemyxDataAPBoost, player),
             lambda state: state.kh_datademyx(player))
    add_rule(world.get_location(LocationName.SaixDataDefenseBoost, player),
             lambda state: state.kh_datasaix(player))
    add_rule(world.get_location(LocationName.XaldinDataDefenseBoost, player),
             lambda state: state.kh_dataxaldin(player))
    add_rule(world.get_location(LocationName.XemnasDataPowerBoost, player),
             lambda state: state.kh_dataxemnas(player))
    add_rule(world.get_location(LocationName.XigbarDataDefenseBoost, player),
             lambda state: state.kh_dataxigbar(player))
    add_rule(world.get_location(LocationName.VexenDataLostIllusion, player),
             lambda state: state.kh_dataaxel(player))
    add_rule(world.get_location(LocationName.LuxordDataAPBoost, player),
             lambda state: state.kh_dataluxord(player))

    for slot, weapon in exclusion_table["WeaponSlots"].items():
        add_rule(world.get_location(slot, player), lambda state: state.has(weapon, player))

    formLogicTable = {
        ItemName.ValorForm:  [LocationName.Valorlvl4,
                              LocationName.Valorlvl5,
                              LocationName.Valorlvl6,
                              LocationName.Valorlvl7],
        ItemName.WisdomForm: [LocationName.Wisdomlvl4,
                              LocationName.Wisdomlvl5,
                              LocationName.Wisdomlvl6,
                              LocationName.Wisdomlvl7],
        ItemName.LimitForm:  [LocationName.Limitlvl4,
                              LocationName.Limitlvl5,
                              LocationName.Limitlvl6,
                              LocationName.Limitlvl7],
        ItemName.MasterForm: [LocationName.Masterlvl4,
                              LocationName.Masterlvl5,
                              LocationName.Masterlvl6,
                              LocationName.Masterlvl7],
        ItemName.FinalForm:  [LocationName.Finallvl4,
                              LocationName.Finallvl5,
                              LocationName.Finallvl6,
                              LocationName.Finallvl7]
    }

    for form in formLogicTable:
        for i in range(4):
            location = world.get_location(formLogicTable[form][i], player)
            set_rule(location, lambda state, i=i + 1, form=form: state.kh_amount_of_forms(player, i, form))

    if world.Goal[player] == "three_proofs":
        add_rule(world.get_location(LocationName.FinalXemnas, player),
                 lambda state: state.kh_three_proof_unlocked(player))
        if world.FinalXemnas[player]:
            world.completion_condition[player] = lambda state: state.kh_victory(player)
        else:
            world.completion_condition[player] = lambda state: state.kh_three_proof_unlocked(player)
    # lucky emblem hunt
    elif world.Goal[player] == "lucky_emblem_hunt":
        add_rule(world.get_location(LocationName.FinalXemnas, player),
                 lambda state: state.kh_lucky_emblem_unlocked(player, world.LuckyEmblemsRequired[player].value))
        if world.FinalXemnas[player]:
            world.completion_condition[player] = lambda state: state.kh_victory(player)
        else:
            world.completion_condition[player] = lambda state: state.kh_lucky_emblem_unlocked(player,
                                                                                              world.LuckyEmblemsRequired[
                                                                                                  player].value)
    # hitlist if == 2
    else:
        add_rule(world.get_location(LocationName.FinalXemnas, player),
                 lambda state: state.kh_hitlist(player, world.BountyRequired[player].value))
        if world.FinalXemnas[player]:
            world.completion_condition[player] = lambda state: state.kh_victory(player)
        else:
            world.completion_condition[player] = lambda state: state.kh_hitlist(player,
                                                                                world.BountyRequired[player].value)

    #  Forbid Abilities on popups due to game limitations
    for location in exclusion_table["Popups"]:
        forbid_items(world.get_location(location, player), exclusionItem_table["Ability"])
        forbid_items(world.get_location(location, player), exclusionItem_table["StatUps"])

    for location in STT_Checks:
        forbid_items(world.get_location(location, player), exclusionItem_table["StatUps"])

    # Santa's house also breaks with stat ups
    for location in {LocationName.SantasHouseChristmasTownMap, LocationName.SantasHouseAPBoost}:
        forbid_items(world.get_location(location, player), exclusionItem_table["StatUps"])

    add_rule(world.get_location(LocationName.TransporttoRemembrance, player),
             lambda state: state.kh_transport(player))

# class KH2EasyRules:
#    player: int
#    world: KH2World
#    region_rules: Dict[str, Callable[[CollectionState], bool]]
#    location_rules: Dict[str, Callable[[CollectionState], bool]]
