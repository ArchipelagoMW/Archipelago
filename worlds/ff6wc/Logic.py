from worlds.AutoWorld import LogicMixin, World
from worlds.ff6wc import Locations
from worlds.ff6wc.Locations import dragons


class LogicFunctions(LogicMixin):
    def _ff6wc_has_enough_characters(self, world, player):
        return self.has_group("characters", player, world.CharacterCount[player])

    def _ff6wc_has_enough_espers(self, world, player):
        return self.has_group("espers", player, world.CharacterCount[player])

    def _ff6wc_has_enough_dragons(self, world, player):
        return self.has_group("dragons", player, world.DragonCount[player])

    def _ff6wc_has_terra(self, player):
        return self.has("TERRA", player)

    def _ff6wc_has_locke(self, player):
        return self.has("LOCKE", player)

    def _ff6wc_has_cyan(self, player):
        return self.has("CYAN", player)

    def _ff6wc_has_shadow(self, player):
        return self.has("SHADOW", player)

    def _ff6wc_has_edgar(self, player):
        return self.has("EDGAR", player)

    def _ff6wc_has_sabin(self, player):
        return self.has("SABIN", player)

    def _ff6wc_has_celes(self, player):
        return self.has("CELES", player)

    def _ff6wc_has_strago(self, player):
        return self.has("STRAGO", player)

    def _ff6wc_has_relm(self, player):
        return self.has("RELM", player)

    def _ff6wc_has_setzer(self, player):
        return self.has("SETZER", player)

    def _ff6wc_has_mog(self, player):
        return self.has("MOG", player)

    def _ff6wc_has_gau(self, player):
        return self.has("GAU", player)

    def _ff6wc_has_gogo(self, player):
        return self.has("GOGO", player)

    def _ff6wc_has_umaro(self, player):
        return self.has("UMARO", player)