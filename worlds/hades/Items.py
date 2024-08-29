from typing import Dict, NamedTuple, Optional

from BaseClasses import Item, ItemClassification


class ItemData(NamedTuple):
    code: Optional[int]
    progression: bool
    event: bool = False
    trap: bool = False


hades_base_item_id = 666100

item_table_pacts: Dict[str, ItemData] = {  
    "HardLaborPactLevel": ItemData(hades_base_item_id, True),
    "LastingConsequencesPactLevel": ItemData(hades_base_item_id+1, True),
    "ConvenienceFeePactLevel": ItemData(hades_base_item_id+2, True),
    "JurySummonsPactLevel": ItemData(hades_base_item_id+3, True),
    "ExtremeMeasuresPactLevel": ItemData(hades_base_item_id+4, True),
    "CalisthenicsProgramPactLevel": ItemData(hades_base_item_id+5, True),
    "BenefitsPackagePactLevel": ItemData(hades_base_item_id+6, True),
    "MiddleManagementPactLevel": ItemData(hades_base_item_id+7, True),
    "UnderworldCustomsPactLevel": ItemData(hades_base_item_id+8, True),
    "ForcedOvertimePactLevel": ItemData(hades_base_item_id+9, True),
    "HeightenedSecurityPactLevel": ItemData(hades_base_item_id+10, True),
    "RoutineInspectionPactLevel": ItemData(hades_base_item_id+11, True),
    "DamageControlPactLevel": ItemData(hades_base_item_id+12, True),
    "ApprovalProcessPactLevel": ItemData(hades_base_item_id+13, True),
    "TightDeadlinePactLevel": ItemData(hades_base_item_id+14, True),
    "PersonalLiabilityPactLevel": ItemData(hades_base_item_id+15, True),  
}

items_table_event: Dict[str, ItemData] = {
    "MegVictory": ItemData(None, True, True),
    "LernieVictory": ItemData(None, True, True),
    "BrosVictory": ItemData(None, True, True),
    "HadesVictory": ItemData(None, True, True),
    "HadesVictorySwordWeapon": ItemData(None, True, True),
    "MegVictorySwordWeapon": ItemData(None, True, True),
    "LernieVictorySwordWeapon" : ItemData(None, True, True),
    "BrosVictorySwordWeapon": ItemData(None, True, True),
    "HadesVictoryBowWeapon": ItemData(None, True, True),
    "MegVictoryBowWeapon": ItemData(None, True, True),
    "LernieVictoryBowWeapon": ItemData(None, True, True),
    "BrosVictoryBowWeapon" : ItemData(None, True, True),
    "HadesVictorySpearWeapon" : ItemData(None, True, True),
    "MegVictorySpearWeapon": ItemData(None, True, True),
    "LernieVictorySpearWeapon": ItemData(None, True, True),
    "BrosVictorySpearWeapon": ItemData(None, True, True),
    "HadesVictoryShieldWeapon": ItemData(None, True, True),
    "MegVictoryShieldWeapon": ItemData(None, True, True),
    "LernieVictoryShieldWeapon": ItemData(None, True, True),
    "BrosVictoryShieldWeapon": ItemData(None, True, True),
    "HadesVictoryFistWeapon": ItemData(None, True, True),
    "MegVictoryFistWeapon": ItemData(None, True, True),
    "LernieVictoryFistWeapon": ItemData(None, True, True),
    "BrosVictoryFistWeapon": ItemData(None, True, True),
    "HadesVictoryGunWeapon": ItemData(None, True, True),
    "MegVictoryGunWeapon": ItemData(None, True, True),
    "LernieVictoryGunWeapon": ItemData(None, True, True),
    "BrosVictoryGunWeapon": ItemData(None, True, True),
}

