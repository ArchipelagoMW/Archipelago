from typing import TYPE_CHECKING
from BaseClasses import MultiWorld, Item, ItemClassification
from .Items import item_table_pacts, item_table_keepsake, items_table_fates_completion, HadesItem
from worlds.AutoWorld import LogicMixin
from worlds.generic.Rules import set_rule, add_rule, add_item_rule
from Utils import visualize_regions
from .Locations import location_weapons_subfixes

if TYPE_CHECKING:
    from . import HadesWorld

class HadesLogic(LogicMixin):
    def _total_heat_level(self, player:int, amount: int, options) -> bool:
        if not options.heat_system == "reverseheat":
            return True
        count=0
        for key in item_table_pacts.keys():
            count = count + self.count(key, player)
        return count >= amount

    def _has_enough_of_item(self, player:int, amount: int, item:str) -> bool:
        return self.count(item, player)>=amount

    def _has_enough_routine_inspection(self, player: int, amount: int, options) -> bool:
        if not options.heat_system == "reverseheat":
            return True
        return self._has_enough_of_item(player, amount, "RoutineInspectionPactLevel")
    
    def _has_enough_urns(self, player: int, amount: int) -> bool:
        return self.count("UrnsOfWealth1Item", player) + self.count("UrnsOfWealth2Item", player) \
            + self.count("UrnsOfWealth3Item", player) >=amount
    
    def _has_enough_throve(self, player: int, amount: int) -> bool:
        return self.count("InfernalTrove1Item", player) + self.count("InfernalTrove2Item", player) \
            + self.count("InfernalTrove3Item", player) >=amount
    
    def _has_enough_weapons(self, player: int, options, amount: int) -> bool:
        if not options.weaponsanity:
            return True
        count = 0
        if (self._has_weapon("SwordWeapon", player, options)):
            count += 1
        if (self._has_weapon("BowWeapon", player, options)):
            count += 1
        if (self._has_weapon("SpearWeapon", player, options)):
            count += 1
        if (self._has_weapon("ShieldWeapon", player, options)):
            count += 1
        if (self._has_weapon("FistWeapon", player, options)):
            count += 1
        if (self._has_weapon("GunWeapon", player, options)):
            count += 1
        return count >= amount
    
    def _has_enough_keepsakes(self, player:int, amount:int, options) -> bool:
        amount_keepsakes = 0
        for keepsake_name in item_table_keepsake:
            amount_keepsakes += self.count(keepsake_name, player)
        return amount_keepsakes >= amount

    def _has_enough_fates_done(self, player:int, amount:int, options) -> bool:
        amount_fates = 0 
        for fates_names in items_table_fates_completion:
            amount_fates += self.count(fates_names, player)
        return amount_fates >= amount
    
    def _has_weapon(self, weaponSubfix, player:int, option) -> bool:
        if not option.weaponsanity:
            return True
        if (weaponSubfix == "SwordWeapon"):
            return ((option.initial_weapon == "Sword") or (self.has("SwordWeaponUnlockItem", player)))
        if (weaponSubfix == "BowWeapon"):
            return ((option.initial_weapon == "Bow") or (self.has("BowWeaponUnlockItem", player)))
        if (weaponSubfix == "SpearWeapon"):
            return ((option.initial_weapon == "Spear") or (self.has("SpearWeaponUnlockItem", player)))
        if (weaponSubfix == "ShieldWeapon"):
            return ((option.initial_weapon == "Shield") or (self.has("ShieldWeaponUnlockItem", player)))
        if (weaponSubfix == "FistWeapon"):
            return ((option.initial_weapon == "Fist") or (self.has("FistWeaponUnlockItem", player)))
        if (weaponSubfix == "GunWeapon"):
            return ((option.initial_weapon == "Gun") or (self.has("GunWeaponUnlockItem", player)))

    def _can_get_victory(self, player: int, options) -> bool:
        can_win = self._has_defeated_boss("HadesVictory", player, options)
        if options.weaponsanity:
            weapons = options.weapons_clears_needed.value
            can_win = (can_win) and (self._enough_weapons_victories(player,options,weapons))
        if options.keepsakesanity:
            keepsakes = options.keepsakes_needed.value
            can_win = (can_win) and (self._has_enough_keepsakes(player,keepsakes,options))
        fates = options.fates_needed.value
        can_win = (can_win) and (self._has_enough_fates_done(player,fates,options))
        return can_win
    
    def _has_defeated_boss(self, bossVictory,player:int, options) -> bool:
        if options.location_system == "roomweaponbased":
            counter=0
            counter += self.count(bossVictory+"SwordWeapon", player)
            counter += self.count(bossVictory+"SpearWeapon", player)
            counter += self.count(bossVictory+"BowWeapon", player)
            counter += self.count(bossVictory+"ShieldWeapon", player)
            counter += self.count(bossVictory+"FistWeapon", player)
            counter += self.count(bossVictory+"GunWeapon", player)
            return counter > 0
        else:
           return self.has(bossVictory, player)

    def _enough_weapons_victories(self,player:int, options, amount: int) -> bool:
        if options.location_system == "roomweaponbased":
            counter=0
            counter += self.count("HadesVictory"+"SwordWeapon", player)
            counter += self.count("HadesVictory"+"SpearWeapon", player)
            counter += self.count("HadesVictory"+"BowWeapon", player)
            counter += self.count("HadesVictory"+"ShieldWeapon", player)
            counter += self.count("HadesVictory"+"FistWeapon", player)
            counter += self.count("HadesVictory"+"GunWeapon", player)
            return counter >= amount
        else:
           return self.has("HadesVictory", player) and self._has_enough_weapons(player, options, amount)

