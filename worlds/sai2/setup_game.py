import struct


def setup_gamevars(world):
    if world.options.switch_states == 0:
        world.light_switch_default = 0x00
        world.sun_switch_default = 0x01
        world.star_switch_default = 0x01
        world.aqua_switch_default = 0x01
        world.moon_switch_default = 0x00
    elif world.options.switch_states == 1:
        world.light_switch_default = 0x01
        world.sun_switch_default = 0x00
        world.star_switch_default = 0x00
        world.aqua_switch_default = 0x00
        world.moon_switch_default = 0x01
    else:
        world.light_switch_default = world.random.randint(0,1)
        world.sun_switch_default = world.random.randint(0,1)
        world.star_switch_default = world.random.randint(0,1)
        world.aqua_switch_default = world.random.randint(0,1)
        world.moon_switch_default = world.random.randint(0,1)
        
    if world.options.world_state == 2:
        world.light_gate = world.random.randint(0,1)
        world.sun_gate = world.random.randint(0,1)
        world.star_gate = world.random.randint(0,1)
        world.aqua_gate = world.random.randint(0,1)
        world.moon_gate = world.random.randint(0,1)
    else:
        world.light_gate = world.options.world_state
        world.sun_gate = world.options.world_state
        world.star_gate = world.options.world_state
        world.aqua_gate = world.options.world_state
        world.moon_gate = world.options.world_state

    if world.options.shortcut_states == 2:
        world.boa_hiya_shortcut = world.random.randint(0,1)
        world.sala_hiya_shortcut = world.random.randint(0,1)
        world.sala_puka_shortcut = world.random.randint(0,1)
        world.fuwa_poka_shortcut = world.random.randint(0,1)
        world.fuwa_puka_shortcut = world.random.randint(0,1)
    else:
        world.boa_hiya_shortcut = world.options.world_state
        world.sala_hiya_shortcut = world.options.world_state
        world.sala_puka_shortcut = world.options.world_state
        world.fuwa_poka_shortcut = world.options.world_state
        world.fuwa_puka_shortcut = world.options.world_state
    if world.options.shortcut_states >= 3:
        world.fuwa_poka_shortcut = 0
        world.fuwa_puka_shortcut = 0


    early_logic_items = [
        "Silver Sword",
        "Shovel"
    ]

    if world.light_gate == 0:
        early_logic_items.append("Light Stone")
    else:
        early_logic_items.extend(["Life Bottle", "Sun Ring"])
        if world.sun_gate == 1:
            early_logic_items.extend(["Shove", "500 Coins", "1000 Coins", "2000 Coins", "5000 Coins"])
            if world.star_gate == 0:
                early_logic_items.append("Star Stone")
        else:
            early_logic_items.append("Sun Stone")

    if world.aqua_gate == 0:
        early_logic_items.append("Aqua Stone")
    else:
        early_logic_items.extend(["1000 Coins", "2000 Coins", "5000 Coins"])
        if world.moon_gate == 0:
            early_logic_items.append("Moon Stone")

    for item in early_logic_items:
        if early_logic_items.count(item) > 1 or (item == "Life Bottle" and world.options.extra_health == 1):
            early_logic_items.remove(item)


    if world.options.world_state != 1:
        #If one, append the Stones corresponding to closed gates
        world.starting_item = world.random.choice(early_logic_items)

    world.locked_skills = ["Shove", "Down Jab", "Up Jab"]
    if world.options.shuffle_skills == 1:
        world.locked_skills.shuffle