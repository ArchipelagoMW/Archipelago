# Character randomization logic.

import collections
import random
import inspect

from ...randomizer.data import characters, spells, palettes
from ...randomizer.logic import flags, utils


# Move this to character classes instead!
def _randomize_learned_spells(world):
    """Perform randomization for which levels characters learn spells.

    Args:
        world(randomizer.logic.main.GameWorld):
    """
    # Shuffle all spells.  There are 27 spells, so add an extra 3 random ones to ensure everybody has 6 spells.
    # In linear mode Group Hug only works with Peach, so remove it from the shuffle and give Peach only 5 spells.
    default_spells = [
        spells.Jump,
        spells.FireOrb,
        spells.SuperJump,
        spells.SuperFlame,
        spells.UltraJump,
        spells.UltraFlame,
        spells.Therapy,
        spells.SleepyTime,
        spells.ComeBack,
        spells.Mute,
        spells.PsychBomb,
        spells.Terrorize,
        spells.PoisonGas,
        spells.Crusher,
        spells.BowserCrush,
        spells.GenoBeam,
        spells.GenoBoost,
        spells.GenoWhirl,
        spells.GenoBlast,
        spells.GenoFlash,
        spells.Thunderbolt,
        spells.HPRain,
        spells.Psychopath,
        spells.Shocker,
        spells.Snowy,
        spells.StarRain,
    ]
    if world.open_mode:
        default_spells.append(spells.GroupHug)

    waiting_spells = default_spells[:]
    charspells = collections.defaultdict(list)

    # Place spells in characters who still need spells until we have no more.
    while True:
        still_need = [c for c in world.characters if
                      (len(charspells[c]) < 5 or (len(charspells[c]) < 6 and (not isinstance(c, characters.Peach) or
                                                                              world.open_mode)))]
        if not still_need:
            break

        for char in still_need:
            possible_spells = [spell for spell in waiting_spells if spell not in charspells[char]]
            spell = random.choice(possible_spells)
            charspells[char].append(spell)

            # Remove spell from list of waiting to be assigned.  If we used them all, reset the list and choose more.
            waiting_spells.remove(spell)
            if not waiting_spells:
                waiting_spells = default_spells[:]

    # Guarantee Geno Boost and Group Hug isn't the last spell a character learns if they have it.
    for character in world.characters:
        our_spells = charspells[character]
        for s in (
                spells.GenoBoost,
                spells.GroupHug,
        ):
            if s in our_spells:
                index = our_spells.index(s)
                if index == (len(our_spells) - 1):
                    new_index = random.randint(0, max(len(our_spells) - 2, 0))
                    our_spells[index], our_spells[new_index] = our_spells[new_index], our_spells[index]

    # Linear mode: Insert Group Hug for Peach, but make sure it's not the final spell learned for balance.
    if not world.open_mode:
        for character in world.characters:
            if isinstance(character, characters.Peach) and len(charspells[character]) < 6:
                charspells[character].insert(random.randint(0, 4), spells.GroupHug)

    # Sanity check to make sure every character has 6 spells and Peach has Group Hug.
    for character in world.characters:
        if len(charspells[character]) != 6:
            raise RuntimeError("Character {} does not have 6 spells: {!r}".format(character, charspells))
        elif (not world.open_mode and isinstance(character, characters.Peach) and
              spells.GroupHug not in charspells[character]):
            raise RuntimeError("Peach was assigned 6 spells before Group Hug: {!r}".format(charspells))

    # Assign chosen spells for each character.  Make the first spell always learned from the start (level 1), and
    # assign the other spells to random levels from 2-20.
    for character in world.characters:
        character.learned_spells = {}
        charlevels = [1] + sorted(random.sample(list(range(2, 20)), 5))
        for level, spell in zip(charlevels, charspells[character]):
            character.learned_spells[level] = spell


