from .ItemPool import garibsanity_world_table, checkpoint_table, world_garib_table, level_event_table, decoupled_garib_table
from .Options import GaribSorting, GaribLogic

world_tables = {
    "Super Mario 64" : [
        "Power Star"
        ]
}

def select_trap_item_name(self, original_name : str) -> str:
    trap_roll = self.random.randint(0, 99)
    #Just give the actual item name 1 of 100 times
    if trap_roll == 0:
        return original_name
    #Give it a name based on the multiworlds connected 1/5th of the time
    if trap_roll > 80:
        multiworld_entries = []
        for world_name in list(self.multiworld.world_name_lookup.keys()):
            if world_name in world_tables:
                multiworld_entries.extend(world_tables[world_name])
        #If any of the games in this multiworld have a Glover connection, use one randomly
        if len(multiworld_entries) > 0:
            return self.random.choice(multiworld_entries)
    #Most of the time, just
    fake_name = self.random.choice(self.fake_item_names)
    
    #Word 'Garib' corruption
    if fake_name.count("Garib") > 0:
        #50/50 the name corrupts
        match self.random.randint(0, 11):
            case 0:
                fake_name.replace("Garib", "Garid")
            case 1:
                fake_name.replace("Garib", "Gerib")
            case 2:
                fake_name.replace("Garib", "Ganib")
            case 3:
                fake_name.replace("Garib", "Garip")
            case 4:
                fake_name.replace("Garib", "Carib")
            case 5:
                fake_name.replace("Garib", "Garlb")
    
    #Level prefix corruption
    if fake_name.startswith(tuple(self.world_prefixes)):
        #1 in every 20 of these has funny prefixes
        if self.random.randint(1, 20) == 20:
            level_swaps = [
            #Plumber
                "BoB",
            #The Blue Ninja
                "TBN",
            #Hill Zone
                "GHZ",
            #Glitter Gulch
                "GGM",
            #Burgered
                "BKd",
            #Wrong prefix
                "Alt",
                "Crm",
                "Prc",
                "Phc",
                "F0F",
                "Otm",
                ]
            fake_name = self.random.choice(level_swaps) + fake_name[3:]
    return fake_name

