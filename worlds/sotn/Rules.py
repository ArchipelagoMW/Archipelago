from worlds.generic.Rules import forbid_item, set_rule
from BaseClasses import MultiWorld

from .Items import vessel_table
from .Locations import location_table

# TODO: Set difficult on locations to enforce castle exploration. Can also be an option


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
    set_rule(location, lambda state: state.has("Form of mist", player) and (state.has("Leap stone", player) or
             state.has("Soul of bat", player) or state.has("Gravity boots", player) or
             (state.has("Form of mist", player) and state.has("Power of mist", player))))
    location = world.get_location("Fire of Bat", player)
    set_rule(location, lambda state: state.has("Soul of bat", player) or (state.has("Gravity boots", player) and
             (state.has("Leap stone", player) or state.has("Soul of wolf", player) or
              state.has("Form of mist", player))))
    location = world.get_location("Echo of Bat", player)
    set_rule(location, lambda state: state.has("Soul of bat", player) or (state.has("Form of mist", player) and
             state.has("Power of mist", player)) or (state.has("Gravity boots", player) and
             (state.has("Leap stone", player) or state.has("Soul of wolf", player) or
              state.has("Form of mist", player))))
    location = world.get_location("Power of Wolf", player)
    set_rule(location, lambda state: state.has("Soul of bat", player) or (state.has("Gravity boots", player) and
             (state.has("Leap stone", player) or state.has("Soul of wolf", player) or
              state.has("Form of mist", player))))
    location = world.get_location("Skill of Wolf", player)
    set_rule(location, lambda state: state.has("Soul of bat", player) or state.has("Gravity boots", player) or
             (state.has("Form of mist", player) and state.has("Power of mist", player)))
    if are:
        location = world.get_location("Form of Mist", player)
        set_rule(location, lambda state: state.has("Jewel of open", player) or state.has("Gravity boots", player) or
                 (state.has("Form of mist", player) and state.has("Power of mist", player)))
    location = world.get_location("Power of Mist", player)
    set_rule(location, lambda state: state.has("Soul of bat", player) or (state.has("Gravity boots", player) and
             (state.has("Leap stone", player) or state.has("Soul of wolf", player) or
              state.has("Form of mist", player))) or (state.has("Form of mist", player) and
                                                      state.has("Power of mist", player)))
    location = world.get_location("Gravity Boots", player)
    set_rule(location, lambda state: state.has("Soul of bat", player) or (state.has("Form of mist", player) and
             state.has("Power of mist", player)) or (state.has("Gravity boots", player) and
             (state.has("Leap stone", player) or state.has("Soul of wolf", player) or
              state.has("Form of mist", player))))
    if not no4:
        location = world.get_location("Holy Symbol", player)
        set_rule(location, lambda state: state.has("Merman statue", player) and state.has("Jewel of open", player))
        location = world.get_location("Merman Statue", player)
        set_rule(location, lambda state: state.has("Jewel of open", player))
    else:
        location = world.get_location("Holy Symbol", player)
        set_rule(location, lambda state: state.has("Merman statue", player) and
                 (state.has("Soul of bat", player) or (state.has("Gravity boots", player) and
                                                       (state.has("Leap stone", player) or
                                                        state.has("Soul of wolf", player) or
                                                        state.has("Form of mist", player))) or
                  (state.has("Form of mist", player) and state.has("Power of mist", player))))
    location = world.get_location("Bat Card", player)
    set_rule(location, lambda state: state.has("Soul of bat", player) or (state.has("Form of mist", player) and
             state.has("Power of mist", player)) or (state.has("Gravity boots", player) and
             (state.has("Leap stone", player) or state.has("Soul of wolf", player) or
              state.has("Form of mist", player))))
    location = world.get_location("Ghost Card", player)
    set_rule(location, lambda state: state.has("Soul of bat", player) or (state.has("Gravity boots", player) and
                                                                          (state.has("Leap stone", player) or
                                                                           state.has("Soul of wolf", player) or
                                                                           state.has("Form of mist", player))) or
             (state.has("Form of mist", player) and state.has("Power of mist", player)))
    location = world.get_location("Faerie Card", player)
    set_rule(location, lambda state: state.has("Leap stone", player) or state.has("Soul of bat", player) or
             state.has("Gravity boots", player) or state.has("Form of mist", player) and
             state.has("Power of mist", player))
    location = world.get_location("Sword Card", player)
    set_rule(location, lambda state: state.has("Soul of bat", player) or (state.has("Form of mist", player) and
             state.has("Power of mist", player)) or (state.has("Gravity boots", player) and
             (state.has("Leap stone", player) or state.has("Soul of wolf", player) or
              state.has("Form of mist", player))))

