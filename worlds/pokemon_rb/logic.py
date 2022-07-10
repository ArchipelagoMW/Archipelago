from ..AutoWorld import LogicMixin


class PokemonLogic(LogicMixin):
    def _pokemon_rb_can_surf(self, player):
        return (self.has("HM03 Surf", player) or self.has("Flippers", player)) and self.has("Soul Badge", player) and self.has("Super Rod", player)

    def _pokemon_rb_can_cut(self, player):
        return (self.has("HM01 Cut", player) or self.has("Master Sword", player)) and self.has("Cascade Badge", player)

    def _pokemon_rb_can_fly(self, player):
        return (self.has("HM02 Fly", player) or self.has("Flute", player)) and self.has("Thunder Badge", player)

    def _pokemon_rb_can_strength(self, player):
        return (self.has("HM04 Strength", player) or self.has("Titan's Mitt", player)) and self.has("Rainbow Badge", player)

    def _pokemon_rb_can_flash(self, player):
        return (self.has("HM05 Flash", player) or self.has("Lamp", player)) and self.has("Boulder Badge", player)

    def _pokemon_rb_can_get_hidden_items(self, player):
        return self.has("Item Finder", player)

    def _pokemon_rb_can_pass_guards(self, player):
        if self.world.routing[player]:
            return self.has("Tea", player)
        #return self.world.get_location("Celadon City - Thirsty Girl Gets Water", player).can_reach(self)
        return self.can_reach(self.word.get_location("Celadon City - Thirsty Girl Gets Water", player))

    def _pokemon_rb_has_badges(self, count, player):
        return (self.has("Boulder Badge", player) + self.has("Cascade Badge", player)
                  + self.has("Thunder Badge", player) + self.has("Rainbow Badge", player)
                  + self.has("Marsh Badge", player) + self.has("Soul Badge", player)
                  + self.has("Volcano Badge", player) + self.has("Earth Badge", player)) >= count