def create_trap_name_table(self) -> list[str]:
    trap_name_table = [
        #Fake balls
        "Basketball",
        "Snow Ball",
        "Tennis Ball",
        "Disco Ball",
        "Monkey Ball",
        "Golf Ball",
        "Dodgeball",
        "Soccer Ball",
        "Pebball",
        "Football",
        "Hockey Puck",
        "Master Ball",
        #Fake glover moves
        "Triple Jump",
        "Backflip",
        #Fake Tools
        "Golf Club",
        "Tennis Racket",
        "Curling Broom",
        "Shovel",
        "Lawnmower",
        "Bus",
        "Magic Wand",
        #Fake ball moves
        "Spin Ball",
        "Flick Ball",
        "Juggle",
        #Funny
        "Cross-Stitch",
        "Free Wizard",
        "Permission to Cheat",
        "Running Boots",
        "Trap (WOULD Be Funny)",
        #Fake potions
        "Awkward Potion",
        "Strength Potion",
        "Toad Potion",
        "Invisibility Potion",
        "Cauldron Potion",
        "Mana Potion",
        "Health Potion",
        "Potion Bottle",
        "Boornerang Ball Potion",
        #Lotions
        "Beachball Lotion",
        "Death Lotion",
        "Helicopter Lotion",
        "Frog Lotion",
        "Boomerang Ball Lotion",
        "Speed Lotion",
        "Sticky Lotion",
        "Hercules Lotion",
        #Fake Filler
        "Line",
        "Lice",
        "Lime",
        "Live",
        "Like",
        "Chicken Song",
        #Things you already have
        "Garib Counter",
        "Lives Display",
        "Roll Ball",
        "Drop Ball",
        "Ledge Sit",
        "Transform Ball",
        #Not Traps
        "Not a Frog Trap",
        "Not a Cursed Ball Trap",
        "Not an Instant Crystal Trap",
        "Not a Camera Rotate Trap",
        "Not a Tip Trap"
    ]
    
    #Fake goal items
    if self.options.victory_condition.value != 2:
        trap_name_table.append("Golden Garib")

    #Fake portal entries
    if self.options.portalsanity:
        for each_prefix in self.level_prefixes:
            trap_name_table.append(each_prefix + "H Exit Gate")
            trap_name_table.append(each_prefix + "H 1 Gate")
            trap_name_table.append(each_prefix + "H 4 Gate")
            trap_name_table.append(each_prefix + "H 2 Stars")
            trap_name_table.append(each_prefix + "H Secret Star")
            trap_name_table.append(each_prefix + "H Secret Gate")
        trap_name_table.extend([
            "Hubworld Tree Gate",
            "Hubworld Castle Cave Gate",
            "OtwH Final Boss Gate"
        ])
    
    #Fake level events
    if self.options.switches_checks:
        trap_name_table.extend([
            "Atl1 Raise Water",
            "Atl2 Free Mermaid",
            "Atl3 Yellow Submarine",
            "Crn1 Fireworks",
            "Crn2 Baseball Minigame",
            "Crn3 Ferris Wheel",
            "Prt1 Dirt Jar",
            "Prt2 Sink Ship",
            "Prt3 Release Kraken",
            "Pht1 Melt Ice",
            "Pht2 Erupt Volcano",
            "Pht3 Dino Wedding",
            "FoF1 Mr Bones",
            "FoF2 Green Castle",
            "FoF3 Drawbridge",
            "Otw1 Ancienter Aliens",
            "Otw2 Bomb",
            "Otw3 Second Magnet",
            "Training Wheel"
        ])
    else:
        trap_name_table.extend(level_event_table.keys())

    #Fake Checkpoints
    if not self.options.checkpoint_checks:
        trap_name_table.extend(checkpoint_table.keys())
    elif not self.options.spawning_checkpoint_randomizer:
        for each_prefix in self.level_prefixes:
            trap_name_table.extend([
                each_prefix + "1 Checkpoint 1",
                each_prefix + "2 Checkpoint 1",
                each_prefix + "3 Checkpoint 1"
            ])
    
    #Fake Garibs
    match self.options.garib_logic:
        #Garibs shouldn't be items at all, add ALL of them
        case GaribLogic.option_level_garibs:
            trap_name_table.extend(garibsanity_world_table.keys())
            trap_name_table.extend(world_garib_table.keys())
            trap_name_table.extend(decoupled_garib_table.keys())
        #Groups can show up, exclude those
        case GaribLogic.option_garib_groups:
            if self.options.garib_sorting != GaribSorting.option_by_level:
                #Anything but the world garib table
                trap_name_table.extend(garibsanity_world_table.keys())
                trap_name_table.extend(decoupled_garib_table.keys())
            else:
                #Anything but decoupled garibs
                trap_name_table.extend(garibsanity_world_table.keys())
                trap_name_table.extend(world_garib_table.keys())
        #Garibsanity exists, exclude singles
        case GaribLogic.option_garibsanity:
            if self.options.garib_sorting != GaribSorting.option_by_level:
                #Anything but the garibsanity world table
                trap_name_table.extend(decoupled_garib_table.keys())
                trap_name_table.extend(world_garib_table.keys())
            else:
                #Anything but a single decoupled garib
                trap_name_table.extend(garibsanity_world_table.keys())
                trap_name_table.extend(world_garib_table.keys())
                trap_name_table.extend(decoupled_garib_table.keys())
    #'Jump'
    if not self.options.randomize_jump:
        trap_name_table.append("Jump")
    else:
        trap_name_table.append("Lump")
    
    #Misnamed Balls
    not_spawning_balls = [
        "Rubber Ball",
        "Bowling Ball",
        "Ball Bearing",
        "Crystal",
        "Power Ball"]
    #Remove the default ball from the list of misnamed balls
    not_spawning_balls.remove(self.starting_ball)
    #Make it an item you can find though, spelled correctly
    trap_name_table.append(self.starting_ball)
    for other_balls in not_spawning_balls:
        trap_name_table.append(other_balls)
        #Ball Mispellings
        if other_balls.count("Ball") > 0:
            trap_name_table.append(other_balls.replace("Ball", "Bell"))
            trap_name_table.append(other_balls.replace("Ball", "Bill"))
            trap_name_table.append(other_balls.replace("Ball", "Bull"))
            trap_name_table.append(other_balls.replace("Ball", "").removeprefix(" ").removesuffix(" "))
        #Other Mispellings
        match other_balls:
            case "Rubber Ball":
                trap_name_table.extend([
                    "Robber Ball",
                    "Rudder Ball"
                    ])
            case "Bowling Ball":
                trap_name_table.extend([
                    "Bowling Pin",
                    "Bowing Ball"
                    ])
            case "Ball Bearing":
                trap_name_table.extend([
                    "Ball Baering",
                    "Ball Pearing"
                    ])
            case "Crystal":
                trap_name_table.extend([
                    "Crystal Ball",
                    "Christal",
                    "Krystal",
                    "Crystall",
                    "Cryztal",
                    "Crstal",
                    ])
            case "Power Ball":
                trap_name_table.extend([
                    "Powder Ball",
                    "Powerball"
                ])
    return trap_name_table