items_table_fates_completion: Dict[str,ItemData] = {
    "IsThereNoEscape?EventItem": ItemData(None, True, True),
    "DistantRelativesEventItem": ItemData(None, True, True),
    "ChthonicColleaguesEventItem": ItemData(None, True, True),
    "TheReluctantMusicianEventItem": ItemData(None, True, True),
    "GoddessOfWisdomEventItem": ItemData(None, True, True),
    "GodOfTheHeavensEventItem": ItemData(None, True, True),
    "GodOfTheSeaEventItem": ItemData(None, True, True),
    "GoddessOfLoveEventItem": ItemData(None, True, True),
    "GodOfWarEventItem": ItemData(None, True, True),
    "GoddessOfTheHuntEventItem": ItemData(None, True, True),
    "GodOfWineEventItem": ItemData(None, True, True),
    "GodOfSwiftnessEventItem": ItemData(None, True, True),
    "GoddessOfSeasonsEventItem": ItemData(None, True, True),
    "PowerWithoutEqualEventItem": ItemData(None, True, True),
    "DivinePairingsEventItem": ItemData(None, True, True),
    "PrimordialBoonsEventItem": ItemData(None, True, True),
    "PrimordialBanesEventItem": ItemData(None, True, True),
    "InfernalArmsEventItem": ItemData(None, True, True),
    "TheStygianBladeEventItem": ItemData(None, True, True),
    "TheHeartSeekingBowEventItem": ItemData(None, True, True),
    "TheShieldOfChaosEventItem": ItemData(None, True, True),
    "TheEternalSpearEventItem": ItemData(None, True, True),
    "TheTwinFistsEventItem": ItemData(None, True, True),
    "TheAdamantRailEventItem": ItemData(None, True, True),
    "MasterOfArmsEventItem": ItemData(None, True, True),
    "AViolentPastEventItem": ItemData(None, True, True),
    "HarshConditionsEventItem": ItemData(None, True, True),
    "SlashedBenefitsEventItem": ItemData(None, True, True),
    "WantonRansackingEventItem": ItemData(None, True, True),
    "ASimpleJobEventItem": ItemData(None, True, True),
    "ChthonicKnowledgeEventItem": ItemData(None, True, True),
    "CustomerLoyaltyEventItem": ItemData(None, True, True),
    "DarkReflectionsEventItem": ItemData(None, True, True),
    "CloseAtHeartEventItem": ItemData(None, True, True),
    "DenizensOfTheDeepEventItem": ItemData(None, True, True),
    "TheUselessTrinketEventItem": ItemData(None, True, True),
}

item_table_filler: Dict[str, ItemData] = {
    "Darkness": ItemData(hades_base_item_id+16, False),
    "Keys": ItemData(hades_base_item_id+17, False),
    "Gemstones": ItemData(hades_base_item_id+18, False),
    "Diamonds": ItemData(hades_base_item_id+19, False),
    "TitanBlood": ItemData(hades_base_item_id+20, False),
    "Nectar": ItemData(hades_base_item_id+21, False),
    "Ambrosia": ItemData(hades_base_item_id+22, False)
}

item_table_keepsake: Dict[str, ItemData] ={
    "CerberusKeepsake": ItemData(hades_base_item_id+23, True),
    "AchillesKeepsake": ItemData(hades_base_item_id+24, True),
    "NyxKeepsake": ItemData(hades_base_item_id+25, True),
    "ThanatosKeepsake": ItemData(hades_base_item_id+26, True),
    "CharonKeepsake": ItemData(hades_base_item_id+27, True),
    "HypnosKeepsake": ItemData(hades_base_item_id+28, True),
    "MegaeraKeepsake": ItemData(hades_base_item_id+29, True),
    "OrpheusKeepsake": ItemData(hades_base_item_id+30, True),
    "DusaKeepsake": ItemData(hades_base_item_id+31, True),
    "SkellyKeepsake": ItemData(hades_base_item_id+32, True),
    "ZeusKeepsake": ItemData(hades_base_item_id+33, True),
    "PoseidonKeepsake": ItemData(hades_base_item_id+34, True),
    "AthenaKeepsake": ItemData(hades_base_item_id+35, True),
    "AphroditeKeepsake": ItemData(hades_base_item_id+36, True),
    "AresKeepsake": ItemData(hades_base_item_id+37, True),
    "ArtemisKeepsake": ItemData(hades_base_item_id+38, True),
    "DionysusKeepsake": ItemData(hades_base_item_id+39, True),
    "HermesKeepsake": ItemData(hades_base_item_id+40, True),
    "DemeterKeepsake": ItemData(hades_base_item_id+41, True),
    "ChaosKeepsake": ItemData(hades_base_item_id+42, True),
    "SisyphusKeepsake": ItemData(hades_base_item_id+43, True),
    "EurydiceKeepsake": ItemData(hades_base_item_id+44, True),
    "PatroclusKeepsake": ItemData(hades_base_item_id+45, True),
}

