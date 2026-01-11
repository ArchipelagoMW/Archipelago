# enemy randomization logic.

import random
from functools import reduce

from ...randomizer.data import bosses, enemies
from ...randomizer.data.formations import FormationMember
from . import flags, utils


def _randomize_enemy_attack(attack):
    """Randomize a single enemy attack.

    Args:
        attack(randomizer.data.attacks.EnemyAttack):
    """
    # Use old logic if no safety checks enabled, allows for instant KO applied to other attacks and random strong stuff.
    if attack.world.settings.is_flag_enabled(flags.EnemyNoSafetyChecks):
        # If the attack has no special damage types or buffs, randomize the attack priority level.
        # Allow a small chance (1 in 495) to get the instant KO flag.  Otherwise attack level is 1-7, lower more likely.
        if not attack.damage_types and not attack.buffs:
            new_attack_level = random.randint(0, random.randint(0, random.randint(0, random.randint(0, 8))))
            if new_attack_level > attack.attack_level:
                # If we got the instant KO flag, also hide the damage numbers.
                if new_attack_level == 8:
                    new_attack_level = 7
                    attack.damage_types = [3, 5]
                attack.attack_level = new_attack_level

        # If there are no buffs applied to the attack, give a 1/5 chance to apply a random status effect.
        # The status effect chosen has a 1/7 chance to be the unused "berserk" status.  If we hit this status, only
        # allow it another 1/5 chance, otherwise reroll it.
        if not attack.buffs and utils.coin_flip(1 / 5):
            while True:
                i = random.randint(0, 6)
                if i != 4 or utils.coin_flip(1 / 5):
                    attack.status_effects = [i]
                    break

        # If there are some buffs given by this attack, give a 50% chance to have an extra random buff.
        if attack.buffs and random.randint(1, 2) == 2:
            unused = list({3, 4, 5, 6} - set(attack.buffs))
            if unused:
                attack.buffs.append(random.choice(unused))

    # If there are status effects, randomize them.
    if attack.status_effects:
        effects = [0, 1, 2, 3, 5, 6]
        # Small chance to include berserk as an option if safety checks are disabled.
        if attack.world.settings.is_flag_enabled(flags.EnemyNoSafetyChecks) and utils.coin_flip(1 / 5):
            effects.append(4)

        attack.status_effects = random.sample(effects, len(attack.status_effects))

    # Shuffle hit rate.  If the attack is instant death, cap hit rate at 99% so items that protect from this
    # actually work.  Protection forces the attack to miss, but 100% hit rate can't miss so it hits anyway.
    if 3 in attack.damage_types:
        max_hit_rate = 99
    else:
        max_hit_rate = 100
    attack.hit_rate = utils.mutate_normal(attack.hit_rate, minimum=1, maximum=max_hit_rate)


