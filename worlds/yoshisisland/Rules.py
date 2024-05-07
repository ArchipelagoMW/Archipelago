from .level_logic import YoshiLogic
from worlds.generic.Rules import set_rule
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from . import YoshisIslandWorld


def set_easy_rules(world: "YoshisIslandWorld") -> None:
    logic = YoshiLogic(world)
    player = world.player

    set_rule(world.multiworld.get_location("Make Eggs, Throw Eggs: Red Coins", player), lambda state: state.has_all({"Dashed Stairs", "Beanstalk"}, player))
    set_rule(world.multiworld.get_location("Make Eggs, Throw Eggs: Flowers", player), lambda state: state.has_all({"Dashed Stairs", "Beanstalk"}, player))
    set_rule(world.multiworld.get_location("Make Eggs, Throw Eggs: Stars", player), lambda state: state.has_all({"Tulip", "Beanstalk", "Dashed Stairs"}, player))
    set_rule(world.multiworld.get_location("Make Eggs, Throw Eggs: Level Clear", player), lambda state: state.has("Beanstalk", player))

    set_rule(world.multiworld.get_location("Watch Out Below!: Red Coins", player), lambda state: state.has_all({"Large Spring Ball", "Helicopter Morph"}, player))
    set_rule(world.multiworld.get_location("Watch Out Below!: Flowers", player), lambda state: state.has_all({"Large Spring Ball", "Helicopter Morph"}, player))
    set_rule(world.multiworld.get_location("Watch Out Below!: Stars", player), lambda state: state.has("Large Spring Ball", player) and logic.has_midring(state))
    set_rule(world.multiworld.get_location("Watch Out Below!: Level Clear", player), lambda state: state.has("Large Spring Ball", player))

    set_rule(world.multiworld.get_location("The Cave Of Chomp Rock: Red Coins", player), lambda state: state.has("Chomp Rock", player))
    set_rule(world.multiworld.get_location("The Cave Of Chomp Rock: Flowers", player), lambda state: state.has("Chomp Rock", player))

    set_rule(world.multiworld.get_location("Burt The Bashful's Fort: Red Coins", player), lambda state: state.has("Spring Ball", player))
    set_rule(world.multiworld.get_location("Burt The Bashful's Fort: Flowers", player), lambda state: state.has_all({"Spring Ball", "Key"}, player) and (state.has("Egg Capacity Upgrade", player, 3) or logic.combat_item(state)))
    set_rule(world.multiworld.get_location("Burt The Bashful's Fort: Stars", player), lambda state: state.has("Spring Ball", player) and (logic.has_midring(state) or state.has("Key", player)))

    set_rule(world.multiworld.get_location("Hop! Hop! Donut Lifts: Stars", player), lambda state: logic.has_midring(state) or logic.cansee_clouds(state))

    set_rule(world.multiworld.get_location("Shy-Guys On Stilts: Red Coins", player), lambda state: state.has_all({"Large Spring Ball", "Flashing Eggs", "Mole Tank Morph", "! Switch"}, player))
    set_rule(world.multiworld.get_location("Shy-Guys On Stilts: Flowers", player), lambda state: state.has("Large Spring Ball", player))
    set_rule(world.multiworld.get_location("Shy-Guys On Stilts: Stars", player), lambda state: (logic.has_midring(state) and state.has("Tulip", player) or logic.has_midring(state) and state.has("Beanstalk", player)) and state.has("Large Spring Ball", player))
    set_rule(world.multiworld.get_location("Shy-Guys On Stilts: Level Clear", player), lambda state: state.has_all({"Large Spring Ball", "Beanstalk"}, player))

    set_rule(world.multiworld.get_location("Touch Fuzzy Get Dizzy: Red Coins", player), lambda state: state.has_all({"Flashing Eggs", "Spring Ball", "Chomp Rock", "Beanstalk"}, player))
    set_rule(world.multiworld.get_location("Touch Fuzzy Get Dizzy: Stars", player), lambda state: logic.has_midring(state) or (logic.cansee_clouds and state.has_all({"Spring Ball", "Chomp Rock", "Beanstalk"}, player)))

    set_rule(world.multiworld.get_location("Salvo The Slime's Castle: Red Coins", player), lambda state: state.has("Platform Ghost", player))
    set_rule(world.multiworld.get_location("Salvo The Slime's Castle: Flowers", player), lambda state: state.has("Platform Ghost", player))
    set_rule(world.multiworld.get_location("Salvo The Slime's Castle: Stars", player), lambda state: logic.has_midring(state) and (state.has("Platform Ghost", player) or state.has_all({"Arrow Wheel", "Key"}, player)))

    set_rule(world.multiworld.get_location("Visit Koopa And Para-Koopa: Red Coins", player), lambda state: state.has_all({"Poochy", "Large Spring Ball", "Spring Ball"}, player))
    set_rule(world.multiworld.get_location("Visit Koopa And Para-Koopa: Flowers", player), lambda state: state.has_all({"Super Star", "Large Spring Ball"}, player))
    set_rule(world.multiworld.get_location("Visit Koopa And Para-Koopa: Stars", player), lambda state: state.has("Large Spring Ball", player) and logic.has_midring(state))
    set_rule(world.multiworld.get_location("Visit Koopa And Para-Koopa: Level Clear", player), lambda state: state.has("Large Spring Ball", player))

    set_rule(world.multiworld.get_location("The Baseball Boys: Red Coins", player), lambda state: state.has_all({"Beanstalk", "Super Star", "Egg Launcher", "Large Spring Ball", "Mole Tank Morph"}, player))
    set_rule(world.multiworld.get_location("The Baseball Boys: Flowers", player), lambda state: state.has_all({"Beanstalk", "Super Star", "Egg Launcher", "Large Spring Ball", "Spring Ball"}, player))
    set_rule(world.multiworld.get_location("The Baseball Boys: Stars", player), lambda state: (logic.has_midring(state) and (state.has("Tulip", player))) and state.has_all({"Beanstalk", "Super Star", "Large Spring Ball", "Egg Launcher"}, player))
    set_rule(world.multiworld.get_location("The Baseball Boys: Level Clear", player), lambda state: state.has_all({"Beanstalk", "Super Star", "Egg Launcher", "Large Spring Ball"}, player))

    set_rule(world.multiworld.get_location("What's Gusty Taste Like?: Red Coins", player), lambda state: state.has("! Switch", player))
    set_rule(world.multiworld.get_location("What's Gusty Taste Like?: Flowers", player), lambda state: state.has_any({"Large Spring Ball", "Super Star"}, player))
    set_rule(world.multiworld.get_location("What's Gusty Taste Like?: Level Clear", player), lambda state: state.has_any({"Large Spring Ball", "Super Star"}, player))

    set_rule(world.multiworld.get_location("Bigger Boo's Fort: Red Coins", player), lambda state: state.has_all({"! Switch", "Key", "Dashed Stairs"}, player))
    set_rule(world.multiworld.get_location("Bigger Boo's Fort: Flowers", player), lambda state: state.has_all({"! Switch", "Key", "Dashed Stairs"}, player))
    set_rule(world.multiworld.get_location("Bigger Boo's Fort: Stars", player), lambda state: state.has_all({"! Switch", "Key", "Dashed Stairs"}, player) and logic.has_midring(state))

    set_rule(world.multiworld.get_location("Watch Out For Lakitu: Red Coins", player), lambda state: state.has("Chomp Rock", player))
    set_rule(world.multiworld.get_location("Watch Out For Lakitu: Flowers", player), lambda state: state.has_all({"Key", "Train Morph", "Chomp Rock"}, player))
    set_rule(world.multiworld.get_location("Watch Out For Lakitu: Level Clear", player), lambda state: state.has("Chomp Rock", player))

    set_rule(world.multiworld.get_location("The Cave Of The Mystery Maze: Red Coins", player), lambda state: state.has("Large Spring Ball", player))
    set_rule(world.multiworld.get_location("The Cave Of The Mystery Maze: Flowers", player), lambda state: state.has_all({"Large Spring Ball", "Egg Launcher"}, player))
    set_rule(world.multiworld.get_location("The Cave Of The Mystery Maze: Stars", player), lambda state: state.has("Large Spring Ball", player) and logic.has_midring(state))
    set_rule(world.multiworld.get_location("The Cave Of The Mystery Maze: Level Clear", player), lambda state: state.has("Large Spring Ball", player))

    set_rule(world.multiworld.get_location("Lakitu's Wall: Red Coins", player), lambda state: (state.has_any({"Dashed Platform", "Giant Eggs"}, player) or logic.combat_item(state)) and state.has("Large Spring Ball", player))
    set_rule(world.multiworld.get_location("Lakitu's Wall: Flowers", player), lambda state: state.has_all({"Large Spring Ball", "! Switch"}, player) and (logic.combat_item(state) or state.has("Giant Eggs", player)))
    set_rule(world.multiworld.get_location("Lakitu's Wall: Stars", player), lambda state: state.has("Giant Eggs", player) and logic.has_midring(state))
    set_rule(world.multiworld.get_location("Lakitu's Wall: Level Clear", player), lambda state: state.has_all({"Large Spring Ball", "Car Morph"}, player))

    set_rule(world.multiworld.get_location("The Potted Ghost's Castle: Red Coins", player), lambda state: state.has_all({"Arrow Wheel", "Key"}, player) and (state.has("Egg Capacity Upgrade", player, 1)))
    set_rule(world.multiworld.get_location("The Potted Ghost's Castle: Flowers", player), lambda state: state.has_all({"Arrow Wheel", "Train Morph", "Key"}, player) and (state.has("Egg Capacity Upgrade", player, 1)))
    set_rule(world.multiworld.get_location("The Potted Ghost's Castle: Stars", player), lambda state: state.has_all({"Arrow Wheel", "Key"}, player) and logic.has_midring(state) and (state.has("Egg Capacity Upgrade", player, 1)))

    set_rule(world.multiworld.get_location("Welcome To Monkey World!: Stars", player), lambda state: logic.has_midring(state))
    set_rule(world.multiworld.get_location("Jungle Rhythm...: Red Coins", player), lambda state: state.has_all({"Dashed Stairs", "Spring Ball"}, player))
    set_rule(world.multiworld.get_location("Jungle Rhythm...: Flowers", player), lambda state: state.has_all({"Dashed Stairs", "Spring Ball"}, player))
    set_rule(world.multiworld.get_location("Jungle Rhythm...: Stars", player), lambda state: logic.has_midring(state) and state.has("Tulip", player))
    set_rule(world.multiworld.get_location("Jungle Rhythm...: Level Clear", player), lambda state: state.has_all({"Dashed Stairs", "Spring Ball"}, player))

    set_rule(world.multiworld.get_location("Nep-Enuts' Domain: Red Coins", player), lambda state: state.has_all({"Submarine Morph", "Helicopter Morph"}, player))
    set_rule(world.multiworld.get_location("Nep-Enuts' Domain: Flowers", player), lambda state: state.has_all({"Submarine Morph", "Helicopter Morph"}, player))
    set_rule(world.multiworld.get_location("Nep-Enuts' Domain: Stars", player), lambda state: logic.has_midring(state) or state.has_all({"Submarine Morph", "Helicopter Morph"}, player))
    set_rule(world.multiworld.get_location("Nep-Enuts' Domain: Level Clear", player), lambda state: state.has_all({"Submarine Morph", "Helicopter Morph"}, player))

    set_rule(world.multiworld.get_location("Prince Froggy's Fort: Red Coins", player), lambda state: state.has("Submarine Morph", player))
    set_rule(world.multiworld.get_location("Prince Froggy's Fort: Flowers", player), lambda state: (state.has("Egg Capacity Upgrade", player, 5) or logic.combat_item(state)) and (state.has("Dashed Platform", player)))
    set_rule(world.multiworld.get_location("Prince Froggy's Fort: Stars", player), lambda state: logic.has_midring(state))

    set_rule(world.multiworld.get_location("Jammin' Through The Trees: Flowers", player), lambda state: state.has("Watermelon", player) or logic.melon_item(state))
    set_rule(world.multiworld.get_location("Jammin' Through The Trees: Stars", player), lambda state: ((logic.has_midring(state) or state.has("Tulip", player)) and logic.cansee_clouds(state)) or logic.has_midring(state) and state.has("Tulip", player))

    set_rule(world.multiworld.get_location("The Cave Of Harry Hedgehog: Red Coins", player), lambda state: state.has_all({"Chomp Rock", "Beanstalk", "Mole Tank Morph", "Large Spring Ball"}, player))
    set_rule(world.multiworld.get_location("The Cave Of Harry Hedgehog: Flowers", player), lambda state: state.has_all({"Chomp Rock", "Beanstalk", "Mole Tank Morph", "Large Spring Ball", "! Switch"}, player))
    set_rule(world.multiworld.get_location("The Cave Of Harry Hedgehog: Stars", player), lambda state: state.has_all({"Tulip", "Large Spring Ball", "Dashed Stairs", "Chomp Rock", "Beanstalk", "Mole Tank Morph"}, player) and logic.has_midring(state))
    set_rule(world.multiworld.get_location("The Cave Of Harry Hedgehog: Level Clear", player), lambda state: state.has_all({"Chomp Rock", "Large Spring Ball", "Key"}, player))

    set_rule(world.multiworld.get_location("Monkeys' Favorite Lake: Red Coins", player), lambda state: state.has_all({"! Switch", "Submarine Morph", "Large Spring Ball", "Beanstalk"}, player))
    set_rule(world.multiworld.get_location("Monkeys' Favorite Lake: Flowers", player), lambda state: state.has_all({"Beanstalk", "Large Spring Ball"}, player))
    set_rule(world.multiworld.get_location("Monkeys' Favorite Lake: Stars", player), lambda state: state.has("Large Spring Ball", player))
    set_rule(world.multiworld.get_location("Monkeys' Favorite Lake: Level Clear", player), lambda state: state.has("Large Spring Ball", player))

    set_rule(world.multiworld.get_location("Naval Piranha's Castle: Red Coins", player), lambda state: (state.has("Egg Capacity Upgrade", player, 3) or logic.combat_item(state)))
    set_rule(world.multiworld.get_location("Naval Piranha's Castle: Flowers", player), lambda state: (state.has("Egg Capacity Upgrade", player, 3) or logic.combat_item(state)))
    set_rule(world.multiworld.get_location("Naval Piranha's Castle: Stars", player), lambda state: logic.has_midring(state) and state.has("Tulip", player))

    set_rule(world.multiworld.get_location("GO! GO! MARIO!!: Red Coins", player), lambda state: state.has("Super Star", player))
    set_rule(world.multiworld.get_location("GO! GO! MARIO!!: Flowers", player), lambda state: state.has("Super Star", player))
    set_rule(world.multiworld.get_location("GO! GO! MARIO!!: Stars", player), lambda state: logic.has_midring(state) or (state.has("Tulip", player) and logic.cansee_clouds(state)))
    set_rule(world.multiworld.get_location("GO! GO! MARIO!!: Level Clear", player), lambda state: state.has("Super Star", player))

    set_rule(world.multiworld.get_location("The Cave Of The Lakitus: Red Coins", player), lambda state: state.has_all({"Large Spring Ball", "! Switch", "Egg Launcher"}, player))
    set_rule(world.multiworld.get_location("The Cave Of The Lakitus: Flowers", player), lambda state: state.has_all({"Large Spring Ball", "Egg Launcher"}, player))
    set_rule(world.multiworld.get_location("The Cave Of The Lakitus: Stars", player), lambda state: state.has_all({"Large Spring Ball", "Spring Ball"}, player))
    set_rule(world.multiworld.get_location("The Cave Of The Lakitus: Level Clear", player), lambda state: state.has("Large Spring Ball", player))

    set_rule(world.multiworld.get_location("Don't Look Back!: Red Coins", player), lambda state: state.has_all({"Helicopter Morph", "! Switch", "Large Spring Ball"}, player))
    set_rule(world.multiworld.get_location("Don't Look Back!: Flowers", player), lambda state: state.has_all({"! Switch", "Large Spring Ball"}, player))
    set_rule(world.multiworld.get_location("Don't Look Back!: Stars", player), lambda state: (logic.has_midring(state) and state.has("Tulip", player)) and state.has("! Switch", player))
    set_rule(world.multiworld.get_location("Don't Look Back!: Level Clear", player), lambda state: state.has("! Switch", player))

    set_rule(world.multiworld.get_location("Marching Milde's Fort: Red Coins", player), lambda state: state.has_all({"Dashed Stairs", "Vanishing Arrow Wheel", "Arrow Wheel", "Bucket", "Key"}, player) and (state.has("Egg Capacity Upgrade", player, 1) or logic.combat_item(state)))
    set_rule(world.multiworld.get_location("Marching Milde's Fort: Flowers", player), lambda state: state.has_all({"Dashed Stairs", "Vanishing Arrow Wheel", "Arrow Wheel", "Bucket"}, player) and (state.has("Egg Capacity Upgrade", player, 1) or logic.combat_item(state)))
    set_rule(world.multiworld.get_location("Marching Milde's Fort: Stars", player), lambda state: state.has("Dashed Stairs", player) and (logic.has_midring(state) or state.has("Vanishing Arrow Wheel", player) or logic.cansee_clouds(state)))

    set_rule(world.multiworld.get_location("Chomp Rock Zone: Red Coins", player), lambda state: state.has_all({"Large Spring Ball", "Chomp Rock"}, player))
    set_rule(world.multiworld.get_location("Chomp Rock Zone: Flowers", player), lambda state: state.has_all({"Chomp Rock", "! Switch", "Spring Ball", "Dashed Platform"}, player))
    set_rule(world.multiworld.get_location("Chomp Rock Zone: Stars", player), lambda state: state.has_all({"Chomp Rock", "! Switch", "Spring Ball", "Dashed Platform"}, player))

    set_rule(world.multiworld.get_location("Lake Shore Paradise: Red Coins", player), lambda state: state.has_any({"Large Spring Ball", "Spring Ball"}, player) and (state.has("Egg Plant", player) or logic.combat_item(state)))
    set_rule(world.multiworld.get_location("Lake Shore Paradise: Flowers", player), lambda state: state.has_any({"Large Spring Ball", "Spring Ball"}, player) and (state.has("Egg Plant", player) or logic.combat_item(state)))
    set_rule(world.multiworld.get_location("Lake Shore Paradise: Stars", player), lambda state: (logic.has_midring(state) or (state.has("Tulip", player) and logic.cansee_clouds(state))) and (state.has("Egg Plant", player) or logic.combat_item(state)))
    set_rule(world.multiworld.get_location("Lake Shore Paradise: Level Clear", player), lambda state: state.has("Egg Plant", player) or logic.combat_item(state))

    set_rule(world.multiworld.get_location("Ride Like The Wind: Red Coins", player), lambda state: state.has("Large Spring Ball", player))
    set_rule(world.multiworld.get_location("Ride Like The Wind: Flowers", player), lambda state: state.has("Large Spring Ball", player))
    set_rule(world.multiworld.get_location("Ride Like The Wind: Stars", player), lambda state: (logic.has_midring(state) and state.has("Helicopter Morph", player)) and state.has("Large Spring Ball", player))
    set_rule(world.multiworld.get_location("Ride Like The Wind: Level Clear", player), lambda state: state.has("Large Spring Ball", player))

    set_rule(world.multiworld.get_location("Hookbill The Koopa's Castle: Red Coins", player), lambda state: state.has_all({"Dashed Stairs", "Vanishing Arrow Wheel", "Key"}, player))
    set_rule(world.multiworld.get_location("Hookbill The Koopa's Castle: Flowers", player), lambda state: state.has_all({"Dashed Stairs", "Vanishing Arrow Wheel", "Key"}, player))
    set_rule(world.multiworld.get_location("Hookbill The Koopa's Castle: Stars", player), lambda state: logic.has_midring(state) and (state.has_any({"Dashed Stairs", "Vanishing Arrow Wheel"}, player)))

    set_rule(world.multiworld.get_location("BLIZZARD!!!: Red Coins", player), lambda state: state.has_all({"Helicopter Morph", "Dashed Stairs"}, player))
    set_rule(world.multiworld.get_location("BLIZZARD!!!: Stars", player), lambda state: logic.cansee_clouds(state) or ((logic.has_midring(state) and state.has("Dashed Stairs", player)) or state.has("Tulip", player)))

    set_rule(world.multiworld.get_location("Ride The Ski Lifts: Stars", player), lambda state: logic.has_midring(state) or state.has("Super Star", player))

    set_rule(world.multiworld.get_location("Danger - Icy Conditions Ahead: Red Coins", player), lambda state: (state.has("Fire Melon", player) or logic.melon_item(state)) and (state.has_all({"Bucket", "Spring Ball", "Super Star", "Skis", "Dashed Platform"}, player)))
    set_rule(world.multiworld.get_location("Danger - Icy Conditions Ahead: Flowers", player), lambda state: (state.has("Fire Melon", player) or logic.melon_item(state)) and state.has_all({"Spring Ball", "Skis", "Dashed Platform"}, player))
    set_rule(world.multiworld.get_location("Danger - Icy Conditions Ahead: Stars", player), lambda state: (logic.has_midring(state) and (state.has("Fire Melon", player) or logic.melon_item(state))) and state.has("Spring Ball", player))
    set_rule(world.multiworld.get_location("Danger - Icy Conditions Ahead: Level Clear", player), lambda state: state.has_all({"Spring Ball", "Skis", "Dashed Platform"}, player))

    set_rule(world.multiworld.get_location("Sluggy The Unshaven's Fort: Red Coins", player), lambda state: state.has_all({"Dashed Stairs", "Dashed Platform", "Platform Ghost"}, player))
    set_rule(world.multiworld.get_location("Sluggy The Unshaven's Fort: Flowers", player), lambda state: state.has_all({"Dashed Stairs", "Platform Ghost", "Dashed Platform"}, player))
    set_rule(world.multiworld.get_location("Sluggy The Unshaven's Fort: Stars", player), lambda state: ((state.has_all({"Dashed Stairs", "Platform Ghost"}, player)) and logic.has_midring(state)) or (logic.cansee_clouds(state) and state.has("Dashed Stairs", player) and state.has("Dashed Platform", player)))

    set_rule(world.multiworld.get_location("Goonie Rides!: Red Coins", player), lambda state: state.has_all({"Helicopter Morph", "! Switch"}, player))
    set_rule(world.multiworld.get_location("Goonie Rides!: Flowers", player), lambda state: state.has_all({"Helicopter Morph", "! Switch"}, player))
    set_rule(world.multiworld.get_location("Goonie Rides!: Stars", player), lambda state: logic.has_midring(state))
    set_rule(world.multiworld.get_location("Goonie Rides!: Level Clear", player), lambda state: state.has_all({"Helicopter Morph", "! Switch"}, player))

    set_rule(world.multiworld.get_location("Welcome To Cloud World: Stars", player), lambda state: logic.has_midring(state) or state.has("Tulip", player))

    set_rule(world.multiworld.get_location("Shifting Platforms Ahead: Red Coins", player), lambda state: state.has("Egg Capacity Upgrade", player, 1) or logic.combat_item(state))
    set_rule(world.multiworld.get_location("Shifting Platforms Ahead: Flowers", player), lambda state: state.has("Egg Capacity Upgrade", player, 1) or logic.combat_item(state))
    set_rule(world.multiworld.get_location("Shifting Platforms Ahead: Stars", player), lambda state: logic.has_midring(state))

    set_rule(world.multiworld.get_location("Raphael The Raven's Castle: Red Coins", player), lambda state: state.has_all({"Arrow Wheel", "Train Morph"}, player))
    set_rule(world.multiworld.get_location("Raphael The Raven's Castle: Flowers", player), lambda state: state.has_all({"Arrow Wheel", "Train Morph"}, player))
    set_rule(world.multiworld.get_location("Raphael The Raven's Castle: Stars", player), lambda state: logic.has_midring(state) and state.has("Arrow Wheel", player))

    set_rule(world.multiworld.get_location("Scary Skeleton Goonies!: Red Coins", player), lambda state: state.has_all({"Dashed Platform", "Large Spring Ball"}, player))
    set_rule(world.multiworld.get_location("Scary Skeleton Goonies!: Flowers", player), lambda state: state.has_all({"Dashed Platform", "Large Spring Ball"}, player))
    set_rule(world.multiworld.get_location("Scary Skeleton Goonies!: Stars", player), lambda state: state.has("Dashed Platform", player) and logic.has_midring(state))
    set_rule(world.multiworld.get_location("Scary Skeleton Goonies!: Level Clear", player), lambda state: state.has_all({"Dashed Platform", "Large Spring Ball"}, player))

    set_rule(world.multiworld.get_location("The Cave Of The Bandits: Red Coins", player), lambda state: state.has("Super Star", player))
    set_rule(world.multiworld.get_location("The Cave Of The Bandits: Flowers", player), lambda state: state.has("Super Star", player))
    set_rule(world.multiworld.get_location("The Cave Of The Bandits: Stars", player), lambda state: logic.cansee_clouds(state) or logic.has_midring(state))
    set_rule(world.multiworld.get_location("The Cave Of The Bandits: Level Clear", player), lambda state: state.has("Super Star", player))

    set_rule(world.multiworld.get_location("Tap-Tap The Red Nose's Fort: Red Coins", player), lambda state: state.has_all({"Spring Ball", "Large Spring Ball", "Egg Plant", "Key"}, player) and (state.has("Egg Capacity Upgrade", player, 3) or logic.combat_item(state)))
    set_rule(world.multiworld.get_location("Tap-Tap The Red Nose's Fort: Flowers", player), lambda state: state.has_all({"Spring Ball", "Large Spring Ball", "Egg Plant", "Key"}, player) and (state.has("Egg Capacity Upgrade", player, 3) or logic.combat_item(state)))
    set_rule(world.multiworld.get_location("Tap-Tap The Red Nose's Fort: Stars", player), lambda state: logic.has_midring(state) and state.has_all({"Spring Ball", "Large Spring Ball", "Egg Plant", "Key"}, player))

    set_rule(world.multiworld.get_location("The Very Loooooong Cave: Red Coins", player), lambda state: state.has("Chomp Rock", player) and (state.has("Egg Capacity Upgrade", player, 3) or logic.combat_item(state)))
    set_rule(world.multiworld.get_location("The Very Loooooong Cave: Flowers", player), lambda state: state.has("Chomp Rock", player) and (state.has("Egg Capacity Upgrade", player, 3) or logic.combat_item(state)))
    set_rule(world.multiworld.get_location("The Very Loooooong Cave: Stars", player), lambda state: state.has("Chomp Rock", player) and (state.has("Egg Capacity Upgrade", player, 3) or logic.combat_item(state)) and logic.has_midring(state))

    set_rule(world.multiworld.get_location("The Deep, Underground Maze: Red Coins", player), lambda state: state.has_all({"Chomp Rock", "Key", "Large Spring Ball"}, player))
    set_rule(world.multiworld.get_location("The Deep, Underground Maze: Flowers", player), lambda state: state.has_all({"Chomp Rock", "Key", "Large Spring Ball"}, player))
    set_rule(world.multiworld.get_location("The Deep, Underground Maze: Stars", player), lambda state: state.has_all({"Chomp Rock", "Tulip", "Key"}, player) or (logic.has_midring(state) and state.has_all({"Key", "Chomp Rock", "Large Spring Ball"}, player)))
    set_rule(world.multiworld.get_location("The Deep, Underground Maze: Level Clear", player), lambda state: state.has_all({"Chomp Rock", "Key", "Large Spring Ball", "Dashed Platform"}, player))

    set_rule(world.multiworld.get_location("KEEP MOVING!!!!: Red Coins", player), lambda state: (state.has("Egg Capacity Upgrade", player, 1) or logic.combat_item(state)))
    set_rule(world.multiworld.get_location("KEEP MOVING!!!!: Flowers", player), lambda state: state.has("Egg Plant", player))
    set_rule(world.multiworld.get_location("KEEP MOVING!!!!: Stars", player), lambda state: logic.has_midring(state))

    set_rule(world.multiworld.get_location("King Bowser's Castle: Red Coins", player), lambda state: state.has_all({"Helicopter Morph", "Egg Plant"}, player) and logic._68CollectibleRoute(state))
    set_rule(world.multiworld.get_location("King Bowser's Castle: Flowers", player), lambda state: state.has_all({"Helicopter Morph", "Egg Plant"}, player) and logic._68CollectibleRoute(state))
    set_rule(world.multiworld.get_location("King Bowser's Castle: Stars", player), lambda state: state.has_all({"Helicopter Morph", "Egg Plant"}, player) and logic._68Route(state))

    set_easy_extra_rules(world)


