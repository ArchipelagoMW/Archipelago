from typing import List, Tuple, Optional, Callable, NamedTuple
from BaseClasses import MultiWorld
from .Options import is_option_enabled, get_option_value

EventId: Optional[int] = None


class LocationData(NamedTuple):
    region: str
    name: str
    code: Optional[int]
    rule: Callable = lambda state: True


def get_locations(world: Optional[MultiWorld], player: Optional[int]) -> Tuple[LocationData, ...]:

    location_table: List[LocationData] = [
        
        #world 1 starts here
        LocationData('Make Eggs, Throw Eggs', 'Make Eggs, Throw Eggs: Red Coins', 160001, lambda state: state.has('Dashed Stairs', player) and state.has('Beanstalk', player)),
        LocationData('Make Eggs, Throw Eggs', 'Make Eggs, Throw Eggs: Flowers', 160002, 
                        lambda state: state.logic_normal(world, player) or 
                                      state.logic_easy(world, player) and state.has('Dashed Stairs', player) and state.has('Beanstalk', player)),
        LocationData('Make Eggs, Throw Eggs', 'Make Eggs, Throw Eggs: Stars', 160003, lambda state: state.has('Dashed Stairs', player) and state.has('Beanstalk', player) and state.has('Tulip', player)),
        LocationData('Make Eggs, Throw Eggs', 'Make Eggs, Throw Eggs: Level Clear', 160004, lambda state: state.has('Beanstalk', player)),

        LocationData('Watch Out Below!', 'Watch Out Below!: Red Coins', 160005, lambda state: state.has('Large Spring Ball', player)),
        LocationData('Watch Out Below!', 'Watch Out Below!: Flowers', 160006, lambda state: state.has('Large Spring Ball', player) and state.has('Helicopter', player)),
        LocationData('Watch Out Below!', 'Watch Out Below!: Stars', 160007, lambda state: state.has('Large Spring Ball', player) and state.has('Middle Ring', player)),
        LocationData('Watch Out Below!', 'Watch Out Below!: Level Clear', 160008, lambda state: state.has('Large Spring Ball', player)),

        LocationData('The Cave Of Chomp Rock', 'The Cave of Chomp Rock: Red Coins', 160009),
        LocationData('The Cave Of Chomp Rock', 'The Cave of Chomp Rock: Flowers', 160010),
        LocationData('The Cave Of Chomp Rock', 'The Cave of Chomp Rock: Stars', 160011, lambda state: state.has('Middle Ring', player)),
        LocationData('The Cave Of Chomp Rock', 'The Cave of Chomp Rock: Level Clear', 160012),

        LocationData("Burt The Bashful's Fort", "Burt The Bashful's Fort: Red Coins", 160013, lambda state: state.has('Spring Ball', player)),
        LocationData("Burt The Bashful's Fort", "Burt The Bashful's Fort: Flowers", 160014, lambda state: state.has('Spring Ball', player) and state.world_1_keys and state.has('Egg Capacity Upgrade', player, 3)),
        LocationData("Burt The Bashful's Fort", "Burt The Bashful's Fort: Stars", 160015, lambda state: state.has('Spring Ball', player)),
        LocationData("Burt The Bashful's Fort", "Burt The Bashful's Fort: Level Clear", 160016, lambda state: state.has('Spring Ball', player) and state.world_1_keys and state.has('Egg Plant', player)),
        LocationData("Burt The Bashful's Fort", "Burt The Bashful Defeated", EventId),

        LocationData("Hop! Hop! Donut Lifts", "Hop! Hop! Donut Lifts: Red Coins", 160018),
        LocationData("Hop! Hop! Donut Lifts", "Hop! Hop! Donut Lifts: Flowers", 160019),
        LocationData("Hop! Hop! Donut Lifts", "Hop! Hop! Donut Lifts: Stars", 160020, lambda state: state.has('Middle Ring', player)),
        LocationData("Hop! Hop! Donut Lifts", "Hop! Hop! Donut Lifts: Level Clear", 160021),

        LocationData("Shy-Guys On Stilts", "Shy-Guys On Stilts: Red Coins", 160022, lambda state: state.has('Large Spring Ball', player) and state.has('Spring Ball', player) and state.has('! Switch', player) and state.has('Flashing Eggs', player) and state.has('Mole Tank', player)),
        LocationData("Shy-Guys On Stilts", "Shy-Guys On Stilts: Flowers", 160023, lambda state: state.has('Spring Ball', player)),
        LocationData("Shy-Guys On Stilts", "Shy-Guys On Stilts: Stars", 160024, lambda state: state.has('Large Spring Ball', player) and state.has('Large Spring Ball', player) and state.lots_of_stars),
        LocationData("Shy-Guys On Stilts", "Shy-Guys On Stilts: Level Clear", 160025, lambda state: state.has('Spring Ball', player) and state.has('Large Spring Ball', player)),

        LocationData("Touch Fuzzy Get Dizzy", "Touch Fuzzy Get Dizzy: Red Coins", 160026, lambda state: state.has('Flashing Eggs', player) and state.has('Spring Ball', player) and state.has('Beanstalk', player) and state.has('Chomp Rock', player)),
        LocationData("Touch Fuzzy Get Dizzy", "Touch Fuzzy Get Dizzy: Flowers", 160027),
        LocationData("Touch Fuzzy Get Dizzy", "Touch Fuzzy Get Dizzy: Stars", 160028, lambda state: state.has('Middle Ring', player)),
        LocationData("Touch Fuzzy Get Dizzy", "Touch Fuzzy Get Dizzy: Level Clear", 160029),

        LocationData("Salvo The Slime's Castle", "Salvo The Slime's Castle: Red Coins", 160030, lambda state: state.has('Platform Ghost', player)),
        LocationData("Salvo The Slime's Castle", "Salvo The Slime's Castle: Flowers", 160031, lambda state: state.has('Platform Ghost', player)),
        LocationData("Salvo The Slime's Castle", "Salvo The Slime's Castle: Stars", 160032, lambda state: state.has('Platform Ghost', player) and state.has('Middle Ring', player)),
        LocationData("Salvo The Slime's Castle", "Salvo The Slime's Castle: Level Clear", 160033, lambda state: state.world_1_keys and state.has('Arrow Wheel', player)),
        LocationData("Salvo The Slime's Castle", "Salvo The Slime Defeated", EventId, lambda state: state.world_1_keys and state.has('Arrow Wheel', player)),


        #world 2 starts here
        LocationData("Visit Koopa And Para-Koopa", "Visit Koopa And Para-Koopa: Red Coins", 160035, lambda state: state.has('Poochy', player) and state.has('Spring Ball', player) and state.has('Large Spring Ball', player)),
        LocationData("Visit Koopa And Para-Koopa", "Visit Koopa And Para-Koopa: Flowers", 160036, lambda state: state.has('Super Star', player) and state.has('Large Spring Ball', player)),
        LocationData("Visit Koopa And Para-Koopa", "Visit Koopa And Para-Koopa: Stars", 160037, lambda state: state.has('Middle Ring', player) and state.has('Large Spring Ball', player)),
        LocationData("Visit Koopa And Para-Koopa", "Visit Koopa And Para-Koopa: Level Clear", 160038, lambda state: state.has('Large Spring Ball', player)),

        LocationData("The Baseball Boys", "The Baseball Boys: Red Coins", 160039, lambda state: state.has('Large Spring Ball', player) and state.has('Super Star', player) and state.has('Beanstalk', player)),
        LocationData("The Baseball Boys", "The Baseball Boys: Flowers", 160040, lambda state: state.has('Large Spring Ball', player) and state.has('Super Star', player) and state.has('Beanstalk', player)),
        LocationData("The Baseball Boys", "The Baseball Boys: Stars", 160041, lambda state: state.has('Large Spring Ball', player) and state.has('Super Star', player) and state.lots_of_stars),
        LocationData("The Baseball Boys", "The Baseball Boys: Level Clear", 160042, lambda state: state.has('Large Spring Ball', player) and state.has('Super Star', player) and state.has('Beanstalk', player)),

        LocationData("What's Gusty Taste Like?", "What's Gusty Taste Like?: Red Coins", 160043, lambda state: state.has('! Switch', player)),
        LocationData("What's Gusty Taste Like?", "What's Gusty Taste Like?: Flowers", 160044),
        LocationData("What's Gusty Taste Like?", "What's Gusty Taste Like?: Stars", 160045),
        LocationData("What's Gusty Taste Like?", "What's Gusty Taste Like?: Level Clear", 160046),

        LocationData("Bigger Boo's Fort", "Bigger Boo's Fort: Red Coins", 160047, lambda state: state.has('! Switch', player) and state.world_2_keys and state.has('Dashed Stairs', player)),
        LocationData("Bigger Boo's Fort", "Bigger Boo's Fort: Flowers", 160048, lambda state: state.has('! Switch', player) and state.world_2_keys and state.has('Dashed Stairs', player)),
        LocationData("Bigger Boo's Fort", "Bigger Boo's Fort: Stars", 160049, lambda state: state.has('! Switch', player) and state.has('Dashed Stairs', player) and (state.has('Middle Ring', player) or state.has('Key', player))),
        LocationData("Bigger Boo's Fort", "Bigger Boo's Fort: Level Clear", 160050, lambda state: state.has('! Switch', player) and state.has('Dashed Stairs', player)),
        LocationData("Bigger Boo's Fort", "Bigger Boo Defeated", EventId),

        LocationData("Watch Out For Lakitu", "Watch Out For Lakitu: Red Coins", 160052),
        LocationData("Watch Out For Lakitu", "Watch Out For Lakitu: Flowers", 160053, lambda state: state.world_2_keys and state.has('Train', player)),
        LocationData("Watch Out For Lakitu", "Watch Out For Lakitu: Stars", 160054),
        LocationData("Watch Out For Lakitu", "Watch Out For Lakitu: Level Clear", 160055),

        LocationData("The Cave Of The Mystery Maze", "The Cave Of The Mystery Maze: Red Coins", 160056, lambda state: state.has('Large Spring Ball', player)),
        LocationData("The Cave Of The Mystery Maze", "The Cave Of The Mystery Maze: Flowers", 160057, lambda state: state.has('Large Spring Ball', player) and state.has('Egg Launcher', player)),
        LocationData("The Cave Of The Mystery Maze", "The Cave Of The Mystery Maze: Stars", 160058, lambda state: (state.has('Large Spring Ball', player) or state.has('Middle Ring', player))),
        LocationData("The Cave Of The Mystery Maze", "The Cave Of The Mystery Maze: Level Clear", 160059, lambda state: state.has('Large Spring Ball', player)),

        LocationData("Lakitu's Wall", "Lakitu's Wall: Red Coins", 160060, lambda state: state.has('Large Spring Ball', player) and (state.has('Dashed Platform', player) or state.has('Giant Eggs', player))),
        LocationData("Lakitu's Wall", "Lakitu's Wall: Flowers", 160061, lambda state: state.has('Large Spring Ball', player) and state.has('! Switch', player)),
        LocationData("Lakitu's Wall", "Lakitu's Wall: Stars", 160062, lambda state: state.has('Giant Eggs', player) or (state.has('Middle Ring', player) or state.has('Tulip', player))),
        LocationData("Lakitu's Wall", "Lakitu's Wall: Level Clear", 160063, lambda state: state.has('Large Spring Ball', player)),

        LocationData("The Potted Ghost's Castle", "The Potted Ghost's Castle: Red Coins", 160064, lambda state: state.has('Arrow Wheel', player) and state.world_2_keys),
        LocationData("The Potted Ghost's Castle", "The Potted Ghost's Castle: Flowers", 160065, lambda state: state.has('Arrow Wheel', player) and state.has('Train', player) and state.world_2_keys),
        LocationData("The Potted Ghost's Castle", "The Potted Ghost's Castle: Stars", 160066, lambda state: state.has('Arrow Wheel', player) and state.world_2_keys and state.has('Middle Ring', player)),
        LocationData("The Potted Ghost's Castle", "The Potted Ghost's Castle: Level Clear", 160067, lambda state: state.has('Arrow Wheel', player) and state.world_2_keys),
        LocationData("The Potted Ghost's Castle", "Roger the Ghost Defeated", EventId),


        #world 3 starts here
        LocationData("Welcome To Monkey World!", "Welcome To Monkey World!: Red Coins", 160069),
        LocationData("Welcome To Monkey World!", "Welcome To Monkey World!: Flowers", 160070),
        LocationData("Welcome To Monkey World!", "Welcome To Monkey World!: Stars", 160071, lambda state: state.has('Middle Ring', player)),
        LocationData("Welcome To Monkey World!", "Welcome To Monkey World!: Level Clear", 160072),

        LocationData("Jungle Rhythm...", "Jungle Rhythm...: Red Coins", 160073, lambda state: state.has('Dashed Stairs', player) and state.has('Spring Ball', player)),
        LocationData("Jungle Rhythm...", "Jungle Rhythm...: Flowers", 160074, lambda state: state.has('Dashed Stairs', player) and state.has('Spring Ball', player)),
        LocationData("Jungle Rhythm...", "Jungle Rhythm...: Stars", 160075, lambda state: state.has('Middle Ring', player) and state.has('Tulip', player)),
        LocationData("Jungle Rhythm...", "Jungle Rhythm...: Level Clear", 160076, lambda state: state.has('Dashed Stairs', player) and state.has('Spring Ball', player)),

        LocationData("Nep-Enuts' Domain", "Nep-Enuts' Domain: Red Coins", 160077, lambda state: state.has('Helicopter', player) and state.has('Submarine', player)),
        LocationData("Nep-Enuts' Domain", "Nep-Enuts' Domain: Flowers", 160078, lambda state: state.has('Helicopter', player) and state.has('Submarine', player)),
        LocationData("Nep-Enuts' Domain", "Nep-Enuts' Domain: Stars", 160079),
        LocationData("Nep-Enuts' Domain", "Nep-Enuts' Domain: Level Clear", 160080, lambda state: state.has('Helicopter', player) and state.has('Submarine', player)),

        LocationData("Prince Froggy's Fort", "Prince Froggy's Fort: Red Coins", 160081, lambda state: state.has('Submarine', player)),
        LocationData("Prince Froggy's Fort", "Prince Froggy's Fort: Flowers", 160082, lambda state: state.has('Egg Capacity Upgrade', player, 5) and state.has('Dashed Platform', player)),
        LocationData("Prince Froggy's Fort", "Prince Froggy's Fort: Stars", 160083, lambda state: (state.has('Dashed Platform', player) or state.has('Middle Ring', player))),
        LocationData("Prince Froggy's Fort", "Prince Froggy's Fort: Level Clear", 160084, lambda state: state.has('Dashed Platform', player) and state.has('Giant Eggs', player)),
        LocationData("Prince Froggy's Fort", "Prince Froggy Defeated", EventId),

        LocationData("Jammin' Through The Trees", "Jammin' Through The Trees: Red Coins", 160086),
        LocationData("Jammin' Through The Trees", "Jammin' Through The Trees: Flowers", 160087, lambda state: state.has('Watermelons', player)),
        LocationData("Jammin' Through The Trees", "Jammin' Through The Trees: Stars", 160088),
        LocationData("Jammin' Through The Trees", "Jammin' Through The Trees: Level Clear", 160089),
        
        LocationData("The Cave Of Harry Hedgehog", "The Cave Of Harry Hedgehog: Red Coins", 160090, lambda state: (state.has('Beanstalk', player) or state.has('Dashed Stairs', player)) and state.has('Mole Tank', player) and state.has('Large Spring Ball', player)),
        LocationData("The Cave Of Harry Hedgehog", "The Cave Of Harry Hedgehog: Flowers", 160091, lambda state: (state.has('Beanstalk', player) or state.has('Dashed Stairs', player)) and state.has('Mole Tank', player) and state.has('Large Spring Ball', player) and state.has('! Switch', player)),
        LocationData("The Cave Of Harry Hedgehog", "The Cave Of Harry Hedgehog: Stars", 160092, lambda state: (state.has('Tulip', player) or state.has('Middle Ring', player)) and (state.has('Dashed Stairs', player) or state.has('Beanstalk', player)) and state.has('Mole Tank', player) and state.has('Large Spring Ball', player)),
        LocationData("The Cave Of Harry Hedgehog", "The Cave Of Harry Hedgehog: Level Clear", 160093, lambda state: state.has('Large Spring Ball', player) and state.world_3_keys),

        LocationData("Monkeys' Favorite Lake", "Monkeys' Favorite Lake: Red Coins", 160094, lambda state: state.has('! Switch', player) and state.has('Submarine', player) and state.has('Beanstalk', player)),
        LocationData("Monkeys' Favorite Lake", "Monkeys' Favorite Lake: Flowers", 160095, lambda state: state.has('Beanstalk', player)),
        LocationData("Monkeys' Favorite Lake", "Monkeys' Favorite Lake: Stars", 160096),
        LocationData("Monkeys' Favorite Lake", "Monkeys' Favorite Lake: Level Clear", 160097),

        LocationData("Naval Piranha's Castle", "Naval Piranha's Castle: Red Coins", 160098, lambda state: state.has('Egg Capacity Upgrade', player, 2)),
        LocationData("Naval Piranha's Castle", "Naval Piranha's Castle: Flowers", 160099, lambda state: state.has('Egg Capacity Upgrade', player, 2)),
        LocationData("Naval Piranha's Castle", "Naval Piranha's Castle: Stars", 160100, lambda state: state.has('Egg Capacity Upgrade', player, 2) and state.has('Middle Ring', player) and state.has('Tulip', player)),
        LocationData("Naval Piranha's Castle", "Naval Piranha's Castle: Level Clear", 160101, lambda state: state.has('Egg Capacity Upgrade', player, 2)),
        LocationData("Naval Piranha's Castle", "Naval Piranha Defeated", EventId),


        #world 4 starts here
        LocationData("GO! GO! MARIO!!", "GO! GO! MARIO!!: Red Coins", 160103, lambda state: state.has('Super Star', player)),
        LocationData("GO! GO! MARIO!!", "GO! GO! MARIO!!: Flowers", 160104, lambda state: state.has('Super Star', player)),
        LocationData("GO! GO! MARIO!!", "GO! GO! MARIO!!: Stars", 160105, lambda state: (state.has('Middle Ring', player) or state.has('Tulip', player))),
        LocationData("GO! GO! MARIO!!", "GO! GO! MARIO!!: Level Clear", 160106, lambda state: state.has('Super Star', player)),

        LocationData("The Cave Of The Lakitus", "The Cave Of The Lakitus: Red Coins", 160107, lambda state: state.has('Large Spring Ball', player) and state.has('! Switch', player) and state.has('Egg Launcher', player)),
        LocationData("The Cave Of The Lakitus", "The Cave Of The Lakitus: Flowers", 160108, lambda state: state.has('Large Spring Ball', player) and state.has('Egg Launcher', player)),
        LocationData("The Cave Of The Lakitus", "The Cave Of The Lakitus: Stars", 160109, lambda state: state.has('Large Spring Ball', player)),
        LocationData("The Cave Of The Lakitus", "The Cave Of The Lakitus: Level Clear", 160110, lambda state: state.has('Large Spring Ball', player)),

        LocationData("Don't Look Back!", "Don't Look Back!: Red Coins", 160111, lambda state: state.has('Helicopter', player) and state.has('! Switch', player) and state.has('Large Spring Ball', player)),
        LocationData("Don't Look Back!", "Don't Look Back!: Flowers", 160112, lambda state: state.has('! Switch', player) and state.has('Large Spring Ball', player)),
        LocationData("Don't Look Back!", "Don't Look Back!: Stars", 160113, lambda state: state.has('! Switch', player) and state.has('Middle Ring', player)),
        LocationData("Don't Look Back!", "Don't Look Back!: Level Clear", 160114, lambda state: state.has('! Switch', player)),

        LocationData("Marching Milde's Fort", "Marching Milde's Fort: Red Coins", 160115, lambda state: state.has('Dashed Stairs', player) and state.has('Arrow Wheel', player) and state.has('Vanishing Arrow Wheel', player) and state.has('Bucket', player) and state.has('Key', player)),
        LocationData("Marching Milde's Fort", "Marching Milde's Fort: Flowers", 160116, lambda state: state.has('Dashed Stairs', player) and state.has('Arrow Wheel', player) and state.has('Vanishing Arrow Wheel', player) and state.has('Bucket', player)),
        LocationData("Marching Milde's Fort", "Marching Milde's Fort: Stars", 160117, lambda state: state.has('Dashed Stairs', player)),
        LocationData("Marching Milde's Fort", "Marching Milde's Fort: Level Clear", 160118, lambda state: state.has('Dashed Stairs', player) and state.has('Arrow Wheel', player) and state.has('Vanishing Arrow Wheel', player) and state.has('Bucket', player) and state.has('Key', player)),
        LocationData("Marching Milde's Fort", "Marching Milde Defeated", EventId),

        LocationData("Chomp Rock Zone", "Chomp Rock Zone: Red Coins", 160120, lambda state: state.has('Large Spring Ball', player)),
        LocationData("Chomp Rock Zone", "Chomp Rock Zone: Flowers", 160121, lambda state: state.has('Chomp Rock', player) and state.has('! Switch', player) and state.has('Dashed Platform', player)),
        LocationData("Chomp Rock Zone", "Chomp Rock Zone: Stars", 160122, lambda state: state.has('Chomp Rock', player) and state.has('Middle Ring', player)),
        LocationData("Chomp Rock Zone", "Chomp Rock Zone: Level Clear", 160123),

        LocationData("Lake Shore Paradise", "Lake Shore Paradise: Red Coins", 160124, lambda state: state.has('Egg Plant', player)),
        LocationData("Lake Shore Paradise", "Lake Shore Paradise: Flowers", 160125, lambda state: state.has('Egg Plant', player)),
        LocationData("Lake Shore Paradise", "Lake Shore Paradise: Stars", 160126, lambda state: state.has('Egg Plant', player) and (state.has('Middle Ring', player) or state.has('Tulip', player))),
        LocationData("Lake Shore Paradise", "Lake Shore Paradise: Level Clear", 160127, lambda state: state.has('Egg Plant', player)),

        LocationData("Ride Like The Wind", "Ride Like The Wind: Red Coins", 160128, lambda state: state.has('Large Spring Ball', player)),
        LocationData("Ride Like The Wind", "Ride Like The Wind: Flowers", 160129, lambda state: state.has('Large Spring Ball', player)),
        LocationData("Ride Like The Wind", "Ride Like The Wind: Stars", 160130, lambda state: state.has('Large Spring Ball', player) and (state.has('Middle Ring', player) or state.has('Helicopter', player))),
        LocationData("Ride Like The Wind", "Ride Like The Wind: Level Clear", 160131, lambda state: state.has('Large Spring Ball', player)),

        LocationData("Hookbill The Koopa's Castle", "Hookbill The Koopa's Castle: Red Coins", 160132, lambda state: state.has('Dashed Stairs', player) and state.has('Vanishing Arrow Wheel', player) and state.has('Key', player)),
        LocationData("Hookbill The Koopa's Castle", "Hookbill The Koopa's Castle: Flowers", 160133, lambda state: state.has('Dashed Stairs', player) and state.has('Vanishing Arrow Wheel', player) and state.has('Key', player)),
        LocationData("Hookbill The Koopa's Castle", "Hookbill The Koopa's Castle: Stars", 160134, lambda state: state.has('Middle Ring', player) and (state.has('Dashed Stairs', player) or state.has('Vanishing Arrow Wheel', player))),
        LocationData("Hookbill The Koopa's Castle", "Hookbill The Koopa's Castle: Level Clear", 160135, lambda state: state.has('Vanishing Arrow Wheel', player) and state.has('Key', player) and state.has('Large Spring Ball', player) and state.has('Egg Capacity Upgrade', player, 2)),
        LocationData("Hookbill The Koopa's Castle", "Hookbill The Koopa Defeated", EventId),


        #world 5 starts here
        LocationData("BLIZZARD!!!", "BLIZZARD!!!: Red Coins", 160137, lambda state: state.has('Helicopter', player) and (state.has('Dashed Stairs', player) or state.has('Ice Melons', player))),
        LocationData("BLIZZARD!!!", "BLIZZARD!!!: Flowers", 160138),
        LocationData("BLIZZARD!!!", "BLIZZARD!!!: Stars", 160139),
        LocationData("BLIZZARD!!!", "BLIZZARD!!!: Level Clear", 160140),

        LocationData("Ride The Ski Lifts", "Ride The Ski Lifts: Red Coins", 160141),
        LocationData("Ride The Ski Lifts", "Ride The Ski Lifts: Flowers", 160142),
        LocationData("Ride The Ski Lifts", "Ride The Ski Lifts: Stars", 160143),
        LocationData("Ride The Ski Lifts", "Ride The Ski Lifts: Level Clear", 160144),

        LocationData("Danger - Icy Conditions Ahead", "Danger - Icy Conditions Ahead: Red Coins", 160145, lambda state: state.can_melt_ice(world, player) and state.has('Spring Ball', player) and state.has('Super Star', player) and state.has('Skis', player) and state.has('Bucket', player)),
        LocationData("Danger - Icy Conditions Ahead", "Danger - Icy Conditions Ahead: Flowers", 160146, lambda state: state.can_melt_ice(world, player) and state.has('Spring Ball', player) and state.has('Skis', player)),
        LocationData("Danger - Icy Conditions Ahead", "Danger - Icy Conditions Ahead: Stars", 160147, lambda state: ((state.has('Middle Ring', player) and state.can_melt_ice(world, player)) or (state.has('Middle Ring', player) and state.has('Tulip', player) and state.has('Super Star', player) and state.has('Dashed Platform', player)) or (state.has('Middle Ring', player) and state.has('Tulip', player) and state.has('Dashed Platform', player) and state.can_melt_ice(world, player))) and state.has('Spring Ball', player)),
        LocationData("Danger - Icy Conditions Ahead", "Danger - Icy Conditions Ahead: Level Clear", 160148, lambda state: state.has('Spring Ball', player) and state.has('Skis', player)),

        LocationData("Sluggy The Unshaven's Fort", "Sluggy The Unshaven's Fort: Red Coins", 160149, lambda state: state.has('Dashed Stairs', player) and state.has('Dashed Platform', player) and state.has('Platform Ghost', player)),
        LocationData("Sluggy The Unshaven's Fort", "Sluggy The Unshaven's Fort: Flowers", 160150, lambda state: state.has('Dashed Stairs', player) and state.has('Dashed Platform', player) and state.has('Platform Ghost', player)),
        LocationData("Sluggy The Unshaven's Fort", "Sluggy The Unshaven's Fort: Stars", 160151, lambda state: state.has('Dashed Stairs', player) and state.has('Dashed Platform', player)),
        LocationData("Sluggy The Unshaven's Fort", "Sluggy The Unshaven's Fort: Level Clear", 160152, lambda state: state.has('Dashed Stairs', player) and state.has('Dashed Platform', player) and (state.has('Egg Plant', player) and state.has('Egg Capacity Upgrade', player, 2) or state.has('Egg Capacity Upgrade', player, 3) and state.has('Middle Ring', player))),
        LocationData("Sluggy The Unshaven's Fort", "Sluggy The Unshaven Defeated", EventId),

        LocationData("Goonie Rides!", "Goonie Rides!: Red Coins", 160154),
        LocationData("Goonie Rides!", "Goonie Rides!: Flowers", 160155, lambda state: state.has('Helicopter', player)),
        LocationData("Goonie Rides!", "Goonie Rides!: Stars", 160156),
        LocationData("Goonie Rides!", "Goonie Rides!: Level Clear", 160157),

        LocationData("Welcome To Cloud World", "Welcome To Cloud World: Red Coins", 160158),
        LocationData("Welcome To Cloud World", "Welcome To Cloud World: Flowers", 160159),
        LocationData("Welcome To Cloud World", "Welcome To Cloud World: Stars", 160160),
        LocationData("Welcome To Cloud World", "Welcome To Cloud World: Level Clear", 160161),

        LocationData("Shifting Platforms Ahead", "Shifting Platforms Ahead: Red Coins", 160162, lambda state: state.has('Egg Capacity Upgrade', player, 1)),
        LocationData("Shifting Platforms Ahead", "Shifting Platforms Ahead: Flowers", 160163, lambda state: state.has('Egg Capacity Upgrade', player, 1)),
        LocationData("Shifting Platforms Ahead", "Shifting Platforms Ahead: Stars", 160164, lambda state: state.has('Middle Ring', player)),
        LocationData("Shifting Platforms Ahead", "Shifting Platforms Ahead: Level Clear", 160165),

        LocationData("Raphael The Raven's Castle", "Raphael The Raven's Castle: Red Coins", 160166, lambda state: state.has('Arrow Wheel', player) and state.has('Train', player)),
        LocationData("Raphael The Raven's Castle", "Raphael The Raven's Castle: Flowers", 160167, lambda state: state.has('Arrow Wheel', player) and state.has('Train', player)),
        LocationData("Raphael The Raven's Castle", "Raphael The Raven's Castle: Stars", 160168, lambda state: state.has('Arrow Wheel', player) and state.has('Middle Ring', player)),
        LocationData("Raphael The Raven's Castle", "Raphael The Raven's Castle: Level Clear", 160169, lambda state: state.has('Arrow Wheel', player) and state.has('Large Spring Ball', player)),
        LocationData("Raphael The Raven's Castle", "Raphael The Raven Defeated", EventId),


        #world 6 starts here
        LocationData("Scary Skeleton Goonies!", "Scary Skeleton Goonies!: Red Coins", 160171, lambda state: state.has('Large Spring Ball', player)),
        LocationData("Scary Skeleton Goonies!", "Scary Skeleton Goonies!: Flowers", 160172, lambda state: state.has('Large Spring Ball', player)),
        LocationData("Scary Skeleton Goonies!", "Scary Skeleton Goonies!: Stars", 160173, lambda state: (state.has('Middle  Ring', player) or state.has('Dashed Platform', player))),
        LocationData("Scary Skeleton Goonies!", "Scary Skeleton Goonies!: Level Clear", 160174, lambda state: state.has('Large Spring Ball', player)),

        LocationData("The Cave Of The Bandits", "The Cave Of The Bandits: Red Coins", 160175, lambda state: state.has('Super Star', player)),
        LocationData("The Cave Of The Bandits", "The Cave Of The Bandits: Flowers", 160176, lambda state: state.has('Super Star', player)),
        LocationData("The Cave Of The Bandits", "The Cave Of The Bandits: Stars", 160177),
        LocationData("The Cave Of The Bandits", "The Cave Of The Bandits: Level Clear", 160178, lambda state: state.has('Super Star', player)),

        LocationData("Beware The Spinning Logs", "Beware The Spinning Logs: Red Coins", 160179, lambda state: state.has('Spring Ball', player)),
        LocationData("Beware The Spinning Logs", "Beware The Spinning Logs: Flowers", 160180),
        LocationData("Beware The Spinning Logs", "Beware The Spinning Logs: Stars", 160181),
        LocationData("Beware The Spinning Logs", "Beware The Spinning Logs: Level Clear", 160182),

        LocationData("Tap-Tap The Red Nose's Fort", "Tap-Tap The Red Nose's Fort: Red Coins", 160183, lambda state: state.has('Spring Ball', player) and state.has('Large Spring Ball', player) and state.has('Egg Plant', player) and state.has('Egg Capacity Upgrade', player, 2) and state.has('Key', player)),
        LocationData("Tap-Tap The Red Nose's Fort", "Tap-Tap The Red Nose's Fort: Flowers", 160184, lambda state: state.has('Spring Ball', player) and state.has('Large Spring Ball', player) and state.has('Egg Plant', player) and state.has('Egg Capacity Upgrade', player, 2) and state.has('Key', player)),
        LocationData("Tap-Tap The Red Nose's Fort", "Tap-Tap The Red Nose's Fort: Stars", 160185, lambda state: state.has('Spring Ball', player) and state.has('Large Spring Ball', player) and state.has('Key', player) and state.has('Egg Plant', player)),
        LocationData("Tap-Tap The Red Nose's Fort", "Tap-Tap The Red Nose's Fort: Level Clear", 160186, lambda state: state.has('Spring Ball', player) and state.has('Large Spring Ball', player) and state.has('Egg Plant', player) and state.has('Egg Capacity Upgrade', player, 2) and state.has('Key', player)),
        LocationData("Tap-Tap The Red Nose's Fort", "Tap-Tap The Red Nose Defeated", EventId),

        LocationData("The Very Loooooong Cave", "The Very Loooooong Cave: Red Coins", 160188, lambda state: state.has('Chomp Rock', player)),
        LocationData("The Very Loooooong Cave", "The Very Loooooong Cave: Flowers", 160189, lambda state: state.has('Chomp Rock', player)),
        LocationData("The Very Loooooong Cave", "The Very Loooooong Cave: Stars", 160190, lambda state: state.logic_normal and (state.has('Chomp Rock', player) and (state.has('Watermelons', player) or state.has('Egg Capacity Upgrade', player, 2)) or state.has('Middle Ring', player))),
        LocationData("The Very Loooooong Cave", "The Very Loooooong Cave: Level Clear", 160191),

        LocationData("The Deep, Underground Maze", "The Deep, Underground Maze: Red Coins", 160192, lambda state: state.has('Chomp Rock', player) and state.has('Key', player) and state.has('Large Spring Ball', player)),
        LocationData("The Deep, Underground Maze", "The Deep, Underground Maze: Flowers", 160193, lambda state: state.has('Chomp Rock', player) and state.has('Key', player) and state.has('Large Spring Ball', player)),
        LocationData("The Deep, Underground Maze", "The Deep, Underground Maze: Stars", 160194, lambda state: state.has('Chomp Rock', player) and (state.has('Tulip', player) or state.has('Middle Ring', player) and state.has('Large Spring Ball', player))),
        LocationData("The Deep, Underground Maze", "The Deep, Underground Maze: Level Clear", 160195, lambda state: state.has('Chomp Rock', player) and state.has('Key', player) and state.has('Large Spring Ball', player) and state.has('Dashed Platform', player)),

        LocationData("KEEP MOVING!!!!", "KEEP MOVING!!!!: Red Coins", 160196),
        LocationData("KEEP MOVING!!!!", "KEEP MOVING!!!!: Flowers", 160197, lambda state: state.has('Egg Plant', player)),
        LocationData("KEEP MOVING!!!!", "KEEP MOVING!!!!: Stars", 160198, lambda state: state.has('Middle Ring', player)),
        LocationData("KEEP MOVING!!!!", "KEEP MOVING!!!!: Level Clear", 160199),

        LocationData("King Bowser's Castle", "King Bowser's Castle: Red Coins", 160200, lambda state: state.castle_door(world, player) and state.has('Helicopter', player) and state.has('Egg Plant', player)),
        LocationData("King Bowser's Castle", "King Bowser's Castle: Flowers", 160201, lambda state: state.castle_door(world, player) and state.has('Helicopter', player) and state.has('Egg Plant', player)),
        LocationData("King Bowser's Castle", "King Bowser's Castle: Stars", 160202, lambda state: state.castle_door(world, player) and state.has('Helicopter', player) and state.has('Egg Plant', player) and state.has('Middle Ring', player)),
        LocationData("King Bowser's Castle", "Saved Baby Luigi", EventId, lambda state: state.castle_door(world, player) and state.has('Helicopter', player) and state.has('Egg Plant', player) and state.has('Giant Eggs', player))
    ]
    if not world or is_option_enabled(world, player, "extras_enabled"):
        location_table += ( 
            LocationData("Poochy Ain't Stupid", "Poochy Ain't Stupid: Red Coins", 160204, lambda state: state.has('Poochy', player)),
            LocationData("Poochy Ain't Stupid", "Poochy Ain't Stupid: Flowers", 160205, lambda state: state.has('Poochy', player)),
            LocationData("Poochy Ain't Stupid", "Poochy Ain't Stupid: Stars", 160206, lambda state: state.has('Poochy', player)),
            LocationData("Poochy Ain't Stupid", "Poochy Ain't Stupid: Level Clear", 160207, lambda state: state.has('Poochy', player)),

            LocationData("Hit That Switch!!", "Hit That Switch!!: Red Coins", 160208, lambda state: state.has('Large Spring Ball', player) and state.has('! Switch', player)),
            LocationData("Hit That Switch!!", "Hit That Switch!!: Flowers", 160209, lambda state: state.has('Large Spring Ball', player) and state.has('! Switch', player)),
            LocationData("Hit That Switch!!", "Hit That Switch!!: Stars", 160210),
            LocationData("Hit That Switch!!", "Hit That Switch!!: Level Clear", 160211, lambda state: state.has('Large Spring Ball', player) and state.has('! Switch', player)),

            LocationData("More Monkey Madness", "More Monkey Madness: Red Coins", 160212),
            LocationData("More Monkey Madness", "More Monkey Madness: Flowers", 160213),
            LocationData("More Monkey Madness", "More Monkey Madness: Stars", 160214),
            LocationData("More Monkey Madness", "More Monkey Madness: Level Clear", 160215),

            LocationData("The Impossible? Maze", "The Impossible? Maze: Red Coins", 160216, lambda state: state.has('Large Spring Ball', player) and state.has('Spring Ball', player) and state.has('Mole Tank', player) and state.has('Helicopter', player) and state.has('Flashing Eggs', player)),
            LocationData("The Impossible? Maze", "The Impossible? Maze: Flowers", 160217, lambda state: state.has('Large Spring Ball', player) and state.has('Spring Ball', player) and state.has('Mole Tank', player) and state.has('Helicopter', player)),
            LocationData("The Impossible? Maze", "The Impossible? Maze: Stars", 160218, lambda state: state.has('Large Spring Ball', player) and state.has('Spring Ball', player) and state.has('Mole Tank', player)),
            LocationData("The Impossible? Maze", "The Impossible? Maze: Level Clear", 160219, lambda state: state.has('Large Spring Ball', player) and state.has('Spring Ball', player) and state.has('Mole Tank', player) and state.has('Helicopter', player)),

            LocationData("Kamek's Revenge", "Kamek's Revenge: Red Coins", 160220, lambda state: state.has('Key', player) and state.has('Helicopter', player) and state.has('Skis', player) and state.has('! Switch', player)),
            LocationData("Kamek's Revenge", "Kamek's Revenge: Flowers", 160221, lambda state: state.has('Key', player) and state.has('Helicopter', player) and state.has('Skis', player)),
            LocationData("Kamek's Revenge", "Kamek's Revenge: Stars", 160222, lambda state: (state.has('Middle Ring', player) or state.has('! Switch', player))),
            LocationData("Kamek's Revenge", "Kamek's Revenge: Level Clear", 160223, lambda state: state.has('Key', player) and state.has('Skis', player) and state.has('Helicopter', player)),

            LocationData("Castles - Masterpiece Set", "Castles - Masterpiece Set: Red Coins", 160224, lambda state: state.has('Large Spring Ball', player)),
            LocationData("Castles - Masterpiece Set", "Castles - Masterpiece Set: Flowers", 160225, lambda state: state.has('Large Spring Ball', player) and state.has('Egg Capacity Upgrade', player, 2)),
            LocationData("Castles - Masterpiece Set", "Castles - Masterpiece Set: Stars", 160226, lambda state: state.has('Large Spring Ball', player)),
            LocationData("Castles - Masterpiece Set", "Castles - Masterpiece Set: Level Clear", 160227, lambda state: state.has('Large Spring Ball', player))
            
        )

    if not world or get_option_value(world, player, "minigames_enabled") == 1 or get_option_value(world, player, "minigames_enabled") == 3:
        location_table+= (
            LocationData("The Cave Of Chomp Rock", "The Cave Of Chomp Rock: Bandit Game", 160228),
            LocationData("Touch Fuzzy, Get Dizzy", "Touch Fuzzy, Get Dizzy: Bandit Game", 160229),
            LocationData("Visit Koopa And Para-Koopa", "Visit Koopa And Para-Koopa: Bandit Game", 160230),
            LocationData("What's Gusty Taste Like?", "What's Gusty Taste Like?: Bandit Game", 160231),
            LocationData("Lakitu's Wall", "Lakitu's Wall: Bandit Game", 160232),
            LocationData("Jungle Rhythm...", "Jungle Rhythm...: Bandit Game", 160233),
            LocationData("Monkeys' Favorite Lake", "Monkeys' Favorite Lake: Bandit Game", 160234),
            LocationData("The Cave Of The Lakitus", "The Cave Of The Lakitus: Bandit Game", 160235),
            LocationData("Lake Shore Paradise", "Lake Shore Paradise: Bandit Game", 160236),
            LocationData("Ride Like The Wind", "Ride Like The Wind: Bandit Game", 160237),
            LocationData("BLIZZARD!!!", "BLIZZARD!!!: Bandit Game", 160238),
            LocationData("Scary Skeleton Goonies!", "Scary Skeleton Goonies!: Bandit Game", 160239),
            LocationData("KEEP MOVING!!!!", "KEEP MOVING!!!!: Bandit Game", 160240)


        )

    if not world or get_option_value(world, player, "minigames_enabled") == 2 or get_option_value(world, player, "minigames_enabled") == 3:
        location_table+= (
            LocationData("Flip Cards", "Flip Cards Victory", 160241),
            LocationData("Scratch And Match", "Scratch Cards Victory", 160242),
            LocationData("Drawing Lots", "Drawing Lots Victory", 160243),
            LocationData("Match Cards", "Match Cards Victory", 160244),
            LocationData("Roulette", "Roulette Victory", 160245),
            LocationData("Slot Machine", "Slot Machine Victory", 160246)


        )

    if not world or get_option_value(world, player, "castle_open_condition") or get_option_value(world, player, "castle_clear_condition")== 2:
        location_table+= (
            LocationData("Salvo The Slime's Castle", "Salvo The Slime's Castle: Flag", 160247,  lambda state: state.world_1_keys(world, player) and state.has('Arrow Wheel', player)),
            LocationData("The Potted Ghost's Castle", "The Potted Ghost's Castle: Flag", 160248, lambda state: state.has('Arrow Wheel', player) and state.world_2_keys(world, player)),
            LocationData("Naval Piranha's Castle", "Naval Piranha's Castle: Flag", 160249, lambda state: state.has('Egg Capacity Upgrade', player, 2)),
            LocationData("Hookbill The Koopa's Castle", "Hookbill The Koopa's Castle: Flag", 160250, lambda state: state.has('Vanishing Arrow Wheel', player) and state.has('Key', player) and state.has('Large Spring Ball', player) and state.has('Egg Capacity Upgrade', player, 2)),
            LocationData("Raphael The Raven's Castle", "Raphael The Raven's Castle: Flag", 160251, lambda state: state.has('Arrow Wheel', player) and state.has('Large Spring Ball', player))


        )

        #Todo later: 1-Up CloudSanity?
        #Keysanity Keys?

    

    return tuple(location_table)