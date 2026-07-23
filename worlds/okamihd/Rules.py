from rule_builder.field_resolvers import FromOption
from rule_builder.rules import Has, And, Rule, OptionFilter, Or, HasGroup, HasAny, HasAll
from .Enums.BrushTechniques import BrushTechniques
from .Enums.DivineInstruments import DivineInstruments
from .Options import ProgressiveWeapons, RequiredDoggorbs, NightTimeChecksRequireCrescent, AlternativeMistSlowdown
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import OkamiWorld

long_swim_rule: Rule = HasAny("Water Tablet", BrushTechniques.GREENSPROUT_WATERLILY)

has_portable_fire_source_strict: Rule = And(Or(Has(DivineInstruments.SOLAR_FLARE.value.item_name),
                                               Has("Progressive Mirror", 4)), Has(BrushTechniques.INFERNO))

has_portable_thunder_source_strict: Rule = And(Or(Has(DivineInstruments.THUNDER_EDGE.value.item_name),
                                                  Has("Progressive Sword", 4)), Has(BrushTechniques.THUNDERSTORM))

has_portable_fire_source: Rule = Or(has_portable_fire_source_strict, Has(BrushTechniques.FIREBURST))

has_portable_thunder_source: Rule = Or(And(Or(Has(DivineInstruments.THUNDER_EDGE.value.item_name),
                                              Has("Progressive Sword", 5)), Has(BrushTechniques.THUNDERSTORM)),
                                       Has(BrushTechniques.THUNDERBOLT))

has_portable_ice_source: Rule = Or(And(Or(Has(DivineInstruments.TUNDRA_BEADS.value.item_name),
                                          Has("Progressive Rosary", 5)), Has(BrushTechniques.BLIZZARD)),
                                   Has(BrushTechniques.ICESTORM))

gale_shrine_access: Rule = HasGroup("canine_warriors", count=FromOption(RequiredDoggorbs))

moon_cave_access: Rule = Has("Serpent Crystal")
n_ryoshima_islands_dragon_rule: Rule = Or(Has("Orca"), HasAll("Water Tablet", "Inside the dragon - Get Dragon Orb"))

n_ryoshima_guardian_sapling_rule: Rule = Or(long_swim_rule, Has("Orca"))

city_checkpoint_drawbridge_rule: Rule = And(
    Has(BrushTechniques.INFERNO),
    Or(Has(BrushTechniques.FIREBURST), Has(
        DivineInstruments.SOLAR_FLARE.value.item_name),
       Has("Progressive Mirror", 4), Has("Moon Cave - Defeat Orochi")))

# Only count Fireburst and icestrom if FireburstIcestormSlowdown is set to true.
slowdown_rule: Rule = Or(Has(BrushTechniques.VEIL_OF_MIST),
                         HasAny(BrushTechniques.FIREBURST, BrushTechniques.ICESTORM, options=[
                             OptionFilter(AlternativeMistSlowdown, AlternativeMistSlowdown.option_true)],
                                filtered_resolution=False))


night_time_check_rule: Rule = Has(BrushTechniques.CRESCENT, options=[
    OptionFilter(NightTimeChecksRequireCrescent, NightTimeChecksRequireCrescent.option_true)], filtered_resolution=True)

moon_cave_fire_rule: Rule = Or(has_portable_fire_source,
                               HasAll("Moon Cave - 3F Push the ball", BrushTechniques.INFERNO))
# Fireburst doesn't light the canons' fuse.
moon_cave_canon_rule: Rule = Or(has_portable_fire_source_strict,
                                HasAll("Moon Cave - 3F Push the ball", BrushTechniques.INFERNO))

moon_cave_4f_fire_rule: Rule = Or(has_portable_fire_source,
                                  HasAll("Moon Cave - 4F Move Fireball", BrushTechniques.INFERNO))

oni_island_1f_thunder_rule = Or(has_portable_thunder_source_strict,
                                HasAll("Oni Island - 1F Grab First Thunder Key", BrushTechniques.THUNDERSTORM))

oni_island_5f_thunder_rule = Or(has_portable_thunder_source,
                                HasAll("Oni Island - 4F Grab Thunder Key", BrushTechniques.THUNDERSTORM))


def has_divine_instrument_tier(tier: int) -> Rule:
    # Special Rule for mirrors, if we check for tier 1 weapon, then Divine retribution, elese we check for tier-1 porgressive mirrors.
    if tier == 1:
        progressive_mirror_rule = Has(DivineInstruments.DIVINE_RETRIBUTION.value.item_name)
    else:
        progressive_mirror_rule = Has('Progressive Mirror', count=(tier - 1))

    progressive_weapon_rule = OptionFilter(ProgressiveWeapons, 1) & Or(progressive_mirror_rule,
                                                                       Has("Progressive Sword", count=tier),
                                                                       Has("Progressive Rosary", count=tier))
    match tier:
        case 5:
            return Or(progressive_weapon_rule, HasGroup('divine_instrument_tier_5', count=1))
        case 4:
            return Or(progressive_weapon_rule, Or(
                HasGroup('divine_instrument_tier_4', count=1),
                HasGroup('divine_instrument_tier_5', count=1)))
        case 3:
            return Or(progressive_weapon_rule, Or(
                HasGroup('divine_instrument_tier_3', count=1),
                HasGroup('divine_instrument_tier_4', count=1),
                HasGroup('divine_instrument_tier_5', count=1)))
        case 2:
            return Or(progressive_weapon_rule, Or(HasGroup('divine_instrument_tier_2', count=1),
                                                  HasGroup('divine_instrument_tier_3', count=1),
                                                  HasGroup('divine_instrument_tier_4', count=1),
                                                  HasGroup('divine_instrument_tier_5', count=1)))

        case 1:
            return Or(progressive_weapon_rule, Or(HasGroup('divine_instrument_tier_1', count=1),
                                                  HasGroup('divine_instrument_tier_2', count=1),
                                                  HasGroup('divine_instrument_tier_3', count=1),
                                                  HasGroup('divine_instrument_tier_4', count=1),
                                                  HasGroup('divine_instrument_tier_5', count=1)))


def set_completion_rules(world: "OkamiWorld"):
    world.set_completion_rule(HasAll("Moon Cave - Defeat Orochi", "Oni Island - Defeat Ninetails"))
    return
