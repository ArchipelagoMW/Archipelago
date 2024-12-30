from worlds.generic.Rules import add_rule

def create_rules(self, locations):
    multiworld = self.multiworld
    player = self.player

    for loc in locations:
        if loc["art"] == "water":
            add_rule(multiworld.get_location(loc.name, player),
            lambda state: state.has("Royal Art of Water Walking", player))
        elif loc["art"] == "flight":
            add_rule(multiworld.get_location(loc.name, player),
            lambda state: state.has("Royal Art of Flight", player))