def _randomize_levelup_xps(levelup_xps):
    """Perform randomization of exp needed to reach each level by shuffling the difference between each level.

    Args:
        levelup_xps():
    """
    gaps = []
    for i in range(1, len(levelup_xps.levels)):
        xp_to_levelup = levelup_xps.get_xp_for_level(i + 1) - levelup_xps.get_xp_for_level(i)
        gaps.append(utils.mutate_normal(xp_to_levelup, minimum=1, maximum=9999))
    gaps.sort()

    # Make sure we total 9999 at lvl 30.  If not, divide the difference into 435 "pieces" and add 1 piece to the
    # first levelup, 2 pieces to the second, etc. to curve it out nicely.
    total = sum(gaps)
    if total != 9999:
        diff = 9999 - total
        piece = diff / sum(range(1, 30))
        for i in range(len(gaps)):
            gaps[i] += round(piece * (i + 1))

    # Check total again for any rounding.  Just alter the final level for that, as it should only be a couple exp.
    total = sum(gaps)
    if total != 9999:
        diff = 9999 - total
        gaps[-1] += diff
        gaps.sort()

    # Now set the amount to level up for each level based on the gaps.
    prev = 0
    levelup_xps.levels[0] = 0
    for i, amt in enumerate(gaps, start=1):
        new_val = prev + amt
        levelup_xps.levels[i] = new_val
        prev = new_val


