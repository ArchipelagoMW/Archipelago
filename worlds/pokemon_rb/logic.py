from . import poke_data


def can_surf(state, world):
    return (((state.has("HM03 Surf", world.player) and can_learn_hm(state, "Surf", world))
             or state.has("Flippers", world.player)) and (state.has("Soul Badge", world.player) or
             state.has(world.extra_badges.get("Surf"), world.player)
             or world.options.badges_needed_for_hm_moves.value == 0))


def can_cut(state, world):
    return ((state.has("HM01 Cut", world.player) and can_learn_hm(state, "Cut", world) or state.has("Master Sword", world.player))
             and (state.has("Cascade Badge", world.player) or
             state.has(world.extra_badges.get("Cut"), world.player) or
             world.options.badges_needed_for_hm_moves.value == 0))


def can_fly(state, world):
    return (((state.has("HM02 Fly", world.player) and can_learn_hm(state, "Fly", world)) or state.has("Flute", world.player)) and
           (state.has("Thunder Badge", world.player) or state.has(world.extra_badges.get("Fly"), world.player)
            or world.options.badges_needed_for_hm_moves.value == 0))


def can_strength(state, world):
    return ((state.has("HM04 Strength", world.player) and can_learn_hm(state, "Strength", world)) or
            state.has("Titan's Mitt", world.player)) and (state.has("Rainbow Badge", world.player) or
            state.has(world.extra_badges.get("Strength"), world.player)
            or world.options.badges_needed_for_hm_moves.value == 0)


def can_flash(state, world):
    return (((state.has("HM05 Flash", world.player) and can_learn_hm(state, "Flash", world)) or state.has("Lamp", world.player))
             and (state.has("Boulder Badge", world.player) or state.has(world.extra_badges.get("Flash"),
             world.player) or world.options.badges_needed_for_hm_moves.value == 0))


def can_learn_hm(state, move, world):
    for pokemon, data in world.local_poke_data.items():
        if state.has(pokemon, world.player) and data["tms"][6] & 1 << (["Cut", "Fly", "Surf", "Strength",
                                                                  "Flash"].index(move) + 2):
            return True
    return False


def can_get_hidden_items(state, world):
    return state.has("Item Finder", world.player) or not world.options.require_item_finder.value


def has_key_items(state, count, player):
    key_items = (len([item for item in ["Bicycle", "Silph Scope", "Item Finder", "Super Rod", "Good Rod",
                                        "Old Rod", "Lift Key", "Card Key", "Town Map", "Coin Case", "S.S. Ticket",
                                        "Secret Key", "Poke Flute", "Mansion Key", "Safari Pass", "Plant Key",
                                        "Hideout Key", "Card Key 2F", "Card Key 3F", "Card Key 4F", "Card Key 5F",
                                        "Card Key 6F", "Card Key 7F", "Card Key 8F", "Card Key 9F", "Card Key 10F",
                                        "Card Key 11F", "Exp. All", "Fire Stone", "Thunder Stone", "Water Stone",
                                        "Leaf Stone", "Moon Stone"] if state.has(item, player)])
                 + min(state.count("Progressive Card Key", player), 10))
    return key_items >= count


def can_pass_guards(state, world):
    if world.options.tea:
        return state.has("Tea", world.player)
    else:
        return state.has("Vending Machine Drinks", world.player)


def has_badges(state, count, player):
    return len([item for item in ["Boulder Badge", "Cascade Badge", "Thunder Badge", "Rainbow Badge", "Marsh Badge",
                                  "Soul Badge", "Volcano Badge", "Earth Badge"] if state.has(item, player)]) >= count


def oaks_aide(state, count, world):
    return ((not world.options.require_pokedex or state.has("Pokedex", world.player))
            and has_pokemon(state, count, world.player))


def has_pokemon(state, count, player):
    obtained_pokemon = set()
    for pokemon in poke_data.pokemon_data.keys():
        if state.has(pokemon, player) or state.has(f"Static {pokemon}", player):
            obtained_pokemon.add(pokemon)

    return len(obtained_pokemon) >= count


def fossil_checks(state, count, player):
    return (state.can_reach('Mt Moon B2F', 'Region', player) and
            state.can_reach('Cinnabar Lab Fossil Room', 'Region', player) and
            state.can_reach('Cinnabar Island', 'Region', player) and len(
        [item for item in ["Dome Fossil", "Helix Fossil", "Old Amber"] if state.has(item, player)]) >= count)


def card_key(state, floor, player):
    return state.has(f"Card Key {floor}F", player) or state.has("Card Key", player) or \
           state.has("Progressive Card Key", player, floor - 1)


def rock_tunnel(state, world):
    return can_flash(state, world) or not world.options.dark_rock_tunnel_logic


def route_3(state, world):
    if world.options.route_3_condition == "defeat_brock":
        return state.has("Defeat Brock", world.player)
    elif world.options.route_3_condition == "defeat_any_gym":
        return state.has_any(["Defeat Brock", "Defeat Misty", "Defeat Lt. Surge", "Defeat Erika", "Defeat Koga",
                              "Defeat Blaine", "Defeat Sabrina", "Defeat Viridian Gym Giovanni"], world.player)
    elif world.options.route_3_condition == "boulder_badge":
        return state.has("Boulder Badge", world.player)
    elif world.options.route_3_condition == "any_badge":
        return state.has_any(["Boulder Badge", "Cascade Badge", "Thunder Badge", "Rainbow Badge", "Marsh Badge",
                              "Soul Badge", "Volcano Badge", "Earth Badge"], world.player)
    # open
    return True


def evolve_level(state, level, player):
    return len([item for item in (
        "Defeat Brock", "Defeat Misty", "Defeat Lt. Surge", "Defeat Erika", "Defeat Koga", "Defeat Blaine",
        "Defeat Sabrina", "Defeat Viridian Gym Giovanni") if state.has(item, player)]) > level / 7