def set_easy_extra_rules(world: "YoshisIslandWorld") -> None:
    player = world.player
    logic = YoshiLogic(world)
    if not world.options.extras_enabled:
        return
    set_rule(world.multiworld.get_location("Poochy Ain't Stupid: Red Coins", player), lambda state: state.has("Poochy", player))
    set_rule(world.multiworld.get_location("Poochy Ain't Stupid: Flowers", player), lambda state: state.has("Poochy", player))
    set_rule(world.multiworld.get_location("Poochy Ain't Stupid: Stars", player), lambda state: state.has("Poochy", player))
    set_rule(world.multiworld.get_location("Poochy Ain't Stupid: Level Clear", player), lambda state: state.has("Poochy", player))

    set_rule(world.multiworld.get_location("Hit That Switch!!: Red Coins", player), lambda state: state.has_all({"Large Spring Ball", "! Switch"}, player))
    set_rule(world.multiworld.get_location("Hit That Switch!!: Flowers", player), lambda state: state.has_all({"Large Spring Ball", "! Switch"}, player))
    set_rule(world.multiworld.get_location("Hit That Switch!!: Level Clear", player), lambda state: state.has_all({"Large Spring Ball", "! Switch"}, player))

    set_rule(world.multiworld.get_location("The Impossible? Maze: Red Coins", player), lambda state: state.has_all({"Spring Ball", "Large Spring Ball", "Mole Tank Morph", "Helicopter Morph", "Flashing Eggs"}, player))
    set_rule(world.multiworld.get_location("The Impossible? Maze: Flowers", player), lambda state: state.has_all({"Spring Ball", "Large Spring Ball", "Mole Tank Morph", "Helicopter Morph"}, player))
    set_rule(world.multiworld.get_location("The Impossible? Maze: Stars", player), lambda state: state.has_all({"Spring Ball", "Large Spring Ball", "Mole Tank Morph"}, player))
    set_rule(world.multiworld.get_location("The Impossible? Maze: Level Clear", player), lambda state: state.has_all({"Spring Ball", "Large Spring Ball", "Mole Tank Morph", "Helicopter Morph"}, player))

    set_rule(world.multiworld.get_location("Kamek's Revenge: Red Coins", player), lambda state: state.has_all({"Key", "Skis", "Helicopter Morph", "! Switch"}, player) and logic.has_midring(state))
    set_rule(world.multiworld.get_location("Kamek's Revenge: Flowers", player), lambda state: state.has_all({"Key", "Skis", "Helicopter Morph", "! Switch"}, player) and logic.has_midring(state))
    set_rule(world.multiworld.get_location("Kamek's Revenge: Stars", player), lambda state: state.has("! Switch", player) and logic.has_midring(state))
    set_rule(world.multiworld.get_location("Kamek's Revenge: Level Clear", player), lambda state: state.has_all({"Key", "Skis", "! Switch", "Helicopter Morph"}, player))

    set_rule(world.multiworld.get_location("Castles - Masterpiece Set: Red Coins", player), lambda state: (state.has("Egg Capacity Upgrade", player, 2) or logic.combat_item(state)) and state.has(("Large Spring Ball"), player))
    set_rule(world.multiworld.get_location("Castles - Masterpiece Set: Flowers", player), lambda state: (state.has("Egg Capacity Upgrade", player, 2) or logic.combat_item(state)) and state.has(("Large Spring Ball"), player))
    set_rule(world.multiworld.get_location("Castles - Masterpiece Set: Stars", player), lambda state: logic.has_midring(state) and state.has(("Large Spring Ball"), player))
    set_rule(world.multiworld.get_location("Castles - Masterpiece Set: Level Clear", player), lambda state: (state.has("Egg Capacity Upgrade", player, 2) or logic.combat_item(state)) and state.has(("Large Spring Ball"), player))