# -----------

def set_rules(world: "HadesWorld", player: int, number_items: int, location_table, options):
    # Set up some logic in areas to avoid having all heats "stack up" as batch in other games.
    total_routine_inspection = int(options.routine_inspection_pact_amount.value)

    if (options.location_system == "roomweaponbased"):
        set_weapon_region_rules(world, player, number_items, location_table, options, 
                                "SwordWeapon", total_routine_inspection);
        set_weapon_region_rules(world, player, number_items, location_table, options, 
                                "SpearWeapon", total_routine_inspection);
        set_weapon_region_rules(world, player, number_items, location_table, options, 
                                "BowWeapon", total_routine_inspection);
        set_weapon_region_rules(world, player, number_items, location_table, options, 
                                "ShieldWeapon", total_routine_inspection);
        set_weapon_region_rules(world, player, number_items, location_table, options, 
                                "FistWeapon", total_routine_inspection);
        set_weapon_region_rules(world, player, number_items, location_table, options, 
                                "GunWeapon", total_routine_inspection);
    else:
        set_rule(world.get_entrance("Exit Tartarus", player), 
                 lambda state: state.has("MegVictory", player) and  \
                    state._total_heat_level(player, min(number_items/4,10), options) and  \
                    state._has_enough_routine_inspection(player,total_routine_inspection-2, options) and  \
                    state._has_enough_weapons(player, options, 2))
        set_rule(world.get_entrance("Exit Asphodel", player), lambda state: state.has("LernieVictory", player) and  \
                    state._total_heat_level(player, min(number_items/2,20), options) and \
                    state._has_enough_routine_inspection(player,total_routine_inspection-1, options) and  \
                    state._has_enough_weapons(player, options, 3))
        set_rule(world.get_entrance("Exit Elyseum", player), lambda state: state.has("BrosVictory", player) and  \
                    state._total_heat_level(player, min(number_items*3/4,30), options) and  \
                    state._has_enough_routine_inspection(player,total_routine_inspection, options) and  \
                    state._has_enough_weapons(player, options, 5))
        set_rule(world.get_location("Beat Hades", player), lambda state:  \
                    state._total_heat_level(player, min(number_items,35), options) and  \
                    state._has_enough_weapons(player, options, 6))
    

    forbid_important_items_on_late_styx(world, player, options)
    world.completion_condition[player] = lambda state: state._can_get_victory(player, options)
    
    if options.keepsakesanity:
        add_rule(world.get_entrance("NPCS", player), lambda state: True)
        add_rule(world.get_location("EurydiceKeepsake",player), lambda state:  \
                 state._has_defeated_boss("LernieVictory", player, options))
        add_rule(world.get_location("ThanatosKeepsake",player), lambda state:  \
                state._has_defeated_boss("HadesVictory", player, options))
        add_rule(world.get_location("PatroclusKeepsake",player), lambda state:  \
                state._has_defeated_boss("BrosVictory", player, options))
        set_keepsake_balance(world, player, location_table, options)
    if options.weaponsanity:
        add_rule(world.get_entrance("Weapon Cache", player), lambda state: True)
    if options.storesanity:
        set_store_rules(world, player, location_table, options)
    if options.fatesanity:
        set_fates_rules(world, player, location_table, options, "")
    set_fates_rules(world, player, location_table, options, "Event")
    

    if options.keepsakesanity and options.storesanity:
        add_rule(world.get_location("OrpheusKeepsake", player), lambda state: \
                state.has("CourtMusicianSentenceItem",player))
        