def _randomize_enemy(enemy):
    """Randomize stats for this enemy.

    Args:
        enemy(randomizer.data.enemies.Enemy):
    """
    # Randomize main stats.  For bosses, don't let the stats go below their vanilla values.
    mutate_attributes = (
        "hp",
        "speed",
        "attack",
        "defense",
        "magic_attack",
        "magic_defense",
        "fp",
        "evade",
        "magic_evade",
    )
    old_stats = {}
    for key in mutate_attributes:
        old_stats[key] = getattr(enemy, key)

    enemy.hp = utils.mutate_normal(enemy.hp, minimum=1, maximum=32000)
    enemy.speed = utils.mutate_normal(enemy.speed)
    enemy.attack = utils.mutate_normal(enemy.attack, minimum=1)
    enemy.defense = utils.mutate_normal(enemy.defense, minimum=1)
    enemy.magic_attack = utils.mutate_normal(enemy.magic_attack, minimum=1)
    enemy.magic_defense = utils.mutate_normal(enemy.magic_defense, minimum=1)
    enemy.fp = utils.mutate_normal(enemy.fp, minimum=1)
    enemy.evade = utils.mutate_normal(enemy.evade, minimum=0, maximum=100)
    enemy.magic_evade = utils.mutate_normal(enemy.magic_evade, minimum=0, maximum=100)

    if enemy.boss:
        for attr, old_val in old_stats.items():
            if getattr(enemy, attr) < old_val:
                setattr(enemy, attr, old_val)

    if enemy.boss:
        # For bosses, allow a small 1/255 chance to be vulnerable to Geno Whirl.
        if utils.coin_flip(1 / 255):
            enemy.death_immune = False

    else:
        # Have a 1/3 chance of reversing instant death immunity for normal enemies.
        if random.randint(1, 3) == 3:
            enemy.death_immune = not enemy.death_immune

        # Randomize morph item chance of success.
        enemy.morph_chance = random.randint(0, 3)

    # Shuffle elemental resistances and status immunities.  Keep the same number but randomize them for now.
    # Keep the total number of elemental/status immunities the same, but mix them together with max 4 of each kind.
    total_immunities = len(enemy.status_immunities) + len(enemy.resistances)
    new_status_immunities = random.randint(max(0, total_immunities - 4), min(total_immunities, 4))
    new_resistances = total_immunities - new_status_immunities

    # Sanity check to make sure we don't have more than the max.
    if new_status_immunities > 4 or new_status_immunities < 0:
        raise ValueError("{}: invalid new_status_immunities {}".format(enemy, new_status_immunities))
    if new_resistances > 4 or new_resistances < 0:
        raise ValueError("{}: invalid new_resistances {}".format(enemy, new_resistances))

    enemy.status_immunities = random.sample(range(0, 4), new_status_immunities)

    # Make a 50/50 chance to prioritize elemental immunities over weaknesses or vice versa.
    # Allow earth (jump) to be in both however, because they can be weak to jump while immune to it.
    # Jump Shoes bypass the immunity and they'll take double damage.
    if utils.coin_flip():
        enemy.resistances = random.sample(range(4, 8), new_resistances)
        potential_weaknesses = set(range(4, 8)) - set(enemy.resistances)
        potential_weaknesses.add(7)
        enemy.weaknesses = random.sample(sorted(potential_weaknesses), min(len(enemy.weaknesses), len(potential_weaknesses)))
    else:
        enemy.weaknesses = random.sample(range(4, 8), len(enemy.weaknesses))
        potential_resistances = set(range(4, 8)) - set(enemy.weaknesses)
        potential_resistances.add(7)
        enemy.resistances = random.sample(sorted(potential_resistances), min(new_resistances, len(potential_resistances)))

    # Randomize flower bonus type and chance for this enemy.
    enemy.flower_bonus_type = random.randint(1, 5)
    enemy.flower_bonus_chance = random.randint(0, 5) + random.randint(0, 5)


