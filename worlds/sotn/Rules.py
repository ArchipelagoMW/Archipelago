from worlds.generic.Rules import forbid_item, set_rule
from BaseClasses import MultiWorld, CollectionState

from .Items import vessel_table
from .Locations import location_table


def sotn_has_transformation(state: CollectionState, player: int) -> bool:
    return (state.has("Soul of bat", player) or state.has("Soul of wolf", player) or
            state.has("Form of mist", player))

def sotn_has_jump(state: CollectionState, player: int) -> bool:
    return state.has("Leap stone", player) or state.has("Gravity boots", player)


def sotn_has_flying(state: CollectionState, player: int) -> bool:
    return (state.has("Soul of bat", player) or
            (state.has("Form of mist", player) and state.has("Power of mist", player)) or
            (state.has("Gravity boots", player) and state.has("Leap stone", player)))


def sotn_has_any(state: CollectionState, player: int) -> bool:
    return sotn_has_jump(state, player) or sotn_has_flying(state, player)


def sotn_has_bat(state: CollectionState, player: int) -> bool:
    return state.has("Soul of bat", player) and state.has("Echo of bat", player)


def sotn_has_reverse(state: CollectionState, player: int) -> bool:
    return state.has("Holy glasses", player) and sotn_has_flying(state, player)

def sotn_has_dracula(state: CollectionState, player: int) -> bool:
    return (sotn_has_reverse(state, player) and state.has("Heart of vlad", player) and
            state.has("Rib of vlad", player) and state.has("Tooth of vlad", player) and
            state.has("Eye of vlad", player) and state.has("Ring of vlad", player))


def set_rules(world: MultiWorld, player: int) -> None:
    no4 = world.opened_no4[player]
    are = world.opened_are[player]
    no2 = world.opened_no2[player]

    for name, data in location_table.items():
        if data.no_offset:
            # Forbid progression_items and vessel on no offsets despawn locations
            location = world.get_location(name, player)
            for pu in vessel_table.items():
                forbid_item(location, pu[0], player)
            # Holy glasses can have progression items
            if name != "NO0 - Holy glasses":
                forbid_item(location, "Gold ring", player)
                forbid_item(location, "Silver ring", player)
                forbid_item(location, "Holy glasses", player)
                forbid_item(location, "Spike breaker", player)

    # Vessels can be on gold ring, but cause some weird visual glitches
    location = world.get_location("NO4 - Gold Ring", player)
    for pu in vessel_table.items():
        forbid_item(location, pu[0], player)
    location = world.get_location("Soul of Bat", player)
    set_rule(location, lambda state: state.has("Form of mist", player) and sotn_has_any(state, player))
    location = world.get_location("Fire of Bat", player)
    set_rule(location, lambda state: sotn_has_flying(state, player))
    location = world.get_location("Echo of Bat", player)
    set_rule(location, lambda state: sotn_has_flying(state, player) and sotn_has_transformation(state, player))
    location = world.get_location("Power of Wolf", player)
    set_rule(location, lambda state: sotn_has_flying(state, player))
    location = world.get_location("Skill of Wolf", player)
    set_rule(location, lambda state: state.has("Gravity boots", player) or sotn_has_flying(state, player))
    if are:
        location = world.get_location("Form of Mist", player)
        set_rule(location, lambda state: state.has("Jewel of open", player) or sotn_has_jump(state, player))
    location = world.get_location("Power of Mist", player)
    set_rule(location, lambda state: sotn_has_flying(state, player))
    location = world.get_location("Gravity Boots", player)
    set_rule(location, lambda state: sotn_has_flying(state, player))
    if not no4:
        location = world.get_location("Holy Symbol", player)
        set_rule(location, lambda state: state.has("Merman statue", player) and state.has("Jewel of open", player))
        location = world.get_location("Merman Statue", player)
        set_rule(location, lambda state: state.has("Jewel of open", player))
    else:
        location = world.get_location("Holy Symbol", player)
        set_rule(location, lambda state: state.has("Merman statue", player) and
                 sotn_has_flying(state, player))
    location = world.get_location("Bat Card", player)
    set_rule(location, lambda state: sotn_has_any(state, player))
    location = world.get_location("Ghost Card", player)
    set_rule(location, lambda state: sotn_has_flying(state, player))
    location = world.get_location("Faerie Card", player)
    set_rule(location, lambda state: sotn_has_any(state, player))
    location = world.get_location("Sword Card", player)
    if no2:
        set_rule(location, lambda state: (state.has("Gravity boots", player) or sotn_has_flying(state, player)) and
                                         (state.has("Jewel of open", player) or sotn_has_jump(state, player)))
    else:
        set_rule(location, lambda state: sotn_has_flying(state, player))

