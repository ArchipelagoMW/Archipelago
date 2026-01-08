from collections import Counter
from typing import TYPE_CHECKING, Callable
from collections import Counter

from BaseClasses import CollectionState, ItemClassification as IC, MultiWorld
from .Locations import SohLocation
from worlds.generic.Rules import set_rule
from worlds.AutoWorld import LogicMixin
from .Enums import *
from .Items import SohItem, item_data_table, ItemType, no_rules_bottles

if TYPE_CHECKING:
    from . import SohWorld

import logging
logger = logging.getLogger("SOH_OOT.Logic")


class rule_wrapper:
    def __init__(self, parent_region: Regions, rule: Callable[[tuple[CollectionState, Regions, "SohWorld"]], bool], world: "SohWorld"):
        self.parent_region = parent_region
        self.world = world
        self.rule = rule

    @staticmethod
    def wrap(parent_region: Regions, rule: Callable[[tuple[CollectionState, Regions, "SohWorld"]], bool], world: "SohWorld") -> Callable[[CollectionState], bool]:
        wrapper = rule_wrapper(parent_region, rule, world)
        return wrapper.evaluate

    def evaluate(self, state: CollectionState) -> bool:
        return self.rule((state, self.parent_region, self.world))


def add_locations(parent_region: Regions, world: "SohWorld",
                  locations: list[tuple[Locations, Callable[[tuple[CollectionState, Regions, "SohWorld"]], bool]]]) -> None:
    for location in locations:
        locationName = location[0]
        def locationRule(bundle): return True
        if len(location) > 1:
            locationRule = location[1]  # type: ignore # noqa
        if locationName in world.included_locations:
            locationAddress = world.included_locations.pop(location[0])
            world.get_region(parent_region).add_locations(
                {str(locationName): locationAddress}, SohLocation)
            set_rule(world.get_location(locationName),
                     rule_wrapper.wrap(parent_region, locationRule, world))


def connect_regions(parent_region: Regions, world: "SohWorld",
                    child_regions: list[tuple[Regions, Callable[[tuple[CollectionState, Regions, "SohWorld"]], bool]]]) -> None:
    for region in child_regions:
        regionName = region[0]
        def regionRule(bundle): return True
        if len(region) > 1:
            regionRule = region[1]  # type: ignore # noqa
        world.get_region(parent_region).connect(world.get_region(regionName),
                                                rule=rule_wrapper.wrap(parent_region, regionRule, world))


def add_events(parent_region: Regions, world: "SohWorld",
               events: list[tuple[StrEnum, Events | StrEnum, Callable[[tuple[CollectionState, Regions, "SohWorld"]], bool]]]) -> None:
    for event in events:
        event_location = event[0]
        event_item = event[1]
        event_rule = event[2]

        world.get_region(parent_region).add_locations(
            {event_location: None}, SohLocation)
        world.get_location(event_location).place_locked_item(
            SohItem(event_item, IC.progression, None, world.player))
        set_rule(world.get_location(event_location),
                 rule_wrapper.wrap(parent_region, event_rule, world))


