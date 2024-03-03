from BaseClasses import MultiWorld
from worlds.AutoWorld import LogicMixin
from .Items import artifact_table


class MetroidPrimeLogic(LogicMixin):

    # logic rules related to needing a combination of items
    def prime_has_missiles(self, world: MultiWorld, player: int) -> bool:
        return self.has_any({'Main Missile', 'Missile Expansion'}, player)

    def prime_has_missile_count(self, world: MultiWorld, player: int) -> int:
        count = 0
        if self.has('Main Missile', player):
            count = 5
        count += self.count('Missile Expansion', player) * 5
        return count

    def prime_artifact_count(self, world: MultiWorld, player: int) -> int:
        count = 0
        for i in artifact_table.keys():
            if self.has(i, player):
                count += 1
        return count

    def prime_etank_count(self, world: MultiWorld, player: int) -> int:
        count = 0
        count += self.count('Energy Tank', player)
        return count

    def prime_can_bomb(self, world: MultiWorld, player: int) -> bool:
        return self.has_all({'Morph Ball', 'Morph Ball Bombs'}, player)

    def prime_can_boost(self, world: MultiWorld, player: int) -> bool:
        return self.has_all({'Morph Ball', 'Boost Ball'}, player)

    def prime_can_spider(self, world: MultiWorld, player: int) -> bool:
        return self.has_all({'Morph Ball', 'Spider Ball'}, player)

    def prime_can_pb(self, world: MultiWorld, player: int) -> bool:
        return self.has('Morph Ball', player) and self.has_any({'Power Bomb', 'Power Bomb Expansion'}, player)

    def prime_can_super(self, world: MultiWorld, player: int) -> bool:
        return self.prime_has_missiles(world, player) and self.has_all({'Charge Beam', 'Super Missile'}, player)

    def prime_can_heat(self, world: MultiWorld, player: int) -> bool:
        return self.has_any({'Varia Suit', 'Gravity Suit', 'Phazon Suit'}, player)

    # logic rules related to accessing regions or subregions

    def prime_late_chozo(self, world: MultiWorld, player: int) -> bool:
        return (self.prime_has_missiles(world, player) and self.prime_can_bomb(world, player) and
                self.prime_can_spider(world, player) and
                ((self.has('Wave Beam', player) and self.prime_can_boost(world, player)) or
                 self.has_all({'Ice Beam', 'Space Jump Boots'}, player)))

    def prime_reflecting_pool(self, world: MultiWorld, player: int) -> bool:
        return (self.prime_late_chozo(world, player) and self.prime_can_boost(world, player) and
                self.has_all({'Space Jump Boots', 'Wave Beam'}, player))

    def prime_frigate(self, world: MultiWorld, player: int) -> bool:
        return (self.prime_has_missiles(world, player) and
                self.has_all({'Morph Ball', 'Space Jump Boots', 'Ice Beam', 'Wave Beam',
                              'Gravity Suit', 'Thermal Visor'}, player))

    def prime_magma_pool(self, world: MultiWorld, player: int) -> bool:
        return self.prime_can_heat(world, player) and self.has('Grapple Beam', player)

    def prime_tower_of_light(self, world: MultiWorld, player: int) -> bool:
        return (self.prime_has_missiles(world, player) and self.prime_can_boost(world, player) and
                self.prime_can_spider(world, player) and self.has_all({'Wave Beam', 'Space Jump Boots'}, player))

    def prime_early_magmoor(self, world: MultiWorld, player: int) -> bool:
        return (self.prime_can_heat(world, player) and self.prime_has_missiles(world, player)
                and self.has('Morph Ball', player) and (self.has('Grapple Beam', player) or
                                                        (self.prime_can_bomb(world, player) or
                                                         self.prime_can_pb(world, player))))

    def prime_late_magmoor(self, world: MultiWorld, player: int) -> bool:
        # through early magmoor
        return ((self.prime_can_heat(world, player) and self.prime_has_missiles(world, player)
                 and self.prime_can_spider(world, player) and self.has_all({'Wave Beam', 'Space Jump Boots'}, player))
                # from mines via tallon
                or (self.prime_frigate(world, player) and self.prime_can_bomb(world, player) and
                    self.prime_can_pb(world, player) and self.prime_can_spider(world, player)))

    def prime_front_phen(self, world: MultiWorld, player: int) -> bool:
        # from early magmoor to shorelines elevator
        return ((self.prime_early_magmoor(world, player) and self.prime_can_bomb(world, player))
                # backwards from quarantine cave
                or (self.prime_late_magmoor(world, player) and self.prime_can_bomb(world, player)
                    and self.prime_can_spider(world, player) and self.has_all({'Thermal Visor', 'Wave Beam'}, player)))

    # basically just ruined courtyard
    def prime_middle_phen(self, world: MultiWorld, player: int) -> bool:
        return (self.prime_front_phen(world, player) and self.has_all({'Space Jump Boots', 'Wave Beam'}, player) and
                ((self.prime_can_bomb(world, player) and self.prime_can_boost(world, player)) or
                 self.prime_can_spider(world, player)))

    def prime_quarantine_cave(self, world: MultiWorld, player: int) -> bool:
        # from ruined courtyard
        return ((self.prime_middle_phen(world, player) and self.prime_can_super(world, player) and
                 self.has('Thermal Visor', player))
                # from late magmoor
                or (self.prime_late_magmoor(world, player) and self.prime_can_bomb(world, player)))

    def prime_far_phen(self, world: MultiWorld, player: int) -> bool:
        return (self.prime_middle_phen(world, player) and self.has('Ice Beam', player) and
                # from labs
                ((self.prime_can_bomb(world, player) and self.has_all({'Boost Ball', 'Space Jump Boots'}, player)) or
                 # from late magmoor elevator
                 (self.prime_can_spider(world, player) and self.prime_can_super(world, player) and
                  self.has('Thermal Visor', player))))

    def prime_labs(self, world: MultiWorld, player: int) -> bool:
        return (self.prime_middle_phen(world, player) and self.prime_can_bomb(world, player)
                and self.has_all({'Boost Ball', 'Space Jump Boots'}, player))
        # or self._prime_far_phen(world, player)     [reverse labs]

    def prime_upper_mines(self, world: MultiWorld, player: int) -> bool:
        # from main quarry via tallon
        return ((self.prime_frigate(world, player) and self.prime_can_bomb(world, player)) or
                # from PPC via magmoor
                (self.prime_late_magmoor(world, player) and self.prime_can_bomb(world, player)
                 and self.prime_can_pb(world, player) and self.has_all({'Spider Ball', 'Ice Beam'}, player)))

    # should also cover reverse lower mines since upper mines can logically expect magmoor elevator
    def prime_lower_mines(self, world: MultiWorld, player: int) -> bool:
        return (self.prime_upper_mines(world, player) and self.prime_can_pb(world, player) and
                self.has_all({'Morph Ball Bombs', 'Boost Ball', 'Spider Ball', 'Plasma Beam',
                              'X-Ray Visor', 'Grapple Beam'}, player))
