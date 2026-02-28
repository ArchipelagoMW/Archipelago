from typing import TYPE_CHECKING
from BaseClasses import Item
from .Items import item_table_pacts, item_table_keepsake, items_table_fates_completion
from worlds.AutoWorld import LogicMixin
from worlds.generic.Rules import set_rule, add_rule, add_item_rule
from .Locations import location_weapons_subfixes

if TYPE_CHECKING:
    from . import HadesWorld


class HadesLogic(LogicMixin):
    def _total_heat_level(self, player: int, amount: int, options) -> bool:
        if not options.heat_system == "reverse_heat":
            return True
        count = 0
        for key in item_table_pacts.keys():
            count = count + self.count(key, player)
        return count >= amount

    def _has_enough_of_item(self, player: int, amount: int, item: str) -> bool:
        return self.count(item, player) >= amount

    def _has_enough_routine_inspection(self, player: int, amount: int, options) -> bool:
        if not options.heat_system == "reverse_heat":
            return True
        return self._has_enough_of_item(player, amount, "Routine Inspection Pact Level")
    
    def _has_enough_urns(self, player: int, amount: int) -> bool:
        return self.count("Urns Of Wealth1 Item", player) + self.count("Urns Of Wealth2 Item", player) \
            + self.count("Urns Of Wealth3 Item", player) >= amount
    
    def _has_enough_throve(self, player: int, amount: int) -> bool:
        return self.count("Infernal Trove1 Item", player) + self.count("Infernal Trove2 Item", player) \
            + self.count("Infernal Trove3 Item", player) >= amount
    
    def _has_enough_weapons(self, player: int, options, amount: int) -> bool:
        if not options.weaponsanity:
            return True
        count = 0
        if self._has_weapon("Sword Weapon", player, options):
            count += 1
        if self._has_weapon("Bow Weapon", player, options):
            count += 1
        if self._has_weapon("Spear Weapon", player, options):
            count += 1
        if self._has_weapon("Shield Weapon", player, options):
            count += 1
        if self._has_weapon("Fist Weapon", player, options):
            count += 1
        if self._has_weapon("Gun Weapon", player, options):
            count += 1
        return count >= amount
    
    def _has_enough_keepsakes(self, player: int, amount: int, options) -> bool:
        amount_keepsakes = 0
        for keepsake_name in item_table_keepsake:
            amount_keepsakes += self.count(keepsake_name, player)
        return amount_keepsakes >= amount

    def _has_enough_fates_done(self, player: int, amount: int, options) -> bool:
        amount_fates = 0 
        for fates_names in items_table_fates_completion:
            amount_fates += self.count(fates_names, player)
        return amount_fates >= amount
    
    def _has_weapon(self, weaponSubfix, player: int, option) -> bool:
        if not option.weaponsanity:
            return True
        if weaponSubfix == "Sword Weapon":
            return ((option.initial_weapon == 0) or (self.has("Sword Weapon Unlock Item", player)))
        if weaponSubfix == "Bow Weapon":
            return ((option.initial_weapon == 1) or (self.has("Bow Weapon Unlock Item", player)))
        if weaponSubfix == "Spear Weapon":
            return ((option.initial_weapon == 2) or (self.has("Spear Weapon Unlock Item", player)))
        if weaponSubfix == "Shield Weapon":
            return ((option.initial_weapon == 3) or (self.has("Shield Weapon Unlock Item", player)))
        if weaponSubfix == "Fist Weapon":
            return ((option.initial_weapon == 4) or (self.has("Fist Weapon Unlock Item", player)))
        if weaponSubfix == "Gun Weapon":
            return ((option.initial_weapon == 5) or (self.has("Gun Weapon Unlock Item", player)))

    def _can_get_victory(self, player: int, options) -> bool:
        can_win = self._has_defeated_boss("Hades Victory", player, options)
        if options.weaponsanity:
            weapons = options.weapons_clears_needed.value
            can_win = (can_win) and (self._enough_weapons_victories(player, options, weapons))
        if options.keepsakesanity:
            keepsakes = options.keepsakes_needed.value
            can_win = (can_win) and (self._has_enough_keepsakes(player, keepsakes, options))
        fates = options.fates_needed.value
        can_win = (can_win) and (self._has_enough_fates_done(player, fates, options))
        return can_win
    
    def _has_defeated_boss(self, bossVictory, player: int, options) -> bool:
        if options.location_system == "room_weapon_based":
            counter = 0
            counter += self.count(bossVictory + " Sword Weapon", player)
            counter += self.count(bossVictory + " Spear Weapon", player)
            counter += self.count(bossVictory + " Bow Weapon", player)
            counter += self.count(bossVictory + " Shield Weapon", player)
            counter += self.count(bossVictory + " Fist Weapon", player)
            counter += self.count(bossVictory + " Gun Weapon", player)
            return counter > 0
        else:
            return self.has(bossVictory, player)

    def _enough_weapons_victories(self, player: int, options, amount: int) -> bool:
        if options.location_system == "room_weapon_based":
            counter = 0
            counter += self.count("Hades Victory" + " Sword Weapon", player)
            counter += self.count("Hades Victory" + " Spear Weapon", player)
            counter += self.count("Hades Victory" + " Bow Weapon", player)
            counter += self.count("Hades Victory" + " Shield Weapon", player)
            counter += self.count("Hades Victory" + " Fist Weapon", player)
            counter += self.count("Hades Victory" + " Gun Weapon", player)
            return counter >= amount
        else:
            return self.has("Hades Victory", player) and self._has_enough_weapons(player, options, amount)