item_table_weapons: Dict[str, ItemData] ={
    "SwordWeaponUnlockItem": ItemData(hades_base_item_id+46, True),
    "BowWeaponUnlockItem": ItemData(hades_base_item_id+47, True),
    "SpearWeaponUnlockItem": ItemData(hades_base_item_id+48, True),
    "ShieldWeaponUnlockItem": ItemData(hades_base_item_id+49, True),
    "FistWeaponUnlockItem": ItemData(hades_base_item_id+50, True),
    "GunWeaponUnlockItem": ItemData(hades_base_item_id+51, True),
}

item_table_store: Dict[str, ItemData] ={
    "FountainUpgrade1Item": ItemData(hades_base_item_id+52, True),
    "FountainUpgrade2Item": ItemData(hades_base_item_id+53, True),
    "FountainTartarusItem": ItemData(hades_base_item_id+54, True),
    "FountainAsphodelItem": ItemData(hades_base_item_id+55, True),
    "FountainElysiumItem": ItemData(hades_base_item_id+56, True),
    "UrnsOfWealth1Item": ItemData(hades_base_item_id+57, True),
    "UrnsOfWealth2Item": ItemData(hades_base_item_id+58, True),
    "UrnsOfWealth3Item": ItemData(hades_base_item_id+59, True),
    "InfernalTrove1Item": ItemData(hades_base_item_id+60, True),
    "InfernalTrove2Item": ItemData(hades_base_item_id+61, True),
    "InfernalTrove3Item": ItemData(hades_base_item_id+62, True),
    "KeepsakeCollectionItem": ItemData(hades_base_item_id+63, True),
    "DeluxeContractorDeskItem": ItemData(hades_base_item_id+64, True),
    "VanquishersKeepItem": ItemData(hades_base_item_id+65, True),
    "FishingRodItem": ItemData(hades_base_item_id+66, True),
    "CourtMusicianSentenceItem": ItemData(hades_base_item_id+67, True),
    "CourtMusicianStandItem": ItemData(hades_base_item_id+68, True),
    "PitchBlackDarknessItem": ItemData(hades_base_item_id+69, True),
    "FatedKeysItem": ItemData(hades_base_item_id+70, True),
    "BrilliantGemstonesItem": ItemData(hades_base_item_id+71, True),
    "VintageNectarItem": ItemData(hades_base_item_id+72, True),
    "DarkerThirstItem": ItemData(hades_base_item_id+73, True),
}

item_table_hidden_aspects : Dict[str, ItemData] ={
    "SwordHiddenAspect" : ItemData(hades_base_item_id+74, True),
    "BowHiddenAspect": ItemData(hades_base_item_id+75, True),
    "SpearHiddenAspect": ItemData(hades_base_item_id+76, True),
    "ShieldHiddenAspect": ItemData(hades_base_item_id+77, True),
    "FistHiddenAspect": ItemData(hades_base_item_id+78, True),
    "GunHiddenAspect": ItemData(hades_base_item_id+79, True)
}