def set_normal_rules(world: "YoshisIslandWorld") -> None:
    logic = YoshiLogic(world)
    player = world.player

    set_rule(world.multiworld.get_location("Make Eggs, Throw Eggs: Red Coins", player), lambda state: state.has("Dashed Stairs", player))
    set_rule(world.multiworld.get_location("Make Eggs, Throw Eggs: Flowers", player), lambda state: state.has("Dashed Stairs", player))
    set_rule(world.multiworld.get_location("Make Eggs, Throw Eggs: Stars", player), lambda state: state.has_any({"Tulip", "Dashed Stairs"}, player))

    set_rule(world.multiworld.get_location("Watch Out Below!: Red Coins", player), lambda state: state.has("Helicopter Morph", player))
    set_rule(world.multiworld.get_location("Watch Out Below!: Flowers", player), lambda state: state.has("Helicopter Morph", player))
    set_rule(world.multiworld.get_location("Watch Out Below!: Stars", player), lambda state: logic.has_midring(state))

    set_rule(world.multiworld.get_location("Burt The Bashful's Fort: Red Coins", player), lambda state: state.has("Spring Ball", player))
    set_rule(world.multiworld.get_location("Burt The Bashful's Fort: Flowers", player), lambda state: state.has_all({"Spring Ball", "Key"}, player) and (state.has("Egg Capacity Upgrade", player, 3) or logic.combat_item(state)))
    set_rule(world.multiworld.get_location("Burt The Bashful's Fort: Stars", player), lambda state: state.has("Spring Ball", player))
    set_rule(world.multiworld.get_location("Burt The Bashful's Fort: Level Clear", player), lambda state: logic._14CanFightBoss(state))


    set_rule(world.multiworld.get_location("Shy-Guys On Stilts: Red Coins", player), lambda state: state.has_all({"Large Spring Ball", "Flashing Eggs", "Mole Tank Morph", "! Switch"}, player))
    set_rule(world.multiworld.get_location("Shy-Guys On Stilts: Flowers", player), lambda state: state.has("Large Spring Ball", player))
    set_rule(world.multiworld.get_location("Shy-Guys On Stilts: Stars", player), lambda state: (logic.has_midring(state) and state.has_any(["Tulip", "Beanstalk"], player)) or (state.has_all(["Tulip", "Beanstalk", "Large Spring Ball"], player)))
    set_rule(world.multiworld.get_location("Shy-Guys On Stilts: Level Clear", player), lambda state: state.has_all({"Large Spring Ball", "Beanstalk"}, player))

    set_rule(world.multiworld.get_location("Touch Fuzzy Get Dizzy: Red Coins", player), lambda state: state.has_all({"Flashing Eggs", "Spring Ball", "Chomp Rock", "Beanstalk"}, player))
    set_rule(world.multiworld.get_location("Touch Fuzzy Get Dizzy: Stars", player), lambda state: logic.has_midring(state) or (logic.cansee_clouds and state.has_all({"Spring Ball", "Chomp Rock", "Beanstalk"}, player)))

    set_rule(world.multiworld.get_location("Salvo The Slime's Castle: Red Coins", player), lambda state: state.has("Platform Ghost", player))
    set_rule(world.multiworld.get_location("Salvo The Slime's Castle: Flowers", player), lambda state: state.has("Platform Ghost", player))
    set_rule(world.multiworld.get_location("Salvo The Slime's Castle: Stars", player), lambda state: logic.has_midring(state) and (state.has("Platform Ghost", player) or state.has_all({"Arrow Wheel", "Key"}, player)))

    set_rule(world.multiworld.get_location("Visit Koopa And Para-Koopa: Red Coins", player), lambda state: state.has_all({"Poochy", "Large Spring Ball", "Spring Ball"}, player))
    set_rule(world.multiworld.get_location("Visit Koopa And Para-Koopa: Flowers", player), lambda state: state.has_all({"Super Star", "Large Spring Ball"}, player))
    set_rule(world.multiworld.get_location("Visit Koopa And Para-Koopa: Stars", player), lambda state: state.has("Large Spring Ball", player) and logic.has_midring(state))
    set_rule(world.multiworld.get_location("Visit Koopa And Para-Koopa: Level Clear", player), lambda state: state.has("Large Spring Ball", player))

    set_rule(world.multiworld.get_location("The Baseball Boys: Red Coins", player), lambda state: state.has_all({"Beanstalk", "Super Star", "Large Spring Ball", "Mole Tank Morph"}, player))
    set_rule(world.multiworld.get_location("The Baseball Boys: Flowers", player), lambda state: state.has_all({"Super Star", "Large Spring Ball", "Beanstalk", "Spring Ball"}, player))
    set_rule(world.multiworld.get_location("The Baseball Boys: Stars", player), lambda state: (logic.has_midring(state) or (state.has("Tulip", player))) and state.has_all({"Beanstalk", "Large Spring Ball"}, player))
    set_rule(world.multiworld.get_location("The Baseball Boys: Level Clear", player), lambda state: state.has_all({"Beanstalk", "Super Star", "Large Spring Ball"}, player))

    set_rule(world.multiworld.get_location("What's Gusty Taste Like?: Red Coins", player), lambda state: state.has("! Switch", player))

    set_rule(world.multiworld.get_location("Bigger Boo's Fort: Red Coins", player), lambda state: state.has_all({"! Switch", "Key", "Dashed Stairs"}, player))
    set_rule(world.multiworld.get_location("Bigger Boo's Fort: Flowers", player), lambda state: state.has_all({"! Switch", "Key", "Dashed Stairs"}, player))
    set_rule(world.multiworld.get_location("Bigger Boo's Fort: Stars", player), lambda state: state.has_all({"! Switch", "Dashed Stairs"}, player))

    set_rule(world.multiworld.get_location("Watch Out For Lakitu: Flowers", player), lambda state: state.has_all({"Key", "Train Morph"}, player))

    set_rule(world.multiworld.get_location("The Cave Of The Mystery Maze: Red Coins", player), lambda state: state.has("Large Spring Ball", player))
    set_rule(world.multiworld.get_location("The Cave Of The Mystery Maze: Flowers", player), lambda state: state.has_all({"Large Spring Ball", "Egg Launcher"}, player))
    set_rule(world.multiworld.get_location("The Cave Of The Mystery Maze: Stars", player), lambda state: state.has("Large Spring Ball", player))
    set_rule(world.multiworld.get_location("The Cave Of The Mystery Maze: Level Clear", player), lambda state: state.has("Large Spring Ball", player))

    set_rule(world.multiworld.get_location("Lakitu's Wall: Flowers", player), lambda state: state.has_all({"Large Spring Ball", "! Switch"}, player) and (logic.combat_item(state) or state.has("Giant Eggs", player)))
    set_rule(world.multiworld.get_location("Lakitu's Wall: Stars", player), lambda state: state.has("Giant Eggs", player) or logic.has_midring(state))

    set_rule(world.multiworld.get_location("The Potted Ghost's Castle: Red Coins", player), lambda state: state.has_all({"Arrow Wheel", "Key"}, player))
    set_rule(world.multiworld.get_location("The Potted Ghost's Castle: Flowers", player), lambda state: state.has_all({"Arrow Wheel", "Key", "Train Morph"}, player))
    set_rule(world.multiworld.get_location("The Potted Ghost's Castle: Stars", player), lambda state: state.has("Arrow Wheel", player) and (logic.has_midring(state) or state.has("Key", player)))

    set_rule(world.multiworld.get_location("Welcome To Monkey World!: Stars", player), lambda state: logic.has_midring(state))

    set_rule(world.multiworld.get_location("Jungle Rhythm...: Red Coins", player), lambda state: state.has("Dashed Stairs", player))
    set_rule(world.multiworld.get_location("Jungle Rhythm...: Flowers", player), lambda state: state.has("Dashed Stairs", player))
    set_rule(world.multiworld.get_location("Jungle Rhythm...: Stars", player), lambda state: logic.has_midring(state) and state.has("Tulip", player))
    set_rule(world.multiworld.get_location("Jungle Rhythm...: Level Clear", player), lambda state: state.has("Dashed Stairs", player))

    set_rule(world.multiworld.get_location("Nep-Enuts' Domain: Red Coins", player), lambda state: state.has_all({"Submarine Morph", "Helicopter Morph"}, player))
    set_rule(world.multiworld.get_location("Nep-Enuts' Domain: Flowers", player), lambda state: state.has_all({"Submarine Morph", "Helicopter Morph"}, player))
    set_rule(world.multiworld.get_location("Nep-Enuts' Domain: Level Clear", player), lambda state: state.has_all({"Submarine Morph", "Helicopter Morph"}, player))

    set_rule(world.multiworld.get_location("Prince Froggy's Fort: Red Coins", player), lambda state: state.has("Submarine Morph", player))
    set_rule(world.multiworld.get_location("Prince Froggy's Fort: Flowers", player), lambda state: (state.has("Egg Capacity Upgrade", player, 5) or logic.combat_item(state)) and (state.has("Dashed Platform", player) or logic.has_midring(state)))
    set_rule(world.multiworld.get_location("Prince Froggy's Fort: Stars", player), lambda state: logic.has_midring(state))

    set_rule(world.multiworld.get_location("Jammin' Through The Trees: Flowers", player), lambda state: state.has("Watermelon", player) or logic.melon_item(state))

    set_rule(world.multiworld.get_location("The Cave Of Harry Hedgehog: Red Coins", player), lambda state: state.has_any({"Dashed Stairs", "Beanstalk"}, player) and state.has_all({"Mole Tank Morph", "Large Spring Ball"}, player))
    set_rule(world.multiworld.get_location("The Cave Of Harry Hedgehog: Flowers", player), lambda state: state.has_any({"Dashed Stairs", "Beanstalk"}, player) and state.has_all({"! Switch", "Mole Tank Morph", "Large Spring Ball"}, player))
    set_rule(world.multiworld.get_location("The Cave Of Harry Hedgehog: Stars", player), lambda state: (state.has_any({"Dashed Stairs", "Beanstalk"}, player) and state.has_all({"Mole Tank Morph", "Large Spring Ball"}, player)) and (logic.has_midring(state) or state.has("Tulip", player)))
    set_rule(world.multiworld.get_location("The Cave Of Harry Hedgehog: Level Clear", player), lambda state: state.has_all({"Large Spring Ball", "Key"}, player))

    set_rule(world.multiworld.get_location("Monkeys' Favorite Lake: Red Coins", player), lambda state: state.has_all({"! Switch", "Submarine Morph", "Large Spring Ball", "Beanstalk"}, player))
    set_rule(world.multiworld.get_location("Monkeys' Favorite Lake: Flowers", player), lambda state: state.has("Beanstalk", player))

    set_rule(world.multiworld.get_location("Naval Piranha's Castle: Red Coins", player), lambda state: (state.has("Egg Capacity Upgrade", player, 1) or logic.combat_item(state)))
    set_rule(world.multiworld.get_location("Naval Piranha's Castle: Flowers", player), lambda state: (state.has("Egg Capacity Upgrade", player, 1) or logic.combat_item(state)))
    set_rule(world.multiworld.get_location("Naval Piranha's Castle: Stars", player), lambda state: (logic.has_midring(state) and state.has("Tulip", player)) and state.has("Egg Capacity Upgrade", player, 1))

    set_rule(world.multiworld.get_location("GO! GO! MARIO!!: Red Coins", player), lambda state: state.has("Super Star", player))
    set_rule(world.multiworld.get_location("GO! GO! MARIO!!: Flowers", player), lambda state: state.has("Super Star", player))
    set_rule(world.multiworld.get_location("GO! GO! MARIO!!: Stars", player), lambda state: logic.has_midring(state) or state.has("Tulip", player))
    set_rule(world.multiworld.get_location("GO! GO! MARIO!!: Level Clear", player), lambda state: state.has("Super Star", player))

    set_rule(world.multiworld.get_location("The Cave Of The Lakitus: Red Coins", player), lambda state: state.has_all({"Large Spring Ball", "! Switch", "Egg Launcher"}, player))
    set_rule(world.multiworld.get_location("The Cave Of The Lakitus: Flowers", player), lambda state: state.has_all({"Large Spring Ball", "Egg Launcher"}, player))
    set_rule(world.multiworld.get_location("The Cave Of The Lakitus: Stars", player), lambda state: state.has("Large Spring Ball", player))
    set_rule(world.multiworld.get_location("The Cave Of The Lakitus: Level Clear", player), lambda state: state.has("Large Spring Ball", player))

    set_rule(world.multiworld.get_location("Don't Look Back!: Red Coins", player), lambda state: state.has_all({"Helicopter Morph", "! Switch", "Large Spring Ball"}, player))
    set_rule(world.multiworld.get_location("Don't Look Back!: Flowers", player), lambda state: state.has("Large Spring Ball", player))
    set_rule(world.multiworld.get_location("Don't Look Back!: Stars", player), lambda state: (logic.has_midring(state) or state.has("Tulip", player)) and state.has("! Switch", player))
    set_rule(world.multiworld.get_location("Don't Look Back!: Level Clear", player), lambda state: state.has("! Switch", player))

    set_rule(world.multiworld.get_location("Marching Milde's Fort: Red Coins", player), lambda state: state.has_all({"Dashed Stairs", "Vanishing Arrow Wheel", "Arrow Wheel", "Bucket", "Key"}, player))
    set_rule(world.multiworld.get_location("Marching Milde's Fort: Flowers", player), lambda state: state.has_all({"Dashed Stairs", "Vanishing Arrow Wheel", "Arrow Wheel", "Bucket"}, player))
    set_rule(world.multiworld.get_location("Marching Milde's Fort: Stars", player), lambda state: state.has("Dashed Stairs", player))

    set_rule(world.multiworld.get_location("Chomp Rock Zone: Red Coins", player), lambda state: state.has_all({"Large Spring Ball", "Chomp Rock"}, player))
    set_rule(world.multiworld.get_location("Chomp Rock Zone: Flowers", player), lambda state: state.has_all({"Chomp Rock", "! Switch", "Dashed Platform"}, player))
    set_rule(world.multiworld.get_location("Chomp Rock Zone: Stars", player), lambda state: state.has_all({"Chomp Rock", "! Switch", "Dashed Platform"}, player))

    set_rule(world.multiworld.get_location("Lake Shore Paradise: Red Coins", player), lambda state: state.has("Egg Plant", player) or logic.combat_item(state))
    set_rule(world.multiworld.get_location("Lake Shore Paradise: Flowers", player), lambda state: state.has("Egg Plant", player) or logic.combat_item(state))
    set_rule(world.multiworld.get_location("Lake Shore Paradise: Stars", player), lambda state: (logic.has_midring(state) or (state.has("Tulip", player) and logic.cansee_clouds(state))) and (state.has("Egg Plant", player) or logic.combat_item(state)))
    set_rule(world.multiworld.get_location("Lake Shore Paradise: Level Clear", player), lambda state: state.has("Egg Plant", player) or logic.combat_item(state))

    set_rule(world.multiworld.get_location("Ride Like The Wind: Red Coins", player), lambda state: state.has("Large Spring Ball", player))
    set_rule(world.multiworld.get_location("Ride Like The Wind: Flowers", player), lambda state: state.has("Large Spring Ball", player))
    set_rule(world.multiworld.get_location("Ride Like The Wind: Stars", player), lambda state: (logic.has_midring(state) or state.has("Helicopter Morph", player)) and state.has("Large Spring Ball", player))
    set_rule(world.multiworld.get_location("Ride Like The Wind: Level Clear", player), lambda state: state.has("Large Spring Ball", player))

    set_rule(world.multiworld.get_location("Hookbill The Koopa's Castle: Red Coins", player), lambda state: state.has_all({"Dashed Stairs", "Vanishing Arrow Wheel", "Key"}, player))
    set_rule(world.multiworld.get_location("Hookbill The Koopa's Castle: Flowers", player), lambda state: state.has_all({"Dashed Stairs", "Vanishing Arrow Wheel", "Key"}, player))
    set_rule(world.multiworld.get_location("Hookbill The Koopa's Castle: Stars", player), lambda state: logic.has_midring(state) or (state.has_any({"Dashed Stairs", "Vanishing Arrow Wheel"}, player)))

    set_rule(world.multiworld.get_location("BLIZZARD!!!: Red Coins", player), lambda state: state.has_any({"Dashed Stairs", "Ice Melon"}, player) and (state.has("Egg Capacity Upgrade", player, 1) or logic.combat_item(state) or state.has("Helicopter Morph", player)))

    set_rule(world.multiworld.get_location("Danger - Icy Conditions Ahead: Red Coins", player), lambda state: (state.has("Fire Melon", player) or logic.melon_item(state)) and (state.has_all({"Spring Ball", "Skis"}, player))  and (state.has("Super Star", player) or logic.melon_item(state)))
    set_rule(world.multiworld.get_location("Danger - Icy Conditions Ahead: Flowers", player), lambda state: (state.has("Fire Melon", player) or logic.melon_item(state)) and state.has_all({"Spring Ball", "Skis"}, player))
    set_rule(world.multiworld.get_location("Danger - Icy Conditions Ahead: Stars", player), lambda state: (logic.has_midring(state) and (state.has("Fire Melon", player) or logic.melon_item(state))) or (logic.has_midring(state) and (state.has_all({"Tulip", "Dashed Platform"}, player))))
    set_rule(world.multiworld.get_location("Danger - Icy Conditions Ahead: Level Clear", player), lambda state: state.has_all({"Spring Ball", "Skis"}, player))

    set_rule(world.multiworld.get_location("Sluggy The Unshaven's Fort: Red Coins", player), lambda state: state.has_all({"Dashed Stairs", "Dashed Platform", "Platform Ghost"}, player))
    set_rule(world.multiworld.get_location("Sluggy The Unshaven's Fort: Flowers", player), lambda state: state.has_all({"Dashed Stairs", "Platform Ghost", "Dashed Platform"}, player))
    set_rule(world.multiworld.get_location("Sluggy The Unshaven's Fort: Stars", player), lambda state: ((state.has_all({"Dashed Stairs", "Platform Ghost"}, player))) or (logic.cansee_clouds(state) and state.has("Dashed Stairs", player)))

    set_rule(world.multiworld.get_location("Goonie Rides!: Red Coins", player), lambda state: state.has("Helicopter Morph", player))
    set_rule(world.multiworld.get_location("Goonie Rides!: Flowers", player), lambda state: state.has_all({"Helicopter Morph", "! Switch"}, player))

    set_rule(world.multiworld.get_location("Shifting Platforms Ahead: Stars", player), lambda state: logic.has_midring(state))

    set_rule(world.multiworld.get_location("Raphael The Raven's Castle: Red Coins", player), lambda state: state.has_all({"Arrow Wheel", "Train Morph"}, player))
    set_rule(world.multiworld.get_location("Raphael The Raven's Castle: Flowers", player), lambda state: state.has_all({"Arrow Wheel", "Train Morph"}, player))
    set_rule(world.multiworld.get_location("Raphael The Raven's Castle: Stars", player), lambda state: logic.has_midring(state))

    set_rule(world.multiworld.get_location("Scary Skeleton Goonies!: Red Coins", player), lambda state: state.has("Large Spring Ball", player))
    set_rule(world.multiworld.get_location("Scary Skeleton Goonies!: Flowers", player), lambda state: state.has("Large Spring Ball", player))
    set_rule(world.multiworld.get_location("Scary Skeleton Goonies!: Stars", player), lambda state: logic.has_midring(state))
    set_rule(world.multiworld.get_location("Scary Skeleton Goonies!: Level Clear", player), lambda state: state.has("Large Spring Ball", player))

    set_rule(world.multiworld.get_location("The Cave Of The Bandits: Red Coins", player), lambda state: state.has("Super Star", player))
    set_rule(world.multiworld.get_location("The Cave Of The Bandits: Flowers", player), lambda state: state.has("Super Star", player))
    set_rule(world.multiworld.get_location("The Cave Of The Bandits: Level Clear", player), lambda state: state.has("Super Star", player))

    set_rule(world.multiworld.get_location("Tap-Tap The Red Nose's Fort: Red Coins", player), lambda state: state.has_all({"Large Spring Ball", "Egg Plant", "Key"}, player) and (state.has("Egg Capacity Upgrade", player, 2) or logic.combat_item(state)))
    set_rule(world.multiworld.get_location("Tap-Tap The Red Nose's Fort: Flowers", player), lambda state: state.has_all({"Large Spring Ball", "Egg Plant", "Key"}, player) and (state.has("Egg Capacity Upgrade", player, 2) or logic.combat_item(state)))
    set_rule(world.multiworld.get_location("Tap-Tap The Red Nose's Fort: Stars", player), lambda state: logic.has_midring(state) and state.has_all({"Spring Ball", "Egg Plant", "Key"}, player))

    set_rule(world.multiworld.get_location("The Very Loooooong Cave: Red Coins", player), lambda state: state.has("Chomp Rock", player) and (state.has("Egg Capacity Upgrade", player, 2) or logic.combat_item(state)))
    set_rule(world.multiworld.get_location("The Very Loooooong Cave: Flowers", player), lambda state: state.has("Chomp Rock", player) and (state.has("Egg Capacity Upgrade", player, 2) or logic.combat_item(state)))
    set_rule(world.multiworld.get_location("The Very Loooooong Cave: Stars", player), lambda state: state.has("Chomp Rock", player) and (state.has("Egg Capacity Upgrade", player, 2) or logic.combat_item(state)) and logic.has_midring(state))

    set_rule(world.multiworld.get_location("The Deep, Underground Maze: Red Coins", player), lambda state: state.has_all({"Chomp Rock", "Key", "Large Spring Ball"}, player))
    set_rule(world.multiworld.get_location("The Deep, Underground Maze: Flowers", player), lambda state: state.has_all({"Chomp Rock", "Key", "Large Spring Ball"}, player))
    set_rule(world.multiworld.get_location("The Deep, Underground Maze: Stars", player), lambda state: state.has_all({"Chomp Rock", "Tulip", "Key"}, player) or (logic.has_midring(state) and state.has_all({"Key", "Chomp Rock", "Large Spring Ball"}, player)))
    set_rule(world.multiworld.get_location("The Deep, Underground Maze: Level Clear", player), lambda state: state.has_all({"Key", "Large Spring Ball", "Dashed Platform"}, player) and (logic.combat_item(state) or state.has("Chomp Rock", player)))

    set_rule(world.multiworld.get_location("KEEP MOVING!!!!: Stars", player), lambda state: logic.has_midring(state))

    set_rule(world.multiworld.get_location("King Bowser's Castle: Red Coins", player), lambda state: state.has_all({"Helicopter Morph", "Egg Plant"}, player) and logic._68CollectibleRoute(state))
    set_rule(world.multiworld.get_location("King Bowser's Castle: Flowers", player), lambda state: state.has_all({"Helicopter Morph", "Egg Plant"}, player) and logic._68CollectibleRoute(state))
    set_rule(world.multiworld.get_location("King Bowser's Castle: Stars", player), lambda state: state.has_all({"Helicopter Morph", "Egg Plant"}, player) and logic._68Route(state))

    set_normal_extra_rules(world)


