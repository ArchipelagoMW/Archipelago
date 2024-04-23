from .extended_logic import logic_helpers
from worlds.generic.Rules import set_rule



logic: logic_helpers
def set_location_rules(world):
    logic = logic_helpers(world)
    multiworld = world.multiworld
    player = world.player

    set_rule(multiworld.get_location("Poka-Poka Lake Chest", player), lambda state: state.has('Silver Sword', player))
    set_rule(multiworld.get_location("Poka-Poka Digging Chest", player), lambda state: state.has('Shovel', player))
    set_rule(multiworld.get_location("Poka-Poka East Cave Chest", player), lambda state: logic.light_switch_on(state))

    set_rule(multiworld.get_location("Poka-Poka Down Blocks Chest", player), lambda state: (state.has('Down Jab', player) and state.has_group("Swords", player, 1)))
    set_rule(multiworld.get_location("Poka-Poka Moon Alcove Chest", player), lambda state: logic.moon_switch_on(state))
    set_rule(multiworld.get_location("Poka-Poka Sun Blocks Chest", player), lambda state: logic.sun_switch_off(state))
    set_rule(multiworld.get_location("Poka-Poka East Cave Chest", player), lambda state: state.has('Elven Flute', player))
    set_rule(multiworld.get_location("Poka-Poka Shrine Chest", player), lambda state: state.has('Elven Flute', player))
    set_rule(multiworld.get_location("Poka-Poka Pushable Rock Chest", player), lambda state: state.has('Shove', player))
    set_rule(multiworld.get_location("Evil Tree Chest", player), lambda state: logic.can_fight_boss(state))

    set_rule(multiworld.get_location("Boa-Boa Sun Alcove Chest", player), lambda state: logic.sun_switch_on(state))
    set_rule(multiworld.get_location("Boa-Boa Sun Block Chest", player), lambda state: (state.has('Elven Flute', player) and logic.sun_switch_off(state)))
    set_rule(multiworld.get_location("Boa-Boa Lava Lake West Chest", player), lambda state: state.has('Shovel', player))
    set_rule(multiworld.get_location("Boa-Boa Eastern Shaft Chest", player), lambda state: (state.has('Down Jab', player) and state.has_group("Swords", player, 1)))
    set_rule(multiworld.get_location("Boa-Boa Western Shaft Chest", player), lambda state: (state.has('Up Jab', player) and state.has_group("Swords", player, 1)))
    set_rule(multiworld.get_location("Boa-Boa Shrine Chest", player), lambda state: state.has('Elven Flute', player))
    set_rule(multiworld.get_location("Tortoise Chest", player), lambda state: (logic.can_fight_boss(state) and state.has("Shove", player)))

    set_rule(multiworld.get_location("Hiya-Hiya Sun Blocks Chest", player), lambda state: logic.sun_switch_off(state))
    set_rule(multiworld.get_location("Hiya-Hiya Hidden Alcove Chest", player), lambda state: (state.has('Shove', player) and logic.star_switch_on(state)))
    set_rule(multiworld.get_location("Hiya-Hiya Up Block Alcove Chest", player), lambda state: (state.has_all({'Shove', "Up Jab"}, player) and state.has_group("Swords", player, 1)))
    set_rule(multiworld.get_location("Hiya-Hiya Trapped Chest", player), lambda state: state.has('Shove', player) and logic.star_switch_off(state))
    set_rule(multiworld.get_location("Hiya-Hiya Ice Cubes Chest", player), lambda state: (state.has_all({'Shove', "Fire Sword"}, player)))
    set_rule(multiworld.get_location("Hiya-Hiya Top Level", player), lambda state: state.has('Shove', player))
    set_rule(multiworld.get_location("Hiya-Hiya Long Fall Chest", player), lambda state: state.has('Shove', player) and logic.star_switch_off(state))
    set_rule(multiworld.get_location("Hiya-Hiya Vines Chest", player), lambda state: state.has('Elven Flute', player))
    set_rule(multiworld.get_location("Hiya-Hiya Shrine Chest", player), lambda state: state.has('Elven Flute', player))
    set_rule(multiworld.get_location("Mammoth Chest", player), lambda state: logic.can_fight_boss(state) and state.has("Shove", player) and logic.star_switch_off(state))

    set_rule(multiworld.get_location("Puka-Puka Light Blocks Chest", player), lambda state: logic.light_switch_on(state) and state.has(("Shovel"), player))
    set_rule(multiworld.get_location("Puka-Puka Down Jab Chest", player), lambda state: (state.has('Down Jab', player) and state.has_group("Swords", player, 1)))
    set_rule(multiworld.get_location("Puka-Puka Star Blocks Chest", player), lambda state: logic.star_switch_on(state))
    set_rule(multiworld.get_location("Puka-Puka Up Jab Chest", player), lambda state: (state.has('Up Jab', player) and state.has_group("Swords", player, 1)))
    set_rule(multiworld.get_location("Puka-Puka Spike Maze Lower Chest", player), lambda state: state.has('Elven Flute', player))
    set_rule(multiworld.get_location("Puka-Puka Spike Maze Upper Chest", player), lambda state: state.has('Elven Flute', player))
    set_rule(multiworld.get_location("Puka-Puka Shrine Chest", player), lambda state: state.has('Elven Flute', player))
    set_rule(multiworld.get_location("Puka-Puka Water Control", player), lambda state: (state.has_all({'Shove', "Shovel"}, player)))
    set_rule(multiworld.get_location("Puka-Puka Underwater Chest", player), lambda state: state.has('Puka-Puka Drained', player))
    set_rule(multiworld.get_location("Puka-Puka Aqua Blocks Chest", player), lambda state: (state.has_all({'Shovel', "Puka-Puka Drained"}, player)) and logic.aqua_switch_off(state))
    set_rule(multiworld.get_location("Octopus Chest", player), lambda state: (state.has_all({'Shovel', "Puka-Puka Drained"}, player)) and logic.aqua_switch_off(state) and logic.can_fight_boss)

    set_rule(multiworld.get_location("Sala-Sala Pyramid Center Chest", player), lambda state: logic.moon_switch_off(state))
    set_rule(multiworld.get_location("Sala-Sala Star Alcove Chest", player), lambda state: logic.star_switch_on(state))
    set_rule(multiworld.get_location("Sala-Sala Near Entrance Chest", player), lambda state: logic.moon_switch_on(state) and state.has("Shovel", player))
    set_rule(multiworld.get_location("Sala-Sala Top of the Pyramid Chest", player), lambda state: logic.moon_switch_on(state) and (state.has_all({"Shovel", "Down Jab"}, player) and state.has_group("Swords", player, 1)))
    set_rule(multiworld.get_location("Sala-Sala Up Jab Chest", player), lambda state: logic.moon_switch_on(state) and (state.has_all({"Shovel", "Up Jab", "Shove"}, player) and state.has_group("Swords", player, 1)))
    set_rule(multiworld.get_location("Sala-Sala All Blocks Chest", player), lambda state: logic.light_switch_on(state) and logic.sun_switch_on(state) and logic.star_switch_on(state) and logic.aqua_switch_on(state) and logic.moon_switch_on(state))
    set_rule(multiworld.get_location("Sala-Sala Farthest Chest", player), lambda state: (state.has_all({'Elven Flute', "Down Jab"}, player) and state.has_group("Swords", player, 1)))
    set_rule(multiworld.get_location("Sala-Sala Shrine Chest", player), lambda state: state.has('Elven Flute', player))
    set_rule(multiworld.get_location("Mummy Chest", player), lambda state: logic.can_fight_boss(state) and logic.has_good_projectile(state))

    set_rule(multiworld.get_location("Fuwa-Fuwa Block Maze Chest", player), lambda state: state.has_all({'Up Jab', 'Down Jab', 'Power Sword'}, player))
    set_rule(multiworld.get_location("Fuwa-Fuwa Moon Block Chest", player), lambda state: logic.moon_switch_on(state))
    set_rule(multiworld.get_location("Fuwa-Fuwa Light Block Chest", player), lambda state: logic.light_switch_on(state) and state.has("Power Sword", player))
    set_rule(multiworld.get_location("Fuwa-Fuwa Bridge Room Chest", player), lambda state: state.has("Shovel", player))
    set_rule(multiworld.get_location("Fuwa-Fuwa Balance Platforms Chest", player), lambda state: state.has("Shovel", player))
    set_rule(multiworld.get_location("Hawk Chest", player), lambda state: logic.can_fight_boss(state) and state.has_all({"Shovel", "Power Sword"}, player))
    set_rule(multiworld.get_location("Phantom Defeat", player), lambda state: (logic.can_fight_final_boss(state) and logic.has_good_projectile(state)) and state.has_all({"Shovel", "Power Sword"}, player))

    #set_rule(multiworld.get_location("Muscle Lizard Chest", player), lambda state: logic.has_early_health(state))
    set_rule(multiworld.get_location("Ice Cave Chest", player), lambda state: state.has('Shove', player))
    set_rule(multiworld.get_location("Saber Tooth Chest", player), lambda state: logic.can_fight_boss(state))
    set_rule(multiworld.get_location("300 Coin Shop", player), lambda state: state.has_group("Coins", player, 1))
    set_rule(multiworld.get_location("500 Coin Shop", player), lambda state: (state.has_group("Coins", player, 2) or state.has_any({"1000 Coins", "2000 Coins", "5000 Coins"}, player)))

    set_rule(multiworld.get_location("Boa-Hiya Shortcut Room", player), lambda state: state.has_all({"Shovel", "Shove"}, player))
    set_rule(multiworld.get_location("Sala-Hiya Shortcut Room", player), lambda state: state.has('Shove', player))
    set_rule(multiworld.get_location("Sala-Puka Shortcut Room", player), lambda state: state.has_all({"Shovel", "Shove"}, player) and logic.moon_switch_on)
    set_rule(multiworld.get_location("Fuwa-Poka Shortcut Room", player), lambda state: state.has_all({"Shovel", "Shove"}, player))
    set_rule(multiworld.get_location("Fuwa-Puka Shortcut Room", player), lambda state: state.has_all({"Down Jab", "Power Sword", "Shove"}, player))


    if world.light_gate == 0:
        set_rule(multiworld.get_location("Light Gate", player), lambda state: state.has('Light Stone', player))

    if world.sun_gate == 0:
        set_rule(multiworld.get_location("Sun Gate", player), lambda state: state.has('Sun Stone', player))

    if world.star_gate == 0:
        set_rule(multiworld.get_location("Star Gate", player), lambda state: state.has('Star Stone', player))

    if world.aqua_gate == 0:
        set_rule(multiworld.get_location("Aqua Gate", player), lambda state: state.has('Aqua Stone', player))

    if world.moon_gate == 0:
        set_rule(multiworld.get_location("Moon Gate", player), lambda state: state.has('Moon Stone', player))