item_table_traps : Dict[str, ItemData] ={
    "MoneyPunishment" : ItemData(hades_base_item_id+80, False, False, True),
    "HealthPunishment": ItemData(hades_base_item_id+81, False, False, True),
}

item_table_helpers : Dict[str, ItemData] ={
    "MaxHealthHelper" : ItemData(hades_base_item_id+82, False, False, False),
    "BoonBoostHelper" : ItemData(hades_base_item_id+83, False, False, False),
    "InitialMoneyHelper" : ItemData(hades_base_item_id+84, False, False, False),
}

def create_filler_pool_options(options):
    item_filler_options = []
    if options.darkness_pack_value.value:
        item_filler_options.append("Darkness")
    if options.keys_pack_value.value:
        item_filler_options.append("Keys")
    if options.gemstones_pack_value.value:
        item_filler_options.append("Gemstones")
    if options.diamonds_pack_value.value:
        item_filler_options.append("Diamonds")
    if options.titan_blood_pack_value.value:
        item_filler_options.append("TitanBlood")
    if options.nectar_pack_value.value:
        item_filler_options.append("Nectar")
    if options.ambrosia_pack_value.value:
        item_filler_options.append("Ambrosia")
    if not item_filler_options:
        item_filler_options.append("Darkness")
    return item_filler_options

def create_trap_pool():
    return [trap for trap in item_table_traps.keys()]


def create_pact_pool_amount(options) -> Dict[str, int]:
    item_pool_pacts = {
        "HardLaborPactLevel": int(options.hard_labor_pact_amount),
        "LastingConsequencesPactLevel": int(options.lasting_consequences_pact_amount),
        "ConvenienceFeePactLevel": int(options.convenience_fee_pact_amount),
        "JurySummonsPactLevel": int(options.jury_summons_pact_amount),
        "ExtremeMeasuresPactLevel": int(options.extreme_measures_pact_amount),
        "CalisthenicsProgramPactLevel": int(options.calisthenics_program_pact_amount),
        "BenefitsPackagePactLevel": int(options.benefits_package_pact_amount),
        "MiddleManagementPactLevel": int(options.middle_management_pact_amount),
        "UnderworldCustomsPactLevel": int(options.underworld_customs_pact_amount),
        "ForcedOvertimePactLevel": int(options.forced_overtime_pact_amount),
        "HeightenedSecurityPactLevel": int(options.heightened_security_pact_amount),
        "RoutineInspectionPactLevel": int(options.routine_inspection_pact_amount),
        "DamageControlPactLevel": int(options.damage_control_pact_amount),
        "ApprovalProcessPactLevel": int(options.approval_process_pact_amount),
        "TightDeadlinePactLevel": int(options.tight_deadline_pact_amount),
        "PersonalLiabilityPactLevel": int(options.personal_liability_pact_amount),
    }
    return item_pool_pacts