# -----------


def set_rules(world: "HadesWorld", player: int, number_items: int, location_table, options):
    # Set up some logic in areas to avoid having all heats "stack up" as batch in other games.
    total_routine_inspection = int(options.routine_inspection_pact_amount.value)

    if options.location_system == "room_weapon_based":
        set_weapon_region_rules(world, player, number_items, location_table, options, 
                                "Sword Weapon", total_routine_inspection)
        set_weapon_region_rules(world, player, number_items, location_table, options, 
                                "Spear Weapon", total_routine_inspection)
        set_weapon_region_rules(world, player, number_items, location_table, options, 
                                "Bow Weapon", total_routine_inspection)
        set_weapon_region_rules(world, player, number_items, location_table, options, 
                                "Shield Weapon", total_routine_inspection)
        set_weapon_region_rules(world, player, number_items, location_table, options, 
                                "Fist Weapon", total_routine_inspection)
        set_weapon_region_rules(world, player, number_items, location_table, options, 
                                "Gun Weapon", total_routine_inspection)
    else:
        set_rule(world.get_entrance("Exit Tartarus", player), 
                 lambda state: state.has("Meg Victory", player) and  \
                    state._total_heat_level(player, min(number_items / 4, 10), options) and  \
                    state._has_enough_routine_inspection(player, total_routine_inspection-2, options) and  \
                    state._has_enough_weapons(player, options, 2))
        set_rule(world.get_entrance("Exit Asphodel", player), lambda state: state.has("Lernie Victory", player) and  \
                    state._total_heat_level(player, min(number_items / 2, 20), options) and \
                    state._has_enough_routine_inspection(player, total_routine_inspection - 1, options) and  \
                    state._has_enough_weapons(player, options, 3))
        set_rule(world.get_entrance("Exit Elysium", player), lambda state: state.has("Bros Victory", player) and  \
                    state._total_heat_level(player, min(number_items * 3 / 4, 30), options) and  \
                    state._has_enough_routine_inspection(player, total_routine_inspection, options) and  \
                    state._has_enough_weapons(player, options, 5))
        set_rule(world.get_location("Beat Hades", player), lambda state: \
                    state._total_heat_level(player, min(number_items, 35), options) and \
                    state._has_enough_weapons(player, options, 6))
    

    forbid_important_items_on_late_styx(world, player, options)
    world.completion_condition[player] = lambda state: state._can_get_victory(player, options)
    
    if options.keepsakesanity:
        add_rule(world.get_entrance("NPCS", player), lambda state: True)
        add_rule(world.get_location("Eurydice Keepsake", player), lambda state: \
                 state._has_defeated_boss("Lernie Victory", player, options))
        add_rule(world.get_location("Thanatos Keepsake", player), lambda state: \
                state._has_defeated_boss("Hades Victory", player, options))
        add_rule(world.get_location("Patroclus Keepsake", player), lambda state: \
                state._has_defeated_boss("Bros Victory", player, options))
        set_keepsake_balance(world, player, location_table, options)
    if options.weaponsanity:
        add_rule(world.get_entrance("Weapon Cache", player), lambda state: True)
    if options.storesanity:
        set_store_rules(world, player, location_table, options)
    if options.fatesanity:
        set_fates_rules(world, player, location_table, options, "")
    set_fates_rules(world, player, location_table, options, " Event")
    

    if options.keepsakesanity and options.storesanity:
        add_rule(world.get_location("Orpheus Keepsake", player), lambda state: \
                state.has("Court Musician Sentence Item",player))
        

