from typing import Callable, TYPE_CHECKING

from BaseClasses import CollectionState
from .Enums import Items

if TYPE_CHECKING:
    from . import SohWorld


def get_soh_rule(world: "SohWorld") -> Callable[[CollectionState], bool]:
    return lambda state: True

def has_item(item_name: str, state: CollectionState, world: "SohWorld") -> bool:
    # Just use .Logic.HasItem directly
    # Import here to avoid circular imports
    from .Logic import HasItem

    # Use the existing function from Logic.py which already implements
    # the full C++ logic.
    return HasItem(state= state, world=world,itemName= item_name)

def can_use(item_name: str, state: CollectionState, world: "SohWorld") -> bool:
    # Import here to avoid circular imports
    from .Logic import CanUse

    # Use the existing CanUse function from Logic.py which already implements
    # the full C++ logic with proper age restrictions, magic requirements, etc.
    return CanUse(state, world, item_name)

def has_explosives(state: CollectionState, world: "SohWorld") -> bool:
    """Check if Link has access to explosives (bombs or bombchus)."""
    return can_use(Items.PROGRESSIVE_BOMB_BAG.value, state, world) or can_use(Items.PROGRESSIVE_BOMBCHU.value, state, world)


def blast_or_smash(state: CollectionState, world: "SohWorld") -> bool:
    """Check if Link can blast or smash obstacles."""
    return has_explosives(state, world) or can_use(Items.MEGATON_HAMMER.value, state, world)


def blue_fire(state: CollectionState, world: "SohWorld") -> bool:
    """Check if Link has access to blue fire."""
    return can_use(Items.BOTTLE_WITH_BLUE_FIRE.value, state, world)  # or blue fire arrows


def has_bottle(state: CollectionState, world: "SohWorld") -> bool:
    """Check if Link has any bottle."""
    from .Logic import HasBottle
    return HasBottle(state, world)

def can_use_sword(state: CollectionState, world: "SohWorld") -> bool:
    """Check if Link can use any sword."""
    return (can_use(Items.KOKIRI_SWORD.value, state, world) or
            can_use(Items.MASTER_SWORD.value, state, world) or
            can_use(Items.BIGGORONS_SWORD.value, state, world))

def has_projectile(state: CollectionState, world: "SohWorld", age: str = "either") -> bool:
    """Check if Link has access to projectiles."""
    if has_explosives(state, world):
        return True
    child_projectiles = (can_use(Items.PROGRESSIVE_SLINGSHOT.value, state, world) or 
                        can_use(Items.BOOMERANG.value, state, world))
    adult_projectiles = (can_use(Items.PROGRESSIVE_HOOKSHOT.value, state, world) or 
                        can_use(Items.PROGRESSIVE_BOW.value, state, world))
    
    if age == "child":
        return child_projectiles
    elif age == "adult":
        return adult_projectiles
    elif age == "both":
        return child_projectiles and adult_projectiles
    else:  # "either"
        return child_projectiles or adult_projectiles

def can_use_projectile(state: CollectionState, world: "SohWorld", age: str = "either") -> bool:
    return (has_explosives(state, world) or can_use(Items.PROGRESSIVE_SLINGSHOT.value, state, world) or
            can_use(Items.BOOMERANG.value, state, world) or can_use(Items.PROGRESSIVE_HOOKSHOT.value, state, world) or
            can_use(Items.PROGRESSIVE_BOW.value, state, world))

def can_break_mud_walls(state: CollectionState, world: "SohWorld") -> bool:
    return blast_or_smash(state, world) or (can_do_trick("Blue Fire Mud Walls", state, world) and blue_fire(state, world))

def can_get_deku_baba_sticks(state: CollectionState, world: "SohWorld") -> bool:
    return can_use(Items.DEKU_STICK.value, state, world) or can_use(Items.BOOMERANG.value, state, world)

def can_get_deku_baba_nuts(state: CollectionState, world: "SohWorld") -> bool:
    return can_use_sword(state, world) or can_use(Items.BOOMERANG.value, state, world)

def is_adult(state: CollectionState, world: "SohWorld") -> bool:
    # For now, return True as a placeholder since age logic is complex and context-dependent
    # The real age checking should be done through the CanUse function's can_be_adult parameter
    # TODO: Implement proper age checking based on world settings and progression
    return True