def set_keepsake_balance(world: "HadesWorld", player: int, location_table, options):
    set_rule(world.get_location("ZeusKeepsake", player), lambda state:   \
            state.has("ZeusKeepsake", player))
    set_rule(world.get_location("PoseidonKeepsake", player), lambda state:   \
            state.has("PoseidonKeepsake", player))
    set_rule(world.get_location("AthenaKeepsake", player), lambda state:   \
            state.has("AthenaKeepsake", player))
    set_rule(world.get_location("AphroditeKeepsake", player), lambda state:   \
            state.has("AphroditeKeepsake", player))
    set_rule(world.get_location("AresKeepsake", player), lambda state:   \
            state.has("AresKeepsake", player))
    set_rule(world.get_location("ArtemisKeepsake", player), lambda state:   \
            state.has("ArtemisKeepsake", player))
    set_rule(world.get_location("DionysusKeepsake", player), lambda state:   \
            state.has("DionysusKeepsake", player))
    set_rule(world.get_location("DemeterKeepsake", player), lambda state:   \
            state.has("DemeterKeepsake", player))
    set_rule(world.get_location("HermesKeepsake", player), lambda state:   \
            state._has_defeated_boss("MegVictory", player, options))


def set_store_rules(world: "HadesWorld", player: int, location_table, options):
    #Fountains
    set_rule(world.get_location("FountainUpgrade1Location", player), lambda state:  \
            state.has("FountainTartarusItem", player))
    set_rule(world.get_location("FountainUpgrade2Location", player), lambda state:  \
            state.has("FountainUpgrade1Item", player) or state.has("FountainUpgrade2Item", player))
    set_rule(world.get_location("FountainAsphodelLocation", player), lambda state:  \
            state.has("FountainTartarusItem", player) and state.has("KeepsakeCollectionItem", player) and  \
            state._has_defeated_boss("MegVictory", player, options))
    set_rule(world.get_location("FountainElysiumLocation", player), lambda state: \
            state.has("FountainTartarusItem", player) and state.has("KeepsakeCollectionItem", player) and  \
            state._has_defeated_boss("LernieVictory", player, options))
    
    #Urns
    set_rule(world.get_location("UrnsOfWealth1Location", player), lambda state:  \
             state.has("FountainTartarusItem", player))
    set_rule(world.get_location("UrnsOfWealth2Location", player), lambda state: state._has_enough_urns(player,1))
    set_rule(world.get_location("UrnsOfWealth3Location", player), lambda state: state._has_enough_urns(player,2))
    
    #Infernal Trove
    set_rule(world.get_location("InfernalTrove2Location", player), lambda state: state._has_enough_throve(player,1) and \
            state.has("FountainElysiumItem",player) and state.has("KeepsakeCollectionItem", player))
    set_rule(world.get_location("InfernalTrove3Location", player), lambda state: state._has_enough_throve(player,2) and \
            state.has("FountainElysiumItem",player) and state.has("KeepsakeCollectionItem", player) and  \
            state.has("DeluxeContractorDeskItem", player))
    
    #Keepsake storage
    set_rule(world.get_location("KeepsakeCollectionLocation", player), lambda state:  \
            state._has_defeated_boss("MegVictory", player, options) and state.has("FountainTartarusItem", player))
    
    #Deluxe contractor desk
    set_rule(world.get_location("DeluxeContractorDeskLocation", player), lambda state:  \
            state.has("FountainElysiumItem", player) and state.has("CourtMusicianSentenceItem", player))
    
    #Other random stuff
    set_rule(world.get_location("VanquishersKeepLocation", player), lambda state:\
            state.has("DeluxeContractorDeskItem", player))
    set_rule(world.get_location("FishingRodLocation", player), lambda state:  \
            state._has_defeated_boss("BrosVictory", player, options) and state.has("FountainTartarusItem", player))
    set_rule(world.get_location("CourtMusicianStandLocation", player), lambda state:  \
            state.has("CourtMusicianSentenceItem", player))
    
    #Orpheus might have other rules depending on settings
    add_rule(world.get_location("CourtMusicianSentenceLocation", player), lambda state:  \
            state._has_defeated_boss("MegVictory", player, options) and state.has("FountainTartarusItem", player))
    
    #Upgrades of runs with gems locations
    set_rule(world.get_location("PitchBlackDarknessLocation", player), lambda state:  \
            state.has("DeluxeContractorDeskItem", player))
    set_rule(world.get_location("FatedKeysLocation", player), lambda state:  \
            state.has("DeluxeContractorDeskItem", player))
    set_rule(world.get_location("BrilliantGemstonesLocation", player), lambda state:  \
            state.has("DeluxeContractorDeskItem", player))
    set_rule(world.get_location("VintageNectarLocation", player), lambda state:  \
            state.has("DeluxeContractorDeskItem", player))
    set_rule(world.get_location("DarkerThirstLocation", player), lambda state: \
            state.has("DeluxeContractorDeskItem", player))
    