def _randomize_character(character):
    """Perform randomization for this character.

    Args:
        character(randomizer.data.characters.Character):
    """
    character.starting_level = utils.mutate_normal(character.starting_level, minimum=1, maximum=30)
    character.speed = utils.mutate_normal(character.speed, minimum=1, maximum=255)

    # Shuffle level up stat bonuses.
    for i, bonus in enumerate(character.levelup_bonuses):
        for attr in character.LEVEL_STATS:
            value = getattr(bonus, attr)
            # Make each bonus at least 1.
            setattr(bonus, attr, max(utils.mutate_normal(value, maximum=15), 1))

    # Shuffle level up stat growths up to level 20.  Past level 20, make them tiny similar to vanilla.
    for attr in character.LEVEL_STATS:
        # Shuffle expected value at level 20 and rework the stat curve based on the final value.
        # Make sure the stat at level 20 is at least one point for each level at minimum.
        value_lvl1 = character.get_stat_at_level(attr, 1)
        value_lvl20 = character.get_stat_at_level(attr, 20)
        value_lvl1 = utils.mutate_normal(value_lvl1, minimum=1)
        value_lvl20 = utils.mutate_normal(value_lvl20, minimum=value_lvl1 + 19)

        # Generate random fixed value points between level 1 and 20 to interpolate between.
        fixed_points = [(1, value_lvl1), (20, value_lvl20)]

        for _ in range(3):
            # Pick a random level range in the fixed points list that is >= 4 levels apart to spread them out a bit.
            range_index = [i for i in range(1, len(fixed_points) - 1) if
                           fixed_points[i][0] - fixed_points[i - 1][0] >= 4]
            if not range_index:
                break

            dex = random.choice(range_index)
            lower_level, lower_value = fixed_points[dex - 1]
            upper_level, upper_value = fixed_points[dex]

            level_interval = (upper_level - lower_level) // 2
            value_interval = (upper_value - lower_value) // 2

            # Increase by at least 1 level, but not all the way to the upper level.
            level_increase = max(random.randint(0, level_interval) + random.randint(0, level_interval), 1)
            level = min(lower_level + level_increase, upper_level - 1)

            # Increase value by at least 1 for each level.
            value_increase = random.randint(0, value_interval) + random.randint(0, value_interval)
            value_increase = max(value_increase, level_increase)
            value = lower_value + value_increase

            fixed_points.append((level, value))
            fixed_points = sorted(fixed_points)

        # Linear interpolate between fixed value points to fill in the other levels.
        for ((level1, value1), (level2, value2)) in zip(fixed_points, fixed_points[1:]):
            level_difference = level2 - level1
            value_difference = value2 - value1
            for l in range(level1 + 1, level2):
                steps_away_from_level1 = l - level1
                factor = steps_away_from_level1 / float(level_difference)
                # Min increase value number of steps away from level1, so we increase by at least 1 for each level.
                v = value1 + max(int(round(factor * value_difference)), steps_away_from_level1)
                fixed_points.append((l, v))

        fixed_points = sorted(fixed_points)
        levels, values = list(zip(*fixed_points))

        # Sanity checks
        num_points = len(fixed_points)
        if num_points != 20:
            raise ValueError("Generated fixed points is not 20 levels: {} instead".format(num_points))

        if levels != tuple(sorted(levels)):
            raise ValueError("Generate levels aren't in order: {!r}".format(levels))

        if values != tuple(sorted(values)):
            raise ValueError("Stat values aren't in order character {}, stat {}: {!r}, fixed_points {!r}".format(
                character.name, attr, values, fixed_points))

        # Get increases for each levelup.
        increases = []
        for value1, value2 in zip(values, values[1:]):
            increases.append(value2 - value1)

        # Frontload bigger stat increases earlier.  For defense, make the frontload factor a bit smaller.
        frontload_factor = random.random() * random.random()
        if attr in ["defense", "magic_defense"]:
            frontload_factor *= random.random()

        max_index = len(increases) - 1
        for n, inc in enumerate(increases):
            factor = (((max_index - n) / float(max_index)) * frontload_factor)
            amount = int(round(inc * factor))
            increases[n] = (inc - amount)

        # Make sure no single level has an increase greater than 15.  Shuffle increases to avoid this.
        while max(increases) > 15:
            i = increases.index(max(increases))
            increases[i] = increases[i] - 1
            choices = [n for (n, v) in enumerate(increases) if v < 15]
            if random.randint(0, len(choices)) == 0:
                value_lvl1 += 1
            elif choices:
                i = random.choice(choices)
                increases[i] = increases[i] + 1

        # Special logic for Mario.
        if isinstance(character, characters.Mario):
            # Make sure Mario has minimum basic starting HP and attack in standard mode.
            if not character.world.open_mode and attr in ["max_hp", "attack"]:
                while value_lvl1 < 20:
                    candidates = [i for i in range(len(increases)) if increases[i] > 0]
                    if not candidates:
                        break
                    value_lvl1 += 1
                    weights = [(len(increases) - i) for i in candidates]
                    chosen = random.choices(candidates, weights=weights)[0]
                    increases[chosen] -= 1

            # Make sure physical attack increase for level 2 is at least 3 because of a weird oversight in the game.
            # The level up stat growths are right after the exp for level up amounts in the data.  The game doesn't
            # actually stop levelling up at 30 however, so if Mario's level 2 stat growths make a two byte "exp"
            # value less than 9999 (the max exp at lvl 30) then the game will continue to level up.  This makes
            # things get messy as dummy spells get learnt and bad data is used for level up stats.  If the physical
            # attack growth is at least 3, this will make two bytes 0x3000 at minimum which is > 12000 no matter
            # what the other values are.  This prevents this bug from happening.
            if attr == 'attack':
                while increases[0] < 3:
                    # Subtract 1 from a random growth that has > 1 currently so we have at least 1 per level.
                    candidates = [i for i in range(1, len(increases)) if increases[i] > 1]
                    if not candidates:
                        break
                    increases[0] += 1
                    weights = [(len(increases) - i) for i in candidates]
                    chosen = random.choices(candidates, weights=weights)[0]
                    increases[chosen] -= 1

        # Set base value and set levelup growth increases to generated values.  Past level 20, just random shuffle
        # between 1-2 to keep increases lower similar to the vanilla game.
        setattr(character, attr, value_lvl1)
        for growth in character.levelup_growths:
            if increases:
                setattr(growth, attr, increases.pop(0))
            else:
                # Beyond level 20, give a 1/3 chance of 2 increase, 2/3 chance of 1 increase.
                setattr(growth, attr, random.choices([1, 2], weights=[2, 1])[0])


def _finalize_character(character):
    """Finalize character data after other shuffling has happened outside of this instance.

    Args:
        character(randomizer.data.characters.Character):
    """
    # Determine starting stats based on starting level and best stat choices up to that point.
    for attr in character.LEVEL_STATS:
        # Make sure stat can't grow beyond max value.  This should be rare, but if it happens then subtract from
        # the levelup growths beyond the starting level to fix it.
        if attr == 'max_hp':
            max_allowed = 999
        else:
            max_allowed = 255

        while character.get_max_stat_at_level(attr, 30) > max_allowed:
            # Subtract 1 from a random growth that has > 1 currently so we have at least 1 per level.
            ss = [s for s in character.levelup_growths[character.starting_level - 1:] if getattr(s, attr) > 1]
            if not ss:
                break
            weights = list(range(len(ss)))
            s = random.choices(ss, weights=weights)[0]
            value = getattr(s, attr)
            setattr(s, attr, value - 1)

        # Set final starting stat value based on optimal bonuses.
        setattr(character, attr, character.get_optimal_stat_at_level(attr, character.starting_level))

    # If we're in debug mode, max all starting stats.
    if character.world.debug_mode:
        character.starting_level = 30
        character.max_hp = 999
        character.speed = 99
        character.attack = 255
        character.defense = 255
        character.magic_attack = 255
        character.magic_defense = 255

    # Set starting spells based on starting level and learned spells.
    character.starting_spells.clear()
    for level in range(1, character.starting_level + 1):
        if character.learned_spells.get(level):
            character.starting_spells.add(character.learned_spells[level])

    # Set starting exp based on starting level.
    character.xp = character.world.levelup_xps.get_xp_for_level(character.starting_level)