def can_use(item: Items, bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    if not has_item(item, bundle):
        return False

    data = item_data_table

    if item in data:
        if data[item].adult_only and not is_adult(bundle):
            return False

        if data[item].child_only and not is_child(bundle):
            return False

        if data[item].item_type == ItemType.magic and not has_item(Items.PROGRESSIVE_MAGIC_METER, bundle):
            return False

        if data[item].item_type == ItemType.song:
            return can_play_song(item, bundle)

    if item in (Items.FIRE_ARROW, Items.ICE_ARROW, Items.LIGHT_ARROW):
        return can_use(Items.FAIRY_BOW, bundle)

    if item in (Items.PROGRESSIVE_BOMBCHU, Items.BOMBCHUS_5, Items.BOMBCHUS_10, Items.BOMBCHUS_20):
        return bombchu_refill(bundle)

    if item == Items.FISHING_POLE:
        return has_item(Items.CHILD_WALLET, bundle)

    if item == Items.EPONA:
        return is_adult(bundle) and can_use(Items.EPONAS_SONG, bundle)

    return True


def can_use_any(names: list[Items], bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    for name in names:
        if can_use(name, bundle):
            return True
    return False


def has_item(item: Items | Events | StrEnum, bundle: tuple[CollectionState, Regions, "SohWorld"], count: int = 1) -> bool:
    state = bundle[0]
    world = bundle[2]
    player = world.player

    if item == Items.STICKS:
        return state.has_all((Events.CAN_FARM_STICKS, Items.DEKU_STICK_BAG), player)

    if item in (Items.PROGRESSIVE_BOMBCHU, Items.BOMBCHUS_5, Items.BOMBCHUS_10, Items.BOMBCHUS_20):
        return bombchus_enabled(bundle)

    if item == Items.NUTS:
        return state.has_all((Events.CAN_FARM_NUTS, Items.DEKU_NUT_BAG), player)

    if item == Items.MAGIC_BEAN:
        return state.has_any({Items.MAGIC_BEAN_PACK, Events.CAN_BUY_BEANS}, player)

    if item == Items.DEKU_SHIELD:
        return state.has(Items.BUY_DEKU_SHIELD, player)

    if item == Items.HYLIAN_SHIELD:
        return state.has(Items.BUY_HYLIAN_SHIELD, player)

    if item == Items.SCARECROW:
        return scarecrows_song(bundle) and can_use(Items.HOOKSHOT, bundle)

    if item == Items.DISTANT_SCARECROW:
        return scarecrows_song(bundle) and can_use(Items.LONGSHOT, bundle)

    if item == Items.FISHING_POLE:
        return (not world.options.shuffle_fishing_pole) or state.has(Items.FISHING_POLE, player)

    if item == Items.EPONA:
        return state.has(Events.FREED_EPONA, player)

    if item in {Items.POCKET_EGG, Items.COJIRO, Items.ODD_MUSHROOM, Items.ODD_POTION, Items.POACHERS_SAW,
                Items.BROKEN_GORONS_SWORD, Items.PRESCRIPTION, Items.EYEBALL_FROG, Items.WORLDS_FINEST_EYEDROPS}:
        return not world.options.shuffle_adult_trade_items or state.has(item, player)

    if item == Items.BOTTLE_WITH_BIG_POE:
        return has_bottle(bundle) and state.has(Events.CAN_DEFEAT_BIG_POE, player)

    if item == Items.BOTTLE_WITH_BLUE_FIRE:
        return has_bottle(bundle) and (state.has(Events.CAN_ACCESS_BLUE_FIRE, player) or state.has(Items.BUY_BLUE_FIRE, player))

    if item == Items.BOTTLE_WITH_BLUE_POTION:
        return has_bottle(bundle) and state.has(Items.BUY_BLUE_POTION, player)

    if item == Items.BOTTLE_WITH_BUGS:
        return has_bottle(bundle) and (state.has(Events.CAN_ACCESS_BUGS, player) or state.has(Items.BUY_BOTTLE_BUG, player))

    if item == Items.BOTTLE_WITH_FAIRY:
        return has_bottle(bundle) and (state.has(Events.CAN_ACCESS_FAIRIES, player) or state.has(Items.BUY_FAIRYS_SPIRIT, player))

    if item == Items.BOTTLE_WITH_FISH:
        return has_bottle(bundle) and (state.has(Events.CAN_ACCESS_FISH, player) or state.has(Items.BUY_FISH, player))

    if item == Items.BOTTLE_WITH_GREEN_POTION:
        return has_bottle(bundle) and state.has(Items.BUY_GREEN_POTION, player)

    if item in (Items.BOTTLE_WITH_MILK, Items.BOTTLE_WITH_POE, Items.BOTTLE_WITH_RED_POTION, Items.EMPTY_BOTTLE):
        return has_bottle(bundle)

    return state.has(item, player, count)


wallet_capacities: dict[Items, int] = {
    Items.CHILD_WALLET: 99,
    Items.ADULT_WALLET: 200,
    Items.GIANT_WALLET: 500,
    Items.TYCOON_WALLET: 999
}


def can_afford(price: int, bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    for wallet, amount in wallet_capacities.items():
        if amount >= price:
            return has_item(wallet, bundle)

    return False


def scarecrows_song(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    state = bundle[0]
    world = bundle[2]
    return ((bool(world.options.skip_scarecrows_song) and has_item(Items.FAIRY_OCARINA, bundle)
            and (ocarina_button_count(bundle) >= 2))
            or (has_item(Events.CHILD_SCARECROW_UNLOCKED, bundle) and has_item(Events.ADULT_SCARECROW_UNLOCKED, bundle)))


def has_bottle(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:  # soup
    return has_bottle_count(bundle, 1)


def has_bottle_count(bundle: tuple[CollectionState, Regions, "SohWorld"], target_count: int) -> bool:
    state = bundle[0]
    world = bundle[2]
    count = 0
    for bottle in no_rules_bottles:
        count += state.count(bottle.value, world.player)
        if count >= target_count:
            return True
    if state.has(Events.DELIVER_LETTER, world.player):
        count += state.count(Items.BOTTLE_WITH_RUTOS_LETTER, world.player)
        if count >= target_count:
            return True
    if state.has(Events.CAN_EMPTY_BIG_POES, world.player):
        count += state.count(Items.BOTTLE_WITH_BIG_POE, world.player)
        if count >= target_count:
            return True
    return False


def bombchu_refill(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    state = bundle[0]
    world = bundle[2]
    return state.has_any([Items.BUY_BOMBCHUS10, Items.BUY_BOMBCHUS20, Events.COULD_PLAY_BOWLING, Events.CARPET_MERCHANT], world.player) or bool(world.options.bombchu_drops)


def bombchus_enabled(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    state = bundle[0]
    world = bundle[2]
    if world.options.bombchu_bag:
        return state.has(Items.PROGRESSIVE_BOMBCHU, world.player)
    return state.has(Items.BOMB_BAG, world.player)


ocarina_buttons_required: dict[str, list[str]] = {
    Items.ZELDAS_LULLABY: [Items.OCARINA_CLEFT_BUTTON, Items.OCARINA_CRIGHT_BUTTON, Items.OCARINA_CUP_BUTTON],
    Items.EPONAS_SONG: [Items.OCARINA_CLEFT_BUTTON, Items.OCARINA_CRIGHT_BUTTON, Items.OCARINA_CUP_BUTTON],
    Items.PRELUDE_OF_LIGHT: [Items.OCARINA_CLEFT_BUTTON, Items.OCARINA_CRIGHT_BUTTON, Items.OCARINA_CUP_BUTTON],
    Items.SARIAS_SONG: [Items.OCARINA_CLEFT_BUTTON, Items.OCARINA_CRIGHT_BUTTON, Items.OCARINA_CDOWN_BUTTON],
    Items.SUNS_SONG: [Items.OCARINA_CRIGHT_BUTTON, Items.OCARINA_CUP_BUTTON, Items.OCARINA_CDOWN_BUTTON],
    Items.SONG_OF_TIME: [Items.OCARINA_A_BUTTON, Items.OCARINA_CRIGHT_BUTTON, Items.OCARINA_CDOWN_BUTTON],
    Items.BOLERO_OF_FIRE: [Items.OCARINA_A_BUTTON, Items.OCARINA_CRIGHT_BUTTON, Items.OCARINA_CDOWN_BUTTON],
    Items.REQUIEM_OF_SPIRIT: [Items.OCARINA_A_BUTTON, Items.OCARINA_CRIGHT_BUTTON, Items.OCARINA_CDOWN_BUTTON],
    Items.SONG_OF_STORMS: [Items.OCARINA_A_BUTTON, Items.OCARINA_CUP_BUTTON, Items.OCARINA_CDOWN_BUTTON],
    Items.MINUET_OF_FOREST: [Items.OCARINA_A_BUTTON, Items.OCARINA_CLEFT_BUTTON, Items.OCARINA_CRIGHT_BUTTON, Items.OCARINA_CUP_BUTTON],
    Items.SERENADE_OF_WATER: [Items.OCARINA_A_BUTTON, Items.OCARINA_CLEFT_BUTTON, Items.OCARINA_CRIGHT_BUTTON, Items.OCARINA_CDOWN_BUTTON],
    Items.NOCTURNE_OF_SHADOW: [Items.OCARINA_A_BUTTON, Items.OCARINA_CLEFT_BUTTON, Items.OCARINA_CRIGHT_BUTTON, Items.OCARINA_CDOWN_BUTTON],
}


def can_play_song(song: StrEnum, bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    state = bundle[0]
    world = bundle[2]
    if not (has_item(Items.FAIRY_OCARINA, bundle) and has_item(song, bundle)):
        return False
    if not world.options.shuffle_ocarina_buttons:
        return True
    else:
        return state.has_all(ocarina_buttons_required[song], world.player)


def has_explosives(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    """Check if Link has access to explosives (bombs or bombchus)."""
    return can_use_any([Items.BOMB_BAG, Items.PROGRESSIVE_BOMBCHU], bundle)


def blast_or_smash(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    """Check if Link can blast or smash obstacles."""
    return has_explosives(bundle) or can_use(Items.MEGATON_HAMMER, bundle)


def blue_fire(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    """Check if Link has access to blue fire."""
    world = bundle[2]
    return ((has_bottle(bundle) and
             (has_item(Events.CAN_ACCESS_BLUE_FIRE, bundle) or
              has_item(Items.BUY_BLUE_FIRE, bundle))) or
            (can_use(Items.ICE_ARROW, bundle) and
             bool(world.options.blue_fire_arrows)))


def can_use_sword(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    """Check if Link can use any sword."""
    return can_use_any([Items.KOKIRI_SWORD, Items.MASTER_SWORD, Items.BIGGORONS_SWORD], bundle)


def has_projectile(bundle: tuple[CollectionState, Regions, "SohWorld"], age: Ages = Ages.null) -> bool:
    """Check if Link has access to projectiles."""
    if has_explosives(bundle):
        return True

    if age == Ages.CHILD:
        return can_use_any([Items.FAIRY_SLINGSHOT, Items.BOOMERANG], bundle)
    elif age == Ages.ADULT:
        return can_use_any([Items.HOOKSHOT, Items.FAIRY_BOW], bundle)
    else:  # "either"
        return can_use_any([Items.FAIRY_SLINGSHOT, Items.BOOMERANG, Items.HOOKSHOT, Items.FAIRY_BOW], bundle)


def can_use_projectile(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    return has_projectile(bundle)


def can_break_mud_walls(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    return blast_or_smash(bundle) or (can_do_trick(Tricks.BLUE_FIRE_MUD_WALLS, bundle) and blue_fire(bundle))


def can_get_deku_baba_sticks(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    return can_use_sword(bundle) or can_use(Items.BOOMERANG, bundle)


def can_get_deku_baba_nuts(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    return can_use_any([Items.FAIRY_SLINGSHOT, Items.FAIRY_BOW, Items.DINS_FIRE], bundle) or can_jump_slash(bundle) or has_explosives(bundle)


def is_adult(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    state = bundle[0]
    parent_region = bundle[1]
    world = bundle[2]
    return state._soh_can_reach_as_age(parent_region, Ages.ADULT, world.player)  # type: ignore # noqa


def at_day(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    return ((is_child(bundle) and has_item(Events.CHILD_CAN_PASS_TIME, bundle))
            or (is_adult(bundle) and has_item(Events.ADULT_CAN_PASS_TIME, bundle)))
    # TODO: Implement starting time of day if that ever gets added


def at_night(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    return ((is_child(bundle) and has_item(Events.CHILD_CAN_PASS_TIME, bundle))
            or (is_adult(bundle) and has_item(Events.ADULT_CAN_PASS_TIME, bundle)))
    # TODO: Implement starting time of day if that ever gets added


def is_child(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    state = bundle[0]
    parent_region = bundle[1]
    world = bundle[2]
    return state._soh_can_reach_as_age(parent_region, Ages.CHILD, world.player)  # type: ignore # noqa


def starting_age(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    world = bundle[2]
    return (world.options.starting_age == 'child' and is_child(bundle)) or (world.options.starting_age == 'adult' and is_adult(bundle))


def can_damage(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    """Check if Link can deal damage to enemies."""
    return (can_jump_slash(bundle) or
            has_explosives(bundle) or
            can_use_any([Items.FAIRY_SLINGSHOT, Items.FAIRY_BOW, Items.DINS_FIRE], bundle))


def can_attack(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    """Check if Link can attack enemies (damage or stun)."""
    return (can_damage(bundle) or
            can_use_any([Items.BOOMERANG, Items.HOOKSHOT], bundle))


def can_standing_shield(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    """Check if Link can use a shield for standing blocks."""
    return (can_use_any([Items.MIRROR_SHIELD, Items.DEKU_SHIELD], bundle) or
            (is_adult(bundle) and can_use(Items.HYLIAN_SHIELD, bundle)))


def can_shield(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    """Check if Link can use a shield for blocking or stunning."""
    return can_use_any([Items.MIRROR_SHIELD, Items.HYLIAN_SHIELD, Items.DEKU_SHIELD], bundle)


def take_damage(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    return (can_use_any([Items.BOTTLE_WITH_FAIRY, Items.NAYRUS_LOVE], bundle)
            or effective_health(bundle) != 1)


def can_do_trick(trick: Tricks, bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    # TODO: Implement specific trick logic based on world settings
    # For now, return False for safety (no tricks assumed)
    return False


def can_get_nighttime_gs(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    world = bundle[2]
    return at_night(bundle) and (not world.options.skulls_sun_song or can_use(Items.SUNS_SONG, bundle))


def can_break_pots(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    """Check if Link can break pots for items."""
    return True


def can_break_crates(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    """Check if Link can break crates."""
    return True


def can_break_small_crates(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    """Check if Link can break small crates."""
    return True


def can_bonk_trees(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    """Check if Link can bonk trees."""
    return True


def can_hit_eye_targets(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    """Check if Link can hit eye switches/targets."""
    return can_use_any([Items.FAIRY_BOW, Items.FAIRY_SLINGSHOT], bundle)


def can_stun_deku(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    """Check if Link can stun Deku Scrubs."""
    return can_attack(bundle) or can_use(Items.NUTS, bundle) or can_reflect_nuts(bundle)


def can_reflect_nuts(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    """Check if Link can reflect Deku Nuts back at enemies."""
    return can_use(Items.DEKU_SHIELD, bundle) or (is_adult(bundle) and has_item(Items.HYLIAN_SHIELD, bundle))


def has_fire_source_with_torch(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    """Check if Link has a fire source that can be used with a torch."""
    return has_fire_source(bundle) or can_use(Items.STICKS, bundle)


def has_fire_source(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    """Check if Link has any fire source."""
    return can_use_any([Items.DINS_FIRE, Items.FIRE_ARROW], bundle)


def can_jump_slash_except_hammer(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    """Check if Link can perform a jump slash with any sword."""
    return can_use(Items.STICKS, bundle) or can_use_sword(bundle)


def can_jump_slash(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    """Check if Link can perform a jump slash at all"""
    return can_jump_slash_except_hammer(bundle) or can_use(Items.MEGATON_HAMMER, bundle)


def call_gossip_fairy_except_suns(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    return can_use_any([Items.ZELDAS_LULLABY, Items.EPONAS_SONG, Items.SONG_OF_TIME], bundle)


def call_gossip_fairy(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    return (call_gossip_fairy_except_suns(bundle) or
            can_use(Items.SUNS_SONG, bundle))


def can_break_lower_hives(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    return can_break_upper_beehives(bundle) or can_use(Items.BOMB_BAG, bundle)


def can_break_upper_beehives(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    world = bundle[2]
    return (hookshot_or_boomerang(bundle) or
            (can_do_trick(Tricks.BOMBCHU_BEEHIVES, bundle) and can_use(Items.PROGRESSIVE_BOMBCHU, bundle)) or
            (bool(world.options.slingbow_break_beehives) and (can_use_any([Items.FAIRY_BOW, Items.FAIRY_SLINGSHOT], bundle))))


def can_open_storms_grotto(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    return (can_use(Items.SONG_OF_STORMS, bundle) and
            (has_item(Items.STONE_OF_AGONY, bundle)
             or can_do_trick(Tricks.GROTTOS_WITHOUT_AGONY, bundle)))


def can_hit_at_range(bundle: tuple[CollectionState, Regions, "SohWorld"],
                     distance: EnemyDistance = EnemyDistance.CLOSE,
                     wall_or_floor: bool = True, in_water: bool = False) -> bool:
    if distance == EnemyDistance.CLOSE and can_use(Items.MEGATON_HAMMER, bundle):
        return True
    if distance <= EnemyDistance.SHORT_JUMPSLASH and can_use(Items.KOKIRI_SWORD, bundle):
        return True
    if distance <= EnemyDistance.MASTER_SWORD_JUMPSLASH and can_use(Items.MASTER_SWORD, bundle):
        return True
    if distance <= EnemyDistance.LONG_JUMPSLASH and can_use_any([Items.BIGGORONS_SWORD, Items.STICKS], bundle):
        return True
    if distance <= EnemyDistance.BOMB_THROW and (not in_water and can_use(Items.BOMB_BAG, bundle)):
        return True
    if distance <= EnemyDistance.HOOKSHOT and (can_use(Items.HOOKSHOT, bundle)
                                               or (wall_or_floor and can_use(Items.BOMBCHUS_5, bundle))):
        return True
    if distance <= EnemyDistance.LONGSHOT and can_use(Items.LONGSHOT, bundle):
        return True
    if distance <= EnemyDistance.FAR and can_use_any([Items.FAIRY_SLINGSHOT, Items.FAIRY_BOW], bundle):
        return True
    return False


def can_kill_enemy(bundle: tuple[CollectionState, Regions, "SohWorld"], enemy: Enemies, distance: EnemyDistance = EnemyDistance.CLOSE,
                   wall_or_floor: bool = True, quantity: int = 1, timer: bool = False, in_water: bool = False) -> bool:
    """
    Check if Link can kill a specific enemy at a given combat range.
    Based on the C++ Logic::CanKillEnemy implementation.

    Args:
        bundle: The standard bundle of state, regions, and the world class
        enemy: Enemy type (e.g., "gold_skulltula", "keese", etc.)
        distance: Combat range - "close", "short_jumpslash", "master_sword_jumpslash",
                     "long_jumpslash", "bomb_throw", "boomerang", "hookshot", "longshot", "far"
        wall_or_floor: Whether enemy is on wall or floor
        quantity: Number of enemies (for ammo considerations)
        timer: Whether there's a timer constraint
        in_water: Whether the fight is underwater
    """

    # Enemy-specific logic based on C++ implementation

    if enemy in [Enemies.GERUDO_GUARD, Enemies.BREAK_ROOM_GUARD]:
        return False

    if enemy == Enemies.GOLD_SKULLTULA:
        return (can_hit_at_range(bundle, distance, wall_or_floor, in_water)
                or (distance <= EnemyDistance.LONGSHOT and wall_or_floor and can_use(Items.BOMBCHUS_5, bundle))
                or (distance <= EnemyDistance.BOOMERANG and can_use_any([Items.DINS_FIRE, Items.BOOMERANG], bundle)))

    if enemy == Enemies.BIG_SKULLTULA:
        return (can_hit_at_range(bundle, distance, wall_or_floor, in_water)
                or (distance <= EnemyDistance.BOOMERANG and can_use(Items.DINS_FIRE, bundle)))

    if enemy in [Enemies.GOHMA_LARVA, Enemies.MAD_SCRUB, Enemies.DEKU_BABA]:
        return can_attack(bundle)

    if enemy == Enemies.DODONGO:
        return (can_use_sword(bundle)
                or can_use_any([Items.MEGATON_HAMMER, Items.FAIRY_SLINGSHOT, Items.FAIRY_BOW], bundle)
                or (quantity <= 5 and can_use(Items.STICKS, bundle))
                or has_explosives(bundle))

    if enemy == Enemies.LIZALFOS:
        return (can_jump_slash(bundle)
                or can_use_any([Items.FAIRY_BOW, Items.FAIRY_SLINGSHOT], bundle)
                or has_explosives(bundle))

    if enemy in [Enemies.KEESE, Enemies.FIRE_KEESE]:
        return (can_hit_at_range(bundle, distance, wall_or_floor, in_water)
                or (distance == EnemyDistance.CLOSE and can_use(Items.KOKIRI_SWORD, bundle))
                or (distance <= EnemyDistance.BOOMERANG and can_use(Items.BOOMERANG, bundle))
                or (distance == EnemyDistance.SHORT_JUMPSLASH and can_use(Items.MEGATON_HAMMER, bundle)))

    if enemy == Enemies.BLUE_BUBBLE:
        return blast_or_smash(bundle) or can_use(Items.FAIRY_BOW, bundle) or \
            ((can_jump_slash_except_hammer(bundle) or can_use(Items.FAIRY_SLINGSHOT, bundle)) and
             (can_use(Items.NUTS, bundle) or hookshot_or_boomerang(bundle) or can_standing_shield(bundle)))

    if enemy == Enemies.DEAD_HAND:
        return can_use_sword(bundle) or (can_use(Items.STICKS, bundle) and can_do_trick(Tricks.BOTW_CHILD_DEADHAND, bundle))

    if enemy == Enemies.WITHERED_DEKU_BABA:
        return can_attack(bundle) or can_use(Items.BOOMERANG, bundle)

    if enemy in [Enemies.LIKE_LIKE, Enemies.FLOORMASTER]:
        return can_damage(bundle)

    if enemy == Enemies.STALFOS:
        if distance <= EnemyDistance.SHORT_JUMPSLASH and can_use_any([Items.MEGATON_HAMMER, Items.KOKIRI_SWORD], bundle):
            return True
        if distance <= EnemyDistance.MASTER_SWORD_JUMPSLASH and can_use(Items.MASTER_SWORD, bundle):
            return True
        if (distance <= EnemyDistance.LONG_JUMPSLASH
                and (can_use(Items.BIGGORONS_SWORD, bundle) or (quantity <= 1 and can_use(Items.STICKS, bundle)))):
            return True
        if distance <= EnemyDistance.BOMB_THROW and quantity <= 2 and not timer and not in_water and \
                (can_use(Items.NUTS, bundle) or hookshot_or_boomerang(bundle)) and can_use(Items.BOMB_BAG, bundle):
            return True
        if distance <= EnemyDistance.HOOKSHOT and wall_or_floor and can_use(Items.BOMBCHUS_5, bundle):
            return True
        if distance <= EnemyDistance.FAR and can_use(Items.FAIRY_BOW, bundle):
            return True
        return False

    if enemy == Enemies.IRON_KNUCKLE:
        return (can_use_sword(bundle) or
                can_use(Items.MEGATON_HAMMER, bundle) or
                has_explosives(bundle))

    if enemy == Enemies.FLARE_DANCER:
        return (can_use_any([Items.MEGATON_HAMMER, Items.HOOKSHOT], bundle)
                or (has_explosives(bundle)
                    and (can_jump_slash_except_hammer(bundle)
                         or can_use_any([Items.FAIRY_BOW, Items.FAIRY_SLINGSHOT, Items.BOOMERANG], bundle))))

    if enemy in [Enemies.WOLFOS, Enemies.WHITE_WOLFOS, Enemies.WALLMASTER]:
        return (can_jump_slash(bundle)
                or can_use_any([Items.FAIRY_BOW, Items.FAIRY_SLINGSHOT, Items.BOMBCHUS_5, Items.DINS_FIRE], bundle)
                or (can_use(Items.BOMB_BAG, bundle)
                    and can_use_any([Items.NUTS, Items.HOOKSHOT, Items.BOOMERANG], bundle)))

    if enemy == Enemies.GERUDO_WARRIOR:
        return can_jump_slash(bundle) or can_use(Items.FAIRY_BOW, bundle) or \
            (can_do_trick(Tricks.GF_WARRIOR_WITH_DIFFICULT_WEAPON, bundle) and
             can_use_any([Items.FAIRY_SLINGSHOT, Items.BOMBCHUS_5], bundle))

    if enemy in [Enemies.GIBDO, Enemies.REDEAD]:
        return can_jump_slash(bundle) or can_use(Items.DINS_FIRE, bundle)

    if enemy == Enemies.MEG:
        return can_use_any([Items.FAIRY_BOW, Items.HOOKSHOT], bundle) or has_explosives(bundle)

    if enemy == Enemies.ARMOS:
        return (blast_or_smash(bundle)
                or can_use_any([Items.MASTER_SWORD, Items.BIGGORONS_SWORD, Items.STICKS, Items.FAIRY_BOW], bundle)
                or (can_use_any([Items.NUTS, Items.HOOKSHOT, Items.BOOMERANG], bundle)
                    and can_use_any([Items.KOKIRI_SWORD, Items.FAIRY_SLINGSHOT], bundle)))

    if enemy == Enemies.GREEN_BUBBLE:
        return (can_jump_slash(bundle)
                or can_use_any([Items.FAIRY_BOW, Items.FAIRY_SLINGSHOT], bundle)
                or has_explosives(bundle))

    if enemy == Enemies.DINOLFOS:
        return can_jump_slash(bundle) or can_use_any([Items.FAIRY_BOW, Items.FAIRY_SLINGSHOT], bundle) or \
            (not timer and can_use(Items.BOMBCHUS_5, bundle))

    if enemy == Enemies.TORCH_SLUG:
        return can_jump_slash(bundle) or has_explosives(bundle) or can_use(Items.FAIRY_BOW, bundle)

    if enemy == Enemies.FREEZARD:
        return (can_use_any([Items.MASTER_SWORD, Items.BIGGORONS_SWORD, Items.MEGATON_HAMMER, Items.STICKS,
                             Items.HOOKSHOT, Items.DINS_FIRE, Items.FIRE_ARROW], bundle)
                or has_explosives(bundle))

    if enemy == Enemies.SHELL_BLADE:
        return (can_jump_slash(bundle) or has_explosives(bundle)
                or can_use_any([Items.HOOKSHOT, Items.FAIRY_BOW, Items.DINS_FIRE], bundle))

    if enemy == Enemies.SPIKE:
        return (can_use_any([Items.MASTER_SWORD, Items.BIGGORONS_SWORD, Items.MEGATON_HAMMER, Items.STICKS,
                            Items.HOOKSHOT, Items.FAIRY_BOW, Items.DINS_FIRE], bundle)
                or has_explosives(bundle))

    if enemy == Enemies.STINGER:
        return (can_hit_at_range(bundle, distance, wall_or_floor, in_water)
                or (distance == EnemyDistance.SHORT_JUMPSLASH and can_use(Items.MEGATON_HAMMER, bundle)))

    if enemy == Enemies.BIG_OCTO:
        # If chasing octo is annoying but with rolls you can catch him, and you need rang to get into this room
        # without shenanigans anyway. Bunny makes it free
        # todo: should this have biggoron sword too?
        return can_use_any([Items.KOKIRI_SWORD, Items.STICKS, Items.MASTER_SWORD], bundle)

    if enemy == Enemies.GOHMA:
        return has_boss_soul(Items.GOHMAS_SOUL, bundle) and can_jump_slash(bundle) and \
            (can_use_any([Items.NUTS, Items.FAIRY_SLINGSHOT, Items.FAIRY_BOW], bundle)
             or hookshot_or_boomerang(bundle))

    if enemy == Enemies.KING_DODONGO:
        return (has_boss_soul(Items.KING_DODONGOS_SOUL, bundle) and can_jump_slash(bundle) and
                (can_use_any([Items.BOMB_BAG, Items.GORONS_BRACELET], bundle) or
                 (can_do_trick(Tricks.DC_DODONGO_CHU, bundle) and is_adult(bundle) and can_use(Items.BOMBCHUS_5, bundle))))

    if enemy == Enemies.BARINADE:
        return (has_boss_soul(Items.BARINADES_SOUL, bundle)
                and can_use(Items.BOOMERANG, bundle) and can_jump_slash_except_hammer(bundle))

    if enemy == Enemies.PHANTOM_GANON:
        return (has_boss_soul(Items.PHANTOM_GANONS_SOUL, bundle) and can_use_sword(bundle)
                and can_use_any([Items.HOOKSHOT, Items.FAIRY_BOW, Items.FAIRY_SLINGSHOT], bundle))

    if enemy == Enemies.VOLVAGIA:
        return has_boss_soul(Items.VOLVAGIAS_SOUL, bundle) and can_use(Items.MEGATON_HAMMER, bundle)

    if enemy == Enemies.MORPHA:
        return (has_boss_soul(Items.MORPHAS_SOUL, bundle) and
                (can_use(Items.HOOKSHOT, bundle) or
                (can_do_trick(Tricks.WATER_MORPHA_WITHOUT_HOOKSHOT, bundle) and has_item(Items.BRONZE_SCALE, bundle))) and
                (can_use_sword(bundle) or can_use(Items.MEGATON_HAMMER, bundle)))

    if enemy == Enemies.BONGO_BONGO:
        return has_boss_soul(Items.BONGO_BONGOS_SOUL, bundle) and \
            (can_use(Items.LENS_OF_TRUTH, bundle) or can_do_trick(Tricks.LENS_BONGO, bundle)) and can_use_sword(bundle) and \
            (can_use_any([Items.HOOKSHOT, Items.FAIRY_BOW, Items.FAIRY_SLINGSHOT], bundle) or
                can_do_trick(Tricks.SHADOW_BONGO, bundle))

    if enemy == Enemies.TWINROVA:
        return has_boss_soul(Items.TWINROVAS_SOUL, bundle) and can_use(Items.MIRROR_SHIELD, bundle) and \
            (can_use_sword(bundle) or can_use(Items.MEGATON_HAMMER, bundle))

    if enemy == Enemies.GANONDORF:
        # RANDOTODO: Trick to use hammer (no jumpslash) or stick (only jumpslash) instead of a sword to reflect the
        # energy ball and either of them regardless of jumpslashing to damage and kill ganondorf

        # Bottle is not taken into account since a sword, hammer or stick are required
        # for killing ganondorf and all of those can reflect the energy ball
        # This will not be the case once ammo logic in taken into account as
        # sticks are limited and using a bottle might become a requirement in that case
        return has_boss_soul(Items.GANONS_SOUL, bundle) and can_use(Items.LIGHT_ARROW, bundle) and can_use_sword(bundle)

    if enemy == Enemies.GANON:
        return has_boss_soul(Items.GANONS_SOUL, bundle) and can_use(Items.MASTER_SWORD, bundle)

    if enemy == Enemies.DARK_LINK:
        # RANDOTODO Dark link is buggy right now, retest when he is not
        return can_jump_slash(bundle) or can_use(Items.FAIRY_BOW, bundle)

    if enemy == Enemies.ANUBIS:
        # there's a restoration that allows beating them with mirror shield + some way to trigger their attack
        return has_fire_source(bundle)

    if enemy == Enemies.BEAMOS:
        return has_explosives(bundle)

    if enemy == Enemies.PURPLE_LEEVER:
        # dies on its own, so this is the conditions to spawn it (killing 10 normal leevers)
        # Sticks and Ice arrows work but will need ammo capacity logic
        # other methods can damage them but not kill them, and they run when hit, making them impractical
        return can_use_any([Items.MASTER_SWORD, Items.BIGGORONS_SWORD], bundle)

    if enemy == Enemies.TENTACLE:
        return can_use(Items.BOOMERANG, bundle)

    if enemy == Enemies.BARI:
        return (hookshot_or_boomerang(bundle)
                or can_use_any([Items.FAIRY_BOW, Items.STICKS, Items.MEGATON_HAMMER, Items.DINS_FIRE], bundle)
                or has_explosives(bundle)
                or (take_damage(bundle) and can_use_sword(bundle)))

    if enemy == Enemies.SHABOM:
        # RANDOTODO when you add better damage logic, you can kill this by taking hits
        return (can_use_any([Items.BOOMERANG, Items.NUTS, Items.DINS_FIRE, Items.ICE_ARROW], bundle)
                or can_jump_slash(bundle))

    if enemy == Enemies.OCTOROK:
        return (can_reflect_nuts(bundle) or hookshot_or_boomerang(bundle)
                or can_use_any([Items.FAIRY_BOW, Items.FAIRY_SLINGSHOT, Items.BOMB_BAG], bundle)
                or (wall_or_floor and can_use(Items.BOMBCHUS_5, bundle)))

    return False


def has_boss_soul(soul: Items, bundle: tuple[CollectionState, Regions, "SohWorld"]):
    world = bundle[2]
    soulsanity = world.options.shuffle_boss_souls
    if not soulsanity:
        return True
    if soul == Items.GANONS_SOUL and soulsanity == "on":
        return True
    return has_item(soul, bundle)


def can_pass_enemy(bundle: tuple[CollectionState, Regions, "SohWorld"], enemy: Enemies,
                   distance: EnemyDistance = EnemyDistance.CLOSE, wall_or_floor: bool = True) -> bool:
    if enemy in {Enemies.GOLD_SKULLTULA, Enemies.GOHMA_LARVA, Enemies.LIZALFOS, Enemies.DODONGO, Enemies.MAD_SCRUB,
                 Enemies.KEESE, Enemies.FIRE_KEESE, Enemies.BLUE_BUBBLE, Enemies.DEAD_HAND, Enemies.DEKU_BABA,
                 Enemies.WITHERED_DEKU_BABA, Enemies.STALFOS, Enemies.FLARE_DANCER, Enemies.WOLFOS,
                 Enemies.WHITE_WOLFOS, Enemies.FLOORMASTER, Enemies.MEG, Enemies.ARMOS, Enemies.FREEZARD, Enemies.SPIKE,
                 Enemies.DARK_LINK, Enemies.ANUBIS, Enemies.WALLMASTER, Enemies.PURPLE_LEEVER, Enemies.OCTOROK}:
        return True

    if enemy == Enemies.GERUDO_GUARD:
        return (can_do_trick(Tricks.PASS_GUARDS_WITH_NOTHING, bundle)
                or has_item(Items.GERUDO_MEMBERSHIP_CARD, bundle)
                or can_use_any([Items.FAIRY_BOW, Items.HOOKSHOT], bundle))

    if enemy == Enemies.BREAK_ROOM_GUARD:
        return (has_item(Items.GERUDO_MEMBERSHIP_CARD, bundle)
                or can_use_any([Items.FAIRY_BOW, Items.HOOKSHOT], bundle))

    if enemy == Enemies.BIG_SKULLTULA:
        return (can_kill_enemy(bundle, enemy, distance, wall_or_floor)
                or can_use_any([Items.NUTS, Items.BOOMERANG], bundle))

    if enemy == Enemies.LIKE_LIKE:
        return (can_kill_enemy(bundle, enemy, distance, wall_or_floor)
                or can_use_any([Items.HOOKSHOT, Items.BOOMERANG], bundle))

    if enemy in [Enemies.GIBDO, Enemies.REDEAD]:
        return (can_kill_enemy(bundle, enemy, distance, wall_or_floor)
                or can_use_any([Items.HOOKSHOT, Items.SUNS_SONG], bundle))

    if enemy in [Enemies.IRON_KNUCKLE, Enemies.BIG_OCTO]:
        return can_kill_enemy(bundle, enemy, distance, wall_or_floor)

    if enemy == Enemies.GREEN_BUBBLE:
        return (can_kill_enemy(bundle, enemy, distance, wall_or_floor)
                or take_damage(bundle)
                or can_use_any([Items.NUTS, Items.BOOMERANG, Items.HOOKSHOT], bundle))

    return can_kill_enemy(bundle, enemy, distance, wall_or_floor)


def can_cut_shrubs(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    """Check if Link can cut shrubs (grass, bushes)."""
    return (can_use_sword(bundle) or
            has_explosives(bundle) or
            can_use_any([Items.BOOMERANG, Items.GORONS_BRACELET, Items.MEGATON_HAMMER], bundle))


def hookshot_or_boomerang(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    """Check if Link has hookshot or boomerang."""
    return can_use_any([Items.HOOKSHOT, Items.BOOMERANG], bundle)


def can_open_underwater_chest(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    return (can_do_trick(Tricks.OPEN_UNDERWATER_CHEST, bundle) and
            can_use(Items.IRON_BOOTS, bundle) and
            can_use(Items.HOOKSHOT, bundle))


def can_open_overworld_door(key: Items, bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    world = bundle[2]
    if not world.options.lock_overworld_doors:
        return True

    return has_item(Items.SKELETON_KEY, bundle) or has_item(key, bundle)


key_to_ring: dict[Items, Items] = {
    Items.FOREST_TEMPLE_SMALL_KEY: Items.FOREST_TEMPLE_KEY_RING,
    Items.FIRE_TEMPLE_SMALL_KEY: Items.FIRE_TEMPLE_KEY_RING,
    Items.WATER_TEMPLE_SMALL_KEY: Items.WATER_TEMPLE_KEY_RING,
    Items.BOTTOM_OF_THE_WELL_SMALL_KEY: Items.BOTTOM_OF_THE_WELL_KEY_RING,
    Items.SHADOW_TEMPLE_SMALL_KEY: Items.SHADOW_TEMPLE_KEY_RING,
    Items.GERUDO_FORTRESS_SMALL_KEY: Items.GERUDO_FORTRESS_KEY_RING,
    Items.TRAINING_GROUND_SMALL_KEY: Items.TRAINING_GROUND_KEY_RING,
    Items.SPIRIT_TEMPLE_SMALL_KEY: Items.SPIRIT_TEMPLE_KEY_RING,
    Items.GANONS_CASTLE_SMALL_KEY: Items.GANONS_CASTLE_KEY_RING,
}


def small_keys(key: Items, requiredAmount: int, bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    state = bundle[0]
    world = bundle[2]
    return (state.has_any((Items.SKELETON_KEY, key_to_ring[key]), world.player)
            or state.has(key, world.player, requiredAmount))


def can_get_enemy_drop(bundle: tuple[CollectionState, Regions, "SohWorld"], enemy: Enemies,
                       distance: EnemyDistance = EnemyDistance.CLOSE, aboveLink: bool = False) -> bool:
    if not can_kill_enemy(bundle, enemy, distance):
        return False

    if distance.value <= EnemyDistance.MASTER_SWORD_JUMPSLASH.value:
        return True

    match enemy:
        case Enemies.GOLD_SKULLTULA:
            if distance <= EnemyDistance.BOOMERANG and can_use(Items.BOOMERANG, bundle):
                return True
            if distance <= EnemyDistance.HOOKSHOT and can_use(Items.HOOKSHOT, bundle):
                return True
            if distance <= EnemyDistance.LONGSHOT and can_use(Items.LONGSHOT, bundle):
                return True
            return False
        case Enemies.KEESE:
            return True
        case Enemies.FIRE_KEESE:
            return True
        case _:
            return aboveLink or (distance.value <= EnemyDistance.BOOMERANG.value and can_use(Items.BOOMERANG, bundle))


def can_detonate_bomb_flowers(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    return can_use_any([Items.FAIRY_BOW, Items.DINS_FIRE], bundle) or has_explosives(bundle)


def can_detonate_upright_bomb_flower(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    return (can_detonate_bomb_flowers(bundle)
            or has_item(Items.GORONS_BRACELET, bundle)
            or (can_do_trick(Tricks.BLUE_FIRE_MUD_WALLS, bundle)
                and blue_fire(bundle)
                and (effective_health(bundle) != 1
                     or can_use(Items.NAYRUS_LOVE, bundle))))


def item_group_count(bundle: tuple[CollectionState, Regions, "SohWorld"], item_group: str) -> int:
    state = bundle[0]
    world = bundle[2]
    return state.count_group_unique(item_group, world.player)


def ocarina_button_count(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> int:
    world = bundle[2]
    if world.options.shuffle_ocarina_buttons:
        return item_group_count(bundle, "Ocarina Buttons")
    return 5


def stone_count(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> int:
    return item_group_count(bundle, "Stones")


def medallion_count(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> int:
    return item_group_count(bundle, "Medallions")


dungeon_events: list[Events] = [Events.DEKU_TREE_COMPLETED, Events.DODONGOS_CAVERN_COMPLETED,
                                Events.JABU_JABUS_BELLY_COMPLETED, Events.FOREST_TEMPLE_COMPLETED,
                                Events.FIRE_TEMPLE_COMPLETED, Events.WATER_TEMPLE_COMPLETED,
                                Events.SPIRIT_TEMPLE_COMPLETED, Events.SHADOW_TEMPLE_COMPLETED]


def dungeon_count(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> int:
    count = 0
    for dungeon in dungeon_events:
        if has_item(dungeon, bundle):
            count += 1
    return count


def can_spawn_soil_skull(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    return is_child(bundle) and can_use(Items.BOTTLE_WITH_BUGS, bundle)


def fire_timer(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> int:
    return 255 if can_use(Items.GORON_TUNIC, bundle) else ((hearts(bundle) * 8) if can_do_trick(Tricks.FEWER_TUNIC_REQUIREMENTS, bundle) else 0)


def water_timer(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> int:
    return 255 if can_use(Items.ZORA_TUNIC, bundle) else ((hearts(bundle) * 8) if can_do_trick(Tricks.FEWER_TUNIC_REQUIREMENTS, bundle) else 0)


def hearts(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> int:
    state = bundle[0]
    world = bundle[2]
    return state.soh_heart_count[world.player]  # type: ignore


def can_open_bomb_grotto(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    return blast_or_smash(bundle) and (has_item(Items.STONE_OF_AGONY, bundle) or can_do_trick(Tricks.GROTTOS_WITHOUT_AGONY, bundle))


def trade_quest_step(item: Items, bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    world = bundle[2]
    # If adult trade shuffle is off, it'll automatically assume the whole trade quest is complete as soon as claim check is obtained.
    if not world.options.shuffle_adult_trade_items:
        return has_item(Items.CLAIM_CHECK, bundle)

    # Items aren't comparable, so recursion is used to replace fallthrough here
    if item == Items.POCKET_EGG:
        return has_item(Items.POCKET_EGG, bundle) or trade_quest_step(Items.COJIRO, bundle)

    if item == Items.COJIRO:
        return has_item(Items.COJIRO, bundle) or trade_quest_step(Items.ODD_MUSHROOM, bundle)

    if item == Items.ODD_MUSHROOM:
        return has_item(Items.ODD_MUSHROOM, bundle) or trade_quest_step(Items.ODD_POTION, bundle)

    if item == Items.ODD_POTION:
        return has_item(Items.ODD_POTION, bundle) or trade_quest_step(Items.POACHERS_SAW, bundle)

    if item == Items.POACHERS_SAW:
        return has_item(Items.POACHERS_SAW, bundle) or trade_quest_step(Items.BROKEN_GORONS_SWORD, bundle)

    if item == Items.BROKEN_GORONS_SWORD:
        return has_item(Items.BROKEN_GORONS_SWORD, bundle) or trade_quest_step(Items.PRESCRIPTION, bundle)

    if item == Items.PRESCRIPTION:
        return has_item(Items.PRESCRIPTION, bundle) or trade_quest_step(Items.WORLDS_FINEST_EYEDROPS, bundle)

    if item == Items.WORLDS_FINEST_EYEDROPS:
        return has_item(Items.WORLDS_FINEST_EYEDROPS, bundle) or trade_quest_step(Items.CLAIM_CHECK, bundle)

    if item == Items.CLAIM_CHECK:
        return has_item(Items.CLAIM_CHECK, bundle)

    return False


def can_build_rainbow_bridge(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    world = bundle[2]

    greg_reward = 0
    if has_item(Items.GREG_THE_GREEN_RUPEE, bundle) and world.options.rainbow_bridge_greg_modifier == "reward":
        greg_reward = 1

    bridge_setting = world.options.rainbow_bridge

    return (bridge_setting == "always_open" or
            (bridge_setting == "vanilla" and has_item(Items.SHADOW_MEDALLION, bundle) and has_item(Items.SPIRIT_MEDALLION, bundle) and can_use(Items.LIGHT_ARROW, bundle)) or
            (bridge_setting == "stones" and ((stone_count(bundle) + greg_reward) >= world.options.rainbow_bridge_stones_required)) or
            (bridge_setting == "medallions" and ((medallion_count(bundle) + greg_reward) >= world.options.rainbow_bridge_medallions_required)) or
            (bridge_setting == "dungeon_rewards" and ((stone_count(bundle) + medallion_count(bundle) + greg_reward) >= world.options.rainbow_bridge_dungeon_rewards_required)) or
            (bridge_setting == "dungeons" and ((dungeon_count(bundle) + greg_reward) >= world.options.rainbow_bridge_dungeons_required)) or
            (bridge_setting == "tokens" and (get_gs_count(bundle) >= world.options.rainbow_bridge_skull_tokens_required)) or
            (bridge_setting == "greg" and has_item(Items.GREG_THE_GREEN_RUPEE, bundle)))


def get_gs_count(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> int:
    state = bundle[0]
    world = bundle[2]
    return state.count(Items.GOLD_SKULLTULA_TOKEN, world.player)


def can_trigger_lacs(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    world = bundle[2]

    greg_reward = 0
    if has_item(Items.GREG_THE_GREEN_RUPEE, bundle) and world.options.ganons_castle_boss_key_greg_modifier == "reward":
        greg_reward = 1

    gbk_setting = world.options.ganons_castle_boss_key

    return ((gbk_setting in ["vanilla", "anywhere", "lacs_vanilla"] and has_item(Items.SHADOW_MEDALLION, bundle) and has_item(Items.SPIRIT_MEDALLION, bundle)) or
            (gbk_setting == "lacs_stones" and (stone_count(bundle) + greg_reward >= world.options.ganons_castle_boss_key_stones_required)) or
            (gbk_setting == "lacs_medallions" and (medallion_count(bundle) + greg_reward >= world.options.ganons_castle_boss_key_medallions_required)) or
            (gbk_setting == "lacs_dungeon_rewards" and (stone_count(bundle) + medallion_count(bundle) + greg_reward >= world.options.ganons_castle_boss_key_dungeon_rewards_required)) or
            (gbk_setting == "lacs_dungeons" and (dungeon_count(bundle) + greg_reward >= world.options.ganons_castle_boss_key_dungeons_required)) or
            (gbk_setting == "lacs_skull_tokens" and (get_gs_count(bundle) >= world.options.ganons_castle_boss_key_skull_tokens_required)))


# TODO implement EffectiveHealth(); Returns 2 for now. Requires implementing a damage multiplier option
def effective_health(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> int:
    return 2


# TODO implement when shuffling keys within a dungeon is implemented
def is_fire_loop_locked(bundle: tuple[CollectionState, Regions, "SohWorld"]) -> bool:
    return True


def can_ground_jump(bundle: tuple[CollectionState, Regions, "SohWorld"], hasBombFlower: bool = False) -> bool:
    return (can_do_trick(Tricks.GROUND_JUMP, bundle)
            and can_standing_shield(bundle)
            and (can_use(Items.BOMB_BAG, bundle) or (hasBombFlower and has_item(Items.GORONS_BRACELET, bundle))))


def can_clear_stalagmite(bundle: tuple[CollectionState, Regions, "SohWorld"]):
    return can_jump_slash(bundle) or has_explosives(bundle)


class SohHeartState(LogicMixin):
    # tracking how many hearts the player has instead of checking the collection state every time
    soh_piece_of_heart_count: Counter[int]
    soh_heart_count: Counter[int]

    def init_mixin(self, parent: MultiWorld):
        soh_players = list(parent.get_game_players(
            "Ship of Harkinian") + parent.get_game_groups("Ship of Harkinian"))
        self.soh_piece_of_heart_count = Counter()
        self.soh_heart_count = Counter({player: 3 for player in soh_players})

    def copy_mixin(self, ret: CollectionState) -> CollectionState:
        ret.soh_piece_of_heart_count = Counter(self.soh_piece_of_heart_count)  # type: ignore # noqa
        ret.soh_heart_count = Counter(self.soh_heart_count)  # type: ignore # noqa
        return ret