def set_keepsake_balance(world: "HadesWorld", player: int, location_table, options):
    set_rule(world.get_location("Zeus Keepsake", player), lambda state:   \
            state.has("Zeus Keepsake", player))
    set_rule(world.get_location("Poseidon Keepsake", player), lambda state:   \
            state.has("Poseidon Keepsake", player))
    set_rule(world.get_location("Athena Keepsake", player), lambda state:   \
            state.has("Athena Keepsake", player))
    set_rule(world.get_location("Aphrodite Keepsake", player), lambda state:   \
            state.has("Aphrodite Keepsake", player))
    set_rule(world.get_location("Ares Keepsake", player), lambda state:   \
            state.has("Ares Keepsake", player))
    set_rule(world.get_location("Artemis Keepsake", player), lambda state:   \
            state.has("Artemis Keepsake", player))
    set_rule(world.get_location("Dionysus Keepsake", player), lambda state:   \
            state.has("Dionysus Keepsake", player))
    set_rule(world.get_location("Demeter Keepsake", player), lambda state:   \
            state.has("Demeter Keepsake", player))
    set_rule(world.get_location("Hermes Keepsake", player), lambda state:   \
            state._has_defeated_boss("Meg Victory", player, options))


def set_store_rules(world: "HadesWorld", player: int, location_table, options):
    #Fountains
    set_rule(world.get_location("Fountain Upgrade1 Location", player), lambda state:  \
            state.has("Fountain Tartarus Item", player))
    set_rule(world.get_location("Fountain Upgrade2 Location", player), lambda state:  \
            state.has("Fountain Upgrade1 Item", player) and state.has("Fountain Tartarus Item", player))
    set_rule(world.get_location("Fountain Asphodel Location", player), lambda state:  \
            state.has("Fountain Tartarus Item", player) and state.has("Keepsake Collection Item", player) and  \
            state._has_defeated_boss("Meg Victory", player, options))
    set_rule(world.get_location("Fountain Elysium Location", player), lambda state: \
            state.has("Fountain Tartarus Item", player) and state.has("Keepsake Collection Item", player) and  \
            state._has_defeated_boss("Lernie Victory", player, options))
    
    #Urns
    set_rule(world.get_location("Urns Of Wealth1 Location", player), lambda state:  \
             state.has("Fountain Tartarus Item", player))
    set_rule(world.get_location("Urns Of Wealth2 Location", player), lambda state: state._has_enough_urns(player,1))
    set_rule(world.get_location("Urns Of Wealth3 Location", player), lambda state: state._has_enough_urns(player,2))
    
    #Infernal Trove
    set_rule(world.get_location("Infernal Trove2 Location", player), lambda state: state._has_enough_throve(player,1) \
        and state.has("Fountain Tartarus Item",player) and state.has("Fountain Asphodel Item",player) \
        and state.has("Fountain Elysium Item",player) and state.has("Keepsake Collection Item", player))

    set_rule(world.get_location("Infernal Trove3 Location", player), lambda state: state._has_enough_throve(player,2) \
        and state.has("Fountain Tartarus Item",player) and state.has("Fountain Asphodel Item",player) \
        and state.has("Fountain Elysium Item",player) and state.has("Keepsake Collection Item", player) \
        and state.has("Deluxe Contractor Desk Item", player))
    
    #Keepsake storage
    set_rule(world.get_location("Keepsake Collection Location", player), lambda state:  \
            state._has_defeated_boss("Meg Victory", player, options) and state.has("Fountain Tartarus Item", player))
    
    #Deluxe contractor desk
    set_rule(world.get_location("Deluxe Contractor Desk Location", player), lambda state:  \
            state.has("Fountain Elysium Item", player) and state.has("Court Musician Sentence Item", player) and \
            state.has("Urns Of Wealth1 Item", player) and state.has("Keepsake Collection Item", player) and \
            state.has("Infernal Trove1 Item", player))
    
    #Other random stuff
    set_rule(world.get_location("Vanquishers Keep Location", player), lambda state:\
            state.has("Deluxe Contractor Desk Item", player))
    set_rule(world.get_location("Fishing Rod Location", player), lambda state:  \
            state._has_defeated_boss("Bros Victory", player, options) and state.has("Fountain Tartarus Item", player))
    set_rule(world.get_location("Court Musician Stand Location", player), lambda state:  \
            state.has("Court Musician Sentence Item", player))
    
    #Orpheus might have other rules depending on settings
    add_rule(world.get_location("Court Musician Sentence Location", player), lambda state:  \
            state._has_defeated_boss("Meg Victory", player, options) and state.has("Fountain Tartarus Item", player))
    
    #Upgrades of runs with gems locations
    set_rule(world.get_location("Pitch Black Darkness Location", player), lambda state:  \
            state.has("Deluxe Contractor Desk Item", player))
    set_rule(world.get_location("Fated Keys Location", player), lambda state:  \
            state.has("Deluxe Contractor Desk Item", player))
    set_rule(world.get_location("Brilliant Gemstones Location", player), lambda state:  \
            state.has("Deluxe Contractor Desk Item", player))
    set_rule(world.get_location("Vintage Nectar Location", player), lambda state:  \
            state.has("Deluxe Contractor Desk Item", player))
    set_rule(world.get_location("Darker Thirst Location", player), lambda state: \
            state.has("Deluxe Contractor Desk Item", player))
    

