from BaseClasses import MultiWorld
from worlds.AutoWorld import LogicMixin


class OracleOfSeasonsState(LogicMixin):
    tloz_oos_available_cuccos: dict[int, dict[str, tuple[int, int, int]]]

    def init_mixin(self, parent: MultiWorld):
        self.tloz_oos_available_cuccos = {player: None for player, world in parent.worlds.items()
                                          if parent.worlds[player].game == "The Legend of Zelda - Oracle of Seasons"}
