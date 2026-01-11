# Spell randomization logic.

import random

from . import flags, utils

from ...randomizer.data import enemies
from ...randomizer.data import spells


def _randomize_spell(spell):
    """Perform randomization for this spell.

    Args:
        spell(randomizer.data.spells.Spell):
    """
    spell.fp = utils.mutate_normal(spell.fp, minimum=1, maximum=99)

    # If this is an enemy spell with status effects, shuffle them.
    if isinstance(spell, spells.EnemySpell) and spell.status_effects:
        effects = [0, 1, 2, 3, 5, 6]
        # Chance to include berserk as an option if safety checks are disabled.
        if spell.world.settings.is_flag_enabled(flags.EnemyNoSafetyChecks) and utils.coin_flip(1 / 5):
            effects.append(4)

        spell.status_effects = random.sample(effects, len(spell.status_effects))

    # Don't shuffle power for certain spells that cause problems if they deal damage.
    if not isinstance(spell, (spells.GenoBoost, spells.Shredder, spells.SleepyTime, spells.Mute, spells.Psychopath)):
        spell.power = utils.mutate_normal(spell.power)

    # Don't shuffle hit rate for certain spells or Geno Boost.  We don't want those to ever be able to miss.
    if not isinstance(spell, (spells.GenoBoost, spells.Therapy, spells.GroupHug, spells.HPRain, spells.Recover,
                              spells.MegaRecover, spells.Shredder, spells.Psychopath)):
        # If the spell is instant death, cap hit rate at 99% so items that protect from this actually work.
        # Protection forces the attack to miss, but 100% hit rate can't "miss" so it hits anyway.
        if spell.instant_ko:
            max_hit_rate = 99
        else:
            max_hit_rate = 100
        spell.hit_rate = utils.mutate_normal(spell.hit_rate, minimum=1, maximum=max_hit_rate)

def _randomize_spell_casting(world):
    for enemy in world.enemies:
        script = enemy.script
        for i in range(len(script)):
            command,args = script[i]
            if command != 'cast_spell': continue
            new_args = []
            for arg in args:
                possible_spells = [spell for spell in spells.SpellsToTargets[getattr(arg, 'index', arg)] if spell.fp <= enemy.fp]
                # This should probably never happen...probably.
                if not possible_spells:
                    possible_spells = [arg]
                new_args.append(random.choice(possible_spells).index)
            script[i] = command, new_args


def randomize_all(world):
    """Randomize everything for spells for a single seed.

    :type world: randomizer.logic.main.GameWorld
    """
    if world.settings.is_flag_enabled(flags.CharacterSpellStats):
        # Randomize spell stats.
        for spell in world.spells:
            if isinstance(spell, spells.CharacterSpell):
                _randomize_spell(spell)

        # Randomize starting FP if we're randomizing spell stats.
        world.starting_fp = utils.mutate_normal(world.starting_fp, minimum=1, maximum=99)

    # Randomize enemy spells.
    if world.settings.is_flag_enabled(flags.EnemyAttacks):
        for spell in world.spells:
            if isinstance(spell, spells.EnemySpell):
                _randomize_spell(spell)

    if world.settings.is_flag_enabled(flags.EnemySpells):
        _randomize_spell_casting(world)

    # If we're generating a debug mode seed for testing, set max FP to start.
    if world.debug_mode:
        world.starting_fp = 99
