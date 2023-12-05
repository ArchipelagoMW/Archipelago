from BaseClasses import MultiWorld
from worlds.AutoWorld import LogicMixin


class MetroidPrimeLogic(LogicMixin):
    def _prime_has_missiles(self, world: MultiWorld, player: int) -> bool:
        return self.has_any({'Missile Launcher', 'Missile Expansion'}, player)

    def _prime_has_missile_count(self, world: MultiWorld, player: int) -> int:
        count = 0
        if self.has({'Missile Launcher'}, player):
            count = 1
        count += self.prog_items['Missile Expansion', player] * 5
        return count

    def _prime_can_bomb(self, world: MultiWorld, player: int) -> bool:
        return self.has({'Morph Ball', 'Morph Ball Bombs'})

    def _prime_can_boost(self, world: MultiWorld, player: int) -> bool:
        return self.has({'Morph Ball', 'Boost Ball'})

    def _prime_can_spider(self, world: MultiWorld, player: int) -> bool:
        return self.has({'Morph Ball', 'Spider Ball'})

    def _prime_can_pb(self, world: MultiWorld, player: int) -> bool:
        return self.has({'Morph Ball', 'Power Bomb'})

    def _prime_can_super(self, world: MultiWorld, player: int) -> bool:
        return self._prime_has_missiles(world, player) and self.has({'Charge Beam', 'Super Missile'})
