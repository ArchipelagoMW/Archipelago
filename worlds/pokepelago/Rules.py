from rule_builder.rules import Has, HasAll
from rule_builder.options import OptionFilter
from typing import TYPE_CHECKING

from .data import GEN_1_TYPES
from .Options import EnableTypeLocks

if TYPE_CHECKING:
    from .__init__ import PokepelagoWorld

def set_rules(world: "PokepelagoWorld"):
    player = world.player
    type_locks_disabled = [OptionFilter(EnableTypeLocks, 0)]

    STARTER_NAMES = ["Bulbasaur", "Charmander", "Squirtle"]
    STARTER_OFFSET = len(STARTER_NAMES)

    # Calculate type offsets (how many of each type are pre-collected via starters)
    TYPE_OFFSETS = {t: 0 for t in GEN_1_TYPES}
    for mon in world.active_pokemon:
        if mon["name"] in STARTER_NAMES:
            for t in mon["types"]:
                if t in TYPE_OFFSETS:
                    TYPE_OFFSETS[t] += 1

    if world.options.dexsanity.value:
        # --- Dexsanity ON ---

        # 1. Rules for LOCATIONS: need the Pokemon Unlock AND type keys (if type locks enabled).
        # Rules go on the location, NOT the entrance, so the "Catch {Pokemon}" entrances are
        # always open and never enter blocked_connections. This keeps blocked_connections to
        # only the 5 tier entrances, making explicit_indirect_conditions=False trivially cheap.
        for mon in world.active_pokemon:
            mon_name = mon["name"]
            unlock_item = f"{mon_name} Unlock"
            type_keys = [f"{t} Type Key" for t in mon["types"]]

            location = world.multiworld.get_location(f"Guess {mon_name}", player)
            rule = Has(unlock_item) & (HasAll(*type_keys) | type_locks_disabled)
            world.set_rule(location, rule)

        # 2. Rules for Global Milestones
        # Use has("Pokemon Unlocks") on the virtual counter maintained by collect/remove overrides.
        # Starter Unlock items are push_precollected, so the counter starts at 3.
        from .Locations import milestones

        for count in milestones:
            loc_name = f"Guessed {count} Pokemon"
            try:
                location = world.multiworld.get_location(loc_name, player)
                c = count + STARTER_OFFSET
                location.access_rule = lambda state, _c=c: state.has("Pokemon Unlocks", player, _c)
            except KeyError:
                pass

        # 3. Rules for Type-Specific Milestones
        # Use has("{Type} Pokemon") on the virtual per-type counter maintained by collect/remove.
        from .Locations import TYPE_MILESTONE_STEPS

        for p_type in GEN_1_TYPES:
            offset = TYPE_OFFSETS.get(p_type, 0)
            for count in TYPE_MILESTONE_STEPS:
                loc_name = f"Caught {count} {p_type} Pokemon"
                try:
                    location = world.multiworld.get_location(loc_name, player)
                    c = count + offset
                    location.access_rule = lambda state, _t=p_type, _c=c: state.has(f"{_t} Pokemon", player, _c)
                except KeyError:
                    pass

    else:
        # --- Dexsanity OFF ---
        # No entrance rules (no per-Pokemon regions). No global milestone rules (freely accessible).
        # If type locks are enabled, type milestone locations require the matching Type Key.
        if world.options.type_locks.value:
            from .Locations import TYPE_MILESTONE_STEPS

            for p_type in GEN_1_TYPES:
                for count in TYPE_MILESTONE_STEPS:
                    loc_name = f"Caught {count} {p_type} Pokemon"
                    try:
                        location = world.multiworld.get_location(loc_name, player)
                        type_key = f"{p_type} Type Key"
                        location.access_rule = lambda state, _k=type_key: state.has(_k, player)
                    except KeyError:
                        pass