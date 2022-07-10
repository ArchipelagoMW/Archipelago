from ..AutoWorld import LogicMixin
from .Regions import ALttpRegion
from .Options import smallkey_shuffle
from .Bosses import can_beat_ganon


class ALttPLogic(LogicMixin):

    def lttp_has_key(self, item, player, count: int = 1):
        if self.world.worlds[player].logic == 'nologic':
            return True
        if self.world.worlds[player].smallkey_shuffle == smallkey_shuffle.option_universal:
            return self.lttp_can_buy_unlimited('Small Key (Universal)', player)
        return self.has(item, player, count)

    def lttp_has_misery_mire_medallion(self, player: int) -> bool:
        return self.has(self.world.required_medallions[player][0], player)

    def lttp_has_turtle_rock_medallion(self, player: int) -> bool:
        return self.has(self.world.required_medallions[player][1], player)

    def lttp_has_triforce_pieces(self, count: int, player: int) -> bool:
        return self.item_count('Triforce Piece', player) >= count

    def lttp_has_crystals(self, count: int, player: int) -> bool:
        found: int = 0
        for crystal in range(7):
            found += self.prog_items[f'Crystal {crystal + 1}', player]
        return found >= count

    def lttp_can_lift_rocks(self, player: int, count: int = 1) -> bool:
        return self.count_group('Gloves', player) >= count

    def lttp_bottle_count(self, player: int) -> int:
        return min(self.world.difficulty_requirements[player].progressive_bottle_limit, self.count_group('Bottles', player))

    def lttp_has_hearts(self, player: int, count: int) -> int:
        return self._lttp_heart_count(player) >= count

    def _lttp_heart_count(self, player: int) -> int:
        diff = self.world.difficulty_requirements[player]
        boss = min(self.count('Boss Heart Container', player), diff.boss_heart_container_limit)
        pieces = min(self.count('Piece of Heart', player), diff.heart_piece_limit) // 4
        count = boss + pieces + self.count('Sanctuary Heart Container', player) + 3
        return count

    def lttp_can_extend_magic(self, player: int, small_magic: int = 16, full_refill: bool = False) -> bool:
        base_magic = 8
        if self.has('Magic Upgrade (1/4)', player):
            base_magic = 32
        elif self.has('Magic Upgrade (1/2)', player):
            base_magic = 16
        if self.lttp_can_buy_unlimited('Green Potion', player) or self.lttp_can_buy_unlimited('Blue Potion', player):
            if self.world.item_functionality == 'hard' and not full_refill:
                base_magic = base_magic + int(base_magic * 0.5 * self.lttp_bottle_count(player))
            elif self.world.item_functionality == 'expert' and not full_refill:
                base_magic = base_magic + int(base_magic * 0.25 * self.lttp_bottle_count(player))
            else:
                base_magic = base_magic + base_magic * self.lttp_bottle_count(player)
        return base_magic >= small_magic

    def lttp_can_kill_most_things(self, player: int, enemies: int = 5) -> bool:
        return self.has_any({'Cane of Somaria', 'Fire Rod'}, player) or \
               (self.has('Cane of Byrna', player) and (enemies < 6 or self.lttp_can_extend_magic(player))) or \
               (self.has('Bombs (10)', player) and enemies < 6) or \
            self.lttp_has_melee_weapon(player) or self.lttp_can_shoot_arrows(player)

    def lttp_can_shoot_arrows(self, player: int) -> bool:
        has_bow = self.has_any({'Bow', 'Silver Bow'}, player)
        if self.world.worlds[player].retro:
            return has_bow and self.lttp_can_buy('Single Arrow', player)
        return has_bow

    def lttp_can_get_good_bee(self, player: int) -> bool:
        cave = self.world.get_region('Good Bee Cave', player)
        return (
            self.has_group('Bottles', player) and self.has('Bug Catching Net', player) and
            (self.has('Pegasus Boots', player) or (self.lttp_has_swords(player) and self.has('Quake', player))) and
            cave.can_reach(self) and self.lttp_is_not_bunny(cave, player)
        )

    def lttp_can_retrieve_tablet(self, player: int) -> bool:
        return self.has('Book of Mudora', player) and \
               (self.lttp_has_swords(player, 2) or
                (self.world.swordless and self.has('Hammer', player)))

    def lttp_has_swords(self, player: int, count: int = 1) -> bool:
        if count == 4:
            return self.has('Golden Sword', player) or self.has('Progressive Sword', player, 4)
        if count == 3:
            return self.has_any({'Tempered Sword', 'Golden Sword'}, player) or self.has('Progressive Sword', player, 3)
        if count == 2:
            return self.has_any({'Master Sword', 'Tempered Sword', 'Golden Sword'}, player) or self.has('Progressive Sword', player, 2)
        return self.has_group('Swords', player)

    def lttp_has_melee_weapon(self, player: int) -> bool:
        return self.lttp_has_swords(player) or self.has('Hammer', player)

    def lttp_has_fire(self, player: int) -> bool:
        return self.has_any({'Fire Rod', 'Lamp'}, player)

    def lttp_can_melt_things(self, player: int) -> bool:
        return self.has('Fire Rod', player) or \
               (self.has('Bombos', player) and
                (self.world.swordless or self.lttp_has_swords(player)))

    def lttp_can_avoid_lasers(self, player: int) -> bool:
        return self.has_any({'Mirror Shield', 'Cane of Byrna', 'Cape'}, player)

    def lttp_is_not_bunny(self, region: ALttpRegion, player: int) -> bool:
        if self.has('Moon Pearl', player):
            return True
        if self.world.worlds[player].mode != 'inverted':
            return region.is_light_world
        else:
            return region.is_dark_world

    def lttp_can_buy(self, item: str, player: int) -> bool:
        return any(shop.has(item) and shop.region.can_reach(self) for shop in self.world.shops)

    def lttp_can_buy_unlimited(self, item: str, player: int) -> bool:
        return any(shop.has_unlimited(item) and shop.region.can_reach(self) for shop in self.world.shops)

    def lttp_can_beat_ganon(self, player: int) -> bool:
        return can_beat_ganon(self, player)


    # glitched rules
    def lttp_can_boots_clip_lw(self, player: int) -> bool:
        if self.world.worlds[player].mode == 'inverted':
            return self.has_all({'Pegasus Boots', 'Moon Pearl'}, player)
        return self.has('Pegasus Boots', player)

    def lttp_can_boots_clip_dw(self, player: int) -> bool:
        if self.world.worlds[player].mode != 'inverted':
            return self.has_all({'Pegasus Boots', 'Moon Pearl'}, player)
        return self.has('Pegasus Boots', player)

    def lttp_can_get_glitched_speed_lw(self, player: int) -> bool:
        rules = self.has_all({'Pegasus Boots', 'Hookshot'}, player) and self.lttp_has_swords(player)
        if self.world.worlds[player].mode == 'inverted':
            return rules and self.has('Moon Pearl', player)
        return rules

    def lttp_can_get_glitched_speed_dw(self, player: int) -> bool:
        rules = self.has_all({'Pegasus Boots', 'Hookshot'}, player) and self.lttp_has_swords(player)
        if self.world.worlds[player].mode != 'inverted':
            return rules and self.has('Moon Pearl', player)
        return rules

    def lttp_can_superbunny_mirror_with_sword(self, player: int) -> bool:
        return self.has('Magic Mirror', player) and self.lttp_has_swords(player)

    def lttp_can_bomb_clip(self, region: ALttpRegion, player: int) -> bool:
        return self.lttp_is_not_bunny(region, player) and self.has('Pegasus Boots', player)

