from ..AutoWorld import LogicMixin


class PokemonLogic(LogicMixin):
    def _pokemon_rb_can_surf(self, player):
        return (((self.has("HM03 Surf", player) and self.has("Super Rod", player)) or self.has("Flippers", player)) and
                (self.has("Soul Badge", player) or self.has(self.world.worlds[player].extra_badges.get("Surf"), player)
                 or self.world.badges_needed_for_hm_moves[player].value == 0))

    def _pokemon_rb_can_cut(self, player):
        return (self.has("HM01 Cut", player) or self.has("Master Sword", player)) and (self.has("Cascade Badge", player)
                or self.has(self.world.worlds[player].extra_badges.get("Cut"), player) or
                self.world.badges_needed_for_hm_moves[player].value == 0)

    def _pokemon_rb_can_fly(self, player):
        return (self.has("HM02 Fly", player) or self.has("Flute", player)) and (self.has("Thunder Badge", player) or
                self.has(self.world.worlds[player].extra_badges.get("Fly"), player) or
                self.world.badges_needed_for_hm_moves[player].value == 0)

    def _pokemon_rb_can_strength(self, player):
        return (self.has("HM04 Strength", player) or self.has("Titan's Mitt", player)) and\
               (self.has("Rainbow Badge", player) or self.has(self.world.worlds[player].extra_badges.get("Strength"), player)
                or self.world.badges_needed_for_hm_moves[player].value == 0)

    def _pokemon_rb_can_flash(self, player):
        return (self.has("HM05 Flash", player) or self.has("Lamp", player)) and (self.has("Boulder Badge", player) or
                self.has(self.world.worlds[player].extra_badges.get("Flash"), player) or self.world.badges_needed_for_hm_moves[player].value == 0)

    def _pokemon_rb_can_get_hidden_items(self, player):
        return self.has("Item Finder", player)

    def _pokemon_rb_cerulean_cave(self, count, player):
        ret = (self.can_reach("Pewter Gym", player=player) + self.can_reach("Cerulean Gym", player=player)
               + self.can_reach("Vermilion Gym", player=player) + self.can_reach("Celadon Gym", player=player)
               + self.can_reach("Saffron Gym", player=player) + self.can_reach("Fuchsia Gym", player=player)
               + self.can_reach("Cinnabar Gym", player=player) + self.can_reach("Viridian Gym", player=player)
               + self.has("Boulder Badge", player) + self.has("Cascade Badge", player) + self.has("Thunder Badge",
                                                                                                  player)
               + self.has("Rainbow Badge", player) + self.has("Soul Badge", player) + self.has("Marsh Badge", player)
               + self.has("Volcano Badge", player) + self.has("Earth Badge", player)
               + self.has("Bicycle", player) + self.has("Silph Scope", player)
               + self.has("Item Finder", player) + self.has("Super Rod", player) + self.has("Good Rod", player)
               + self.has("Old Rod", player) + self.has("Lift Key", player) + self.has("Card Key", player)
               + self.has("Town Map", player) + self.has("Coin Case", player) + self.has("S.S. Ticket", player))
        if self.world.extra_key_items[player].value:
            return (ret + self.has("Secret Key", player) + self.has("Mansion Key", player)
                    + self.has("Safari Pass", player) + self.has("Plant Key", player)
                    + self.has("Hideout Key", player)) >= count
        return (ret + self.has("HM01 Cut", player) + self.has("HM02 Fly", player) + self.has("HM03 Surf")
                + self.has("HM04 Strength", player) + self.has("HM05 Flash", player)) >= count

    def _pokemon_rb_can_pass_guards(self, player):
        return self.has("Tea", player)

    def _pokemon_rb_has_badges(self, count, player):
        return (self.has("Boulder Badge", player) + self.has("Cascade Badge", player)
                + self.has("Thunder Badge", player) + self.has("Rainbow Badge", player)
                + self.has("Marsh Badge", player) + self.has("Soul Badge", player)
                + self.has("Volcano Badge", player) + self.has("Earth Badge", player)) >= count