def set_fates_rules(world: "HadesWorld", player: int, location_table, options, subfix: str):
    #Rules that dont depend on other settings
    set_rule(world.get_location("Is There No Escape?" + subfix, player), lambda state: \
            state._has_defeated_boss("Hades Victory", player, options))
    set_rule(world.get_location("Harsh Conditions" + subfix, player), lambda state:  \
            state._has_defeated_boss("Hades Victory", player, options))
    set_rule(world.get_location("Slashed Benefits" + subfix, player), lambda state:  \
            state._has_defeated_boss("Hades Victory", player, options))
    set_rule(world.get_location("The Useless Trinket" + subfix, player), lambda state:  \
            state._has_defeated_boss("Hades Victory", player, options))
    set_rule(world.get_location("Wanton Ransacking" + subfix, player), lambda state:  \
            state._has_defeated_boss("Hades Victory", player, options))
    set_rule(world.get_location("Dark Reflections" + subfix, player), lambda state:  \
            state._has_defeated_boss("Hades Victory", player, options))

    #Rules that depend on storesanity
    if options.storesanity:
        set_rule(world.get_location("The Reluctant Musician" + subfix, player), lambda state:  \
                state.has("Court Musician Sentence Item", player))
        set_rule(world.get_location("Denizens Of The Deep" + subfix, player), lambda state:  \
                state._has_defeated_boss("Hades Victory", player, options) and state.has("Fishing Rod Item",player))
    else:
        set_rule(world.get_location("The Reluctant Musician" + subfix, player), lambda state:  \
                state._has_defeated_boss("Meg Victory", player, options))
        set_rule(world.get_location("Denizens Of The Deep" + subfix, player), lambda state: \
                state._has_defeated_boss("Hades Victory", player, options))
    #This part depends on weaponsanity, but the false option is handled on has_enough_weapons
    set_rule(world.get_location("Infernal Arms" + subfix, player), lambda state:  \
            state._has_enough_weapons(player, options, 6))
    set_rule(world.get_location("A Violent Past" + subfix, player), lambda state:  \
            state._has_enough_weapons(player, options, 6))
    set_rule(world.get_location("Master Of Arms" + subfix, player), lambda state:  \
            state._has_enough_weapons(player, options, 6) and  \
            state._has_defeated_boss("Hades Victory", player, options))
   
    #rules that depend on weaponsanity:
    if options.weaponsanity:
        set_rule(world.get_location("The Stygian Blade" + subfix, player), lambda state: \
                state.has("Sword Weapon Unlock Item", player) or options.initial_weapon == 0)
        set_rule(world.get_location("The Heart Seeking Bow" + subfix, player), lambda state: \
                state.has("Bow Weapon Unlock Item", player) or options.initial_weapon == 1)
        set_rule(world.get_location("The Eternal Spear" + subfix, player), lambda state: \
                state.has("Spear Weapon Unlock Item", player) or options.initial_weapon == 2)
        set_rule(world.get_location("The Shield Of Chaos" + subfix, player), lambda state: \
                state.has("Shield Weapon Unlock Item", player) or options.initial_weapon == 3)
        set_rule(world.get_location("The Twin Fists" + subfix, player), lambda state: \
                state.has("Fist Weapon Unlock Item", player) or options.initial_weapon == 4)
        set_rule(world.get_location("The Adamant Rail" + subfix, player), lambda state: \
                state.has("Gun Weapon Unlock Item", player) or options.initial_weapon == 5)
        
    if options.keepsakesanity:
        set_rule(world.get_location("Close At Heart" + subfix, player), lambda state: \
                state._has_enough_keepsakes(player, 23, options))
        #This is balancing rules, so grinding gods is less painful
        set_rule(world.get_location("Goddess Of Wisdom" + subfix, player), lambda state: \
                state.has("Athena Keepsake", player))
        set_rule(world.get_location("God Of The Heavens" + subfix, player), lambda state: \
                state.has("Zeus Keepsake", player))
        set_rule(world.get_location("God Of The Sea" + subfix, player), lambda state: \
                state.has("Poseidon Keepsake", player))
        set_rule(world.get_location("Goddess Of Love" + subfix, player), lambda state: \
                state.has("Aphrodite Keepsake", player))
        set_rule(world.get_location("God Of War" + subfix, player), lambda state: \
                state.has("Ares Keepsake", player))
        set_rule(world.get_location("Goddess Of The Hunt" + subfix, player), lambda state: \
                state.has("Artemis Keepsake", player))
        set_rule(world.get_location("God Of Wine" + subfix, player), lambda state: \
                state.has("Dionysus Keepsake", player))
        set_rule(world.get_location("God Of Swiftness" + subfix, player), lambda state: \
                state.has("Hermes Keepsake", player))
        set_rule(world.get_location("Goddess Of Seasons" + subfix, player), lambda state: \
                state.has("Demeter Keepsake", player))
        
        #Balancing rules
        #Put here a rule that you need to have all God keepsakes for the DivinePairis?
        set_rule(world.get_location("Primordial Boons" + subfix, player), lambda state: \
                state.has("Chaos Keepsake", player))
        set_rule(world.get_location("Primordial Banes" + subfix, player), lambda state: \
                state.has("Chaos Keepsake", player))
        
        #Balacing rules for DivinePairings
        add_rule(world.get_location("Divine Pairings" + subfix, player), lambda state: \
                state.has("Athena Keepsake", player))
        add_rule(world.get_location("Divine Pairings" + subfix, player), lambda state: \
                state.has("Zeus Keepsake", player))
        add_rule(world.get_location("Divine Pairings" + subfix, player), lambda state: \
                state.has("Poseidon Keepsake", player))
        add_rule(world.get_location("Divine Pairings" + subfix, player), lambda state: \
                state.has("Aphrodite Keepsake", player))
        add_rule(world.get_location("Divine Pairings" + subfix, player), lambda state: \
                state.has("Ares Keepsake", player))
        add_rule(world.get_location("Divine Pairings" + subfix, player), lambda state: \
                state.has("Artemis Keepsake", player))
        add_rule(world.get_location("Divine Pairings" + subfix, player), lambda state: \
                state.has("Dionysus Keepsake", player))
        add_rule(world.get_location("Divine Pairings" + subfix, player), lambda state: \
                state.has("Hermes Keepsake", player))
        add_rule(world.get_location("Divine Pairings" + subfix, player), lambda state: \
                state.has("Demeter Keepsake", player))

    # This is extra balancing rules to avoid fates being a pain in the butt
    add_rule(world.get_location("Primordial Boons" + subfix, player), lambda state: \
                state._has_defeated_boss("Lernie Victory", player, options))
    add_rule(world.get_location("Primordial Banes" + subfix, player), lambda state: \
                state._has_defeated_boss("Lernie Victory", player, options))
    
    set_rule(world.get_location("Power Without Equal" + subfix, player), lambda state: \
                state._has_defeated_boss("Bros Victory", player, options))
    add_rule(world.get_location("Divine Pairings" + subfix, player), lambda state: \
                state._has_defeated_boss("Lernie Victory", player, options))
        