# Items rules
    if are:
        location = world.get_location("ARE - Holy sword(Hidden attic)", player)
        set_rule(location, lambda state: (state.has("Jewel of open", player) or sotn_has_jump(state, player)) and
                 state.has("Gravity boots", player) or sotn_has_flying(state, player))
        location = world.get_location("ARE - Minotaurus/Werewolf kill", player)
        set_rule(location, lambda state: state.has("Jewel of open", player) or sotn_has_any(state, player))
    else:
        location = world.get_location("ARE - Holy sword(Hidden attic)", player)
        set_rule(location, lambda state: state.has("Gravity boots", player) or sotn_has_flying(state, player))
        location = world.get_location("ARE - Minotaurus/Werewolf kill", player)
        set_rule(location, lambda state: sotn_has_any(state, player))

    # CAT - Catacombs worst case scenario player can get here with only jewel, soul and power of wolf
    # Spike breaker locations
    location = world.get_location("CAT - Library card(Spike breaker)", player)
    set_rule(location, lambda state: (state.has("Spike breaker", player) and sotn_has_any(state, player)) or
             sotn_has_bat(state, player))

    location = world.get_location("CAT - Cross shuriken 1(Spike breaker)", player)
    set_rule(location, lambda state: (state.has("Spike breaker", player) and sotn_has_any(state, player)) or
             sotn_has_bat(state, player))

    location = world.get_location("CAT - Cross shuriken 2(Spike breaker)", player)
    set_rule(location, lambda state: (state.has("Spike breaker", player) and sotn_has_any(state, player)) or
             sotn_has_bat(state, player))

    location = world.get_location("CAT - Karma coin 1(Spike breaker)", player)
    set_rule(location, lambda state: (state.has("Spike breaker", player) and sotn_has_any(state, player)) or
             sotn_has_bat(state, player))

    location = world.get_location("CAT - Karma coin 2(Spike breaker)", player)
    set_rule(location, lambda state: (state.has("Spike breaker", player) and sotn_has_any(state, player)) or
             sotn_has_bat(state, player))

    location = world.get_location("CAT - Spike breaker", player)
    set_rule(location, lambda state: (state.has("Spike breaker", player) and sotn_has_any(state, player)) or
             sotn_has_bat(state, player))

    location = world.get_location("CAT - Icebrand", player)
    set_rule(location, lambda state: sotn_has_flying(state, player) or state.has("Gravity boots", player))

    location = world.get_location("CAT - Ballroom mask", player)
    set_rule(location, lambda state: sotn_has_flying(state, player) or state.has("Gravity boots", player))

    location = world.get_location("CAT - Heart Vessel(Ballroom mask)", player)
    set_rule(location, lambda state: sotn_has_flying(state, player) or state.has("Gravity boots", player))

    # CHI - Abandoned Mine Same as CAT
    # Demon card locations
    location = world.get_location("CHI - Power of sire(Demon)", player)
    set_rule(location, lambda state: state.has("Demon card", player))

    location = world.get_location("CHI - Barley tea(Demon)", player)
    set_rule(location, lambda state: state.has("Demon card", player))

    location = world.get_location("CHI - Peanuts 1(Demon)", player)
    set_rule(location, lambda state: state.has("Demon card", player))

    location = world.get_location("CHI - Peanuts 2(Demon)", player)
    set_rule(location, lambda state: state.has("Demon card", player))

    location = world.get_location("CHI - Peanuts 3(Demon)", player)
    set_rule(location, lambda state: state.has("Demon card", player))

    location = world.get_location("CHI - Peanuts 4(Demon)", player)
    set_rule(location, lambda state: state.has("Demon card", player))

    location = world.get_location("CHI - Turkey(Demon)", player)
    set_rule(location, lambda state: state.has("Demon card", player))

    location = world.get_location("CHI - Ring of ares", player)
    set_rule(location, lambda state: state.has("Demon card", player))

    location = world.get_location("Enemysanity: 95 - Venus weed", player)
    set_rule(location, lambda state: state.has("Demon card", player))

    location = world.get_location("Dropsanity: 95 - Venus weed", player)
    set_rule(location, lambda state: state.has("Demon card", player))

    # DAI - Royal Chapel Worst case scenario only Jewel, maybe didn't have Jewel if he came from NZ1
    location = world.get_location("DAI - Silver ring", player)
    set_rule(location, lambda state: state.has("Form of mist", player) and state.has("Jewel of open", player) and
             state.has("Spike breaker", player))

    location = world.get_location("DAI - Morningstar", player)
    set_rule(location, lambda state: sotn_has_any(state, player))

    location = world.get_location("DAI - Boomerang(Stairs)", player)
    set_rule(location, lambda state: sotn_has_any(state, player))

    location = world.get_location("DAI - TNT(Stairs)", player)
    set_rule(location, lambda state: sotn_has_any(state, player))

    location = world.get_location("DAI - Shuriken(Stairs)", player)
    set_rule(location, lambda state: sotn_has_any(state, player))

    location = world.get_location("DAI - Magic missile(Stairs)", player)
    set_rule(location, lambda state: sotn_has_any(state, player))

    location = world.get_location("DAI - Ankh of life(Stairs)", player)
    set_rule(location, lambda state: sotn_has_any(state, player))

    location = world.get_location("DAI - Mystic pendant", player)
    set_rule(location, lambda state: sotn_has_any(state, player))

    location = world.get_location("DAI - Hippogryph kill", player)
    set_rule(location, lambda state: sotn_has_any(state, player))

    # LIB - Long Library
    # Upper part of LIB(Faerie card) can be access with leap stone + kick and jump from an enemy
    location = world.get_location("LIB - Takemitsu", player)
    set_rule(location, lambda state: sotn_has_any(state, player))

    location = world.get_location("LIB - Onyx", player)
    set_rule(location, lambda state: sotn_has_any(state, player))

    location = world.get_location("LIB - Frankfurter", player)
    set_rule(location, lambda state: sotn_has_any(state, player))

    location = world.get_location("LIB - Potion", player)
    set_rule(location, lambda state: sotn_has_any(state, player))

    location = world.get_location("LIB - Antivenom", player)
    set_rule(location, lambda state: sotn_has_any(state, player))

    location = world.get_location("LIB - Lesser Demon kill", player)
    set_rule(location, lambda state: sotn_has_any(state, player))

    location = world.get_location("Enemysanity: 65 - Flea armor", player)
    set_rule(location, lambda state: sotn_has_any(state, player))

    location = world.get_location("Enemysanity: 80 - Lesser demon", player)
    set_rule(location, lambda state: sotn_has_any(state, player))

    location = world.get_location("Dropsanity: 54 - Corpseweed", player)
    set_rule(location, lambda state: sotn_has_any(state, player))

    location = world.get_location("Dropsanity: 65 - Flea armor", player)
    set_rule(location, lambda state: sotn_has_any(state, player))

    # If the player got here with only leap stone, leap jump on flea man
    location = world.get_location("LIB - Stone mask", player)
    set_rule(location, lambda state: sotn_has_any(state, player))

    location = world.get_location("LIB - Holy rod", player)
    set_rule(location, lambda state: sotn_has_any(state, player))

    location = world.get_location("LIB - Topaz circlet", player)
    set_rule(location, lambda state: sotn_has_any(state, player))

    # NO0 - Marble Gallery
    location = world.get_location("NO0 - Str. potion", player)
    set_rule(location, lambda state: state.has("Gravity boots", player) or sotn_has_flying(state, player))

    location = world.get_location("NO0 - Hammer(Spirit)", player)
    set_rule(location, lambda state: state.has("Gravity boots", player) or sotn_has_flying(state, player))

    location = world.get_location("NO0 - Life Vessel(Left clock)", player)
    if are:
        set_rule(location, lambda state: sotn_has_any(state, player) or state.has("Jewel of open", player))
    else:
        set_rule(location, lambda state: sotn_has_any(state, player))

    location = world.get_location("NO0 - Hammer(Middle clock)", player)
    set_rule(location, lambda state: sotn_has_flying(state, player))

    location = world.get_location("NO0 - Life apple(Middle clock)", player)
    set_rule(location, lambda state: sotn_has_flying(state, player))

    location = world.get_location("NO0 - Potion(Middle clock)", player)
    set_rule(location, lambda state: sotn_has_flying(state, player))

    location = world.get_location("NO0 - Library card(Jewel)", player)
    set_rule(location, lambda state: state.has("Jewel of open", player))

    location = world.get_location("NO0 - Attack potion(Jewel)", player)
    set_rule(location, lambda state: state.has("Jewel of open", player))

    # Player could get stopwatch from Black Marble Gallery
    location = world.get_location("NO0 - Heart Vessel(Right clock)", player)
    set_rule(location, lambda state: (state.has("Cube of zoe", player) and sotn_has_any(state, player)) or
             sotn_has_reverse(state, player))

    location = world.get_location("NO0 - Alucart shield", player)
    set_rule(location, lambda state: (state.has("Cube of zoe", player) and sotn_has_any(state, player)) or
             sotn_has_reverse(state, player))

    location = world.get_location("NO0 - Alucart mail", player)
    set_rule(location, lambda state: (state.has("Cube of zoe", player) and sotn_has_any(state, player)) or
             sotn_has_reverse(state, player))

    location = world.get_location("NO0 - Alucart sword", player)
    set_rule(location, lambda state: (state.has("Cube of zoe", player) and sotn_has_any(state, player)) or
             sotn_has_reverse(state, player))

    location = world.get_location("NO0 - Heart Vessel(Inside)", player)
    set_rule(location, lambda state: state.has("Silver ring", player) and state.has("Gold ring", player))

    location = world.get_location("NO0 - Life Vessel(Inside)", player)
    set_rule(location, lambda state: state.has("Silver ring", player) and state.has("Gold ring", player))

    location = world.get_location("NO0 - Holy glasses", player)
    set_rule(location, lambda state: state.has("Silver ring", player) and state.has("Gold ring", player))

    # NO1 - Outer Wall
    location = world.get_location("NO1 - Garnet", player)
    set_rule(location, lambda state: sotn_has_any(state, player))

    # NO2 - Olrox's Quarters
    location = world.get_location("NO2 - Manna prism", player)
    set_rule(location, lambda state: state.has("Gravity boots", player) or sotn_has_flying(state, player))

    location = world.get_location("NO2 - Resist fire", player)
    set_rule(location, lambda state: sotn_has_flying(state, player))

    location = world.get_location("NO2 - Luck potion", player)
    set_rule(location, lambda state: sotn_has_flying(state, player))

    location = world.get_location("NO2 - Estoc", player)
    set_rule(location, lambda state: sotn_has_flying(state, player))

    location = world.get_location("NO2 - Iron ball", player)
    set_rule(location, lambda state: sotn_has_flying(state, player))

    location = world.get_location("NO2 - Olrox kill", player)
    set_rule(location, lambda state: sotn_has_flying(state, player) and sotn_has_transformation(state, player))

    if no2:
        location = world.get_location("NO2 - Garnet", player)
        set_rule(location, lambda state:
        (state.has("Gravity boots", player) or sotn_has_flying(state, player)) and (
         sotn_has_any(state, player) or state.has("Jewel of open", player)))

        location = world.get_location("NO2 - Heart Vessel", player)
        set_rule(location, lambda state: state.has("Leap stone", player) or sotn_has_any(state, player))
    else:
        location = world.get_location("NO2 - Garnet", player)
        set_rule(location, lambda state: sotn_has_flying(state, player))

        location = world.get_location("NO2 - Heart Vessel", player)
        set_rule(location, lambda state: sotn_has_flying(state, player))

    location = world.get_location("Enemysanity: 57 - Spectral sword", player)
    set_rule(location, lambda state: sotn_has_any(state, player))

    location = world.get_location("Enemysanity: 83 - Blade", player)
    set_rule(location, lambda state: sotn_has_any(state, player))

    location = world.get_location("Enemysanity: 85 - Hammer", player)
    set_rule(location, lambda state: sotn_has_any(state, player))

    location = world.get_location("Enemysanity: 92 - Olrox", player)
    set_rule(location, lambda state: sotn_has_flying(state, player))

    location = world.get_location("Dropsanity: 57 - Spectral sword", player)
    set_rule(location, lambda state: sotn_has_any(state, player))

    location = world.get_location("Dropsanity: 83 - Blade", player)
    set_rule(location, lambda state: sotn_has_any(state, player))

    location = world.get_location("Dropsanity: 85 - Hammer", player)
    set_rule(location, lambda state: sotn_has_any(state, player))

    # NO3 - Castle Entrance
    location = world.get_location("NO3 - Life Vessel (Above entry)", player)
    set_rule(location, lambda state: sotn_has_flying(state, player))

    location = world.get_location("NO3 - Holy mail", player)
    set_rule(location, lambda state: state.has("Gravity boots", player) or sotn_has_flying(state, player))

    location = world.get_location("NO3 - Life Apple (Hidden room)", player)
    set_rule(location, lambda state: state.has("Soul of bat", player) and state.has("Soul of wolf", player))

    location = world.get_location("NO3 - Jewel sword", player)
    set_rule(location, lambda state: state.has("Soul of bat", player) and state.has("Soul of wolf", player))

    if no4:
        # With backdoor open, every item beyond waterfall need some kinda of flying or jewel + regular need
        location = world.get_location("NO4 - Scylla kill", player)
        set_rule(location, lambda state: sotn_has_flying(state, player) or state.has("Jewel of open", player))

        location = world.get_location("NO4 - Succubus kill", player)
        set_rule(location, lambda state: sotn_has_flying(state, player) or
                                         (state.has("Jewel of open", player) and sotn_has_flying(state, player)))

        location = world.get_location("NO4 - Toadstool(Waterfall)", player)
        set_rule(location, lambda state: sotn_has_any(state, player) or state.has("Jewel of open", player))

        location = world.get_location("NO4 - Shiitake(Waterfall)", player)
        set_rule(location, lambda state: sotn_has_flying(state, player) or state.has("Jewel of open", player))

        location = world.get_location("NO4 - Secret boots", player)
        set_rule(location, lambda state: sotn_has_flying(state, player) or
                                         (state.has("Jewel of open", player) and sotn_has_any(state, player)))

        location = world.get_location("NO4 - Herald Shield", player)
        set_rule(location, lambda state: sotn_has_flying(state, player) or (state.has("Jewel of open", player) and
                                                                            state.has("Soul of wolf", player) and
                                                                            state.has("Power of wolf", player)))

        location = world.get_location("NO4 - Pentagram", player)
        set_rule(location, lambda state: sotn_has_flying(state, player))

        location = world.get_location("NO4 - Life Vessel(Bellow bridge)", player)
        set_rule(location, lambda state: sotn_has_flying(state, player) or (state.has("Jewel of open", player) and
                                                                            state.has("Soul of wolf", player) and
                                                                            state.has("Power of wolf", player)))

        location = world.get_location("NO4 - Heart Vessel(Bellow bridge)", player)
        set_rule(location, lambda state: sotn_has_flying(state, player) or (state.has("Jewel of open", player) and
                                                                            state.has("Soul of wolf", player) and
                                                                            state.has("Power of wolf", player)))

        location = world.get_location("NO4 - Antivenom(Underwater)", player)
        set_rule(location, lambda state: sotn_has_flying(state, player) or state.has("Jewel of open", player))

        location = world.get_location("NO4 - Life Vessel(Underwater)", player)
        set_rule(location, lambda state: sotn_has_flying(state, player) or state.has("Jewel of open", player))

        location = world.get_location("NO4 - Toadstool(26)", player)
        set_rule(location, lambda state: sotn_has_flying(state, player) or state.has("Jewel of open", player))

        location = world.get_location("NO4 - Shiitake(27)", player)
        set_rule(location, lambda state: sotn_has_flying(state, player) or state.has("Jewel of open", player))

        location = world.get_location("NO4 - Nunchaku", player)
        set_rule(location, lambda state: state.has("Holy symbol", player) and
                                         (sotn_has_flying(state, player) or state.has("Jewel of open", player)))

        location = world.get_location("NO4 - Shiitake(12)", player)
        set_rule(location, lambda state: sotn_has_flying(state, player) or state.has("Jewel of open", player))

        location = world.get_location("NO4 - Life Vessel(1)", player)
        set_rule(location, lambda state: sotn_has_flying(state, player) or state.has("Jewel of open", player))

        location = world.get_location("NO4 - Heart Vessel(0)", player)
        set_rule(location, lambda state: sotn_has_flying(state, player) or state.has("Jewel of open", player))

        location = world.get_location("NO4 - Bandanna", player)
        set_rule(location, lambda state: sotn_has_flying(state, player) or state.has("Jewel of open", player))

        location = world.get_location("NO4 - Zircon", player)
        set_rule(location, lambda state: (sotn_has_flying(state, player) or state.has("Jewel of open", player)) and
                                         sotn_has_any(state, player))

        location = world.get_location("NO4 - Claymore", player)
        set_rule(location, lambda state: (state.has("Jewel of open", player) and sotn_has_flying(state, player)) or
                                         sotn_has_flying(state, player))

        location = world.get_location("NO4 - Meal ticket 1(Succubus)", player)
        set_rule(location, lambda state: (state.has("Jewel of open", player) and sotn_has_flying(state, player)) or
                                         sotn_has_flying(state, player))

        location = world.get_location("NO4 - Meal ticket 2(Succubus)", player)
        set_rule(location, lambda state: (state.has("Jewel of open", player) and sotn_has_flying(state, player)) or
                                         sotn_has_flying(state, player))

        location = world.get_location("NO4 - Meal ticket 3(Succubus)", player)
        set_rule(location, lambda state: (state.has("Jewel of open", player) and sotn_has_flying(state, player)) or
                                         sotn_has_flying(state, player))

        location = world.get_location("NO4 - Meal ticket 4(Succubus)", player)
        set_rule(location, lambda state: (state.has("Jewel of open", player) and sotn_has_flying(state, player)) or
                                         sotn_has_flying(state, player))

        location = world.get_location("NO4 - Moonstone", player)
        set_rule(location, lambda state: (state.has("Jewel of open", player) and sotn_has_flying(state, player)) or
                                         sotn_has_flying(state, player))

        location = world.get_location("NO4 - Gold Ring", player)
        set_rule(location, lambda state: (state.has("Jewel of open", player) and sotn_has_flying(state, player)) or
                                         sotn_has_flying(state, player))

        location = world.get_location("NO4 - Resist ice", player)
        set_rule(location, lambda state: state.has("Jewel of open", player) or sotn_has_flying(state, player))

        location = world.get_location("NO4 - Scimitar", player)
        set_rule(location, lambda state: state.has("Jewel of open", player) or sotn_has_flying(state, player))

        location = world.get_location("NO4 - Pot roast", player)
        set_rule(location, lambda state: state.has("Jewel of open", player) or sotn_has_flying(state, player))

        location = world.get_location("NO4 - Crystal cloak", player)
        set_rule(location, lambda state: state.has("Jewel of open", player) or sotn_has_flying(state, player))

        location = world.get_location("NO4 - Life Vessel(Holy)", player)
        set_rule(location, lambda state: state.has("Jewel of open", player) or sotn_has_flying(state, player))

        location = world.get_location("NO4 - Knuckle duster(Holy)", player)
        set_rule(location, lambda state: state.has("Jewel of open", player) or sotn_has_flying(state, player))

        location = world.get_location("NO4 - Onyx(Holy)", player)
        set_rule(location, lambda state: sotn_has_flying(state, player) or (state.has("Merman statue", player) or
                                                                            sotn_has_any(state, player) and
                                                                            state.has("Jewel of open", player)))

        location = world.get_location("NO4 - Elixir(Holy)", player)
        set_rule(location, lambda state: state.has("Merman statue", player) and (state.has("Jewel of open", player) or
                                                                         sotn_has_flying(state, player)))

        location = world.get_location("Enemysanity: 37 - Scylla wyrm", player)
        set_rule(location, lambda state: state.has("Jewel of open", player) or sotn_has_flying(state, player))

        location = world.get_location("Enemysanity: 44 - Toad", player)
        set_rule(location, lambda state: state.has("Jewel of open", player) or sotn_has_flying(state, player))

        location = world.get_location("Enemysanity: 48 - Frog", player)
        set_rule(location, lambda state: state.has("Jewel of open", player) or sotn_has_flying(state, player))

        location = world.get_location("Enemysanity: 59 - Scylla", player)
        set_rule(location, lambda state: state.has("Jewel of open", player) or sotn_has_flying(state, player))

        location = world.get_location("Enemysanity: 93 - Succubus", player)
        set_rule(location, lambda state: state.has("Jewel of open", player) or sotn_has_flying(state, player))

        location = world.get_location("Enemysanity: 79 - Fishhead", player)
        set_rule(location, lambda state: state.has("Holy symbol", player) and
                                         (state.has("Jewel of open", player) or sotn_has_flying(state, player)))

        location = world.get_location("Enemysanity: 91 - Killer fish", player)
        set_rule(location, lambda state: state.has("Holy symbol", player) and
                                         (state.has("Jewel of open", player) or sotn_has_flying(state, player)))

        location = world.get_location("Dropsanity: 44 - Toad", player)
        set_rule(location, lambda state: state.has("Jewel of open", player) or sotn_has_flying(state, player))

        location = world.get_location("Dropsanity: 48 - Frog", player)
        set_rule(location, lambda state: state.has("Jewel of open", player) or sotn_has_flying(state, player))

        location = world.get_location("Dropsanity: 79 - Fishhead", player)
        set_rule(location, lambda state: state.has("Holy symbol", player) and
                                         (state.has("Jewel of open", player) or sotn_has_flying(state, player)))

        location = world.get_location("Dropsanity: 91 - Killer fish", player)
        set_rule(location, lambda state: state.has("Holy symbol", player) and
                                         (state.has("Jewel of open", player) or sotn_has_flying(state, player)))
    else:
        # NO3 - Life Vessel (UC exit) is the same need as NO4
        location = world.get_location("NO3 - Life Vessel (UC exit)", player)
        set_rule(location, lambda state: state.has("Jewel of open", player))
        # NO4 - Underground Caverns need only Jewel
        location = world.get_location("NO4 - Zircon", player)
        set_rule(location, lambda state: sotn_has_any(state, player))

        # Succubus
        location = world.get_location("NO4 - Claymore", player)
        set_rule(location, lambda state: sotn_has_flying(state, player))

        location = world.get_location("NO4 - Meal ticket 1(Succubus)", player)
        set_rule(location, lambda state: sotn_has_flying(state, player))

        location = world.get_location("NO4 - Meal ticket 2(Succubus)", player)
        set_rule(location, lambda state: sotn_has_flying(state, player))

        location = world.get_location("NO4 - Meal ticket 3(Succubus)", player)
        set_rule(location, lambda state: sotn_has_flying(state, player))

        location = world.get_location("NO4 - Meal ticket 4(Succubus)", player)
        set_rule(location, lambda state: sotn_has_flying(state, player))

        location = world.get_location("NO4 - Moonstone", player)
        set_rule(location, lambda state: sotn_has_flying(state, player))

        location = world.get_location("NO4 - Gold Ring", player)
        set_rule(location, lambda state: sotn_has_flying(state, player))

        location = world.get_location("NO4 - Succubus kill", player)
        set_rule(location, lambda state: sotn_has_flying(state, player) or
                                         (state.has("Jewel of open", player) and sotn_has_flying(state, player)))

        location = world.get_location("NO4 - Secret boots", player)
        set_rule(location, lambda state: sotn_has_any(state, player))

        location = world.get_location("NO4 - Herald Shield", player)
        set_rule(location, lambda state: state.has("Leap stone", player) or sotn_has_flying(state, player) or
                                         (state.has("Soul of wolf", player) and state.has("Power of wolf", player)))

        location = world.get_location("NO4 - Life Vessel(Bellow bridge)", player)
        set_rule(location, lambda state: state.has("Leap stone", player) or sotn_has_flying(state, player) or
                                         (state.has("Soul of wolf", player) and state.has("Power of wolf", player)))

        location = world.get_location("NO4 - Heart Vessel(Bellow bridge)", player)
        set_rule(location, lambda state: state.has("Leap stone", player) or sotn_has_flying(state, player) or
                                         (state.has("Soul of wolf", player) and state.has("Power of wolf", player)))

        location = world.get_location("NO4 - Elixir(Holy)", player)
        set_rule(location, lambda state: state.has("Merman statue", player))

        location = world.get_location("NO4 - Onyx(Holy)", player)
        set_rule(location, lambda state: state.has("Merman statue", player) or sotn_has_any(state, player))

        location = world.get_location("NO4 - Nunchaku", player)
        set_rule(location, lambda state: state.has("Holy symbol", player))

        location = world.get_location("Enemysanity: 37 - Scylla wyrm", player)
        set_rule(location, lambda state: state.has("Jewel of open", player))

        location = world.get_location("Enemysanity: 44 - Toad", player)
        set_rule(location, lambda state: state.has("Jewel of open", player))

        location = world.get_location("Enemysanity: 48 - Frog", player)
        set_rule(location, lambda state: state.has("Jewel of open", player))

        location = world.get_location("Enemysanity: 49 - Frozen shade", player)
        set_rule(location, lambda state: state.has("Jewel of open", player))

        location = world.get_location("Enemysanity: 59 - Scylla", player)
        set_rule(location, lambda state: state.has("Jewel of open", player))

        location = world.get_location("Enemysanity: 93 - Succubus", player)
        set_rule(location, lambda state: state.has("Jewel of open", player) and sotn_has_flying(state, player))

        location = world.get_location("Enemysanity: 79 - Fishhead", player)
        set_rule(location, lambda state: state.has("Holy symbol", player) and state.has("Jewel of open", player))

        location = world.get_location("Enemysanity: 91 - Killer fish", player)
        set_rule(location, lambda state: state.has("Holy symbol", player) and state.has("Jewel of open", player))

        """location = world.get_location("Enemysanity: 37 - Scylla wyrm", player)
        set_rule(location, lambda state: state.has("Jewel of open", player))"""

        location = world.get_location("Dropsanity: 44 - Toad", player)
        set_rule(location, lambda state: state.has("Jewel of open", player))

        location = world.get_location("Dropsanity: 48 - Frog", player)
        set_rule(location, lambda state: state.has("Jewel of open", player))

        location = world.get_location("Dropsanity: 49 - Frozen shade", player)
        set_rule(location, lambda state: state.has("Jewel of open", player))

        location = world.get_location("Dropsanity: 79 - Fishhead", player)
        set_rule(location, lambda state: state.has("Holy symbol", player) and state.has("Jewel of open", player))

        location = world.get_location("Dropsanity: 91 - Killer fish", player)
        set_rule(location, lambda state: state.has("Holy symbol", player) and state.has("Jewel of open", player))

    # NZ1 - Clock tower
    location = world.get_location("NZ1 - Bekatowa", player)
    set_rule(location, lambda state: sotn_has_flying(state, player))

    location = world.get_location("NZ1 - Shaman shield", player)
    set_rule(location, lambda state: sotn_has_flying(state, player))

    location = world.get_location("NZ1 - Ice mail", player)
    set_rule(location, lambda state: sotn_has_flying(state, player))

    # Can come from DAI or NO1
    location = world.get_location("NZ1 - Gold plate", player)
    set_rule(location, lambda state: sotn_has_any(state, player) or (state.has("Jewel of open", player) and
                                                                     (state.has("Gravity boots", player) or
                                                                      sotn_has_flying(state, player))))

    location = world.get_location("NZ1 - Star flail", player)
    set_rule(location, lambda state: sotn_has_any(state, player) or (state.has("Jewel of open", player) and
                                                                     (state.has("Gravity boots", player) or
                                                                      sotn_has_flying(state, player))))

    location = world.get_location("NZ1 - Steel helm", player)
    set_rule(location, lambda state: sotn_has_any(state, player) or (state.has("Jewel of open", player) and
                                                                     (state.has("Gravity boots", player) or
                                                                      sotn_has_flying(state, player))))

    location = world.get_location("NZ1 - Life Vessel(Gear train)", player)
    set_rule(location, lambda state: sotn_has_any(state, player) or (state.has("Jewel of open", player) and
                                                                     (state.has("Gravity boots", player) or
                                                                      sotn_has_flying(state, player))))

    location = world.get_location("NZ1 - Heart Vessel(Gear train)", player)
    set_rule(location, lambda state: sotn_has_any(state, player) or (state.has("Jewel of open", player) and
                                                                     (state.has("Gravity boots", player) or
                                                                      sotn_has_flying(state, player))))

    location = world.get_location("NZ1 - Pot roast", player)
    set_rule(location, lambda state: sotn_has_any(state, player) or (state.has("Jewel of open", player) and
                                                                     (state.has("Gravity boots", player) or
                                                                      sotn_has_flying(state, player))))

    location = world.get_location("NZ1 - Healing mail", player)
    set_rule(location, lambda state: sotn_has_any(state, player) or (state.has("Jewel of open", player) and
                                                                     (state.has("Gravity boots", player) or
                                                                      sotn_has_flying(state, player))))

    location = world.get_location("NZ1 - TNT", player)
    set_rule(location, lambda state: sotn_has_any(state, player) or (state.has("Jewel of open", player) and
                                                                     (state.has("Gravity boots", player) or
                                                                      sotn_has_flying(state, player))))

    location = world.get_location("NZ1 - Bwaka knife", player)
    set_rule(location, lambda state: sotn_has_any(state, player) or (state.has("Jewel of open", player) and
                                                                     (state.has("Gravity boots", player) or
                                                                      sotn_has_flying(state, player))))

    location = world.get_location("NZ1 - Shuriken", player)
    set_rule(location, lambda state: sotn_has_any(state, player) or (state.has("Jewel of open", player) and
                                                                     (state.has("Gravity boots", player) or
                                                                      sotn_has_flying(state, player))))

    location = world.get_location("NZ1 - Karasuman kill", player)
    set_rule(location, lambda state: sotn_has_any(state, player) or (state.has("Jewel of open", player) and
                                                                     (state.has("Gravity boots", player) or
                                                                      sotn_has_flying(state, player))))

    # TOP - Castle Keep
    location = world.get_location("TOP - Turquoise", player)
    set_rule(location, lambda state: sotn_has_any(state, player))

    location = world.get_location("TOP - Turkey(Behind wall)", player)
    set_rule(location, lambda state: sotn_has_any(state, player))

    location = world.get_location("TOP - Falchion", player)
    set_rule(location, lambda state: state.has("Gravity boots", player) or sotn_has_flying(state, player))

    # High jump need it items and Richter
    location = world.get_location("TOP - Fire mail(Behind wall)", player)
    set_rule(location, lambda state: sotn_has_flying(state, player))

    world.get_location("TOP - Heart Vessel(Before Richter)", player)
    set_rule(location, lambda state: sotn_has_flying(state, player))

    location = world.get_location("TOP - Sirloin(Above Richter)", player)
    set_rule(location, lambda state: sotn_has_flying(state, player))

    location = world.get_location("TOP - Turkey(Above Richter)", player)
    set_rule(location, lambda state: sotn_has_flying(state, player))

    location = world.get_location("TOP - Pot roast(Above Richter)", player)
    set_rule(location, lambda state: sotn_has_flying(state, player))

    location = world.get_location("TOP - Frankfurter(Above Richter)", player)
    set_rule(location, lambda state: sotn_has_flying(state, player))

    location = world.get_location("TOP - Resist stone(Above Richter)", player)
    set_rule(location, lambda state: sotn_has_flying(state, player))

    location = world.get_location("TOP - Resist dark(Above Richter)", player)
    set_rule(location, lambda state: sotn_has_flying(state, player))

    location = world.get_location("TOP - Resist holy(Above Richter)", player)
    set_rule(location, lambda state: sotn_has_flying(state, player))

    location = world.get_location("TOP - Platinum mail(Above Richter)", player)
    set_rule(location, lambda state: sotn_has_flying(state, player))

    location = world.get_location("TOP - Life Vessel 1(Viewing room)", player)
    set_rule(location, lambda state: sotn_has_flying(state, player))

    location = world.get_location("TOP - Life Vessel 2(Viewing room)", player)
    set_rule(location, lambda state: sotn_has_flying(state, player))

    location = world.get_location("TOP - Heart Vessel 1(Viewing room)", player)
    set_rule(location, lambda state: sotn_has_flying(state, player))

    location = world.get_location("TOP - Heart Vessel 2(Viewing room)", player)
    set_rule(location, lambda state: sotn_has_flying(state, player))

    location = world.get_location("TOP - Heart Vessel(Before Richter)", player)
    set_rule(location, lambda state: sotn_has_flying(state, player))

    location = world.get_location("RNO0 - Heart Refresh(Inside clock)", player)
    set_rule(location, lambda state: sotn_has_dracula(state, player))

    # Reverse Castle -> Already have some kind of high jump
    location = world.get_location("RDAI - Twilight cloak", player)
    set_rule(location, lambda state: state.has("Spike breaker", player) and state.has("Form of mist", player) or
             (state.has("Form of mist", player) and state.has("Power of mist", player)))

    location = world.get_location("RNO2 - Akmodan II kill", player)
    set_rule(location, lambda state: sotn_has_transformation(state, player))

    location = world.get_location("RNO2 - Heart Vessel", player)
    set_rule(location, lambda state: sotn_has_transformation(state, player))

    location = world.get_location("RNO3 - Zircon", player)
    set_rule(location, lambda state: state.has("Soul of wolf", player) and state.has("Soul of bat", player))

    location = world.get_location("RNO3 - Opal", player)
    set_rule(location, lambda state: state.has("Soul of wolf", player) and state.has("Soul of bat", player))

    location = world.get_location("RNO3 - Beryl circlet", player)
    set_rule(location, lambda state: state.has("Soul of wolf", player) and state.has("Soul of bat", player))

    location = world.get_location("RNO0 - Library card", player)
    set_rule(location, lambda state: state.has("Jewel of open", player))

    location = world.get_location("RNO1 - Hammer", player)
    set_rule(location, lambda state: state.has("Form of mist", player))

    location = world.get_location("RNO1 - Shotel", player)
    set_rule(location, lambda state: state.has("Form of mist", player))

    location = world.get_location("RLIB - Staurolite", player)
    set_rule(location, lambda state: state.has("Form of mist", player))

    location = world.get_location("RNO4 - Life Vessel(Underwater)", player)
    set_rule(location, lambda state: state.has("Gravity boots", player))

    location = world.get_location("RNO4 - Bat Pentagram", player)
    set_rule(location, lambda state: state.has("Leap stone", player) or state.has("Soul of bat", player))

    location = world.get_location("RNO4 - Potion(Underwater)", player)
    set_rule(location, lambda state: state.has("Gravity boots", player))

    location = world.get_location("RNO4 - Heart Vessel(Air pocket)", player)
    set_rule(location, lambda state: state.has("Gravity boots", player) and state.has("Holy symbol", player))

    location = world.get_location("RNO4 - Osafune katana", player)
    set_rule(location, lambda state: state.has("Soul of bat", player) or (state.has("Gravity boots", player) and
                                                  (state.has("Leap stone", player))))

    location = world.get_location("RCHI - Power of Sire(Demon)", player)
    set_rule(location, lambda state: state.has("Demon card", player))

    location = world.get_location("RCHI - Life apple(Demon)", player)
    set_rule(location, lambda state: state.has("Demon card", player))

    location = world.get_location("RCHI - Green tea(Demon)", player)
    set_rule(location, lambda state: state.has("Demon card", player))

    location = world.get_location("RCAT - Resist thunder", player)
    set_rule(location, lambda state: state.has("Soul of bat", player) or
             (state.has("Form of mist", player) and state.has("Power of mist", player)) or
             (state.has("Spike Breaker", player) and (state.has("Leap stone", player) or
                                                      state.has("Gravity boots", player))))

    location = world.get_location("RCAT - Resist fire", player)
    set_rule(location, lambda state: state.has("Soul of bat", player) or
             (state.has("Form of mist", player) and state.has("Power of mist", player)) or
             (state.has("Spike Breaker", player) and (state.has("Leap stone", player) or
                                                      state.has("Gravity boots", player))))

    location = world.get_location("RCAT - Karma coin(4)(Spike breaker)", player)
    set_rule(location, lambda state: state.has("Soul of bat", player) or
             (state.has("Form of mist", player) and state.has("Power of mist", player)) or
             (state.has("Spike Breaker", player) and (state.has("Leap stone", player) or
                                                      state.has("Gravity boots", player))))

    location = world.get_location("RCAT - Karma coin(5)(Spike breaker)", player)
    set_rule(location, lambda state: state.has("Soul of bat", player) or
             (state.has("Form of mist", player) and state.has("Power of mist", player)) or
             (state.has("Spike Breaker", player) and (state.has("Leap stone", player) or
                                                      state.has("Gravity boots", player))))

    location = world.get_location("RCAT - Red bean bun", player)
    set_rule(location, lambda state: state.has("Soul of bat", player) or
             (state.has("Form of mist", player) and state.has("Power of mist", player)) or
             (state.has("Spike Breaker", player) and (state.has("Leap stone", player) or
                                                      state.has("Gravity boots", player))))

    location = world.get_location("RCAT - Elixir", player)
    set_rule(location, lambda state: state.has("Soul of bat", player) or
             (state.has("Form of mist", player) and state.has("Power of mist", player)) or
             (state.has("Spike Breaker", player) and (state.has("Leap stone", player) or
                                                      state.has("Gravity boots", player))))

    location = world.get_location("RCAT - Library card", player)
    set_rule(location, lambda state: state.has("Soul of bat", player) or
             (state.has("Form of mist", player) and state.has("Power of mist", player)) or
             (state.has("Spike Breaker", player) and (state.has("Leap stone", player) or
                                                      state.has("Gravity boots", player))))

    # Exploration rules
    location = world.get_location("Exploration 40", player)
    set_rule(location, lambda state: state.has("Jewel of open", player) or state.has("Leap stone", player) or
                                     state.has("Gravity boots", player) or state.has("Soul of bat", player))

    location = world.get_location("Exploration 50", player)
    set_rule(location, lambda state: state.has("Jewel of open", player) or state.has("Leap stone", player) or
                                     state.has("Gravity boots", player) or state.has("Soul of bat", player))

    location = world.get_location("Exploration 60", player)
    set_rule(location, lambda state: state.has("Jewel of open", player) and (state.has("Leap stone", player) or
                                                                             state.has("Gravity boots", player) or
                                                                             state.has("Soul of bat", player)))

    location = world.get_location("Exploration 70", player)
    set_rule(location, lambda state: state.has("Jewel of open", player) and (state.has("Leap stone", player) or
                                                                             state.has("Gravity boots", player) or
                                                                             state.has("Soul of bat", player)))

    location = world.get_location("Exploration 80", player)
    set_rule(location, lambda state: state.has("Jewel of open", player) and (state.has("Soul of bat", player) or
                                                                             (state.has("Gravity boots", player) and
                                                                              (state.has("Leap stone", player) or
                                                                               state.has("Soul of wolf", player) or
                                                                               state.has("Form of mist", player)) or
                                                                              (state.has("Form of mist", player) and
                                                                               state.has("Power of mist", player)))))

    location = world.get_location("Exploration 90", player)
    set_rule(location, lambda state: state.has("Jewel of open", player) and (state.has("Soul of bat", player) or
                                                                             (state.has("Gravity boots", player) and
                                                                              (state.has("Leap stone", player) or
                                                                               state.has("Soul of wolf", player) or
                                                                               state.has("Form of mist", player)) or
                                                                              (state.has("Form of mist", player) and
                                                                               state.has("Power of mist", player)))))

    location = world.get_location("Exploration 100", player)
    set_rule(location, lambda state: state.has("Holy glasses", player) and state.has("Jewel of open", player) and
                                     (state.has("Soul of bat", player) or (state.has("Form of mist", player) and
                                                                           state.has("Power of mist", player)) or
                                      (state.has("Gravity boots", player) and (state.has("Leap stone", player) or
                                                                               state.has("Soul of wolf", player) or
                                                                               state.has("Form of mist", player)))))

    location = world.get_location("Exploration 110", player)
    set_rule(location, lambda state: state.has("Holy glasses", player) and state.has("Jewel of open", player) and
                                     (state.has("Soul of bat", player) or (state.has("Form of mist", player) and
                                                                           state.has("Power of mist", player)) or
                                      (state.has("Gravity boots", player) and (state.has("Leap stone", player) or
                                                                               state.has("Soul of wolf", player) or
                                                                               state.has("Form of mist", player)))))

    location = world.get_location("Exploration 120", player)
    set_rule(location, lambda state: state.has("Holy glasses", player) and state.has("Jewel of open", player) and
                                     (state.has("Soul of bat", player) or (state.has("Form of mist", player) and
                                                                           state.has("Power of mist", player)) or
                                      (state.has("Gravity boots", player) and (state.has("Leap stone", player) or
                                                                               state.has("Soul of wolf", player) or
                                                                               state.has("Form of mist", player)))))

    location = world.get_location("Exploration 130", player)
    set_rule(location, lambda state: state.has("Holy glasses", player) and state.has("Jewel of open", player) and
                                     (state.has("Soul of bat", player) or (state.has("Form of mist", player) and
                                                                           state.has("Power of mist", player)) or
                                      (state.has("Gravity boots", player) and (state.has("Leap stone", player) or
                                                                               state.has("Soul of wolf", player) or
                                                                               state.has("Form of mist", player)))))

    location = world.get_location("Exploration 140", player)
    set_rule(location, lambda state: state.has("Holy glasses", player) and state.has("Jewel of open", player) and
                                     (state.has("Soul of bat", player) or (state.has("Form of mist", player) and
                                                                           state.has("Power of mist", player)) or
                                      (state.has("Gravity boots", player) and (state.has("Leap stone", player) or
                                                                               state.has("Soul of wolf", player) or
                                                                               state.has("Form of mist", player)))))

    location = world.get_location("Exploration 150", player)
    set_rule(location, lambda state: state.has("Holy glasses", player) and state.has("Jewel of open", player) and
                                     (state.has("Soul of bat", player) or (state.has("Form of mist", player) and
                                                                           state.has("Power of mist", player)) or
                                      (state.has("Gravity boots", player) and (state.has("Leap stone", player) or
                                                                               state.has("Soul of wolf", player) or
                                                                               state.has("Form of mist", player)))))

    location = world.get_location("Exploration 160", player)
    set_rule(location, lambda state: state.has("Holy glasses", player) and state.has("Jewel of open", player) and
                                     (state.has("Soul of bat", player) or (state.has("Form of mist", player) and
                                                                           state.has("Power of mist", player)) or
                                      (state.has("Gravity boots", player) and (state.has("Leap stone", player) or
                                                                               state.has("Soul of wolf", player) or
                                                                               state.has("Form of mist", player)))))

    location = world.get_location("Exploration 170", player)
    set_rule(location, lambda state: state.has("Holy glasses", player) and state.has("Jewel of open", player) and
                                     (state.has("Soul of bat", player) or (state.has("Form of mist", player) and
                                                                           state.has("Power of mist", player)) or
                                      (state.has("Gravity boots", player) and (state.has("Leap stone", player) or
                                                                               state.has("Soul of wolf", player) or
                                                                               state.has("Form of mist", player)))))

    location = world.get_location("Exploration 180", player)
    set_rule(location, lambda state: state.has("Holy glasses", player) and state.has("Jewel of open", player) and
                                     (state.has("Soul of bat", player) or (state.has("Form of mist", player) and
                                                                           state.has("Power of mist", player)) or
                                      (state.has("Gravity boots", player) and (state.has("Leap stone", player) or
                                                                               state.has("Soul of wolf", player) or
                                                                               state.has("Form of mist", player)))))

    location = world.get_location("Exploration 190", player)
    set_rule(location, lambda state: state.has("Soul of bat", player) and state.has("Soul of wolf", player) and
                                     state.has("Form of mist", player) and state.has("Merman statue", player) and
                                     state.has("Spike breaker", player) and state.has("Demon card", player) and
                                     state.has("Holy symbol", player) and state.has("Holy glasses", player) and
                                     state.has("Silver ring", player) and state.has("Gold ring", player))

    location = world.get_location("Exploration 200", player)
    set_rule(location, lambda state: state.has("Soul of bat", player) and state.has("Soul of wolf", player) and
                                     state.has("Form of mist", player) and state.has("Merman statue", player) and
                                     state.has("Spike breaker", player) and state.has("Demon card", player) and
                                     state.has("Holy symbol", player) and state.has("Holy glasses", player) and
                                     state.has("Silver ring", player) and state.has("Gold ring", player))

    location = world.get_location("Exploration 40 item", player)
    set_rule(location, lambda state: state.has("Jewel of open", player) or state.has("Leap stone", player) or
                                     state.has("Gravity boots", player) or state.has("Soul of bat", player))

    location = world.get_location("Exploration 50 item", player)
    set_rule(location, lambda state: state.has("Jewel of open", player) or state.has("Leap stone", player) or
                                     state.has("Gravity boots", player) or state.has("Soul of bat", player))

    location = world.get_location("Exploration 60 item", player)
    set_rule(location, lambda state: state.has("Jewel of open", player) and (state.has("Leap stone", player) or
                                                                             state.has("Gravity boots", player) or
                                                                             state.has("Soul of bat", player)))

    location = world.get_location("Exploration 70 item", player)
    set_rule(location, lambda state: state.has("Jewel of open", player) and (state.has("Leap stone", player) or
                                                                             state.has("Gravity boots", player) or
                                                                             state.has("Soul of bat", player)))

    location = world.get_location("Exploration 80 item", player)
    set_rule(location, lambda state: state.has("Jewel of open", player) and (state.has("Soul of bat", player) or
                                                                             (state.has("Gravity boots", player) and
                                                                              (state.has("Leap stone", player) or
                                                                               state.has("Soul of wolf", player) or
                                                                               state.has("Form of mist", player)) or
                                                                              (state.has("Form of mist", player) and
                                                                               state.has("Power of mist", player)))))

    location = world.get_location("Exploration 90 item", player)
    set_rule(location, lambda state: state.has("Jewel of open", player) and (state.has("Soul of bat", player) or
                                                                             (state.has("Gravity boots", player) and
                                                                              (state.has("Leap stone", player) or
                                                                               state.has("Soul of wolf", player) or
                                                                               state.has("Form of mist", player)) or
                                                                              (state.has("Form of mist", player) and
                                                                               state.has("Power of mist", player)))))

    location = world.get_location("Exploration 100 item", player)
    set_rule(location, lambda state: state.has("Holy glasses", player) and
                                     state.has("Jewel of open", player) and (state.has("Soul of bat", player) or
                                                                             (state.has("Form of mist", player) and
                                                                              state.has("Power of mist", player)) or
                                                                             (state.has("Gravity boots", player) and
                                                                              (state.has("Leap stone", player) or
                                                                               state.has("Soul of wolf", player) or
                                                                               state.has("Form of mist", player)))))

    location = world.get_location("Exploration 110 item", player)
    set_rule(location, lambda state: state.has("Holy glasses", player) and state.has("Jewel of open", player) and
                                     (state.has("Soul of bat", player) or (state.has("Form of mist", player) and
                                                                           state.has("Power of mist", player)) or
                                      (state.has("Gravity boots", player) and (state.has("Leap stone", player) or
                                                                               state.has("Soul of wolf", player) or
                                                                               state.has("Form of mist", player)))))

    location = world.get_location("Exploration 120 item", player)
    set_rule(location, lambda state: state.has("Holy glasses", player) and state.has("Jewel of open", player) and
                                     (state.has("Soul of bat", player) or (state.has("Form of mist", player) and
                                                                           state.has("Power of mist", player)) or
                                      (state.has("Gravity boots", player) and (state.has("Leap stone", player) or
                                                                               state.has("Soul of wolf", player) or
                                                                               state.has("Form of mist", player)))))

    location = world.get_location("Exploration 130 item", player)
    set_rule(location, lambda state: state.has("Holy glasses", player) and state.has("Jewel of open", player) and
                                     (state.has("Soul of bat", player) or (state.has("Form of mist", player) and
                                                                           state.has("Power of mist", player)) or
                                      (state.has("Gravity boots", player) and (state.has("Leap stone", player) or
                                                                               state.has("Soul of wolf", player) or
                                                                               state.has("Form of mist", player)))))

    location = world.get_location("Exploration 140 item", player)
    set_rule(location, lambda state: state.has("Holy glasses", player) and state.has("Jewel of open", player) and
                                     (state.has("Soul of bat", player) or (state.has("Form of mist", player) and
                                                                           state.has("Power of mist", player)) or
                                      (state.has("Gravity boots", player) and (state.has("Leap stone", player) or
                                                                               state.has("Soul of wolf", player) or
                                                                               state.has("Form of mist", player)))))

    location = world.get_location("Exploration 150 item", player)
    set_rule(location, lambda state: state.has("Holy glasses", player) and state.has("Jewel of open", player) and
                                     (state.has("Soul of bat", player) or (state.has("Form of mist", player) and
                                                                           state.has("Power of mist", player)) or
                                      (state.has("Gravity boots", player) and (state.has("Leap stone", player) or
                                                                               state.has("Soul of wolf", player) or
                                                                               state.has("Form of mist", player)))))

    location = world.get_location("Exploration 160 item", player)
    set_rule(location, lambda state: state.has("Holy glasses", player) and state.has("Jewel of open", player) and
                                     (state.has("Soul of bat", player) or (state.has("Form of mist", player) and
                                                                           state.has("Power of mist", player)) or
                                      (state.has("Gravity boots", player) and (state.has("Leap stone", player) or
                                                                               state.has("Soul of wolf", player) or
                                                                               state.has("Form of mist", player)))))

    location = world.get_location("Exploration 170 item", player)
    set_rule(location, lambda state: state.has("Holy glasses", player) and state.has("Jewel of open", player) and
                                     (state.has("Soul of bat", player) or (state.has("Form of mist", player) and
                                                                           state.has("Power of mist", player)) or
                                      (state.has("Gravity boots", player) and (state.has("Leap stone", player) or
                                                                               state.has("Soul of wolf", player) or
                                                                               state.has("Form of mist", player)))))

    location = world.get_location("Exploration 180 item", player)
    set_rule(location, lambda state: state.has("Holy glasses", player) and state.has("Jewel of open", player) and
                                     (state.has("Soul of bat", player) or (state.has("Form of mist", player) and
                                                                           state.has("Power of mist", player)) or
                                      (state.has("Gravity boots", player) and (state.has("Leap stone", player) or
                                                                               state.has("Soul of wolf", player) or
                                                                               state.has("Form of mist", player)))))

    location = world.get_location("Exploration 190 item", player)
    set_rule(location, lambda state: state.has("Soul of bat", player) and state.has("Soul of wolf", player) and
                                     state.has("Form of mist", player) and state.has("Merman statue", player) and
                                     state.has("Spike breaker", player) and state.has("Demon card", player) and
                                     state.has("Holy symbol", player) and state.has("Holy glasses", player) and
                                     state.has("Silver ring", player) and state.has("Gold ring", player))

    location = world.get_location("Exploration 200 item", player)
    set_rule(location, lambda state: state.has("Soul of bat", player) and state.has("Soul of wolf", player) and
                                     state.has("Form of mist", player) and state.has("Merman statue", player) and
                                     state.has("Spike breaker", player) and state.has("Demon card", player) and
                                     state.has("Holy symbol", player) and state.has("Holy glasses", player) and
                                     state.has("Silver ring", player) and state.has("Gold ring", player))