def set_normal_extra_rules(world: "YoshisIslandWorld") -> None:
    player = world.player
    logic = YoshiLogic(world)
    if not world.options.extras_enabled:
        return

    set_rule(world.multiworld.get_location("Poochy Ain't Stupid: Red Coins", player), lambda state: state.has("Poochy", player))
    set_rule(world.multiworld.get_location("Poochy Ain't Stupid: Flowers", player), lambda state: state.has("Poochy", player))
    set_rule(world.multiworld.get_location("Poochy Ain't Stupid: Stars", player), lambda state: state.has("Poochy", player))
    set_rule(world.multiworld.get_location("Poochy Ain't Stupid: Level Clear", player), lambda state: state.has("Poochy", player))

    set_rule(world.multiworld.get_location("Hit That Switch!!: Red Coins", player), lambda state: state.has_all({"Large Spring Ball", "! Switch"}, player))
    set_rule(world.multiworld.get_location("Hit That Switch!!: Flowers", player), lambda state: state.has_all({"Large Spring Ball", "! Switch"}, player))
    set_rule(world.multiworld.get_location("Hit That Switch!!: Level Clear", player), lambda state: state.has_all({"Large Spring Ball", "! Switch"}, player))

    set_rule(world.multiworld.get_location("The Impossible? Maze: Red Coins", player), lambda state: state.has_all({"Spring Ball", "Large Spring Ball", "Mole Tank Morph", "Helicopter Morph", "Flashing Eggs"}, player))
    set_rule(world.multiworld.get_location("The Impossible? Maze: Flowers", player), lambda state: state.has_all({"Spring Ball", "Large Spring Ball", "Mole Tank Morph", "Helicopter Morph"}, player))
    set_rule(world.multiworld.get_location("The Impossible? Maze: Stars", player), lambda state: state.has_all({"Spring Ball", "Large Spring Ball", "Mole Tank Morph"}, player))
    set_rule(world.multiworld.get_location("The Impossible? Maze: Level Clear", player), lambda state: state.has_all({"Spring Ball", "Large Spring Ball", "Mole Tank Morph", "Helicopter Morph"}, player))

    set_rule(world.multiworld.get_location("Kamek's Revenge: Red Coins", player), lambda state: state.has_all({"Key", "Skis", "Helicopter Morph", "! Switch"}, player) and logic.has_midring(state))
    set_rule(world.multiworld.get_location("Kamek's Revenge: Flowers", player), lambda state: state.has_all({"Key", "Skis", "Helicopter Morph", "! Switch"}, player) and logic.has_midring(state))
    set_rule(world.multiworld.get_location("Kamek's Revenge: Stars", player), lambda state: state.has("! Switch", player) or logic.has_midring(state))
    set_rule(world.multiworld.get_location("Kamek's Revenge: Level Clear", player), lambda state: state.has_all({"Key", "Skis", "Helicopter Morph"}, player))

    set_rule(world.multiworld.get_location("Castles - Masterpiece Set: Red Coins", player), lambda state: (state.has("Egg Capacity Upgrade", player, 1) or logic.combat_item(state)) and state.has(("Large Spring Ball"), player))
    set_rule(world.multiworld.get_location("Castles - Masterpiece Set: Flowers", player), lambda state: (state.has("Egg Capacity Upgrade", player, 1) or logic.combat_item(state)) and state.has(("Large Spring Ball"), player))
    set_rule(world.multiworld.get_location("Castles - Masterpiece Set: Stars", player), lambda state: logic.has_midring(state) or state.has(("Large Spring Ball"), player))
    set_rule(world.multiworld.get_location("Castles - Masterpiece Set: Level Clear", player), lambda state: (state.has("Egg Capacity Upgrade", player, 1) or logic.combat_item(state)) and state.has(("Large Spring Ball"), player))