def can_damage(state: CollectionState, world: "SohWorld") -> bool:
    """Check if Link can deal damage to enemies."""
    return (can_use(Items.PROGRESSIVE_SLINGSHOT.value, state, world) or 
            can_jump_slash(state, world) or 
            has_explosives(state, world) or 
            can_use(Items.DINS_FIRE.value, state, world) or
            can_use(Items.PROGRESSIVE_BOW.value, state, world))


def can_attack(state: CollectionState, world: "SohWorld") -> bool:
    """Check if Link can attack enemies (damage or stun)."""
    return (can_damage(state, world) or 
            can_use(Items.BOOMERANG.value, state, world) or
            can_use(Items.PROGRESSIVE_HOOKSHOT.value, state, world))

def can_standing_shield(state: CollectionState, world: "SohWorld") -> bool:
    """Check if Link can use a shield for standing blocks."""
    return (can_use(Items.MIRROR_SHIELD.value, state, world) or # Only adult can use mirror shield
            (is_adult(state, world) and can_use(Items.HYLIAN_SHIELD.value, state, world)) or
            can_use(Items.DEKU_SHIELD.value, state, world)) # Only child can use deku shield

def can_shield(state: CollectionState, world: "SohWorld") -> bool:
    """Check if Link can use a shield for blocking or stunning."""
    return (can_use(Items.MIRROR_SHIELD.value, state, world) or
            can_use(Items.HYLIAN_SHIELD.value, state, world) or
            can_use(Items.DEKU_SHIELD.value, state, world))

def take_damage(state: CollectionState, world: "SohWorld") -> bool:
    # return CanUse(RG_BOTTLE_WITH_FAIRY) || EffectiveHealth() != 1 || CanUse(RG_NAYRUS_LOVE);
    return (can_use(Items.BOTTLE_WITH_FAIRY.value, state, world) or can_use(Items.NAYRUS_LOVE.value, state, world)
            or True)  #TODO: Implement "|| EffectiveHealth()"

def can_do_trick(trick: str, state: CollectionState, world: "SohWorld") -> bool:
    # TODO: Implement specific trick logic based on world settings
    # For now, return False for safety (no tricks assumed)
    return False


def can_break_pots(state: CollectionState, world: "SohWorld") -> bool:
    """Check if Link can break pots for items."""
    return (can_jump_slash(state, world) or 
           can_use(Items.BOOMERANG.value, state, world) or
           has_explosives(state, world) or
           can_use(Items.PROGRESSIVE_HOOKSHOT.value, state, world))


def can_break_crates(state: CollectionState, world: "SohWorld") -> bool:
    """Check if Link can break crates."""
    return (can_jump_slash(state, world) or 
           has_explosives(state, world))


def can_hit_eye_targets(state: CollectionState, world: "SohWorld") -> bool:
    """Check if Link can hit eye switches/targets."""
    return (can_use(Items.PROGRESSIVE_BOW.value, state, world) or 
           can_use(Items.PROGRESSIVE_SLINGSHOT.value, state, world) or
           can_use(Items.PROGRESSIVE_HOOKSHOT.value, state, world) or
           can_use(Items.BOOMERANG.value, state, world))


def can_stun_deku(state: CollectionState, world: "SohWorld") -> bool:
    """Check if Link can stun Deku Scrubs."""
    return can_attack(state, world) or can_use(Items.DEKU_NUT_BAG.value, state, world) or can_shield(state, world) # Is this right for nuts?


def can_reflect_nuts(state: CollectionState, world: "SohWorld") -> bool:
    """Check if Link can reflect Deku Nuts back at enemies."""
    return can_stun_deku(state, world)

def has_fire_source_with_torch(state: CollectionState, world: "SohWorld") -> bool:
    """Check if Link has a fire source that can be used with a torch."""
    return has_fire_source(state, world) or can_use(Items.STICKS, state, world)

def has_fire_source(state: CollectionState, world: "SohWorld") -> bool:
    """Check if Link has any fire source."""
    return (can_use(Items.DINS_FIRE.value, state, world) or 
           can_use(Items.FIRE_ARROW.value, state, world))


def can_jump_slash(state: CollectionState, world: "SohWorld") -> bool:
    """Check if Link can perform a jump slash with any sword."""
    return (can_use(Items.KOKIRI_SWORD.value, state, world) or 
            can_use(Items.MASTER_SWORD.value, state, world) or 
            can_use(Items.BIGGORONS_SWORD.value, state, world) or
            can_use(Items.MEGATON_HAMMER.value, state, world))  # Hammer can substitute for sword in some cases


