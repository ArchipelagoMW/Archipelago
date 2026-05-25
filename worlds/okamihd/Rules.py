from rule_builder.field_resolvers import FromOption
from rule_builder.rules import Has, And, Rule, OptionFilter, Or, HasGroup, HasAny, HasAll
from worlds.AutoWorld import CollectionState
from .Enums.BrushTechniques import BrushTechniques
from .Enums.DivineInstruments import DivineInstruments
from .Enums.LocationType import LocationType
from .Options import ProgressiveWeapons, RequiredDoggorbs, NightTimeChecksRequireCrescent
from .Types import LocData, ExitData, EventData
from BaseClasses import Location, Entrance
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from . import OkamiWorld

has_portable_fire_source: Rule = Or(And(Or(Has(DivineInstruments.SOLAR_FLARE.value.item_name),
                                           Has("Progressive Mirror", 4)), Has(BrushTechniques.INFERNO)),
                                    Has(BrushTechniques.FIREBURST))

has_portable_thunder_source: Rule = Or(And(Or(Has(DivineInstruments.THUNDER_EDGE.value.item_name),
                                              Has("Progressive Sword", 5)), Has(BrushTechniques.THUNDERSTORM)),
                                       Has(BrushTechniques.THUNDERBOLT))

has_portable_ice_source: Rule = Or(And(Or(Has(DivineInstruments.TUNDRA_BEADS.value.item_name),
                                          Has("Progressive Rosary", 5)), Has(BrushTechniques.BLIZZARD)),
                                   Has(BrushTechniques.ICESTORM))

gale_shrine_access: Rule = HasGroup("canine_warriors", count=FromOption(RequiredDoggorbs))

moon_cave_access: Rule = Has("Serpent Crystal")

# Probably should be removed;Directly add it to the checks that require it.
def has_soup_ingerdients(state: CollectionState, world: "OkamiWorld", amount: int) -> bool:
    return state.has_group("soup_ingredients", world.player, amount)


night_time_check_rule: Rule = Has(BrushTechniques.CRESCENT, options=[
    OptionFilter(NightTimeChecksRequireCrescent, NightTimeChecksRequireCrescent.option_true)], filtered_resolution=True)

moon_cave_fire_rule: Rule = Or(has_portable_fire_source,
                               HasAll("Moon Cave - 3F Push the ball", BrushTechniques.INFERNO))
#Fireburst doesn't light the canons' fuse.
moon_cave_canon_rule: Rule = And(
    Or(HasAny(DivineInstruments.SOLAR_FLARE.value.item_name, "Moon Cave - 3F Push the ball"),
       Has("Progressive Mirror", 4)), Has(BrushTechniques.INFERNO))

moon_cave_4f_fire_rule: Rule = Or(has_portable_fire_source,
                                  HasAll("Moon Cave - 4F Move Fireball", BrushTechniques.INFERNO))
# FIXME Once we've figured out which story trigger can spawn the thunder source here
gen_thunder_chest_rule: Rule = has_portable_thunder_source


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