def _randomize_formation(formation):
    """Randomize this enemy formation."""

    def get_distance(x1, y1, x2, y2):
        return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

    def get_collective_distance(x1, y1, points):
        distances = [get_distance(x1, y1, x2, y2) for x2, y2 in points]
        return reduce(lambda a, b: a * b, distances, 1)

    def select_most_distance(possible_points, points):
        chosen = max(possible_points, key=lambda c: get_collective_distance(c[0], c[1], points))
        return chosen

    # Max enemies for a given group.
    max_enemies = 6

    # Don't shuffle any formations with bosses or hidden enemies (special battle events), or empty groups.
    if formation.bosses or formation.hidden_enemies or not formation.members:
        return

    # If we have less than three leader enemies, get a randomized similar ranked one.
    candidates = list(formation.leaders)
    while len(candidates) < 3:
        base = random.choice(candidates)
        new = base.get_similar()
        if new not in candidates:
            candidates.append(new)

    # Make sure we have at most three unique candidates.
    num_candidates = len(set(candidates))
    if num_candidates > 3:
        raise ValueError("Got more than three unique candidates, {} instead".format(num_candidates))

    # Pick random number of enemies for the group, weighted slightly lower.
    num_enemies = random.randint(1, random.randint(3, max_enemies))
    num_enemies = max(num_enemies, len(formation.leaders))
    chosen_enemies = list(formation.leaders)

    # Fill out the number of enemies with randomly chosen candidates, but make sure VRAM palette totals less than
    # 64 because the VRAM can only hold so much palette data at once.
    while len(chosen_enemies) < num_enemies:
        vram_total = sum([e.palette for e in chosen_enemies])
        sub_candidates = candidates + chosen_enemies

        # Exclude any enemies that are unique per battle.
        sub_candidates = [e for e in sub_candidates if not e.one_per_battle or e not in chosen_enemies]

        sub_candidates = [e for e in sub_candidates if vram_total + e.palette <= 64]
        if not sub_candidates:
            break
        chosen_enemies.append(random.choice(sub_candidates))

    random.shuffle(chosen_enemies)

    # Randomize coordinates for the chosen enemies.
    formation.members = []
    done_coordinates = []
    for i, enemy in enumerate(chosen_enemies):
        if not done_coordinates:
            x, y = random.choice(formation.VALID_COORDINATES)
        else:
            candidates = random.sample(formation.VALID_COORDINATES, len(chosen_enemies) * 2)
            x, y = select_most_distance(candidates, done_coordinates)

        done_coordinates.append((x, y))
        formation.members.append(FormationMember(i, False, enemy, x, y))

    formation.members.sort(key=lambda m: m.index)

    done_coordinates = sorted(done_coordinates)
    for i, (x, y) in enumerate(done_coordinates):
        formation.members[i].x_pos = x
        formation.members[i].y_pos = y