# Items rules
    set_rule(world.get_location("ARE - Holy sword(Hidden attic)", player), lambda state:
             state.has("Gravity boots", player) or state.has("Soul of bat", player) or
             (state.has("Form of mist", player) and state.has("Power of mist", player)))

    # CAT - Catacombs worst case scenario player can get here with only jewel, soul and power of wolf
    # Spike breaker locations
    set_rule(world.get_location("CAT - Library card(Spike breaker)", player), lambda state:
             (state.has("Soul of bat", player) and state.has("Echo of bat", player)) or
             (state.has("Spike breaker", player) and (state.has("Leap stone", player) or
                                                      state.has("Gravity boots", player) or
                                                      state.has("Soul of bat", player))))

    set_rule(world.get_location("CAT - Cross shuriken 1(Spike breaker)", player), lambda state:
             (state.has("Soul of bat", player) and state.has("Echo of bat", player)) or
             (state.has("Spike breaker", player) and (state.has("Leap stone", player) or
                                                      state.has("Gravity boots", player) or
                                                      state.has("Soul of bat", player))))

    set_rule(world.get_location("CAT - Cross shuriken 2(Spike breaker)", player), lambda state:
             (state.has("Soul of bat", player) and state.has("Echo of bat", player)) or
             (state.has("Spike breaker", player) and (state.has("Leap stone", player) or
                                                      state.has("Gravity boots", player) or
                                                      state.has("Soul of bat", player))))

    set_rule(world.get_location("CAT - Karma coin 1(Spike breaker)", player), lambda state:
             (state.has("Soul of bat", player) and state.has("Echo of bat", player)) or
             (state.has("Spike breaker", player) or (state.has("Leap stone", player) or
                                                     state.has("Gravity boots", player) or
                                                     state.has("Soul of bat", player))))

    set_rule(world.get_location("CAT - Karma coin 2(Spike breaker)", player), lambda state:
             (state.has("Soul of bat", player) and state.has("Echo of bat", player)) or
             (state.has("Spike breaker", player) or (state.has("Leap stone", player) or
                                                     state.has("Gravity boots", player) or
                                                     state.has("Soul of bat", player))))

    set_rule(world.get_location("CAT - Spike breaker", player), lambda state:
             (state.has("Soul of bat", player) and state.has("Echo of bat", player)) or
             (state.has("Spike breaker", player) or (state.has("Leap stone", player) or
                                                     state.has("Gravity boots", player) or
                                                     state.has("Soul of bat", player))))

    set_rule(world.get_location("CAT - Icebrand", player), lambda
             state: state.has("Soul of bat", player) or state.has("Gravity boots", player) or
             (state.has("Form of mist", player) and state.has("Power of mist", player)))

    set_rule(world.get_location("CAT - Ballroom mask", player), lambda
             state: state.has("Soul of bat", player) or state.has("Gravity boots", player) or
             (state.has("Form of mist", player) and state.has("Power of mist", player)))

    set_rule(world.get_location("CAT - Heart Vessel(Ballroom mask)", player), lambda
             state: state.has("Soul of bat", player) or state.has("Gravity boots", player) or
             (state.has("Form of mist", player) and state.has("Power of mist", player)))

    # CHI - Abandoned Mine Same as CAT
    # Demon card locations
    set_rule(world.get_location("CHI - Power of sire(Demon)", player), lambda
             state: state.has("Demon card", player))

    set_rule(world.get_location("CHI - Barley tea(Demon)", player), lambda
             state: state.has("Demon card", player))

    set_rule(world.get_location("CHI - Peanuts 1(Demon)", player), lambda
             state: state.has("Demon card", player))

    set_rule(world.get_location("CHI - Peanuts 2(Demon)", player), lambda
             state: state.has("Demon card", player))

    set_rule(world.get_location("CHI - Peanuts 3(Demon)", player), lambda
             state: state.has("Demon card", player))

    set_rule(world.get_location("CHI - Peanuts 4(Demon)", player), lambda
             state: state.has("Demon card", player))

    set_rule(world.get_location("CHI - Turkey(Demon)", player), lambda
             state: state.has("Demon card", player))

    set_rule(world.get_location("CHI - Ring of ares", player), lambda
             state: state.has("Demon card", player))

    # DAI - Royal Chapel Worst case scenario only Jewel, maybe didn't have Jewel if he came from NZ1
    set_rule(world.get_location("DAI - Silver ring", player), lambda
             state: state.has("Form of mist", player) and state.has("Jewel of open", player) and
             state.has("Spike breaker", player))

    set_rule(world.get_location("DAI - Morningstar", player), lambda
             state: state.has("Leap stone", player) or state.has("Gravity boots", player) or
             state.has("Soul of bat", player) or (state.has("Form of mist", player) and
             state.has("Power of mist", player)))

    set_rule(world.get_location("DAI - Boomerang(Stairs)", player), lambda
             state: state.has("Leap stone", player) or state.has("Gravity boots", player) or
             state.has("Soul of bat", player) or (state.has("Form of mist", player) and
                                                  state.has("Power of mist", player)))

    set_rule(world.get_location("DAI - TNT(Stairs)", player), lambda
             state: state.has("Leap stone", player) or state.has("Gravity boots", player) or
             state.has("Soul of bat", player) or (state.has("Form of mist", player) and
                                                  state.has("Power of mist", player)))

    set_rule(world.get_location("DAI - Shuriken(Stairs)", player), lambda
             state: state.has("Leap stone", player) or state.has("Gravity boots", player) or
             state.has("Soul of bat", player) or (state.has("Form of mist", player) and
             state.has("Power of mist", player)))

    set_rule(world.get_location("DAI - Magic missile(Stairs)", player), lambda
             state: state.has("Leap stone", player) or state.has("Gravity boots", player) or
             state.has("Soul of bat", player) or (state.has("Form of mist", player) and
             state.has("Power of mist", player)))

    set_rule(world.get_location("DAI - Ankh of life(Stairs)", player), lambda
             state: state.has("Gravity boots", player) or state.has("Soul of bat", player) or
             (state.has("Form of mist", player) and state.has("Power of mist", player)))

    set_rule(world.get_location("DAI - Mystic pendant", player), lambda
             state: state.has("Gravity boots", player) or state.has("Soul of bat", player) or
             (state.has("Form of mist", player) and state.has("Power of mist", player)))

    # LIB - Long Library
    # Upper part of LIB(Faerie card) can be access with leap stone + kick and jump from an enemy
    set_rule(world.get_location("LIB - Takemitsu", player), lambda state: state.has("Leap stone", player) or
             state.has("Soul of bat", player) or state.has("Gravity boots", player) or
             (state.has("Form of mist", player) and state.has("Power of mist", player)))

    set_rule(world.get_location("LIB - Onyx", player), lambda state: state.has("Leap stone", player) or
             state.has("Soul of bat", player) or state.has("Gravity boots", player) or
             (state.has("Form of mist", player) and state.has("Power of mist", player)))

    set_rule(world.get_location("LIB - Frankfurter", player), lambda
             state: state.has("Leap stone", player) or state.has("Soul of bat", player) or
             state.has("Gravity boots", player) or (state.has("Form of mist", player) and
             state.has("Power of mist", player)))

    set_rule(world.get_location("LIB - Potion", player), lambda state: state.has("Leap stone", player) or
             state.has("Soul of bat", player) or state.has("Gravity boots", player) or
             (state.has("Form of mist", player) and state.has("Power of mist", player)))

    set_rule(world.get_location("LIB - Antivenom", player), lambda state: state.has("Leap stone", player) or
             state.has("Soul of bat", player) or state.has("Gravity boots", player) or
             (state.has("Form of mist", player) and state.has("Power of mist", player)))

    set_rule(world.get_location("LIB - Lesser Demon kill", player), lambda
             state: state.has("Leap stone", player) or state.has("Soul of bat", player) or
             state.has("Gravity boots", player) or (state.has("Form of mist", player) and
             state.has("Power of mist", player)))

    # If the player got here with only leap stone, he might need more to get to the upper part
    set_rule(world.get_location("LIB - Stone mask", player), lambda
             state: state.has("Gravity boots", player) or state.has("Soul of bat", player) or
             (state.has("Form of mist", player) and state.has("Power of mist", player)))

    set_rule(world.get_location("LIB - Holy rod", player), lambda
             state: state.has("Gravity boots", player) or state.has("Soul of bat", player) or
             (state.has("Form of mist", player) and state.has("Power of mist", player)))

    set_rule(world.get_location("LIB - Topaz circlet", player), lambda
             state: state.has("Gravity boots", player) or state.has("Soul of bat", player) or
             (state.has("Form of mist", player) and state.has("Power of mist", player)))

    # NO0 - Marble Gallery
    set_rule(world.get_location("NO0 - Str. potion", player), lambda state:
             state.has("Soul of bat", player) or state.has("Gravity boots", player) or
             (state.has("Form of mist", player) and state.has("Power of mist", player)))

    set_rule(world.get_location("NO0 - Hammer(Spirit)", player), lambda state:
             state.has("Soul of bat", player) or state.has("Gravity boots", player) or
             (state.has("Form of mist", player) and state.has("Power of mist", player)))

    set_rule(world.get_location("NO0 - Life Vessel(Left clock)", player), lambda state:
             state.has("Leap stone", player) or state.has("Soul of bat", player) or
             state.has("Gravity boots", player) or (state.has("Form of mist", player) and
             state.has("Power of mist", player)))

    set_rule(world.get_location("NO0 - Hammer(Middle clock)", player), lambda state:
             state.has("Soul of bat", player) or (state.has("Form of mist", player) and
             state.has("Power of mist", player)) or (state.has("Gravity boots", player) and
                                                     (state.has("Leap stone", player) or
                                                      state.has("Soul of wolf", player) or
                                                      state.has("Form of mist", player))))

    set_rule(world.get_location("NO0 - Life apple(Middle clock)", player), lambda state:
             state.has("Soul of bat", player) or (state.has("Form of mist", player) and
             state.has("Power of mist", player)) or (state.has("Gravity boots", player) and
                                                     (state.has("Leap stone", player) or
                                                      state.has("Soul of wolf", player) or
                                                      state.has("Form of mist", player))))

    set_rule(world.get_location("NO0 - Potion(Middle clock)", player), lambda state:
             state.has("Soul of bat", player) or (state.has("Form of mist", player) and
             state.has("Power of mist", player)) or (state.has("Gravity boots", player) and
                                                     (state.has("Leap stone", player) or
                                                      state.has("Soul of wolf", player) or
                                                      state.has("Form of mist", player))))

    set_rule(world.get_location("NO0 - Library card(Jewel)", player), lambda state:
             state.has("Jewel of open", player))

    set_rule(world.get_location("NO0 - Attack potion(Jewel)", player), lambda state:
             state.has("Jewel of open", player))

    set_rule(world.get_location("NO0 - Heart Vessel(Right clock)", player), lambda state:
             state.has("Cube of zoe", player) and (state.has("Leap stone", player) or
                                                   state.has("Soul of bat", player) or
                                                   state.has("Gravity boots", player) or
                                                   (state.has("Form of mist", player) and
                                                    state.has("Power of mist", player))))

    set_rule(world.get_location("NO0 - Alucart shield", player), lambda state:
             state.has("Cube of zoe", player) and (state.has("Leap stone", player) or
                                                   state.has("Soul of bat", player) or
                                                   state.has("Gravity boots", player) or
                                                   (state.has("Form of mist", player) and
                                                    state.has("Power of mist", player))))

    set_rule(world.get_location("NO0 - Alucart mail", player), lambda state:
             state.has("Cube of zoe", player) and (state.has("Leap stone", player) or
                                                   state.has("Soul of bat", player) or
                                                   state.has("Gravity boots", player) or
                                                   (state.has("Form of mist", player) and
                                                    state.has("Power of mist", player))))

    set_rule(world.get_location("NO0 - Alucart sword", player), lambda state:
             state.has("Cube of zoe", player) and (state.has("Leap stone", player) or
                                                   state.has("Soul of bat", player) or
                                                   state.has("Gravity boots", player) or
                                                   (state.has("Form of mist", player) and
                                                    state.has("Power of mist", player))))

    set_rule(world.get_location("NO0 - Heart Vessel(Inside)", player), lambda state:
             state.has("Silver ring", player) and state.has("Gold ring", player))

    set_rule(world.get_location("NO0 - Life Vessel(Inside)", player), lambda state:
             state.has("Silver ring", player) and state.has("Gold ring", player))

    set_rule(world.get_location("NO0 - Holy glasses", player), lambda state:
             state.has("Silver ring", player) and state.has("Gold ring", player))

    # NO1 - Outer Wall
    set_rule(world.get_location("NO1 - Garnet", player), lambda state: state.has("Soul of bat", player) or
             state.has("Gravity boots", player) or state.has("Leap stone", player) and
             (state.has("Form of mist", player) and state.has("Power of mist", player)))

    # NO2 - Olrox's Quarters
    set_rule(world.get_location("NO2 - Manna prism", player), lambda state:
             state.has("Soul of bat", player) or (state.has("Form of mist", player) and
             state.has("Power of mist", player)) or (state.has("Gravity boots", player) and
                                                     (state.has("Leap stone", player) or
                                                      state.has("Soul of wolf", player) or
                                                      state.has("Form of mist", player))))

    set_rule(world.get_location("NO2 - Resist fire", player), lambda state:
             state.has("Soul of bat", player) or (state.has("Form of mist", player) and
             state.has("Power of mist", player)) or (state.has("Gravity boots", player) and
                                                     (state.has("Leap stone", player) or
                                                      state.has("Soul of wolf", player) or
                                                      state.has("Form of mist", player))))

    set_rule(world.get_location("NO2 - Luck potion", player), lambda state:
             state.has("Soul of bat", player) or (state.has("Form of mist", player) and
             state.has("Power of mist", player)) or (state.has("Gravity boots", player) and
                                                     (state.has("Leap stone", player) or
                                                      state.has("Soul of wolf", player) or
                                                      state.has("Form of mist", player))))

    set_rule(world.get_location("NO2 - Estoc", player), lambda state:
             state.has("Soul of bat", player) or (state.has("Form of mist", player) and
             state.has("Power of mist", player)) or (state.has("Gravity boots", player) and
                                                     (state.has("Leap stone", player) or
                                                      state.has("Soul of wolf", player) or
                                                      state.has("Form of mist", player))))

    set_rule(world.get_location("NO2 - Garnet", player), lambda state:
             state.has("Soul of bat", player) or (state.has("Form of mist", player) and
             state.has("Power of mist", player)) or (state.has("Gravity boots", player) and
                                                     (state.has("Leap stone", player) or
                                                      state.has("Soul of wolf", player) or
                                                      state.has("Form of mist", player))))

    set_rule(world.get_location("NO2 - Iron ball", player), lambda state:
             state.has("Soul of bat", player) or (state.has("Form of mist", player) and
             state.has("Power of mist", player)) or (state.has("Gravity boots", player) and
                                                     (state.has("Leap stone", player) or
                                                      state.has("Soul of wolf", player) or
                                                      state.has("Form of mist", player))))
    if not no2:
        set_rule(world.get_location("NO2 - Heart Vessel", player), lambda state:
                 state.has("Soul of bat", player) or (state.has("Form of mist", player) and
                 state.has("Power of mist", player)) or (state.has("Gravity boots", player) and
                                                         (state.has("Leap stone", player) or
                                                          state.has("Soul of wolf", player) or
                                                          state.has("Form of mist", player))))
    else:
        set_rule(world.get_location("NO2 - Heart Vessel", player), lambda state:
                 state.has("Jewel of open", player) or state.has("Leap stone", player) or
                 state.has("Gravity boots", player) or state.has("Soul of bat", player) or
                 (state.has("Form of mist", player) and state.has("Power of mist", player)))

    set_rule(world.get_location("NO2 - Olrox kill", player), lambda state:
             state.has("Soul of bat", player) or (state.has("Form of mist", player) and
             state.has("Power of mist", player)) or (state.has("Gravity boots", player) and
                                                     (state.has("Leap stone", player) or
                                                      state.has("Soul of wolf", player) or
                                                      state.has("Form of mist", player))))

    # NO3 - Castle Entrance
    set_rule(world.get_location("NO3 - Life Vessel (Above entry)", player), lambda state:
             state.has("Soul of bat", player) or (state.has("Gravity boots", player) and
                                                  (state.has("Leap stone", player) or
                                                   state.has("Soul of wolf", player) or
                                                   state.has("Form of mist", player))))

    set_rule(world.get_location("NO3 - Holy mail", player), lambda state:
             state.has("Soul of bat", player) or (state.has("Gravity boots", player) and
                                                  (state.has("Leap stone", player) or
                                                   state.has("Soul of wolf", player) or
                                                   state.has("Form of mist", player))))

    set_rule(world.get_location("NO3 - Life Apple (Hidden room)", player), lambda state:
             state.has("Soul of bat", player) and state.has("Soul of wolf", player))

    set_rule(world.get_location("NO3 - Jewel sword", player), lambda state:
             state.has("Soul of bat", player) and state.has("Soul of wolf", player))

    if not no4:
        set_rule(world.get_location("NO3 - Life Vessel (UC exit)", player), lambda state:
                 state.has("Jewel of open", player))

        # NO4 - Underground Caverns need only Jewel
        set_rule(world.get_location("NO4 - Zircon", player), lambda state: state.has("Soul of bat", player) or
                 state.has("Leap stone", player) or (state.has("Gravity boots", player) and
                                                     (state.has("Soul of wolf", player) or
                                                      state.has("Form of mist", player))) or
                 (state.has("Form of mist", player) and state.has("Power of mist", player)))

        # Succubus
        set_rule(world.get_location("NO4 - Claymore", player), lambda state: state.has("Soul of bat", player) or
                 (state.has("Gravity boots", player) and (state.has("Leap stone", player) or
                                                          state.has("Soul of wolf", player) or
                                                          state.has("Form of mist", player))) or
                 (state.has("Form of mist", player) and state.has("Power of mist", player)))

        set_rule(world.get_location("NO4 - Meal ticket 1(Succubus)", player), lambda state:
                 state.has("Soul of bat", player) or (state.has("Gravity boots", player) and
                                                      (state.has("Leap stone", player) or
                                                       state.has("Soul of wolf", player) or
                                                       state.has("Form of mist", player))) or
                 (state.has("Form of mist", player) and state.has("Power of mist", player)))

        set_rule(world.get_location("NO4 - Meal ticket 2(Succubus)", player), lambda state:
                 state.has("Soul of bat", player) or (state.has("Gravity boots", player) and
                                                      (state.has("Leap stone", player) or
                                                       state.has("Soul of wolf", player) or
                                                       state.has("Form of mist", player))) or
                 (state.has("Form of mist", player) and state.has("Power of mist", player)))

        set_rule(world.get_location("NO4 - Meal ticket 3(Succubus)", player), lambda state:
                 state.has("Soul of bat", player) or (state.has("Gravity boots", player) and
                                                      (state.has("Leap stone", player) or
                                                       state.has("Soul of wolf", player) or
                                                       state.has("Form of mist", player))) or
                 (state.has("Form of mist", player) and state.has("Power of mist", player)))

        set_rule(world.get_location("NO4 - Meal ticket 4(Succubus)", player), lambda state:
                 state.has("Soul of bat", player) or (state.has("Gravity boots", player) and
                                                      (state.has("Leap stone", player) or
                                                       state.has("Soul of wolf", player) or
                                                       state.has("Form of mist", player))) or
                 (state.has("Form of mist", player) and state.has("Power of mist", player)))

        set_rule(world.get_location("NO4 - Moonstone", player), lambda state:
                 state.has("Soul of bat", player) or (state.has("Gravity boots", player) and
                                                      (state.has("Leap stone", player) or
                                                       state.has("Soul of wolf", player) or
                                                       state.has("Form of mist", player))) or
                 (state.has("Form of mist", player) and state.has("Power of mist", player)))

        set_rule(world.get_location("NO4 - Gold Ring", player), lambda state:
                 state.has("Soul of bat", player) or (state.has("Gravity boots", player) and
                                                      (state.has("Leap stone", player) or
                                                       state.has("Soul of wolf", player) or
                                                       state.has("Form of mist", player))) or
                 (state.has("Form of mist", player) and state.has("Power of mist", player)))

        set_rule(world.get_location("NO4 - Secret boots", player), lambda state:
                 state.has("Leap stone", player) or state.has("Soul of bat", player) or
                 state.has("Gravity boots", player) or (state.has("Form of mist", player) and
                                                        state.has("Power of mist", player)))

        set_rule(world.get_location("NO4 - Toadstool(Waterfall)", player), lambda state:
                 state.has("Leap stone", player) or state.has("Soul of bat", player) or
                 state.has("Gravity boots", player) or (state.has("Form of mist", player) and
                                                        state.has("Power of mist", player)))

        set_rule(world.get_location("NO4 - Shiitake(Waterfall)", player), lambda state:
                 state.has("Leap stone", player) or state.has("Soul of bat", player) or
                 state.has("Gravity boots", player) or (state.has("Form of mist", player) and
                                                        state.has("Power of mist", player)))

        set_rule(world.get_location("NO4 - Herald Shield", player), lambda state:
                 state.has("Leap stone", player) or state.has("Soul of bat", player) or
                 (state.has("Form of mist", player) and state.has("Power of mist", player)) or
                 (state.has("Gravity boots", player) and (state.has("Leap stone", player) or
                                                          state.has("Soul of wolf", player) or
                                                          state.has("Form of mist", player))) or
                 (state.has("Soul of wolf", player) and state.has("Power of wolf", player)))

        set_rule(world.get_location("NO4 - Life Vessel(Bellow bridge)", player), lambda state:
                 state.has("Leap stone", player) or state.has("Soul of bat", player) or
                 (state.has("Form of mist", player) and state.has("Power of mist", player)) or
                 (state.has("Gravity boots", player) and (state.has("Leap stone", player) or
                                                         state.has("Soul of wolf", player) or
                                                         state.has("Form of mist", player))) or
                 (state.has("Soul of wolf", player) and state.has("Power of wolf", player)))

        set_rule(world.get_location("NO4 - Heart Vessel(Bellow bridge)", player), lambda state:
                 state.has("Leap stone", player) or state.has("Soul of bat", player) or
                 (state.has("Form of mist", player) and state.has("Power of mist", player)) or
                 (state.has("Gravity boots", player) and (state.has("Leap stone", player) or
                                                          state.has("Soul of wolf", player) or
                                                          state.has("Form of mist", player))) or
                 (state.has("Soul of wolf", player) and state.has("Power of wolf", player)))

        set_rule(world.get_location("NO4 - Elixir(Holy)", player), lambda state:
                 state.has("Merman statue", player))

        set_rule(world.get_location("NO4 - Onyx(Holy)", player), lambda state:
                 state.has("Leap stone", player) or state.has("Gravity boots", player) or
                 state.has("Soul of bat", player) or state.has("Merman statue", player) or
                 (state.has("Form of mist", player) and state.has("Power of mist", player)))

        set_rule(world.get_location("NO4 - Nunchaku", player), lambda state: state.has("Holy symbol", player))

        set_rule(world.get_location("NO4 - Antivenom(Underwater)", player), lambda state:
                 state.has("Holy symbol", player))

        set_rule(world.get_location("NO4 - Life Vessel(Underwater)", player), lambda state:
                 state.has("Holy symbol", player))
    else:
        # With backdoor open, every item beyond waterfall need some kinda of flying
        set_rule(world.get_location("NO4 - Toadstool(Waterfall)", player), lambda state:
                 state.has("Leap stone", player) or state.has("Soul of bat", player) or
                 state.has("Gravity boots", player) or
                 (state.has("Form of mist", player) and state.has("Power of mist", player)))

        set_rule(world.get_location("NO4 - Shiitake(Waterfall)", player), lambda state:
                 state.has("Soul of bat", player) or
                 (state.has("Form of mist", player) and state.has("Power of mist", player)) or
                 (state.has("Gravity boots", player) and (state.has("Leap stone", player) or
                                                          state.has("Soul of wolf", player) or
                                                          state.has("Form of mist", player))))

        set_rule(world.get_location("NO4 - Secret boots", player), lambda state:
                 state.has("Soul of bat", player) or
                 (state.has("Form of mist", player) and state.has("Power of mist", player)) or
                 (state.has("Gravity boots", player) and (state.has("Leap stone", player) or
                                                          state.has("Soul of wolf", player) or
                                                          state.has("Form of mist", player))))

        set_rule(world.get_location("NO4 - Herald Shield", player), lambda state:
                 state.has("Soul of bat", player) or
                 (state.has("Form of mist", player) and state.has("Power of mist", player)) or
                 (state.has("Gravity boots", player) and (state.has("Leap stone", player) or
                                                          state.has("Soul of wolf", player) or
                                                          state.has("Form of mist", player))))

        set_rule(world.get_location("NO4 - Pentagram", player), lambda state:
                 state.has("Soul of bat", player) or
                 (state.has("Form of mist", player) and state.has("Power of mist", player)) or
                 (state.has("Gravity boots", player) and (state.has("Leap stone", player) or
                                                          state.has("Soul of wolf", player) or
                                                          state.has("Form of mist", player))))

        set_rule(world.get_location("NO4 - Life Vessel(Bellow bridge)", player), lambda state:
                 state.has("Soul of bat", player) or
                 (state.has("Form of mist", player) and state.has("Power of mist", player)) or
                 (state.has("Gravity boots", player) and (state.has("Leap stone", player) or
                                                          state.has("Soul of wolf", player) or
                                                          state.has("Form of mist", player))))

        set_rule(world.get_location("NO4 - Heart Vessel(Bellow bridge)", player), lambda state:
                 state.has("Soul of bat", player) or
                 (state.has("Form of mist", player) and state.has("Power of mist", player)) or
                 (state.has("Gravity boots", player) and (state.has("Leap stone", player) or
                                                          state.has("Soul of wolf", player) or
                                                          state.has("Form of mist", player))))

        # It's underwater, but you probably could swim without Holy symbol
        set_rule(world.get_location("NO4 - Antivenom(Underwater)", player), lambda state:
                 state.has("Soul of bat", player) or
                 (state.has("Form of mist", player) and state.has("Power of mist", player)) or
                 (state.has("Gravity boots", player) and (state.has("Leap stone", player) or
                                                          state.has("Soul of wolf", player) or
                                                          state.has("Form of mist", player))))

        set_rule(world.get_location("NO4 - Life Vessel(Underwater)", player), lambda state:
                 state.has("Soul of bat", player) or
                 (state.has("Form of mist", player) and state.has("Power of mist", player)) or
                 (state.has("Gravity boots", player) and (state.has("Leap stone", player) or
                                                          state.has("Soul of wolf", player) or
                                                          state.has("Form of mist", player))))

        set_rule(world.get_location("NO4 - Toadstool(26)", player), lambda state:
                 state.has("Soul of bat", player) or
                 (state.has("Form of mist", player) and state.has("Power of mist", player)) or
                 (state.has("Gravity boots", player) and (state.has("Leap stone", player) or
                                                          state.has("Soul of wolf", player) or
                                                          state.has("Form of mist", player))))

        set_rule(world.get_location("NO4 - Shiitake(27)", player), lambda state:
                 state.has("Soul of bat", player) or
                 (state.has("Form of mist", player) and state.has("Power of mist", player)) or
                 (state.has("Gravity boots", player) and (state.has("Leap stone", player) or
                                                          state.has("Soul of wolf", player) or
                                                          state.has("Form of mist", player))))

        set_rule(world.get_location("NO4 - Nunchaku", player), lambda state:
                 state.has("Holy symbol", player) and
                 (state.has("Soul of bat", player) or
                 (state.has("Form of mist", player) and state.has("Power of mist", player)) or
                 (state.has("Gravity boots", player) and (state.has("Leap stone", player) or
                                                          state.has("Soul of wolf", player) or
                                                          state.has("Form of mist", player)))))

        set_rule(world.get_location("NO4 - Shiitake(12)", player), lambda state:
                 state.has("Soul of bat", player) or
                 (state.has("Form of mist", player) and state.has("Power of mist", player)) or
                 (state.has("Gravity boots", player) and (state.has("Leap stone", player) or
                                                          state.has("Soul of wolf", player) or
                                                          state.has("Form of mist", player))))

        set_rule(world.get_location("NO4 - Life Vessel(1)", player), lambda state:
                 state.has("Soul of bat", player) or
                 (state.has("Form of mist", player) and state.has("Power of mist", player)) or
                 (state.has("Gravity boots", player) and (state.has("Leap stone", player) or
                                                          state.has("Soul of wolf", player) or
                                                          state.has("Form of mist", player))))

        set_rule(world.get_location("NO4 - Heart Vessel(0)", player), lambda state:
                 state.has("Soul of bat", player) or
                 (state.has("Form of mist", player) and state.has("Power of mist", player)) or
                 (state.has("Gravity boots", player) and (state.has("Leap stone", player) or
                                                          state.has("Soul of wolf", player) or
                                                          state.has("Form of mist", player))))

        set_rule(world.get_location("NO4 - Bandanna", player), lambda state:
                 state.has("Soul of bat", player) or
                 (state.has("Form of mist", player) and state.has("Power of mist", player)) or
                 (state.has("Gravity boots", player) and (state.has("Leap stone", player) or
                                                          state.has("Soul of wolf", player) or
                                                          state.has("Form of mist", player))))

        set_rule(world.get_location("NO4 - Zircon", player), lambda state:
                 state.has("Soul of bat", player) or
                 (state.has("Form of mist", player) and state.has("Power of mist", player)) or
                 (state.has("Gravity boots", player) and (state.has("Leap stone", player) or
                                                          state.has("Soul of wolf", player) or
                                                          state.has("Form of mist", player))))

        set_rule(world.get_location("NO4 - Claymore", player), lambda state:
                 state.has("Soul of bat", player) or
                 (state.has("Form of mist", player) and state.has("Power of mist", player)) or
                 (state.has("Gravity boots", player) and (state.has("Leap stone", player) or
                                                          state.has("Soul of wolf", player) or
                                                          state.has("Form of mist", player))))

        set_rule(world.get_location("NO4 - Meal ticket 1(Succubus)", player), lambda state:
                 state.has("Soul of bat", player) or
                 (state.has("Form of mist", player) and state.has("Power of mist", player)) or
                 (state.has("Gravity boots", player) and (state.has("Leap stone", player) or
                                                          state.has("Soul of wolf", player) or
                                                          state.has("Form of mist", player))))

        set_rule(world.get_location("NO4 - Meal ticket 2(Succubus)", player), lambda state:
                 state.has("Soul of bat", player) or
                 (state.has("Form of mist", player) and state.has("Power of mist", player)) or
                 (state.has("Gravity boots", player) and (state.has("Leap stone", player) or
                                                          state.has("Soul of wolf", player) or
                                                          state.has("Form of mist", player))))

        set_rule(world.get_location("NO4 - Meal ticket 3(Succubus)", player), lambda state:
                 state.has("Soul of bat", player) or
                 (state.has("Form of mist", player) and state.has("Power of mist", player)) or
                 (state.has("Gravity boots", player) and (state.has("Leap stone", player) or
                                                          state.has("Soul of wolf", player) or
                                                          state.has("Form of mist", player))))

        set_rule(world.get_location("NO4 - Meal ticket 4(Succubus)", player), lambda state:
                 state.has("Soul of bat", player) or
                 (state.has("Form of mist", player) and state.has("Power of mist", player)) or
                 (state.has("Gravity boots", player) and (state.has("Leap stone", player) or
                                                          state.has("Soul of wolf", player) or
                                                          state.has("Form of mist", player))))

        set_rule(world.get_location("NO4 - Moonstone", player), lambda state:
                 state.has("Soul of bat", player) or
                 (state.has("Form of mist", player) and state.has("Power of mist", player)) or
                 (state.has("Gravity boots", player) and (state.has("Leap stone", player) or
                                                          state.has("Soul of wolf", player) or
                                                          state.has("Form of mist", player))))

        set_rule(world.get_location("NO4 - Gold Ring", player), lambda state:
                 state.has("Soul of bat", player) or
                 (state.has("Form of mist", player) and state.has("Power of mist", player)) or
                 (state.has("Gravity boots", player) and (state.has("Leap stone", player) or
                                                          state.has("Soul of wolf", player) or
                                                          state.has("Form of mist", player))))

        set_rule(world.get_location("NO4 - Resist ice", player), lambda state:
                 state.has("Soul of bat", player) or
                 (state.has("Form of mist", player) and state.has("Power of mist", player)) or
                 (state.has("Gravity boots", player) and (state.has("Leap stone", player) or
                                                          state.has("Soul of wolf", player) or
                                                          state.has("Form of mist", player))))

        set_rule(world.get_location("NO4 - Scimitar", player), lambda state:
                 state.has("Soul of bat", player) or
                 (state.has("Form of mist", player) and state.has("Power of mist", player)) or
                 (state.has("Gravity boots", player) and (state.has("Leap stone", player) or
                                                          state.has("Soul of wolf", player) or
                                                          state.has("Form of mist", player))))

        set_rule(world.get_location("NO4 - Pot roast", player), lambda state:
                 state.has("Soul of bat", player) or
                 (state.has("Form of mist", player) and state.has("Power of mist", player)) or
                 (state.has("Gravity boots", player) and (state.has("Leap stone", player) or
                                                          state.has("Soul of wolf", player) or
                                                          state.has("Form of mist", player))))

        set_rule(world.get_location("NO4 - Crystal cloak", player), lambda state:
                 state.has("Soul of bat", player) or
                 (state.has("Form of mist", player) and state.has("Power of mist", player)) or
                 (state.has("Gravity boots", player) and (state.has("Leap stone", player) or
                                                          state.has("Soul of wolf", player) or
                                                          state.has("Form of mist", player))))

        set_rule(world.get_location("NO4 - Life Vessel(Holy)", player), lambda state:
                 state.has("Soul of bat", player) or
                 (state.has("Form of mist", player) and state.has("Power of mist", player)) or
                 (state.has("Gravity boots", player) and (state.has("Leap stone", player) or
                                                          state.has("Soul of wolf", player) or
                                                          state.has("Form of mist", player))))

        set_rule(world.get_location("NO4 - Knuckle duster(Holy)", player), lambda state:
                 state.has("Soul of bat", player) or
                 (state.has("Form of mist", player) and state.has("Power of mist", player)) or
                 (state.has("Gravity boots", player) and (state.has("Leap stone", player) or
                                                          state.has("Soul of wolf", player) or
                                                          state.has("Form of mist", player))))

        set_rule(world.get_location("NO4 - Onyx(Holy)", player), lambda state:
                 (state.has("Holy symbol", player) or state.has("Merman statue", player)) and
                 (state.has("Soul of bat", player) or
                 (state.has("Form of mist", player) and state.has("Power of mist", player)) or
                 (state.has("Gravity boots", player) and (state.has("Leap stone", player) or
                                                          state.has("Soul of wolf", player) or
                                                          state.has("Form of mist", player)))))

        set_rule(world.get_location("NO4 - Elixir(Holy)", player), lambda state:
                 state.has("Merman statue", player) and
                 (state.has("Soul of bat", player) or
                 (state.has("Form of mist", player) and state.has("Power of mist", player)) or
                 (state.has("Gravity boots", player) and (state.has("Leap stone", player) or
                                                          state.has("Soul of wolf", player) or
                                                          state.has("Form of mist", player)))))

    # NZ1 - Clock tower
    set_rule(world.get_location("NZ1 - Bekatowa", player), lambda state:
             state.has("Soul of bat", player) or state.has("Gravity boots", player) or
             (state.has("Form of mist", player) and state.has("Power of mist", player)))

    set_rule(world.get_location("NZ1 - Shaman shield", player), lambda state:
             state.has("Soul of bat", player) or state.has("Gravity boots", player) or
             (state.has("Form of mist", player) and state.has("Power of mist", player)))

    set_rule(world.get_location("NZ1 - Ice mail", player), lambda state:
             state.has("Soul of bat", player) or state.has("Gravity boots", player) or
             (state.has("Form of mist", player) and state.has("Power of mist", player)))

    # Can come from DAI or NO1
    set_rule(world.get_location("NZ1 - Gold plate", player), lambda state:
             state.has("Jewel of open", player) or state.has("Leap stone", player) or
             state.has("Soul of bat", player) or state.has("Gravity boots", player) or
             (state.has("Form of mist", player) and state.has("Power of mist", player)))

    set_rule(world.get_location("NZ1 - Star flail", player), lambda state:
             state.has("Jewel of open", player) or state.has("Leap stone", player) or
             state.has("Soul of bat", player) or state.has("Gravity boots", player) or
             (state.has("Form of mist", player) and state.has("Power of mist", player)))

    set_rule(world.get_location("NZ1 - Steel helm", player), lambda state:
             state.has("Jewel of open", player) or state.has("Leap stone", player) or
             state.has("Soul of bat", player) or state.has("Gravity boots", player) or
             (state.has("Form of mist", player) and state.has("Power of mist", player)))

    set_rule(world.get_location("NZ1 - Life Vessel(Gear train)", player), lambda state:
             state.has("Jewel of open", player) or state.has("Leap stone", player) or
             state.has("Soul of bat", player) or state.has("Gravity boots", player) or
             (state.has("Form of mist", player) and state.has("Power of mist", player)))

    set_rule(world.get_location("NZ1 - Heart Vessel(Gear train)", player), lambda state:
             state.has("Jewel of open", player) or state.has("Leap stone", player) or
             state.has("Soul of bat", player) or state.has("Gravity boots", player) or
             (state.has("Form of mist", player) and state.has("Power of mist", player)))

    set_rule(world.get_location("NZ1 - Pot roast", player), lambda state:
             state.has("Jewel of open", player) or state.has("Leap stone", player) or
             state.has("Soul of bat", player) or state.has("Gravity boots", player) or
             (state.has("Form of mist", player) and state.has("Power of mist", player)))

    set_rule(world.get_location("NZ1 - Healing mail", player), lambda state:
             state.has("Jewel of open", player) or state.has("Leap stone", player) or
             state.has("Soul of bat", player) or state.has("Gravity boots", player) or
             (state.has("Form of mist", player) and state.has("Power of mist", player)))

    set_rule(world.get_location("NZ1 - TNT", player), lambda state:
             state.has("Jewel of open", player) or state.has("Leap stone", player) or
             state.has("Soul of bat", player) or state.has("Gravity boots", player) or
             (state.has("Form of mist", player) and state.has("Power of mist", player)))

    set_rule(world.get_location("NZ1 - Bwaka knife", player), lambda state:
             state.has("Jewel of open", player) or state.has("Leap stone", player) or
             state.has("Soul of bat", player) or state.has("Gravity boots", player) or
             (state.has("Form of mist", player) and state.has("Power of mist", player)))

    set_rule(world.get_location("NZ1 - Shuriken", player), lambda state:
             state.has("Jewel of open", player) or state.has("Leap stone", player) or
             state.has("Soul of bat", player) or state.has("Gravity boots", player) or
             (state.has("Form of mist", player) and state.has("Power of mist", player)))

    set_rule(world.get_location("NZ1 - Karasuman kill", player), lambda state:
             state.has("Jewel of open", player) or state.has("Leap stone", player) or
             state.has("Soul of bat", player) or state.has("Gravity boots", player) or
             (state.has("Form of mist", player) and state.has("Power of mist", player)))

    # TOP - Castle Keep Required Leap or Bat or Gravity or (form and power of mist)
    set_rule(world.get_location("TOP - Turquoise", player), lambda state:
             state.has("Leap stone", player) or state.has("Soul of bat", player) or
             state.has("Gravity boots", player) or
             (state.has("Form of mist", player) and state.has("Power of mist", player)))

    set_rule(world.get_location("TOP - Falchion", player), lambda state:
             state.has("Leap stone", player) or state.has("Soul of bat", player) or
             state.has("Gravity boots", player) or
             (state.has("Form of mist", player) and state.has("Power of mist", player)))

    set_rule(world.get_location("TOP - Turkey(Behind wall)", player), lambda state:
             state.has("Leap stone", player) or state.has("Soul of bat", player) or
             state.has("Gravity boots", player) or
             (state.has("Form of mist", player) and state.has("Power of mist", player)))

    # High jump need it items and Richter
    set_rule(world.get_location("TOP - Fire mail(Behind wall)", player), lambda state:
             state.has("Soul of bat", player) or (state.has("Gravity boots", player) and
                                                  (state.has("Leap stone", player) or
                                                   state.has("Soul of wolf", player) or
                                                   state.has("Form of mist", player))) or
             (state.has("Form of mist", player) and state.has("Power of mist", player)))

    set_rule(world.get_location("TOP - Heart Vessel(Before Richter)", player), lambda state:
             state.has("Soul of bat", player) or (state.has("Gravity boots", player) and
                                                  (state.has("Leap stone", player) or
                                                   state.has("Soul of wolf", player) or
                                                   state.has("Form of mist", player))) or
             (state.has("Form of mist", player) and state.has("Power of mist", player)))

    set_rule(world.get_location("TOP - Sirloin(Above Richter)", player), lambda state:
             state.has("Soul of bat", player) or (state.has("Gravity boots", player) and
                                                  (state.has("Leap stone", player) or
                                                   state.has("Soul of wolf", player) or
                                                   state.has("Form of mist", player))) or
             (state.has("Form of mist", player) and state.has("Power of mist", player)))

    set_rule(world.get_location("TOP - Turkey(Above Richter)", player), lambda state:
             state.has("Soul of bat", player) or (state.has("Gravity boots", player) and
                                                  (state.has("Leap stone", player) or
                                                   state.has("Soul of wolf", player) or
                                                   state.has("Form of mist", player))) or
             (state.has("Form of mist", player) and state.has("Power of mist", player)))

    set_rule(world.get_location("TOP - Pot roast(Above Richter)", player), lambda state:
             state.has("Soul of bat", player) or (state.has("Gravity boots", player) and
                                                  (state.has("Leap stone", player) or
                                                   state.has("Soul of wolf", player) or
                                                   state.has("Form of mist", player))) or
             (state.has("Form of mist", player) and state.has("Power of mist", player)))

    set_rule(world.get_location("TOP - Frankfurter(Above Richter)", player), lambda state:
             state.has("Soul of bat", player) or (state.has("Gravity boots", player) and
                                                  (state.has("Leap stone", player) or
                                                   state.has("Soul of wolf", player) or
                                                   state.has("Form of mist", player))) or
             (state.has("Form of mist", player) and state.has("Power of mist", player)))

    set_rule(world.get_location("TOP - Resist stone(Above Richter)", player), lambda state:
             state.has("Soul of bat", player) or (state.has("Gravity boots", player) and
                                                  (state.has("Leap stone", player) or
                                                   state.has("Soul of wolf", player) or
                                                   state.has("Form of mist", player))) or
             (state.has("Form of mist", player) and state.has("Power of mist", player)))

    set_rule(world.get_location("TOP - Resist dark(Above Richter)", player), lambda state:
             state.has("Soul of bat", player) or (state.has("Gravity boots", player) and
                                                  (state.has("Leap stone", player) or
                                                   state.has("Soul of wolf", player) or
                                                   state.has("Form of mist", player))) or
             (state.has("Form of mist", player) and state.has("Power of mist", player)))

    set_rule(world.get_location("TOP - Resist holy(Above Richter)", player), lambda state:
             state.has("Soul of bat", player) or (state.has("Gravity boots", player) and
                                                  (state.has("Leap stone", player) or
                                                   state.has("Soul of wolf", player) or
                                                   state.has("Form of mist", player))) or
             (state.has("Form of mist", player) and state.has("Power of mist", player)))

    set_rule(world.get_location("TOP - Platinum mail(Above Richter)", player), lambda state:
             state.has("Soul of bat", player) or (state.has("Gravity boots", player) and
                                                  (state.has("Leap stone", player) or
                                                   state.has("Soul of wolf", player) or
                                                   state.has("Form of mist", player))) or
             (state.has("Form of mist", player) and state.has("Power of mist", player)))

    set_rule(world.get_location("TOP - Life Vessel 1(Viewing room)", player), lambda state:
             state.has("Soul of bat", player) or (state.has("Gravity boots", player) and
                                                  (state.has("Leap stone", player) or
                                                   state.has("Soul of wolf", player) or
                                                   state.has("Form of mist", player))) or
             (state.has("Form of mist", player) and state.has("Power of mist", player)))

    set_rule(world.get_location("TOP - Life Vessel 2(Viewing room)", player), lambda state:
             state.has("Soul of bat", player) or (state.has("Gravity boots", player) and
                                                  (state.has("Leap stone", player) or
                                                   state.has("Soul of wolf", player) or
                                                   state.has("Form of mist", player))) or
             (state.has("Form of mist", player) and state.has("Power of mist", player)))

    set_rule(world.get_location("TOP - Heart Vessel 1(Viewing room)", player), lambda state:
             state.has("Soul of bat", player) or (state.has("Gravity boots", player) and
                                                  (state.has("Leap stone", player) or
                                                   state.has("Soul of wolf", player) or
                                                   state.has("Form of mist", player))) or
             (state.has("Form of mist", player) and state.has("Power of mist", player)))

    set_rule(world.get_location("TOP - Heart Vessel 2(Viewing room)", player), lambda state:
             state.has("Soul of bat", player) or (state.has("Gravity boots", player) and
                                                  (state.has("Leap stone", player) or
                                                   state.has("Soul of wolf", player) or
                                                   state.has("Form of mist", player))) or
             (state.has("Form of mist", player) and state.has("Power of mist", player)))

    set_rule(world.get_location("TOP - Heart Vessel(Before Richter)", player), lambda state:
             state.has("Soul of bat", player) or (state.has("Gravity boots", player) and
                                                  (state.has("Leap stone", player) or
                                                   state.has("Soul of wolf", player) or
                                                   state.has("Form of mist", player))) or
             (state.has("Form of mist", player) and state.has("Power of mist", player)))

    set_rule(world.get_location("RNO0 - Heart Refresh(Inside clock)", player), lambda state:
             (state.has("Holy glasses", player) and (state.has("Soul of bat", player) or
                                                     (state.has("Gravity boots", player) and
                                                      (state.has("Leap stone", player) or
                                                       state.has("Soul of wolf", player) or
                                                       state.has("Form of mist", player))) or
                                                     (state.has("Form of mist", player) and
                                                      state.has("Power of mist", player)))))

    # Reverse Castle -> Already have some kind of high jump
    set_rule(world.get_location("RDAI - Twilight cloak", player), lambda state:
             state.has("Spike breaker", player) and state.has("Form of mist", player))

    set_rule(world.get_location("RNO2 - Akmodan II kill", player), lambda state:
             state.has("Soul of bat", player) or state.has("Soul of wolf", player) or state.has("Form of mist", player))

    set_rule(world.get_location("RNO2 - Heart Vessel", player), lambda state:
             state.has("Soul of bat", player) or state.has("Soul of wolf", player) or state.has("Form of mist", player))

    set_rule(world.get_location("RNO3 - Zircon", player), lambda state:
             state.has("Soul of wolf", player) and state.has("Soul of bat", player))

    set_rule(world.get_location("RNO3 - Opal", player), lambda state:
             state.has("Soul of wolf", player) and state.has("Soul of bat", player))

    set_rule(world.get_location("RNO3 - Beryl circlet", player), lambda state:
             state.has("Soul of wolf", player) and state.has("Soul of bat", player))

    set_rule(world.get_location("RNO0 - Library card", player), lambda state:
             state.has("Jewel of open", player))

    set_rule(world.get_location("RNO1 - Hammer", player), lambda state: state.has("Form of mist", player))

    set_rule(world.get_location("RNO1 - Shotel", player), lambda state: state.has("Form of mist", player))

    set_rule(world.get_location("RLIB - Staurolite", player), lambda state:
             state.has("Form of mist", player))

    set_rule(world.get_location("RNO4 - Life Vessel(Underwater)", player), lambda state:
             state.has("Gravity boots", player))

    set_rule(world.get_location("RNO4 - Bat Pentagram", player), lambda state:
             state.has("Leap stone", player) or state.has("Soul of bat", player))

    set_rule(world.get_location("RNO4 - Potion(Underwater)", player), lambda state:
             state.has("Gravity boots", player))

    set_rule(world.get_location("RNO4 - Life Vessel(Underwater)", player), lambda state:
             state.has("Gravity boots", player))

    set_rule(world.get_location("RNO4 - Osafune katana", player), lambda state:
             state.has("Soul of bat", player) or (state.has("Gravity boots", player) and
                                                  (state.has("Leap stone", player) or
                                                   state.has("Soul of wolf", player))))

    set_rule(world.get_location("RCHI - Power of Sire(Demon)", player), lambda state:
             state.has("Demon card", player))

    set_rule(world.get_location("RCHI - Life apple(Demon)", player), lambda state:
             state.has("Demon card", player))

    set_rule(world.get_location("RCHI - Green tea(Demon)", player), lambda state:
             state.has("Demon card", player))

    set_rule(world.get_location("RCAT - Resist thunder", player), lambda state:
             state.has("Soul of bat", player) or
             (state.has("Form of mist", player) and state.has("Power of mist", player)) or
             (state.has("Spike Breaker", player) and (state.has("Leap stone", player) or
                                                      state.has("Gravity boots", player))))

    set_rule(world.get_location("RCAT - Resist fire", player), lambda state:
             state.has("Soul of bat", player) or
             (state.has("Form of mist", player) and state.has("Power of mist", player)) or
             (state.has("Spike Breaker", player) and (state.has("Leap stone", player) or
                                                      state.has("Gravity boots", player))))

    set_rule(world.get_location("RCAT - Karma coin(4)(Spike breaker)", player), lambda state:
             state.has("Soul of bat", player) or
             (state.has("Form of mist", player) and state.has("Power of mist", player)) or
             (state.has("Spike Breaker", player) and (state.has("Leap stone", player) or
                                                      state.has("Gravity boots", player))))

    set_rule(world.get_location("RCAT - Karma coin(5)(Spike breaker)", player), lambda state:
             state.has("Soul of bat", player) or
             (state.has("Form of mist", player) and state.has("Power of mist", player)) or
             (state.has("Spike Breaker", player) and (state.has("Leap stone", player) or
                                                      state.has("Gravity boots", player))))

    set_rule(world.get_location("RCAT - Red bean bun", player), lambda state:
             state.has("Soul of bat", player) or
             (state.has("Form of mist", player) and state.has("Power of mist", player)) or
             (state.has("Spike Breaker", player) and (state.has("Leap stone", player) or
                                                      state.has("Gravity boots", player))))

    set_rule(world.get_location("RCAT - Elixir", player), lambda state:
             state.has("Soul of bat", player) or
             (state.has("Form of mist", player) and state.has("Power of mist", player)) or
             (state.has("Spike Breaker", player) and (state.has("Leap stone", player) or
                                                      state.has("Gravity boots", player))))

    set_rule(world.get_location("RCAT - Library card", player), lambda state:
             state.has("Soul of bat", player) or
             (state.has("Form of mist", player) and state.has("Power of mist", player)) or
             (state.has("Spike Breaker", player) and (state.has("Leap stone", player) or
                                                      state.has("Gravity boots", player))))