def set_hard_rules(world: "YoshisIslandWorld"):
    logic = YoshiLogic(world)
    player = world.player

    set_rule(world.multiworld.get_location("Burt The Bashful's Fort: Red Coins", player), lambda state: state.has("Spring Ball", player))
    set_rule(world.multiworld.get_location("Burt The Bashful's Fort: Flowers", player), lambda state: state.has_all({"Spring Ball", "Key"}, player) and (state.has("Egg Capacity Upgrade", player, 3) or logic.combat_item(state)))
    set_rule(world.multiworld.get_location("Burt The Bashful's Fort: Stars", player), lambda state: state.has("Spring Ball", player))

    set_rule(world.multiworld.get_location("Shy-Guys On Stilts: Red Coins", player), lambda state: state.has_all({"Large Spring Ball", "Flashing Eggs", "Mole Tank Morph", "! Switch"}, player))
    set_rule(world.multiworld.get_location("Shy-Guys On Stilts: Level Clear", player), lambda state: state.has("Large Spring Ball", player))

    set_rule(world.multiworld.get_location("Touch Fuzzy Get Dizzy: Red Coins", player), lambda state: state.has_all({"Flashing Eggs", "Spring Ball", "Chomp Rock", "Beanstalk"}, player))

    set_rule(world.multiworld.get_location("Salvo The Slime's Castle: Red Coins", player), lambda state: state.has("Platform Ghost", player))
    set_rule(world.multiworld.get_location("Salvo The Slime's Castle: Flowers", player), lambda state: state.has("Platform Ghost", player))

    set_rule(world.multiworld.get_location("Visit Koopa And Para-Koopa: Red Coins", player), lambda state: state.has("Large Spring Ball", player) and (state.has("Poochy", player) or logic.melon_item(state)))
    set_rule(world.multiworld.get_location("Visit Koopa And Para-Koopa: Flowers", player), lambda state: state.has_all({"Super Star", "Large Spring Ball"}, player))
    set_rule(world.multiworld.get_location("Visit Koopa And Para-Koopa: Stars", player), lambda state: state.has("Large Spring Ball", player))
    set_rule(world.multiworld.get_location("Visit Koopa And Para-Koopa: Level Clear", player), lambda state: state.has("Large Spring Ball", player))

    set_rule(world.multiworld.get_location("The Baseball Boys: Red Coins", player), lambda state: state.has("Mole Tank Morph", player) and (state.has_any({"Ice Melon", "Large Spring Ball"}, player) or logic.melon_item(state)))
    set_rule(world.multiworld.get_location("The Baseball Boys: Flowers", player), lambda state: (state.has_any({"Ice Melon", "Large Spring Ball"}, player) or logic.melon_item(state)))
    set_rule(world.multiworld.get_location("The Baseball Boys: Level Clear", player), lambda state: (state.has_any({"Ice Melon", "Large Spring Ball"}, player) or logic.melon_item(state)))

    set_rule(world.multiworld.get_location("What's Gusty Taste Like?: Red Coins", player), lambda state: state.has("! Switch", player))

    set_rule(world.multiworld.get_location("Bigger Boo's Fort: Red Coins", player), lambda state: state.has_all({"! Switch", "Key"}, player))
    set_rule(world.multiworld.get_location("Bigger Boo's Fort: Flowers", player), lambda state: state.has_all({"! Switch", "Key"}, player))
    set_rule(world.multiworld.get_location("Bigger Boo's Fort: Stars", player), lambda state: state.has("! Switch", player))

    set_rule(world.multiworld.get_location("Watch Out For Lakitu: Flowers", player), lambda state: state.has_all({"Key", "Train Morph"}, player))

    set_rule(world.multiworld.get_location("The Cave Of The Mystery Maze: Red Coins", player), lambda state: state.has("Large Spring Ball", player))
    set_rule(world.multiworld.get_location("The Cave Of The Mystery Maze: Flowers", player), lambda state: state.has("Large Spring Ball", player))
    set_rule(world.multiworld.get_location("The Cave Of The Mystery Maze: Level Clear", player), lambda state: state.has("Large Spring Ball", player))

    set_rule(world.multiworld.get_location("Lakitu's Wall: Flowers", player), lambda state: state.has("! Switch", player))
    set_rule(world.multiworld.get_location("Lakitu's Wall: Stars", player), lambda state: state.has("Giant Eggs", player) or logic.has_midring(state))

    set_rule(world.multiworld.get_location("The Potted Ghost's Castle: Red Coins", player), lambda state: state.has_all({"Arrow Wheel", "Key"}, player))
    set_rule(world.multiworld.get_location("The Potted Ghost's Castle: Flowers", player), lambda state: state.has_all({"Arrow Wheel", "Key", "Train Morph"}, player))
    set_rule(world.multiworld.get_location("The Potted Ghost's Castle: Stars", player), lambda state: state.has("Arrow Wheel", player))

    set_rule(world.multiworld.get_location("Welcome To Monkey World!: Stars", player), lambda state: logic.has_midring(state))

    set_rule(world.multiworld.get_location("Jungle Rhythm...: Red Coins", player), lambda state: state.has("Dashed Stairs", player))
    set_rule(world.multiworld.get_location("Jungle Rhythm...: Flowers", player), lambda state: state.has("Dashed Stairs", player))
    set_rule(world.multiworld.get_location("Jungle Rhythm...: Stars", player), lambda state: logic.has_midring(state) and state.has("Tulip", player))
    set_rule(world.multiworld.get_location("Jungle Rhythm...: Level Clear", player), lambda state: state.has("Dashed Stairs", player))

    set_rule(world.multiworld.get_location("Nep-Enuts' Domain: Red Coins", player), lambda state: state.has_all({"Submarine Morph", "Helicopter Morph"}, player))
    set_rule(world.multiworld.get_location("Nep-Enuts' Domain: Flowers", player), lambda state: state.has_all({"Submarine Morph", "Helicopter Morph"}, player))
    set_rule(world.multiworld.get_location("Nep-Enuts' Domain: Level Clear", player), lambda state: state.has_all({"Submarine Morph", "Helicopter Morph"}, player))

    set_rule(world.multiworld.get_location("Prince Froggy's Fort: Red Coins", player), lambda state: state.has("Submarine Morph", player))
    set_rule(world.multiworld.get_location("Prince Froggy's Fort: Flowers", player), lambda state: (state.has("Egg Capacity Upgrade", player, 5) or logic.combat_item(state)))

    set_rule(world.multiworld.get_location("The Cave Of Harry Hedgehog: Red Coins", player), lambda state: state.has("Mole Tank Morph", player))
    set_rule(world.multiworld.get_location("The Cave Of Harry Hedgehog: Flowers", player), lambda state: state.has_all({"Mole Tank Morph", "! Switch"}, player))
    set_rule(world.multiworld.get_location("The Cave Of Harry Hedgehog: Stars", player), lambda state: logic.has_midring(state) or state.has("Tulip", player))
    set_rule(world.multiworld.get_location("The Cave Of Harry Hedgehog: Level Clear", player), lambda state: state.has_all({"Large Spring Ball", "Key"}, player))

    set_rule(world.multiworld.get_location("Monkeys' Favorite Lake: Red Coins", player), lambda state: state.has_all({"! Switch", "Submarine Morph"}, player))

    set_rule(world.multiworld.get_location("GO! GO! MARIO!!: Red Coins", player), lambda state: state.has("Super Star", player))
    set_rule(world.multiworld.get_location("GO! GO! MARIO!!: Flowers", player), lambda state: state.has("Super Star", player))
    set_rule(world.multiworld.get_location("GO! GO! MARIO!!: Level Clear", player), lambda state: state.has("Super Star", player))

    set_rule(world.multiworld.get_location("The Cave Of The Lakitus: Red Coins", player), lambda state: state.has_all({"! Switch", "Egg Launcher"}, player))
    set_rule(world.multiworld.get_location("The Cave Of The Lakitus: Flowers", player), lambda state: state.has("Egg Launcher", player))

    set_rule(world.multiworld.get_location("Don't Look Back!: Red Coins", player), lambda state: state.has_all({"Helicopter Morph", "Large Spring Ball"}, player))
    set_rule(world.multiworld.get_location("Don't Look Back!: Flowers", player), lambda state: state.has("Large Spring Ball", player))
    set_rule(world.multiworld.get_location("Don't Look Back!: Stars", player), lambda state: logic.has_midring(state) or state.has("Tulip", player))

    set_rule(world.multiworld.get_location("Marching Milde's Fort: Red Coins", player), lambda state: state.has_all({"Dashed Stairs", "Vanishing Arrow Wheel", "Arrow Wheel", "Bucket", "Key"}, player))
    set_rule(world.multiworld.get_location("Marching Milde's Fort: Flowers", player), lambda state: state.has_all({"Dashed Stairs", "Vanishing Arrow Wheel", "Arrow Wheel", "Bucket"}, player))
    set_rule(world.multiworld.get_location("Marching Milde's Fort: Stars", player), lambda state: state.has("Dashed Stairs", player))

    set_rule(world.multiworld.get_location("Chomp Rock Zone: Red Coins", player), lambda state: state.has("Large Spring Ball", player))
    set_rule(world.multiworld.get_location("Chomp Rock Zone: Flowers", player), lambda state: state.has_all({"Chomp Rock", "! Switch"}, player))
    set_rule(world.multiworld.get_location("Chomp Rock Zone: Stars", player), lambda state: state.has_all({"Chomp Rock", "! Switch"}, player))

    set_rule(world.multiworld.get_location("Lake Shore Paradise: Stars", player), lambda state: (logic.has_midring(state) or (state.has("Tulip", player) and logic.cansee_clouds(state))))

    set_rule(world.multiworld.get_location("Ride Like The Wind: Red Coins", player), lambda state: state.has("Large Spring Ball", player))
    set_rule(world.multiworld.get_location("Ride Like The Wind: Flowers", player), lambda state: state.has("Large Spring Ball", player))
    set_rule(world.multiworld.get_location("Ride Like The Wind: Stars", player), lambda state: (logic.has_midring(state) or state.has("Helicopter Morph", player)) and state.has("Large Spring Ball", player))
    set_rule(world.multiworld.get_location("Ride Like The Wind: Level Clear", player), lambda state: state.has("Large Spring Ball", player))

    set_rule(world.multiworld.get_location("Hookbill The Koopa's Castle: Red Coins", player), lambda state: state.has_all({"Key", "Dashed Stairs"}, player))
    set_rule(world.multiworld.get_location("Hookbill The Koopa's Castle: Flowers", player), lambda state: state.has_all({"Dashed Stairs", "Key"}, player))

    set_rule(world.multiworld.get_location("Danger - Icy Conditions Ahead: Red Coins", player), lambda state: (state.has("Fire Melon", player) or logic.melon_item(state)) and (state.has_all({"Spring Ball", "Skis"}, player))  and (state.has("Super Star", player) or logic.melon_item(state)))
    set_rule(world.multiworld.get_location("Danger - Icy Conditions Ahead: Flowers", player), lambda state: (state.has("Fire Melon", player) or logic.melon_item(state)) and state.has_all({"Spring Ball", "Skis"}, player))
    set_rule(world.multiworld.get_location("Danger - Icy Conditions Ahead: Stars", player), lambda state: (logic.has_midring(state) and (state.has("Fire Melon", player) or logic.melon_item(state))) or (logic.has_midring(state) and (state.has_all({"Tulip", "Dashed Platform"}, player))))
    set_rule(world.multiworld.get_location("Danger - Icy Conditions Ahead: Level Clear", player), lambda state: state.has_all({"Spring Ball", "Skis"}, player))

    set_rule(world.multiworld.get_location("Sluggy The Unshaven's Fort: Red Coins", player), lambda state: state.has_all({"Dashed Stairs", "Dashed Platform", "Platform Ghost"}, player))
    set_rule(world.multiworld.get_location("Sluggy The Unshaven's Fort: Flowers", player), lambda state: state.has_all({"Dashed Stairs", "Platform Ghost"}, player))

    set_rule(world.multiworld.get_location("Shifting Platforms Ahead: Stars", player), lambda state: logic.has_midring(state))

    set_rule(world.multiworld.get_location("Raphael The Raven's Castle: Red Coins", player), lambda state: state.has_all({"Arrow Wheel", "Train Morph"}, player))
    set_rule(world.multiworld.get_location("Raphael The Raven's Castle: Flowers", player), lambda state: state.has_all({"Arrow Wheel", "Train Morph"}, player))

    set_rule(world.multiworld.get_location("Scary Skeleton Goonies!: Red Coins", player), lambda state: state.has("Large Spring Ball", player))
    set_rule(world.multiworld.get_location("Scary Skeleton Goonies!: Flowers", player), lambda state: state.has("Large Spring Ball", player))
    set_rule(world.multiworld.get_location("Scary Skeleton Goonies!: Stars", player), lambda state: logic.has_midring(state))
    set_rule(world.multiworld.get_location("Scary Skeleton Goonies!: Level Clear", player), lambda state: state.has("Large Spring Ball", player))

    set_rule(world.multiworld.get_location("The Cave Of The Bandits: Red Coins", player), lambda state: state.has("Super Star", player))
    set_rule(world.multiworld.get_location("The Cave Of The Bandits: Flowers", player), lambda state: state.has("Super Star", player))
    set_rule(world.multiworld.get_location("The Cave Of The Bandits: Level Clear", player), lambda state: state.has("Super Star", player))

    set_rule(world.multiworld.get_location("Tap-Tap The Red Nose's Fort: Red Coins", player), lambda state: state.has_all({"Egg Plant", "Key"}, player) and (state.has("Egg Capacity Upgrade", player, 1) or logic.combat_item(state)))
    set_rule(world.multiworld.get_location("Tap-Tap The Red Nose's Fort: Flowers", player), lambda state: state.has_all({"Egg Plant", "Key"}, player) and (state.has("Egg Capacity Upgrade", player, 1) or logic.combat_item(state)))
    set_rule(world.multiworld.get_location("Tap-Tap The Red Nose's Fort: Stars", player), lambda state: state.has("Egg Plant", player) and state.has("Key", player))

    set_rule(world.multiworld.get_location("The Very Loooooong Cave: Stars", player), lambda state: logic.has_midring(state))

    set_rule(world.multiworld.get_location("The Deep, Underground Maze: Red Coins", player), lambda state: state.has_all({"Key", "Large Spring Ball"}, player) and (logic.combat_item(state) or state.has("Chomp Rock", player)))
    set_rule(world.multiworld.get_location("The Deep, Underground Maze: Flowers", player), lambda state: state.has_all({"Key", "Large Spring Ball"}, player) and (logic.combat_item(state) or state.has("Chomp Rock", player)))
    set_rule(world.multiworld.get_location("The Deep, Underground Maze: Stars", player), lambda state: state.has_all({"Chomp Rock", "Key"}, player))
    set_rule(world.multiworld.get_location("The Deep, Underground Maze: Level Clear", player), lambda state: state.has_all({"Key", "Large Spring Ball", "Dashed Platform"}, player) and (logic.combat_item(state) or state.has("Chomp Rock", player)))

    set_rule(world.multiworld.get_location("KEEP MOVING!!!!: Stars", player), lambda state: logic.has_midring(state))

    set_rule(world.multiworld.get_location("King Bowser's Castle: Red Coins", player), lambda state: state.has("Helicopter Morph", player) and logic._68CollectibleRoute(state))
    set_rule(world.multiworld.get_location("King Bowser's Castle: Flowers", player), lambda state: state.has("Helicopter Morph", player) and logic._68CollectibleRoute(state))
    set_rule(world.multiworld.get_location("King Bowser's Castle: Stars", player), lambda state: state.has("Helicopter Morph", player) and logic._68Route(state))

    set_hard_extra_rules(world)