def randomize_all(world):
    """Randomize everything for enemies for a single seed.

    :type world: randomizer.logic.main.GameWorld
    """
    if world.settings.is_flag_enabled(flags.EnemyAttacks):
        # *** Shuffle enemy attacks ***
        # Intershuffle hit rate of attacks with status effects.
        with_status_effects = [a for a in world.enemy_attacks if a.status_effects]
        for attr in ('hit_rate', ):
            shuffled = with_status_effects[:]
            random.shuffle(shuffled)
            swaps = []
            for attack in shuffled:
                swaps.append(getattr(attack, attr))
            for attack, swapped_val in zip(with_status_effects, swaps):
                setattr(attack, attr, swapped_val)

        # Now perform normal shuffle for the rest, and get patch data.
        for attack in world.enemy_attacks:
            _randomize_enemy_attack(attack)

    if world.settings.is_flag_enabled(flags.EnemyStats):

        # *** Shuffle enemy stats ***
        # Start with inter-shuffling some stats between non-boss enemies around the same rank as each other.
        candidates = [m for m in world.enemies if not m.boss]
        candidates.sort(key=lambda c: c.rank)

        for attribute in ("hp", "speed", "defense", "magic_defense", "evade", "magic_evade", "resistances",
                          "weaknesses", "status_immunities"):
            shuffled = candidates[:]
            max_index = len(candidates) - 1
            done = set()

            # For each enemy, have a 50/50 chance of swapping stat with the next enemy up sorted by rank.
            for i in range(len(candidates)):
                new_index = i
                if shuffled[i] in done:
                    continue
                while random.randint(0, 1) == 1:
                    new_index += 1
                new_index = int(round(new_index))
                new_index = min(new_index, max_index)
                a, b = shuffled[i], shuffled[new_index]
                done.add(a)
                shuffled[i] = b
                shuffled[new_index] = a

            # Now swap attribute values with shuffled list.
            swaps = []
            for a, b in zip(candidates, shuffled):
                aval, bval = getattr(a, attribute), getattr(b, attribute)
                swaps.append(bval)
            for a, bval in zip(candidates, swaps):
                setattr(a, attribute, bval)

        # Now inter-shuffle morph chances randomly.
        valid = [enemy for enemy in world.enemies if not enemy.boss]
        morph_chances = [enemy.morph_chance for enemy in valid]
        random.shuffle(morph_chances)
        for chance, enemy in zip(morph_chances, valid):
            enemy.morph_chance = chance

        # Finally shuffle enemy attribute values as normal.
        for enemy in world.enemies:
            _randomize_enemy(enemy)

        # Special logic for Smithy 2: All heads must have the same HP!  Use the base head enemy for this.
        main_head = world.get_enemy_instance(enemies.Smithy2Head)
        for e in (enemies.Smithy2TankHead, enemies.Smithy2SafeHead, enemies.Smithy2MageHead, enemies.Smithy2ChestHead):
            head = world.get_enemy_instance(e)
            head.hp = main_head.hp

    # Randomize individual rewards on their own.
    if world.settings.is_flag_enabled(flags.EnemyDrops):
        for enemy in world.enemies:
            enemy.coins = utils.mutate_normal(enemy.coins, maximum=255)

            # For bosses, don't let exp go above vanilla.  For normal enemies, don't let it go below.
            oldxp = enemy.xp
            enemy.xp = utils.mutate_normal(enemy.xp, minimum=1, maximum=0xffff)
            if enemy.boss:
                enemy.xp = min(oldxp, enemy.xp)
            else:
                enemy.xp = max(oldxp, enemy.xp)

            # Shuffle reward items with other consumable items.
            linked = enemy.normal_item == enemy.rare_item
            consumables = [i for i in world.items if i.consumable and not i.reuseable]

            # Shuffle normal item, if this reward has one.
            if enemy.normal_item:
                enemy.normal_item = enemy.normal_item.get_similar(consumables)

            # If we're linked, set the rare item to the normal one.  Otherwise shuffle the rare one as well.
            if linked:
                enemy.rare_item = enemy.normal_item
            elif enemy.rare_item:
                enemy.rare_item = enemy.rare_item.get_similar(consumables)

            # If we have a morph chance, randomize the Yoshi Cookie item.
            if enemy.morph_chance:
                enemy.yoshi_cookie_item = random.choice(consumables)
            else:
                enemy.yoshi_cookie_item = None

    # Shuffle enemy formations.
    if world.settings.is_flag_enabled(flags.EnemyFormations):
        for formation in world.enemy_formations:
            _randomize_formation(formation)

    # XP boost.
    if world.settings.is_flag_enabled(flags.ExperienceBoost2x):
        for enemy in world.enemies:
            enemy.xp *= 2
    elif world.settings.is_flag_enabled(flags.ExperienceBoost3x):
        for enemy in world.enemies:
            enemy.xp *= 3

    boss_enemies = set()
    # No XP from regular encounters.
    if world.settings.is_flag_enabled(flags.ExperienceNoRegular) or world.settings.is_flag_enabled(flags.ExperienceNoBosses):
        for location in world.boss_locations:
            if isinstance(location, bosses.BossLocation):
                for member in location.formation.members:
                    boss_enemies.add(member.enemy)

    if world.settings.is_flag_enabled(flags.ExperienceNoRegular):
        for enemy in world.enemies:
            if (not enemy.boss or enemy not in boss_enemies):
                enemy.xp = 0

    if world.settings.is_flag_enabled(flags.ExperienceNoBosses):
        for enemy in boss_enemies:
            enemy.xp = 0

    # If Gk is set, dont let any agent in a boss fight be hit by OHKO
    if world.settings.is_flag_enabled(flags.NoOHKO):
        for enemy in world.enemies:
            if enemy.boss:
                enemy.death_immune = True

    # If palette swap is enabled, give us a 50/50 chance at a chocolate cake.
    if world.settings.is_flag_enabled(flags.PaletteSwaps):
        world.chocolate_cake = utils.coin_flip()
