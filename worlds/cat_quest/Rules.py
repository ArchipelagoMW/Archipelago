from worlds.generic.Rules import add_rule

def create_rules(self, locations):
    multiworld = self.multiworld
    player = self.player

    for loc in locations:
        if loc["art"] == "water":
            add_rule(multiworld.get_location(loc["name"], player),
            lambda state: state.has("Royal Art of Water Walking", player))
        elif loc["art"] == "flight":
            add_rule(multiworld.get_location(loc["name"], player),
            lambda state: state.has("Royal Art of Flight", player))
        elif loc["art"] == "both":
            add_rule(multiworld.get_location(loc["name"], player),
            lambda state: state.has("Royal Art of Flight", player) and state.has("Royal Art of Water Walking", player))
        elif loc["art"] == "either":
            add_rule(multiworld.get_location(loc["name"], player),
            lambda state: state.has("Royal Art of Flight", player) or state.has("Royal Art of Water Walking", player))
        
        if loc["hasFist"] == True:
            add_rule(multiworld.get_location(loc["name"], player),
            lambda state: state.has("Flamepurr", player) or state.has("Lightnyan", player) or state.has("Freezepaw", player) or state.has("Cattrap", player) or state.has("Astropaw", player))
