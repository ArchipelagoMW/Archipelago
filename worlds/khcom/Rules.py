from worlds.generic.Rules import add_rule, set_rule, forbid_item


def set_rules(self) -> None:
    set_rule(self.multiworld.get_entrance("Floor 1 Room of Beginnings", self.player), lambda state: state.has("Key of Beginnings F01", self.player))
    set_rule(self.multiworld.get_entrance("Floor 1 Room of Guidance", self.player), lambda state: state.has("Key of Guidance F01", self.player))
    set_rule(self.multiworld.get_entrance("Floor 1 Room of Truth", self.player), lambda state: state.has("Key to Truth F01", self.player))
    
    set_rule(self.multiworld.get_entrance("Floor 2 Room of Beginnings", self.player), lambda state: state.has("Key of Beginnings F02", self.player))
    set_rule(self.multiworld.get_entrance("Floor 2 Room of Guidance", self.player), lambda state: state.has("Key of Guidance F02", self.player))
    set_rule(self.multiworld.get_entrance("Floor 2 Room of Truth", self.player), lambda state: state.has("Key to Truth F02", self.player))
        
    set_rule(self.multiworld.get_entrance("Floor 3 Room of Beginnings", self.player), lambda state: state.has("Key of Beginnings F03", self.player))
    set_rule(self.multiworld.get_entrance("Floor 3 Room of Guidance", self.player), lambda state: state.has("Key of Guidance F03", self.player))
    set_rule(self.multiworld.get_entrance("Floor 3 Room of Truth", self.player), lambda state: state.has("Key to Truth F03", self.player))
    
    set_rule(self.multiworld.get_entrance("Floor 4 Room of Beginnings", self.player), lambda state: state.has("Key of Beginnings F04", self.player))
    set_rule(self.multiworld.get_entrance("Floor 4 Room of Guidance", self.player), lambda state: state.has("Key of Guidance F04", self.player))
    set_rule(self.multiworld.get_entrance("Floor 4 Room of Truth", self.player), lambda state: state.has("Key to Truth F04", self.player))
    
    set_rule(self.multiworld.get_entrance("Floor 5 Room of Beginnings", self.player), lambda state: state.has("Key of Beginnings F05", self.player))
    set_rule(self.multiworld.get_entrance("Floor 5 Room of Guidance", self.player), lambda state: state.has("Key of Guidance F05", self.player))
    set_rule(self.multiworld.get_entrance("Floor 5 Room of Truth", self.player), lambda state: state.has("Key to Truth F05", self.player))
    
    set_rule(self.multiworld.get_entrance("Floor 6 Room of Beginnings", self.player), lambda state: state.has("Key of Beginnings F06", self.player))
    set_rule(self.multiworld.get_entrance("Floor 6 Room of Guidance", self.player), lambda state: state.has("Key of Guidance F06", self.player))
    set_rule(self.multiworld.get_entrance("Floor 6 Room of Truth", self.player), lambda state: state.has("Key to Truth F06", self.player))
    
    set_rule(self.multiworld.get_entrance("Floor 7 Room of Beginnings", self.player), lambda state: state.has("Key of Beginnings F07", self.player))
    set_rule(self.multiworld.get_entrance("Floor 7 Room of Guidance", self.player), lambda state: state.has("Key of Guidance F07", self.player))
    set_rule(self.multiworld.get_entrance("Floor 7 Room of Truth", self.player), lambda state: state.has("Key to Truth F07", self.player))
    
    set_rule(self.multiworld.get_entrance("Floor 8 Room of Beginnings", self.player), lambda state: state.has("Key of Beginnings F08", self.player))
    set_rule(self.multiworld.get_entrance("Floor 8 Room of Guidance", self.player), lambda state: state.has("Key of Guidance F08", self.player))
    set_rule(self.multiworld.get_entrance("Floor 8 Room of Truth", self.player), lambda state: state.has("Key to Truth F08", self.player))
    
    set_rule(self.multiworld.get_entrance("Floor 9 Room of Beginnings", self.player), lambda state: state.has("Key of Beginnings F09", self.player))
    set_rule(self.multiworld.get_entrance("Floor 9 Room of Guidance", self.player), lambda state: state.has("Key of Guidance F09", self.player))
    set_rule(self.multiworld.get_entrance("Floor 9 Room of Truth", self.player), lambda state: state.has("Key to Truth F09", self.player))
    
    set_rule(self.multiworld.get_entrance("Floor 11 Room of Beginnings", self.player), lambda state: state.has("Key of Beginnings F11", self.player))
    
    set_rule(self.multiworld.get_entrance("Floor 12 Room of Beginnings", self.player), lambda state: state.has("Key of Beginnings F12", self.player))
    set_rule(self.multiworld.get_entrance("Floor 12 Room of Guidance", self.player), lambda state: state.has("Key of Guidance F12", self.player))
    
    set_rule(self.multiworld.get_entrance("Floor 13 Room of Beginnings", self.player), lambda state: state.has("Key of Beginnings F13", self.player))
    set_rule(self.multiworld.get_entrance("Floor 13 Room of Guidance", self.player), lambda state: state.has("Key of Guidance F13", self.player))
    set_rule(self.multiworld.get_entrance("Floor 13 Room of Truth", self.player), lambda state: state.has("Key to Truth F13", self.player))