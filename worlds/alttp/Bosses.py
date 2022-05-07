from typing import Callable, Optional, NamedTuple

from Fill import FillError


# TODO some of the different shuffles can be rewritten as proper functions and figure out what ';' is
class Boss(NamedTuple):
    """Class to handle necessary information for each boss."""
    # TODO look into how names are handled and see about eliminating enemizer_name variable
    name: str
    enemizer_name: str
    defeat_rule: Callable
    player: int

    def can_defeat(self, state) -> bool:
        return self.defeat_rule(state, self.player)

    def __repr__(self):
        return f"Boss({self.name})"


def boss_factory(boss: str, player: int) -> Optional[Boss]:
    if boss in boss_table:
        enemizer_name, defeat_rule = boss_table[boss]
        return Boss(boss, enemizer_name, defeat_rule, player)


def can_beat_armos(state, player: int):
    return (
            state.has_melee_weapon(player) or
            state.can_shoot_arrows(player) or
            (state.has('Cane of Somaria', player) and state.can_extend_magic(player, 10)) or
            (state.has('Cane of Byrna', player) and state.can_extend_magic(player, 16)) or
            (state.has('Ice Rod', player) and state.can_extend_magic(player, 32)) or
            (state.has('Fire Rod', player) and state.can_extend_magic(player, 32)) or
            state.has('Blue Boomerang', player) or
            state.has('Red Boomerang', player)
    )


def can_beat_lanmo(state, player: int):
    return (
            state.has_melee_weapon(player) or
            state.has('Fire Rod', player) or
            state.has('Ice Rod', player) or
            state.has('Cane of Somaria', player) or
            state.has('Cane of Byrna', player) or
            state.can_shoot_arrows(player)
    )


def can_beat_moldorm(state, player: int):
    return state.has_melee_weapon(player)


def can_beat_helma(state, player: int):
    return state.has_sword(player, 1) or state.can_shoot_arrows(player) or (
        state.has_hammer(player) if logic_trick.hamdorm[player] else False)


def can_beat_arrghus(state, player: int):
    if not state.has('Hookshot', player):
        return False
    if state.has_melee_weapon(player):
        return True
    return (
            (state.has('Fire Rod', player) and
             (state.can_shoot_arrows(player) or state.can_extend_magic(player, 12))) or
            (state.has('Ice Rod', player) and (state.can_shoot_arrows(player) or state.can_extend_magic(player, 16)))
    )


def can_beat_mothula(state, player: int):
    return (
            state.has_melee_weapon(player) or
            (state.has('Fire Rod', player) and state.can_extend_magic(player, 10)) or
            # TODO: Not sure how much (if any) extend magic is needed for these two, since they only apply
            # to non-vanilla locations, so are harder to test, so sticking with what VT has for now:
            (state.has('Cane of Somaria', player) and state.can_extend_magic(player, 16)) or
            (state.has('Cane of Byrna', player) and state.can_extend_magic(player, 16)) or
            state.can_get_good_bee(player)
    )


def can_beat_blind(state, player: int):
    return state.has_melee_weapon(player) or state.has('Cane of Somaria', player) or state.has('Cane of Byrna', player)


def can_beat_kholdstare(state, player: int):
    return (
            (
                    state.has('Fire Rod', player) or
                    (
                            state.has('Bombos', player) and
                            (
                                    state.has_sword(player, 1) or state.world.swordless[player]
                            )
                    )
            ) and
            (
                    state.has_melee_weapon(player) or
                    (
                            state.has('Fire Rod', player) and
                            state.can_extend_magic(player, 20)
                    ) or
                    (
                            state.has('Fire Rod', player) and
                            state.has('Bombos', player) and
                            state.world.swordless[player] and
                            state.can_extend_magic(player, 16)
                    )
            )
    )


def can_beat_vitreous(state, player: int):
    return state.can_shoot_arrows(player) or state.has_melee_weapon(player)


def can_beat_trinexx(state, player: int):
    if not (state.has('Fire Rod', player) and state.has('Ice Rod', player)):
        return False

    return state.has('Hammer', player) or state.has_sword(player, 3) or \
        (state.has_sword(player, 2) and state.can_extend_magic(player, 16)) or \
        (state.has_sword(player, 1) and state.can_extend_magic(player, 32))


def can_beat_agahnim(state, player: int):
    return state.has_sword(player, 1) or state.has('Hammer', player) or state.has('Bug Catching Net', player)


def can_beat_ganon(state, player: int):
    if state.world.swordless[player]:
        return state.has('Hammer', player) and state.has_fire_source(player) and \
               state.has('Silver Bow', player) and state.can_shoot_arrows(player)

    can_hurt = state.has_sword(player, 2)
    common = can_hurt and state.has_fire_source(player)
    if state.world.logic[player] != 'noglitches':
        return common and (state.has_sword(player, 3) or
                           (state.has('Silver Bow', player) and state.can_shoot_arrows(player)) or
                           state.has('Lamp', player) or
                           state.can_extend_magic(player, 12))

    else:
        return common and state.has('Silver Bow', player) and state.can_shoot_arrows(player)


boss_table = {
    'Armos Knights': ('Armos', can_beat_armos),
    'Lanmolas': ('Lanmola', can_beat_lanmo),
    'Moldorm': ('Moldorm', can_beat_moldorm),
    'Helmasaur King': ('Helmasaur', can_beat_helma),
    'Arrghus': ('Arrghus', can_beat_arrghus),
    'Mothula': ('Mothula', can_beat_mothula),
    'Blind': ('Blind', can_beat_blind),
    'Kholdstare': ('Kholdstare', can_beat_kholdstare),
    'Vitreous': ('Vitreous', can_beat_vitreous),
    'Trinexx': ('Trinexx', can_beat_trinexx),
    'Agahnim': ('Agahnim', can_beat_agahnim),
    'Agahnim 2': ('Agahnim 2', can_beat_agahnim)
}