# BELOW IS AI SLOP
# Based on C++ Logic

def can_hit_switch(state: CollectionState, world: "SohWorld", distance: str = "close",
                   in_water: bool = False) -> bool:
    if distance == "close":
        return (can_jump_slash(state, world) or
                has_explosives(state, world) or
                can_use(Items.BOOMERANG.value, state, world) or
                can_use(Items.PROGRESSIVE_HOOKSHOT.value, state, world))

    elif distance in ["short_jumpslash", "master_sword_jumpslash", "long_jumpslash"]:
        return can_jump_slash(state, world)

    elif distance == "bomb_throw":
        return has_explosives(state, world)

    elif distance == "boomerang":
        return can_use(Items.BOOMERANG.value, state, world)

    elif distance in ["hookshot", "longshot"]:
        return can_use(Items.PROGRESSIVE_HOOKSHOT.value, state, world)

    elif distance == "far":
        return (can_use(Items.PROGRESSIVE_BOW.value, state, world) or
                can_use(Items.PROGRESSIVE_HOOKSHOT.value, state, world) or
                has_explosives(state, world))

    return False

def can_kill_enemy(state: CollectionState, world: "SohWorld", enemy: str, combat_range: str = "close",
                   wall_or_floor: bool = True, quantity: int = 1, timer: bool = False, in_water: bool = False) -> bool:
    """
    Check if Link can kill a specific enemy at a given combat range.
    Based on the C++ Logic::CanKillEnemy implementation.

    Args:
        enemy: Enemy type (e.g., "gold_skulltula", "keese", etc.)
        combat_range: Combat range - "close", "short_jumpslash", "master_sword_jumpslash",
                     "long_jumpslash", "bomb_throw", "boomerang", "hookshot", "longshot", "far"
        wall_or_floor: Whether enemy is on wall or floor
        quantity: Number of enemies (for ammo considerations)
        timer: Whether there's a timer constraint
        in_water: Whether the fight is underwater
    """

    # Define what weapons work at each range
    def can_hit_at_range(range_type: str) -> bool:
        if range_type == "close":
            return (can_jump_slash(state, world) or
                    has_explosives(state, world) or
                    can_use(Items.DINS_FIRE.value, state, world))

        elif range_type in ["short_jumpslash", "master_sword_jumpslash", "long_jumpslash"]:
            return can_jump_slash(state, world)

        elif range_type == "bomb_throw":
            return has_explosives(state, world)

        elif range_type == "boomerang":
            return can_use(Items.BOOMERANG.value, state, world)

        elif range_type == "hookshot":
            return can_use(Items.PROGRESSIVE_HOOKSHOT.value, state, world)

        elif range_type == "longshot":
            return can_use(Items.PROGRESSIVE_HOOKSHOT.value, state, world)  # Longshot is progressive hookshot level 2

        elif range_type == "far":
            return (can_use(Items.PROGRESSIVE_BOW.value, state, world) or
                    can_use(Items.PROGRESSIVE_SLINGSHOT.value, state, world) or
                    can_use(Items.PROGRESSIVE_HOOKSHOT.value, state, world) or
                    has_explosives(state, world))

        return False

    # Enemy-specific logic based on C++ implementation
    enemy_lower = enemy.lower().replace(" ", "_")

    # Guards (need specific items or tricks)
    if enemy_lower in ["gerudo_guard", "break_room_guard"]:
        return (can_use(Items.PROGRESSIVE_BOW.value, state, world) or
                can_use(Items.PROGRESSIVE_HOOKSHOT.value, state, world) or
                has_explosives(state, world))

    # Gold Skulltulas and similar enemies that can be hit at various ranges
    if enemy_lower in ["gold_skulltula", "big_skulltula"]:
        return can_hit_at_range(combat_range)

    # Small enemies that are easy to kill
    if enemy_lower in ["gohma_larva", "mad_scrub", "deku_baba", "withered_deku_baba"]:
        return can_hit_at_range(combat_range)

    # Dodongo (requires explosives or specific attacks)
    if enemy_lower == "dodongo":
        if combat_range in ["close", "short_jumpslash", "master_sword_jumpslash", "long_jumpslash"]:
            return (can_jump_slash(state, world) or has_explosives(state, world))
        return has_explosives(state, world)

    # Lizalfos (requires good weapons)
    if enemy_lower == "lizalfos":
        return (can_jump_slash(state, world) or
                can_use(Items.PROGRESSIVE_BOW.value, state, world) or
                has_explosives(state, world))

    # Flying enemies
    if enemy_lower in ["keese", "fire_keese"]:
        return can_hit_at_range(combat_range)

    # Bubbles (need specific attacks)
    if enemy_lower in ["blue_bubble", "green_bubble"]:
        return (can_jump_slash(state, world) or
                can_use(Items.PROGRESSIVE_BOW.value, state, world) or
                can_use(Items.PROGRESSIVE_HOOKSHOT.value, state, world) or
                can_use(Items.BOOMERANG.value, state, world))

    # Tough enemies
    if enemy_lower in ["dead_hand", "like_like", "floormaster", "wallmaster"]:
        return (can_jump_slash(state, world) or
                can_use(Items.PROGRESSIVE_BOW.value, state, world) or
                has_explosives(state, world))

    # Stalfos (needs good weapons)
    if enemy_lower == "stalfos":
        return can_hit_at_range(combat_range) and (
                can_jump_slash(state, world) or
                can_use(Items.MEGATON_HAMMER.value, state, world))

    # Iron Knuckle (very tough)
    if enemy_lower == "iron_knuckle":
        return (can_jump_slash(state, world) or
                can_use(Items.MEGATON_HAMMER.value, state, world) or
                has_explosives(state, world))

    # Fire enemies
    if enemy_lower in ["flare_dancer", "torch_slug"]:
        return (can_jump_slash(state, world) or
                can_use(Items.PROGRESSIVE_BOW.value, state, world) or
                can_use(Items.PROGRESSIVE_HOOKSHOT.value, state, world) or
                has_explosives(state, world))

    # Wolfos
    if enemy_lower in ["wolfos", "white_wolfos"]:
        return (can_jump_slash(state, world) or
                can_use(Items.PROGRESSIVE_BOW.value, state, world) or
                has_explosives(state, world))

    # Gerudo Warrior
    if enemy_lower == "gerudo_warrior":
        return (can_jump_slash(state, world) or
                can_use(Items.PROGRESSIVE_BOW.value, state, world) or
                has_explosives(state, world))

    # ReDeads and Gibdos
    if enemy_lower in ["gibdo", "redead"]:
        return (can_jump_slash(state, world) or
                can_use(Items.PROGRESSIVE_BOW.value, state, world) or
                can_use(Items.SUNS_SONG.value, state, world) or
                has_explosives(state, world))

    # Other enemies
    if enemy_lower in ["meg", "armos", "dinolfos", "freezard", "shell_blade", "spike", "stinger"]:
        return can_hit_at_range(combat_range)

    # Water enemies
    if enemy_lower in ["big_octo", "bari", "shabom", "octorok", "tentacle"]:
        if in_water:
            return (can_use(Items.PROGRESSIVE_HOOKSHOT.value, state, world) or
                    can_use(Items.PROGRESSIVE_BOW.value, state, world) or
                    has_explosives(state, world))
        return can_hit_at_range(combat_range)

    # Bosses
    if enemy_lower in ["gohma", "king_dodongo", "barinade", "phantom_ganon", "volvagia",
                       "morpha", "bongo_bongo", "twinrova", "ganondorf", "ganon"]:
        # Bosses generally require good weapons and specific strategies
        return (can_jump_slash(state, world) or
                can_use(Items.PROGRESSIVE_BOW.value, state, world) or
                has_explosives(state, world))

    # Dark Link (special case)
    if enemy_lower == "dark_link":
        return (can_use(Items.MEGATON_HAMMER.value, state, world) or
                can_use(Items.PROGRESSIVE_BOW.value, state, world) or
                has_explosives(state, world))

    # Beamos (needs ranged attacks)
    if enemy_lower == "beamos":
        return (can_use(Items.PROGRESSIVE_BOW.value, state, world) or
                can_use(Items.PROGRESSIVE_HOOKSHOT.value, state, world) or
                has_explosives(state, world))

    # Purple Leever
    if enemy_lower == "purple_leever":
        return can_hit_at_range(combat_range)

    # Anubis (tough enemy)
    if enemy_lower == "anubis":
        return (can_jump_slash(state, world) or
                can_use(Items.PROGRESSIVE_BOW.value, state, world) or
                has_explosives(state, world))

    # Default case - assume basic combat is sufficient
    return can_damage(state, world)