event_item_pairs: Dict[str, str] = {
    "Beat Hades": "HadesVictory",
    "Beat Meg": "MegVictory",
    "Beat Lernie": "LernieVictory",
    "Beat Bros": "BrosVictory",
    "IsThereNoEscape?Event": "IsThereNoEscape?EventItem",
    "DistantRelativesEvent": "DistantRelativesEventItem",
    "ChthonicColleaguesEvent": "ChthonicColleaguesEventItem",
    "TheReluctantMusicianEvent": "TheReluctantMusicianEventItem",
    "GoddessOfWisdomEvent": "GoddessOfWisdomEventItem",
    "GodOfTheHeavensEvent": "GodOfTheHeavensEventItem",
    "GodOfTheSeaEvent": "GodOfTheSeaEventItem",
    "GoddessOfLoveEvent": "GoddessOfLoveEventItem",
    "GodOfWarEvent": "GodOfWarEventItem",
    "GoddessOfTheHuntEvent": "GoddessOfTheHuntEventItem",
    "GodOfWineEvent": "GodOfWineEventItem",
    "GodOfSwiftnessEvent": "GodOfSwiftnessEventItem",
    "GoddessOfSeasonsEvent": "GoddessOfSeasonsEventItem",
    "PowerWithoutEqualEvent": "PowerWithoutEqualEventItem",
    "DivinePairingsEvent": "DivinePairingsEventItem",
    "PrimordialBoonsEvent": "PrimordialBoonsEventItem",
    "PrimordialBanesEvent": "PrimordialBanesEventItem",
    "InfernalArmsEvent": "InfernalArmsEventItem",
    "TheStygianBladeEvent": "TheStygianBladeEventItem",
    "TheHeartSeekingBowEvent": "TheHeartSeekingBowEventItem",
    "TheShieldOfChaosEvent": "TheShieldOfChaosEventItem",
    "TheEternalSpearEvent": "TheEternalSpearEventItem",
    "TheTwinFistsEvent": "TheTwinFistsEventItem",
    "TheAdamantRailEvent": "TheAdamantRailEventItem",
    "MasterOfArmsEvent": "MasterOfArmsEventItem",
    "AViolentPastEvent": "AViolentPastEventItem",
    "HarshConditionsEvent": "HarshConditionsEventItem",
    "SlashedBenefitsEvent": "SlashedBenefitsEventItem",
    "WantonRansackingEvent": "WantonRansackingEventItem",
    "ASimpleJobEvent": "ASimpleJobEventItem",
    "ChthonicKnowledgeEvent": "ChthonicKnowledgeEventItem",
    "CustomerLoyaltyEvent": "CustomerLoyaltyEventItem",
    "DarkReflectionsEvent": "DarkReflectionsEventItem",
    "CloseAtHeartEvent": "CloseAtHeartEventItem",
    "DenizensOfTheDeepEvent": "DenizensOfTheDeepEventItem",
    "TheUselessTrinketEvent": "TheUselessTrinketEventItem", 
}