def apply_event_or_location_rules(loc: Location, name: str, data: LocData | EventData, world: "OkamiWorld"):
    ## RULE BUILDER REWORK:
    # - FOR EACH LOCATION, BUILD AN ARRAY OF RULES THAT WILL BE ADDED TO THE world.set_rule(loc,AND(*Rules))

    rules: List[Rule] = []

    required_techinques = []
    required_power_slash_level = data.power_slash_level
    required_cherry_bomb_level = data.cherry_bomb_level

    if len(data.mandatory_enemies) > 0:
        weapon_tier_required = 0
        for e in data.mandatory_enemies:
            weapon_tier_required = max(weapon_tier_required, e.value.required_weapon_tier)
            if len(e.value.required_techniques) > 0:
                required_techinques += e.value.required_techniques
            if e.value.requires_slash:
                required_power_slash_level = max(required_power_slash_level, 1)
            if e.value.requires_bomb:
                required_cherry_bomb_level = max(required_cherry_bomb_level, 1)

        if weapon_tier_required > 0:
            rules.append(has_divine_instrument_tier(weapon_tier_required))

    required_techinques += data.required_brush_techniques

    match data.type:
        case LocationType.TREASURE_BUD:
            required_techinques += [BrushTechniques.GREENSPROUT_BLOOM]
        case LocationType.BURIED_UNDER_LEAF_PILE:
            required_techinques += [BrushTechniques.GALESTORM]
        case LocationType.BURIED_CHEST:
            if world.options.NightTimeChecksRequireCrescent:
                required_techinques += [BrushTechniques.CRESCENT]
        case LocationType.STONE_BURIED_CHEST:
            # FIXME when dojo techniques are handled
            if world.options.NightTimeChecksRequireCrescent:
                required_techinques += [BrushTechniques.CRESCENT]
        case LocationType.BURNING_CHEST:
            rules.append(HasAny(BrushTechniques.GALESTORM, BrushTechniques.WATERSPOUT))
        case LocationType.BURNING_CHEST_NO_WATER:
            required_techinques += [BrushTechniques.GALESTORM]
        case LocationType.UNDERWATER_CHEST:
            required_power_slash_level = max(required_power_slash_level, 1)
        case LocationType.UNDERWATER_CHEST_SHALLOW:
            rules.append(HasAny(BrushTechniques.POWER_SLASH, BrushTechniques.CHERRY_BOMB))
        case LocationType.DIGGING_MINIGAME_EARLY:
            required_power_slash_level = max(required_power_slash_level, 1)
            required_cherry_bomb_level = max(required_cherry_bomb_level, 1)
            required_techinques += [BrushTechniques.GREENSPROUT_BLOOM]
        case LocationType.DIGGING_MINIGAME_LATER:
            required_power_slash_level = max(required_power_slash_level, 1)
            required_cherry_bomb_level = max(required_cherry_bomb_level, 1)
            required_techinques += [BrushTechniques.GREENSPROUT_BLOOM, BrushTechniques.WATERSPOUT,
                                    BrushTechniques.GALESTORM]
        case LocationType.FROZEN_CHEST:
            required_techinques += [BrushTechniques.INFERNO]
        case LocationType.FISHING_MINIGAME:
            required_power_slash_level = max(required_power_slash_level, 1)
        case LocationType.THUNDER_CHEST:
            required_techinques += [BrushTechniques.THUNDERBOLT]

        case _:
            required_techinques += []

    if data.needs_long_swim:
        rules.append(HasAny("Water Tablet", BrushTechniques.GREENSPROUT_WATERLILY))

    if len(required_techinques) > 0:
        rules.append(HasAll(*required_techinques))

    if required_power_slash_level > 0:
        rules.append(Has(BrushTechniques.POWER_SLASH, count=required_power_slash_level))

    if required_cherry_bomb_level > 0:
        rules.append(Has(BrushTechniques.CHERRY_BOMB, count=required_cherry_bomb_level))

    if len(data.required_items_events) > 0:
        rules.append(HasAll(*data.required_items_events))

    if data.special_rule is not None:
        # Append special rule if it's defined
        rules.append(data.special_rule)


    # Set the location to require all concatenated rule
    if len(rules) > 0:
        final_rule = And(*rules)
        world.set_rule(loc, final_rule)


#    print(final_rule)
# else:
#    print("no rule for this check")

def apply_exit_rules(etr: Entrance, name: str, data: ExitData, world: "OkamiWorld"):
    rules: List[Rule] = []
    if data.needs_long_swim:
        rules.append(HasAny("Water Tablet", BrushTechniques.GREENSPROUT_WATERLILY))

    if len(data.has_events) > 0:
        rules.append(HasAll(*data.has_events))

    if len(rules) > 0:

        final_rule = And(*rules)
        world.set_rule(etr, final_rule)


def set_completion_rules(world: "OkamiWorld"):
    world.set_completion_rule(HasAll("Moon Cave - Defeat Orochi", "Gale Shrine - Defeat Crimson Helm","Tsuta Ruins - Defeat the spider queen"))

    return