def set_fates_rules(world: "HadesWorld", player: int, location_table, options, subfix: str):
    #Rules that dont depend on other settings
    set_rule(world.get_location("IsThereNoEscape?"+subfix, player), lambda state: \
            state._has_defeated_boss("HadesVictory", player, options))
    set_rule(world.get_location("HarshConditions"+subfix, player), lambda state:  \
            state._has_defeated_boss("HadesVictory", player, options))
    set_rule(world.get_location("SlashedBenefits"+subfix, player), lambda state:  \
            state._has_defeated_boss("HadesVictory", player, options))
    set_rule(world.get_location("TheUselessTrinket"+subfix, player), lambda state:  \
            state._has_defeated_boss("HadesVictory", player, options))
    set_rule(world.get_location("WantonRansacking"+subfix, player), lambda state:  \
            state._has_defeated_boss("HadesVictory", player, options))
    set_rule(world.get_location("DarkReflections"+subfix, player), lambda state:  \
            state._has_defeated_boss("HadesVictory", player, options))

    #Rules that depend on storesanity
    if options.storesanity:
        set_rule(world.get_location("TheReluctantMusician"+subfix, player), lambda state:  \
                state.has("CourtMusicianSentenceItem", player))
        set_rule(world.get_location("DenizensOfTheDeep"+subfix, player), lambda state:  \
                state._has_defeated_boss("HadesVictory", player, options) and state.has("FishingRodItem",player))
    else:
        set_rule(world.get_location("TheReluctantMusician"+subfix, player), lambda state:  \
                state._has_defeated_boss("MegVictory", player, options))
        set_rule(world.get_location("DenizensOfTheDeep"+subfix, player), lambda state: \
                state._has_defeated_boss("HadesVictory", player, options))
    #This part depends on weaponsanity, but the false option is handled on has_enough_weapons
    set_rule(world.get_location("InfernalArms"+subfix, player), lambda state:  \
            state._has_enough_weapons(player, options, 6))
    set_rule(world.get_location("AViolentPast"+subfix, player), lambda state:  \
            state._has_enough_weapons(player, options, 6))
    set_rule(world.get_location("MasterOfArms"+subfix, player), lambda state:  \
            state._has_enough_weapons(player, options, 6) and  \
            state._has_defeated_boss("HadesVictory", player, options))
   
    #rules that depend on weaponsanity:
    if options.weaponsanity:
        set_rule(world.get_location("TheStygianBlade"+subfix, player), lambda state: \
                state.has("SwordWeaponUnlockItem", player) or options.initial_weapon == "Sword")
        set_rule(world.get_location("TheHeartSeekingBow"+subfix, player), lambda state: \
                state.has("BowWeaponUnlockItem", player) or options.initial_weapon == "Bow")
        set_rule(world.get_location("TheEternalSpear"+subfix, player), lambda state: \
                state.has("SpearWeaponUnlockItem", player) or options.initial_weapon == "Spear")
        set_rule(world.get_location("TheShieldOfChaos"+subfix, player), lambda state: \
                state.has("ShieldWeaponUnlockItem", player) or options.initial_weapon == "Shield")
        set_rule(world.get_location("TheTwinFists"+subfix, player), lambda state: \
                state.has("FistWeaponUnlockItem", player) or options.initial_weapon == "Fist")
        set_rule(world.get_location("TheAdamantRail"+subfix, player), lambda state: \
                state.has("GunWeaponUnlockItem", player) or options.initial_weapon == "Gun")
        
    if options.keepsakesanity:
        set_rule(world.get_location("CloseAtHeart"+subfix, player), lambda state: \
                state._has_enough_keepsakes(player, 23, options))
        #This is balancing rules, so grinding gods is less painful
        set_rule(world.get_location("GoddessOfWisdom"+subfix, player), lambda state: \
                state.has("AthenaKeepsake", player))
        set_rule(world.get_location("GodOfTheHeavens"+subfix, player), lambda state: \
                state.has("ZeusKeepsake", player))
        set_rule(world.get_location("GodOfTheSea"+subfix, player), lambda state: \
                state.has("PoseidonKeepsake", player))
        set_rule(world.get_location("GoddessOfLove"+subfix, player), lambda state: \
                state.has("AphroditeKeepsake", player))
        set_rule(world.get_location("GodOfWar"+subfix, player), lambda state: \
                state.has("AresKeepsake", player))
        set_rule(world.get_location("GoddessOfTheHunt"+subfix, player), lambda state: \
                state.has("ArtemisKeepsake", player))
        set_rule(world.get_location("GodOfWine"+subfix, player), lambda state: \
                state.has("DionysusKeepsake", player))
        set_rule(world.get_location("GodOfSwiftness"+subfix, player), lambda state: \
                state.has("HermesKeepsake", player))
        set_rule(world.get_location("GoddessOfSeasons"+subfix, player), lambda state: \
                state.has("DemeterKeepsake", player))
        
        #Balancing rules
        #Put here a rule that you need to have all God keepsakes for the DivinePairis?
        set_rule(world.get_location("PrimordialBoons"+subfix, player), lambda state: \
                state.has("ChaosKeepsake", player))
        set_rule(world.get_location("PrimordialBanes"+subfix, player), lambda state: \
                state.has("ChaosKeepsake", player))
        
        #Balacing rules for DivinePairings
        add_rule(world.get_location("DivinePairings"+subfix, player), lambda state: \
                state.has("AthenaKeepsake", player))
        add_rule(world.get_location("DivinePairings"+subfix, player), lambda state: \
                state.has("ZeusKeepsake", player))
        add_rule(world.get_location("DivinePairings"+subfix, player), lambda state: \
                state.has("PoseidonKeepsake", player))
        add_rule(world.get_location("DivinePairings"+subfix, player), lambda state: \
                state.has("AphroditeKeepsake", player))
        add_rule(world.get_location("DivinePairings"+subfix, player), lambda state: \
                state.has("AresKeepsake", player))
        add_rule(world.get_location("DivinePairings"+subfix, player), lambda state: \
                state.has("ArtemisKeepsake", player))
        add_rule(world.get_location("DivinePairings"+subfix, player), lambda state: \
                state.has("DionysusKeepsake", player))
        add_rule(world.get_location("DivinePairings"+subfix, player), lambda state: \
                state.has("HermesKeepsake", player))
        add_rule(world.get_location("DivinePairings"+subfix, player), lambda state: \
                state.has("DemeterKeepsake", player))

    #This is extra balancing rules to avoid fates being a pain in the butt
    add_rule(world.get_location("PrimordialBoons"+subfix, player), lambda state: \
                state._has_defeated_boss("LernieVictory", player, options))
    add_rule(world.get_location("PrimordialBanes"+subfix, player), lambda state: \
                state._has_defeated_boss("LernieVictory", player, options))
    
    set_rule(world.get_location("PowerWithoutEqual"+subfix, player), lambda state: \
                state._has_defeated_boss("BrosVictory", player, options))
    add_rule(world.get_location("DivinePairings"+subfix, player), lambda state: \
                state._has_defeated_boss("LernieVictory", player, options))
        