def set_hard_extra_rules(world: "YoshisIslandWorld") -> None:
    player = world.player
    logic = YoshiLogic(world)
    if not world.options.extras_enabled:
        return
    set_rule(world.multiworld.get_location("Poochy Ain't Stupid: Red Coins", player), lambda state: state.has("Poochy", player))
    set_rule(world.multiworld.get_location("Poochy Ain't Stupid: Flowers", player), lambda state: state.has("Poochy", player))
    set_rule(world.multiworld.get_location("Poochy Ain't Stupid: Stars", player), lambda state: state.has("Poochy", player))
    set_rule(world.multiworld.get_location("Poochy Ain't Stupid: Level Clear", player), lambda state: state.has("Poochy", player))

    set_rule(world.multiworld.get_location("Hit That Switch!!: Red Coins", player), lambda state: state.has_all({"Large Spring Ball", "! Switch"}, player))
    set_rule(world.multiworld.get_location("Hit That Switch!!: Flowers", player), lambda state: state.has_all({"Large Spring Ball", "! Switch"}, player))
    set_rule(world.multiworld.get_location("Hit That Switch!!: Level Clear", player), lambda state: state.has_all({"Large Spring Ball", "! Switch"}, player))

    set_rule(world.multiworld.get_location("The Impossible? Maze: Red Coins", player), lambda state: state.has_all({"Spring Ball", "Large Spring Ball", "Mole Tank Morph", "Helicopter Morph", "Flashing Eggs"}, player))
    set_rule(world.multiworld.get_location("The Impossible? Maze: Flowers", player), lambda state: state.has_all({"Spring Ball", "Large Spring Ball", "Mole Tank Morph", "Helicopter Morph"}, player))
    set_rule(world.multiworld.get_location("The Impossible? Maze: Stars", player), lambda state: state.has_all({"Spring Ball", "Large Spring Ball", "Mole Tank Morph"}, player))
    set_rule(world.multiworld.get_location("The Impossible? Maze: Level Clear", player), lambda state: state.has_all({"Spring Ball", "Large Spring Ball", "Mole Tank Morph", "Helicopter Morph"}, player))

    set_rule(world.multiworld.get_location("Kamek's Revenge: Red Coins", player), lambda state: state.has_all({"Key", "Skis", "Helicopter Morph"}, player))
    set_rule(world.multiworld.get_location("Kamek's Revenge: Flowers", player), lambda state: state.has_all({"Key", "Skis", "Helicopter Morph", "! Switch"}, player))
    set_rule(world.multiworld.get_location("Kamek's Revenge: Stars", player), lambda state: state.has("! Switch", player) or logic.has_midring(state))
    set_rule(world.multiworld.get_location("Kamek's Revenge: Level Clear", player), lambda state: state.has_all({"Key", "Skis", "Helicopter Morph"}, player))

    set_rule(world.multiworld.get_location("Castles - Masterpiece Set: Red Coins", player), lambda state: state.has(("Large Spring Ball"), player))
    set_rule(world.multiworld.get_location("Castles - Masterpiece Set: Flowers", player), lambda state: state.has(("Large Spring Ball"), player))
    set_rule(world.multiworld.get_location("Castles - Masterpiece Set: Stars", player), lambda state: True)
    set_rule(world.multiworld.get_location("Castles - Masterpiece Set: Level Clear", player), lambda state: state.has(("Large Spring Ball"), player))