def randomize_all(world):
    """Randomize everything for characters for a single seed.

    :type world: randomizer.logic.main.GameWorld
    """
    # Palettes!!!!
    def find_subclasses(module, clazz):
        return [
            cls
            for name, cls in inspect.getmembers(module)
            if inspect.isclass(cls) and issubclass(cls, clazz) and cls != clazz
        ]
    mario_palettes = find_subclasses(palettes, palettes.MarioPalette)
    mallow_palettes = find_subclasses(palettes, palettes.MallowPalette)
    geno_palettes = find_subclasses(palettes, palettes.GenoPalette)
    bowser_palettes = find_subclasses(palettes, palettes.BowserPalette)
    toadstool_palettes = find_subclasses(palettes, palettes.ToadstoolPalette)

    if world.settings.is_flag_enabled(flags.PaletteSwaps):
        world.characters[0].palette = random.choice(mario_palettes)
        world.characters[1].palette = random.choice(mallow_palettes)
        world.characters[2].palette = random.choice(geno_palettes)
        world.characters[3].palette = random.choice(bowser_palettes)
        world.characters[4].palette = random.choice(toadstool_palettes)

    # Shuffle learned spells for all characters.
    if world.settings.is_flag_enabled(flags.CharacterLearnedSpells):
        _randomize_learned_spells(world)

    # Shuffle character stats.
    if world.settings.is_flag_enabled(flags.CharacterStats):
        _randomize_levelup_xps(world.levelup_xps)

        # Intershuffle levelup stat bonuses up to level 20 between all characters for variance.
        all_bonuses = []
        for character in world.characters:
            all_bonuses += character.levelup_bonuses[:19]

        # Shuffle physical and magical bonuses together.
        for attrs in (
                ('max_hp',),
                ('attack', 'defense'),
                ('magic_attack', 'magic_defense'),
        ):
            # Shuffle between all characters.
            shuffled = all_bonuses[:]
            random.shuffle(shuffled)

            for attr in attrs:
                swaps = []
                for s in shuffled:
                    swaps.append(getattr(s, attr))
                for bonus, bval in zip(all_bonuses, swaps):
                    setattr(bonus, attr, bval)

            # For any bonuses that are zero, pick a random non-zero one.
            non_zeros = [b for b in all_bonuses if all([getattr(b, attr) for attr in attrs])]
            for bonus in all_bonuses:
                for attr in attrs:
                    while getattr(bonus, attr) == 0:
                        setattr(bonus, attr, getattr(random.choice(non_zeros), attr))

        # Now randomize everything else including the intershuffled bonus values and other levelup growths.
        for character in world.characters:
            _randomize_character(character)

    # If we're shuffling join order, do that now before we finalize the characters.  For standard mode, keep Mario as
    # the first character and shuffle the others.  For open mode, shuffle the whole list.
    if world.settings.is_flag_enabled(flags.CharacterJoinOrder):
        if world.open_mode:
            random.shuffle(world.character_join_order)
        else:
            extra_characters = world.character_join_order[1:]
            random.shuffle(extra_characters)
            world.character_join_order = world.character_join_order[:1] + extra_characters

    #No Free Characters and Choose Starting Characters logic - adjust join order where appropriate
    if world.open_mode:
        # Fail if starter is excluded, or if everyone excluded
        if (world.settings.is_flag_enabled(flags.ExcludeMario) and world.settings.is_flag_enabled(
                flags.StartMario)) or (
                world.settings.is_flag_enabled(flags.ExcludeMallow) and world.settings.is_flag_enabled(
            flags.StartMallow)) or (
                world.settings.is_flag_enabled(flags.ExcludeGeno) and world.settings.is_flag_enabled(
            flags.StartGeno)) or (
                world.settings.is_flag_enabled(flags.ExcludeBowser) and world.settings.is_flag_enabled(
            flags.StartBowser)) or (
                world.settings.is_flag_enabled(flags.ExcludeToadstool) and world.settings.is_flag_enabled(
            flags.StartToadstool)):
            raise flags.FlagError("Cannot exclude your starter")
        elif world.settings.is_flag_enabled(flags.ExcludeMario) and world.settings.is_flag_enabled(
                flags.ExcludeMallow) and world.settings.is_flag_enabled(
            flags.ExcludeGeno) and world.settings.is_flag_enabled(
            flags.ExcludeBowser) and world.settings.is_flag_enabled(flags.ExcludeToadstool):
            raise flags.FlagError("Cannot exclude all 5 characters")
        # Move chosen starting character to front of join order
        else:
            for char in world.character_join_order:
                if (world.settings.is_flag_enabled(flags.StartMario) and char.index == 0) or (
                        world.settings.is_flag_enabled(flags.StartMallow) and char.index == 4) or (
                        world.settings.is_flag_enabled(flags.StartGeno) and char.index == 3) or (
                        world.settings.is_flag_enabled(flags.StartBowser) and char.index == 2) or (
                        world.settings.is_flag_enabled(flags.StartToadstool) and char.index == 1):
                    world.character_join_order.insert(0, world.character_join_order.pop(
                        world.character_join_order.index(char)))
        #Count number of excluded characters, and empty their slots
        position_iterator = 0
        empties = 0
        world.meta_join_order = world.character_join_order.copy()
        for char in world.meta_join_order:
            if (world.settings.is_flag_enabled(flags.ExcludeMario) and char.index == 0) or (
                    world.settings.is_flag_enabled(flags.ExcludeMallow) and char.index == 4) or (
                    world.settings.is_flag_enabled(flags.ExcludeGeno) and char.index == 3) or (
                    world.settings.is_flag_enabled(flags.ExcludeBowser) and char.index == 2) or (
                    world.settings.is_flag_enabled(flags.ExcludeToadstool) and char.index == 1):
                world.meta_join_order[position_iterator] = None
                empties += 1
            position_iterator += 1
        #Make sure first three slots are filled when NFC is turned off, when possible
        if not world.settings.is_flag_enabled(flags.NoFreeCharacters):
            for i in range(empties):
                position_iterator = 0
                for char in world.meta_join_order:
                    if char is None and position_iterator < 3:
                        if char in world.meta_join_order:
                            world.meta_join_order.append(world.meta_join_order.pop(world.meta_join_order.index(char)))
                        if char in world.character_join_order:
                            world.character_join_order.append(world.character_join_order.pop(world.character_join_order[position_iterator]))
                    position_iterator += 1

    # Adjust starting levels according to join order.  Get original levels, then update starting levels based on
    # join order with Mallow = 4, Geno = 3, Bowser = 2, Peach = 1.
    orig_levels = {}
    for character in world.characters:
        orig_levels[character.index] = character.starting_level

    # For open mode, make the first three characters level 1 to start.  The final two join at Bowyer and Bundt,
    # so make their levels the same as Geno and Peach respectively.
    if world.open_mode:
        world.character_join_order[0].starting_level = 1
        if world.settings.is_flag_enabled(flags.NoFreeCharacters):
            world.character_join_order[1].starting_level = orig_levels[4]
            world.character_join_order[2].starting_level = orig_levels[2]
        else:
            world.character_join_order[1].starting_level = 1
            world.character_join_order[2].starting_level = 1
        world.character_join_order[3].starting_level = orig_levels[3]
        world.character_join_order[4].starting_level = orig_levels[1]
    # For standard mode, just make their levels the same as the vanilla join order.
    else:
        for i, character in enumerate(world.character_join_order[1:]):
            character.starting_level = orig_levels[4 - i]

    # Now finalize the characters and get patch data.
    for character in world.characters:
        _finalize_character(character)