boss_location_table = [
    ('Ganons Tower', 'top'),
    ('Tower of Hera', None),
    ('Skull Woods', None),
    ('Ganons Tower', 'middle'),
    ('Eastern Palace', None),
    ('Desert Palace', None),
    ('Palace of Darkness', None),
    ('Swamp Palace', None),
    ('Thieves Town', None),
    ('Ice Palace', None),
    ('Misery Mire', None),
    ('Turtle Rock', None),
    ('Ganons Tower', 'bottom')
]


def can_place_boss(boss: str, dungeon_name: str, level: Optional[str] = None) -> bool:
    # blacklist
    if boss in {'Agahnim', 'Agahnim 2', 'Ganon'}:
        return False

    if dungeon_name == 'Ganons Tower':
        if level == 'top':
            if boss in {'Armos Knights', 'Arrghus', 'Blind', 'Trinexx', 'Lanmolas'}:
                return False
        elif level == 'middle':
            if boss == 'Blind':
                return False
    elif dungeon_name == 'Tower of Hera':
        if boss in {'Armos Knights', 'Arrghus', 'Blind', 'Trinexx', 'Lanmolas'}:
            return False
    elif dungeon_name == 'Skull Woods':
        if boss == 'Trinexx':
            return False

    return True


restrictive_boss_locations = {}
for location in boss_location_table:
    restrictive_boss_locations[location] = not all(can_place_boss(boss, *location)
                                                   for boss in boss_table if not boss.startswith('Agahnim'))


def place_boss(world, player: int, boss: str, location: str, level: Optional[str]):
    if location == 'Ganons Tower' and world.mode[player] == 'inverted':
        location = 'Inverted Ganons Tower'
    world.get_dungeon(location, player).bosses[level] = boss_factory(boss, player)


def format_boss_location(location, level):
    return location + (' (' + level + ')' if level else '')


def place_bosses(world, player: int):
    if world.boss_shuffle[player] == 'none':
        return
    # Most restrictive to least order sort
    boss_locations = boss_location_table.copy()
    world.random.shuffle(boss_locations)
    boss_locations.sort(key=lambda location: -int(restrictive_boss_locations[location]))

    all_bosses = boss_table.keys()
    placeable_bosses = [boss for boss in all_bosses if boss not in {'Agahnim', 'Agahnim 2', 'Ganon'}]

    shuffle_mode = world.boss_shuffle[player]
    already_placed_bosses = []
    if ';' in shuffle_mode:
        bosses = shuffle_mode.split(';')
        shuffle_mode = bosses.pop()
        for boss in bosses:
            if '-' in boss:
                loc, boss = boss.split('-')
                boss = boss.title()
                level = None
                if loc.split(' ')[-1] in {'top', 'middle', 'bottom'}:
                    loc = loc.split(' ')
                    level = loc[-1]
                    loc = ' '.join(loc[:-1])
                loc = loc.title().replace('Of', 'of')
                if can_place_boss(boss, loc, level) and (loc, level) in boss_locations:
                    place_boss(world, player, boss, loc, level)
                    already_placed_bosses.append(boss)
                    boss_locations.remove((loc, level))
                else:
                    raise Exception(f"Cannot place {boss} at {format_boss_location(loc, level)} for player {player}")
            else:
                boss = boss.title()
                boss_locations, already_placed_bosses = place_where_possible(world, player, boss, boss_locations)

        if shuffle_mode == 'none':
            return

        if shuffle_mode in ['basic', 'full']:
            if world.boss_shuffle[player] == 'basic':
                bosses = placeable_bosses + ['Armos Knights', 'Lanmolas', 'Moldorm']
            else:
                bosses = placeable_bosses + world.random.sample(placeable_bosses, 3)

            for boss in already_placed_bosses:
                if boss in bosses:
                    bosses.remove(boss)

            world.random.shuffle(bosses)
            for loc, level in boss_locations:
                for _ in range(len(bosses)):
                    boss = bosses.pop()
                    if can_place_boss(boss, loc, level):
                        break
                    bosses.insert(0, boss)
                place_boss(world, player, boss, loc, level)

        elif shuffle_mode == 'chaos':
            for loc, level in boss_locations:
                try:
                    boss = world.random.choice(
                        [b for b in placeable_bosses if can_place_boss(b, loc, level)]
                    )
                except IndexError:
                    raise FillError(f'Could not place boss for location {format_boss_location(loc, level)}')
                else:
                    place_boss(world, player, boss, loc, level)

        elif shuffle_mode == 'singularity':
            primary_boss = world.random.choice(placeable_bosses)
            remaining_boss_locations, _ = place_where_possible(world, player, primary_boss, boss_locations)
            if remaining_boss_locations:
                # pick a boss to go into the remaining locations
                remaining_boss = world.random.choice([boss for boss in placeable_bosses if all(
                    can_place_boss(boss, loc, level) for loc, level in remaining_boss_locations)])
                remaining_boss_locations, _ = place_where_possible(world, player, remaining_boss,
                                                                   remaining_boss_locations)
                if remaining_boss_locations:
                    raise Exception("Unfilled boss locations!")
        else:
            raise FillError(f"Could not find boss shuffle mode {shuffle_mode}")


def place_where_possible(world, player: int, boss: str, boss_locations):
    remainder = []
    already_placed = []
    for loc, level in boss_locations:
        if can_place_boss(boss, loc, level):
            place_boss(world, player, boss, loc, level)
            already_placed.append(boss)
        else:
            remainder.append((loc, level))
    return remainder, already_placed