def set_weapon_region_rules(world: "HadesWorld", player: int, number_items: int, 
                            location_table, options, weaponSubfix: str, total_routine_inspection: int):
    set_rule(world.get_entrance("Zags room " + weaponSubfix, player), lambda state: \
            state._has_weapon(weaponSubfix, player, options))
    set_rule(world.get_entrance("Exit Tartarus " + weaponSubfix, player), lambda state: \
            state.has("Meg Victory " + weaponSubfix, player) and \
            state._total_heat_level(player, min(number_items / 4, 10), options) and \
            state._has_enough_routine_inspection(player, total_routine_inspection - 2, options) and \
            state._has_enough_weapons(player, options, 2))
    set_rule(world.get_entrance("Exit Asphodel " + weaponSubfix, player), lambda state: \
            state.has("Lernie Victory " + weaponSubfix, player) and \
            state._total_heat_level(player, min(number_items / 2, 20), options) and \
            state._has_enough_routine_inspection(player, total_routine_inspection - 1, options) and \
            state._has_enough_weapons(player, options, 3))
    set_rule(world.get_entrance("Exit Elysium " + weaponSubfix, player), lambda state: \
            state.has("Bros Victory " + weaponSubfix, player)  and \
            state._total_heat_level(player, min(number_items * 3 / 4, 30), options) and \
            state._has_enough_routine_inspection(player, total_routine_inspection, options) and \
            state._has_enough_weapons(player, options, 5))
    set_rule(world.get_location("Beat Hades " + weaponSubfix, player), lambda state: \
            state._total_heat_level(player, min(number_items, 35), options) and \
            state._has_enough_weapons(player, options, 6))
    

def forbid_important_items_on_late_styx(world: "HadesWorld", player: int, options):
    if options.location_system == "room_weapon_based":
        for weaponString in location_weapons_subfixes:
                late_styx_region = world.get_region("Styx Late " + weaponString, player)
                for location in late_styx_region.locations:
                        add_item_rule(location,
                                lambda item: not item.advancement or item_is_plando(world, item, player))
    else:
        late_styx_region = world.get_region("Styx Late", player)
        for location in late_styx_region.locations:
                add_item_rule(location,
                        lambda item: not item.advancement or item_is_plando(world, item, player))
                

def item_is_plando(world: "HadesWorld", item: Item, player: int) -> bool:
    return item in world.plando_items[player]