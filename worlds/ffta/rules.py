from worlds.generic.Rules import add_rule, set_rule, forbid_item, CollectionRule
from .items import MissionUnlockItems


def rule_generator(world, item: str) -> CollectionRule:
    return lambda state: state.has(item, world.player)


def rule_generator_progressive(world, item: str, num: int) -> CollectionRule:
    return lambda state: state.has(item, world.player, num)


def set_rules(world) -> None:

    # Set final mission unlock to require all paths based on settings
    if world.options.goal.value == 0:
        final_mission_names = ["Royal Valley", "Decision Time"]
        final_mission = final_mission_names[world.options.final_mission.value]
        if world.options.gate_paths.value > 1:
            for path in range(0, world.options.gate_paths.value):
                add_rule(world.multiworld.get_location(final_mission, world.player),
                         rule_generator(world, f"Path {path+1} Complete"))

    if world.options.goal.value == 1:
        add_rule(world.multiworld.get_entrance("Totema 1", world.player),
                 lambda state: state.has("Water Sigil", world.player))

        add_rule(world.multiworld.get_entrance("Totema 2", world.player),
                 lambda state: state.has("Fire Sigil", world.player))

        add_rule(world.multiworld.get_entrance("Totema 3", world.player),
                 lambda state: state.has("Wind Sigil", world.player))

        add_rule(world.multiworld.get_entrance("Totema 4", world.player),
                 lambda state: state.has("Earth Sigil", world.player))

        add_rule(world.multiworld.get_entrance("Totema 5", world.player),
                 lambda state: state.has("Old Statue", world.player))

    num_gates = world.options.gate_num.value
    num_gates += world.options.gate_paths.value - 1

    # gate_items_static = [
    #     ("Magic Trophy", "Fight Trophy"),       # Gate 2
    #     ("Magic Medal", "Ancient Medal"),       # Gate 3
    #     ("Choco Bread", "Choco Gratin"),        # Gate 4
    #     ("Black Thread", "White Thread"),       # Gate 5
    #     ("Thunderstone", "Stormstone"),         # Gate 6
    #     ("Ahriman Eye", "Ahriman Wing"),        # Gate 7
    #     ("Magic Cloth", "Magic Cotton"),        # Gate 8
    #     ("Adaman Alloy", "Mysidia Alloy"),      # Gate 9
    #     ("Elda's Cup", "Gold Vessel"),          # Gate 10
    #     ("Kiddy Bread", "Grownup Bread"),       # Gate 11
    #     ("Danbukwood", "Moonwood"),             # Gate 12
    #     ("Dragon Bone", "Animal Bone"),         # Gate 13
    #     ("Magic Fruit", "Power Fruit"),         # Gate 14
    #     ("Malboro Wine", "Gedegg Soup"),        # Gate 15
    #     ("Encyclopedia", "Dictionary"),         # Gate 16
    #     ("Rat Tail", "Rabbit Tail"),            # Gate 17
    #     ("Stasis Rope", "Mythril Pick"),        # Gate 18
    #     ("Clock Gear", "Gun Gear"),             # Gate 19
    #     ("Blood Shawl", "Blood Apple"),         # Gate 20
    #     ("Eldagusto", "Cyril Ice"),             # Gate 21
    #     ("Crystal", "Trichord"),                # Gate 22
    #     ("Tranquil Box", "Flower Vase"),        # Gate 23
    #     ("Cat's Tears", "Dame's Blush"),        # Gate 24
    #     ("Justice Badge", "Friend Badge"),      # Gate 25
    #     ("Love Potion", "Tonberry Lamp"),       # Gate 26
    #     ("Runba's Tale", "The Hero Gaol"),      # Gate 27
    #     ("Mind Ceffyl", "Body Ceffyl"),         # Gate 28
    #     ("Ancient Bills", "Ancient Coins"),     # Gate 29
    #     ("Blue Rose", "White Flowers"),         # Gate 30
    #     ("Gysahl Greens", "Chocobo Egg"),       # Gate 31
    #     ("Delta Fang", "Esteroth"),             # Gate 32
    #     ("Moon Bloom", "Telaq Flowers"),        # Gate 33
    # ]
    gate_items = [(MissionUnlockItems[i].itemName,
                   MissionUnlockItems[i+1].itemName) for i in range(0, len(MissionUnlockItems), 2)]

    gates = world.multiworld.get_regions(world.player)
    dispatch_gates = [x.name for x in gates if x.name.startswith("Dispatch")][1:]
    gates = [x.name for x in gates if x.name.startswith("Gate")][1:]

    if world.options.progressive_gates.value == 1:
        sphere = 0
        for i, gate in enumerate(gates):
            path = i % world.options.gate_paths.value
            if path == 0:
                sphere += 1
            if world.options.gate_items.value == 1:
                add_rule(world.multiworld.get_entrance(gate, world.player),
                         rule_generator_progressive(world, f"Progressive Path {path+1}", sphere * 2))
            else:
                add_rule(world.multiworld.get_entrance(gate, world.player),
                         rule_generator_progressive(world, f"Progressive Path {path+1}", sphere))

        for i, dispatch_gate in enumerate(dispatch_gates):
            add_rule(world.multiworld.get_entrance(dispatch_gate, world.player),
                     rule_generator_progressive(world, "Progressive Dispatch", (i+1)))
    else:
        for i, gate in enumerate(gates):
            item1 = gate_items[i][0]
            item2 = gate_items[i][1]

            add_rule(world.multiworld.get_entrance(gate, world.player),
                     rule_generator(world, item1))

            if world.options.gate_items.value == 1:
                add_rule(world.multiworld.get_entrance(gate, world.player),
                         rule_generator(world, item2))

        for i, dispatch_gate in enumerate(dispatch_gates):
            add_rule(world.multiworld.get_entrance(dispatch_gate, world.player),
                     rule_generator(world, item2))
