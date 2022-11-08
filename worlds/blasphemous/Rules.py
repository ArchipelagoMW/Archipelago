from worlds.generic.Rules import add_rule
from ..AutoWorld import LogicMixin


class BlasphemousLogic(LogicMixin):
    def _blasphemous_blood_relic(self, player):
        return self.has("Blood Perpetuated in Sand", player)

    def _blasphemous_water_relic(self, player):
        return self.has("Nail Uprooted from Dirt", player)

    def _blasphemous_corpse_relic(self, player):
        return self.has("Shroud of Dreamt Sins", player)

    def _blasphemous_fall_relic(self, player):
        return self.has("Linen of Golden Thread", player)

    def _blasphemous_miasma_relic(self, player):
        return self.has("Silvered Lung of Dolphos", player)
    
    def _blasphemous_root_relic(self, player):
        return self.has("Three Gnarled Tongues", player)

    def _blasphemous_qi_cloth(self, player):
        return self.has("Linen Cloth", player)

    def _blasphemous_qi_egg(self, player):
        return self.has_group("egg", player, 3)

    def _blasphemous_qi_hand(self, player):
        return self.has("Severed Hand", player)

    def _blasphemous_tirso_1(self, player):
        return self.has_group("tirso", player, 1)
    
    def _blasphemous_tirso_2(self, player):
        return self.has_group("tirso", player, 2)

    def _blasphemous_tirso_3(self, player):
        return self.has_group("tirso", player, 3)

    def _blasphemous_tirso_4(self, player):
        return self.has_group("tirso", player, 4)

    def _blasphemous_tirso_5(self, player):
        return self.has_group("tirso", player, 5)

    def _blasphemous_tirso_6(self, player):
        return self.has_group("tirso", player, 6)

    def _blasphemous_tentudia_1(self, player):
        return self.has_group("tentudia", player, 1)

    def _blasphemous_tentudia_2(self, player):
        return self.has_group("tentudia", player, 2)

    def _blasphemous_tentudia_3(self, player):
        return self.has_group("tentudia", player, 3)

def rules(blasphemousworld):
    world = blasphemousworld.multiworld
    player = blasphemousworld.player

    # entrances
    for i in world.get_region("Deambulatory of His Holiness", player).entrances:
        add_rule(i, lambda state: state._blasphemous_3_masks(player))
    for i in world.get_region("Ferrous Tree", player).entrances:
        add_rule(i, lambda state: state._blasphemous_3_wounds(player))
    for i in world.get_region("Hall of the Dawning", player).entrances:
        add_rule(i, lambda state: state._blasphemous_3_wounds(player))
    for i in world.get_region("Mourning and Havoc", player).entrances:
        add_rule(i, lambda state: state._blasphemous_blood_relic(player) or state.can_reach("Mother of Mothers"))
    for i in world.get_region("Patio of the Silent Steps", player).entrances:
        add_rule(i, lambda state: state._blasphemous_3_wounds(player))
    for i in world.get_region("The Resting Place of the Sister", player).entrances:
        add_rule(i, lambda state: state._blasphemous_blood_relic(player))
    for i in world.get_region("The Sleeping Canvases", player).entrances:
        add_rule(i, lambda state: state._blasphemous_3_wounds(player))
    for i in world.get_region("Wall of the Holy Prohibitions", player).entrances:
        add_rule(i, lambda state: state._blasphemous_1_mask(player))