def set_weapon_region_rules(world: "HadesWorld", player: int, number_items: int, 
                            location_table, options, weaponSubfix: str, total_routine_inspection:int):
    set_rule(world.get_entrance("Zags room"+weaponSubfix, player), lambda state: \
            state._has_weapon(weaponSubfix, player, options))
    set_rule(world.get_entrance("Exit Tartarus"+weaponSubfix, player), lambda state: \
            state.has("MegVictory"+weaponSubfix, player) and \
            state._total_heat_level(player, min(number_items/4,10), options) and \
            state._has_enough_routine_inspection(player,total_routine_inspection-2, options) and \
            state._has_enough_weapons(player, options, 2))
    set_rule(world.get_entrance("Exit Asphodel"+weaponSubfix, player), lambda state: \
            state.has("LernieVictory"+weaponSubfix, player) and \
            state._total_heat_level(player, min(number_items/2,20), options) and \
            state._has_enough_routine_inspection(player,total_routine_inspection-1, options) and \
            state._has_enough_weapons(player, options, 3))
    set_rule(world.get_entrance("Exit Elyseum"+weaponSubfix, player), lambda state: \
            state.has("BrosVictory"+weaponSubfix, player)  and \
            state._total_heat_level(player, min(number_items*3/4,30), options) and \
            state._has_enough_routine_inspection(player,total_routine_inspection, options) and \
            state._has_enough_weapons(player, options, 5))
    set_rule(world.get_location("Beat Hades"+weaponSubfix, player), lambda state: \
            state._total_heat_level(player, min(number_items,35), options) and \
            state._has_enough_weapons(player, options, 6))
    

def forbid_important_items_on_late_styx(world: "HadesWorld", player: int, options):
    if options.location_system == "roomweaponbased":
        for weaponString in location_weapons_subfixes:
                late_styx_region = world.get_region("StyxLate"+weaponString, player)
                for location in late_styx_region.locations:
                        add_item_rule(location,
                                lambda item: not item.advancement or item_is_plando(world, item, player))
    else:
        late_styx_region = world.get_region("StyxLate", player)
        for location in late_styx_region.locations:
                add_item_rule(location,
                        lambda item: not item.advancement or item_is_plando(world, item, player))
                


def item_is_plando(world: "HadesWorld", item: Item, player: int) -> bool:
    return item in world.plando_items[player]