event_item_pairs_weapon_mode: Dict[str, str] = {
    "IsThereNoEscape?Event": "IsThereNoEscape?EventItem",
    "DistantRelativesEvent": "DistantRelativesEventItem",
    "ChthonicColleaguesEvent": "ChthonicColleaguesEventItem",
    "TheReluctantMusicianEvent": "TheReluctantMusicianEventItem",
    "GoddessOfWisdomEvent": "GoddessOfWisdomEventItem",
    "GodOfTheHeavensEvent": "GodOfTheHeavensEventItem",
    "GodOfTheSeaEvent": "GodOfTheSeaEventItem",
    "GoddessOfLoveEvent": "GoddessOfLoveEventItem",
    "GodOfWarEvent": "GodOfWarEventItem",
    "GoddessOfTheHuntEvent": "GoddessOfTheHuntEventItem",
    "GodOfWineEvent": "GodOfWineEventItem",
    "GodOfSwiftnessEvent": "GodOfSwiftnessEventItem",
    "GoddessOfSeasonsEvent": "GoddessOfSeasonsEventItem",
    "PowerWithoutEqualEvent": "PowerWithoutEqualEventItem",
    "DivinePairingsEvent": "DivinePairingsEventItem",
    "PrimordialBoonsEvent": "PrimordialBoonsEventItem",
    "PrimordialBanesEvent": "PrimordialBanesEventItem",
    "InfernalArmsEvent": "InfernalArmsEventItem",
    "TheStygianBladeEvent": "TheStygianBladeEventItem",
    "TheHeartSeekingBowEvent": "TheHeartSeekingBowEventItem",
    "TheShieldOfChaosEvent": "TheShieldOfChaosEventItem",
    "TheEternalSpearEvent": "TheEternalSpearEventItem",
    "TheTwinFistsEvent": "TheTwinFistsEventItem",
    "TheAdamantRailEvent": "TheAdamantRailEventItem",
    "MasterOfArmsEvent": "MasterOfArmsEventItem",
    "AViolentPastEvent": "AViolentPastEventItem",
    "HarshConditionsEvent": "HarshConditionsEventItem",
    "SlashedBenefitsEvent": "SlashedBenefitsEventItem",
    "WantonRansackingEvent": "WantonRansackingEventItem",
    "ASimpleJobEvent": "ASimpleJobEventItem",
    "ChthonicKnowledgeEvent": "ChthonicKnowledgeEventItem",
    "CustomerLoyaltyEvent": "CustomerLoyaltyEventItem",
    "DarkReflectionsEvent": "DarkReflectionsEventItem",
    "CloseAtHeartEvent": "CloseAtHeartEventItem",
    "DenizensOfTheDeepEvent": "DenizensOfTheDeepEventItem",
    "TheUselessTrinketEvent": "TheUselessTrinketEventItem", 
    "Beat HadesSwordWeapon": "HadesVictorySwordWeapon",
    "Beat MegSwordWeapon": "MegVictorySwordWeapon",
    "Beat LernieSwordWeapon": "LernieVictorySwordWeapon",
    "Beat BrosSwordWeapon": "BrosVictorySwordWeapon",
    "Beat HadesBowWeapon": "HadesVictoryBowWeapon",
    "Beat MegBowWeapon": "MegVictoryBowWeapon",
    "Beat LernieBowWeapon": "LernieVictoryBowWeapon",
    "Beat BrosBowWeapon": "BrosVictoryBowWeapon",
    "Beat HadesSpearWeapon": "HadesVictorySpearWeapon",
    "Beat MegSpearWeapon": "MegVictorySpearWeapon",
    "Beat LernieSpearWeapon": "LernieVictorySpearWeapon",
    "Beat BrosSpearWeapon": "BrosVictorySpearWeapon",
    "Beat HadesShieldWeapon": "HadesVictoryShieldWeapon",
    "Beat MegShieldWeapon": "MegVictoryShieldWeapon",
    "Beat LernieShieldWeapon": "LernieVictoryShieldWeapon",
    "Beat BrosShieldWeapon": "BrosVictoryShieldWeapon",
    "Beat HadesFistWeapon": "HadesVictoryFistWeapon",
    "Beat MegFistWeapon": "MegVictoryFistWeapon",
    "Beat LernieFistWeapon": "LernieVictoryFistWeapon",
    "Beat BrosFistWeapon": "BrosVictoryFistWeapon",
    "Beat HadesGunWeapon": "HadesVictoryGunWeapon",
    "Beat MegGunWeapon": "MegVictoryGunWeapon",
    "Beat LernieGunWeapon": "LernieVictoryGunWeapon",
    "Beat BrosGunWeapon": "BrosVictoryGunWeapon",
}



item_table = {
    **item_table_pacts,
    **items_table_event,
    **items_table_fates_completion,
    **item_table_filler,
    **item_table_keepsake,
    **item_table_weapons,
    **item_table_store,
    **item_table_hidden_aspects,
    **item_table_traps,
    **item_table_helpers,
}

group_pacts = {"pacts":item_table_pacts.keys()}
group_fillers = {"fillers":item_table_filler.keys()}
group_contractor = {"contractor":item_table_store.keys()}
group_weapons = {"weapons":item_table_weapons.keys()}
group_aspects = {"aspects":item_table_hidden_aspects.keys()}
group_keepsakes = {"keepsakes":item_table_keepsake.keys()}

item_name_groups = {
    **group_pacts,
    **group_fillers,
    **group_contractor,
    **group_weapons,
    **group_aspects,
    **group_keepsakes,
}

class HadesItem(Item):
    game = "Hades"

    def __init__(self, name, player: int = None):
        item_data = item_table[name]
        if item_data.progression:
            itemClass = ItemClassification.progression
        elif item_data.trap:
            itemClass = ItemClassification.trap
        else:
            itemClass = ItemClassification.filler
            
        super(HadesItem, self).__init__(
            name,
            itemClass,
            item_data.code, player
        )

    def is_progression(self):
        return self.classification == ItemClassification.progression
