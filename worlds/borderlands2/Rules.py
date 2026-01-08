from worlds.generic.Rules import set_rule, add_rule

from . import Borderlands2World
from .Regions import region_data_table
from .Locations import Borderlands2Location
from .Items import Borderlands2Item
from BaseClasses import ItemClassification

# TODO record and calculate how much jump is required
locs_with_jump_required = [
    "Vending Tundra Farm: Guns",
    "Quest ThreeHornsValley: No Vacancy",
    "Vending ThreeHornsValley Motel: Guns",
    "Vending ThreeHornsValley Motel: Zed's Meds",
    "Vending ThreeHornsValley Motel: Ammo Dump",
    "Quest ThreeHornsValley: Neither Rain nor Sleet nor Skags",
    "Quest Dust: Too Close For Missiles",
    "Quest Tundra Express: The Pretty Good Train Robbery",
    "Quest Tundra Express: Mine, All Mine",
    "Quest Highlands: Hidden Journals",
    "Quest Fridge: Note for Self-Person",
    "Enemy BloodshotStronghold: Flinter",
    "Enemy TundraExpress: Prospector Zeke",
    "Enemy CausticCaverns: Badass Creeper",
    "Symbol SouthernShelfBay: Ice Flows Shipwreck",
    "Symbol SouthernShelf: Flynt's Ship",
    "Symbol SouthernShelf: Safehouse",
    "Symbol ThreeHornsDivide: Billboard",
    "Symbol Sanctuary: Rooftop",
    "Symbol Sanctuary: Parkour Door",
    "Symbol Southpaw: Parkour",
    "Symbol Southpaw: Engine",
    "Symbol ThreeHornsValley: Frostsprings Wall",
    "Symbol Dust: Moonshiner Lid",
    "Symbol Bloodshot: Switch Room",
    "Symbol Fridge: Secret Stash",
    "Symbol Fridge: Sheetmetal Roof",
    "Symbol ThousandCuts: No Man's Land Shack",
    "Symbol Lynchwood: Gunslinger Roof",
    "Symbol Lynchwood: Main Street",
    "Symbol Opportunity: Office Bridge",
    "Symbol BadassCrater: Billboard Lower",
    "Symbol HerosPass: Strut",
    "Chest EridiumBlight: Volcano Free Chest",
    "Chest EridiumBlight: Pipe Dreaming",
    "Chest VaultOfTheWarrior: Lava River Cave",
    "Chest BloodshotStronghold: Jail Cell",
    "Chest BloodshotStronghold: Flinter's Room",
    "Chest BloodshotRamparts: Car Junkyard Trunk",
    "Chest Fridge: Smashhead's Cave",
    "Chest AridNexusBoneyard: Eridium Pump Station 2",
    "Chest AridNexusBoneyard: Eridium Pump Station 3",
    "Chest FriendshipGulag: Gulag Awning",
    "Chest FrostburnCanyon: Incinerator Camp",
    "Chest WildlifePreserve: Observation Wing #1",
    "Chest WildlifePreserve: Mordy's Secrest Stash",
    "Chest TundraExpress: Mount Molehill Mine Top",
    "Chest LeviathansLair: Outer #5",
    "Chest LeviathansLair: Outer #1",
    "Chest LeviathansLair: Outer #6",
    "Chest LeviathansLair: Outer #4",
    "Chest LeviathansLair: Outer #3",
    "Chest LeviathansLair: Outer #7",
    "Chest LeviathansLair: Outer #2",
    "Chest LeviathansLair: Inner #1",
    "Chest LeviathansLair: Inner #2",
    "Chest LeviathansLair: Inner #3",
    "Chest LeviathansLair: Inner #4",
    "Chest LeviathansLair: Inner #5",
    "Chest LeviathansLair: Inner #6",
    "Chest Forge: Forge Parkour",
    "Chest SawtoothCauldron: Smoking Guano Grotto Platform",
    "Chest SawtoothCauldron: Cramfist's Foundry",
    "Chest SawtoothCauldron: Mortar's Elevator",
    "Chest Southpaw: After Oney",
    "Chest AridNexusBadlands: Hey! Over Here!",
    "Chest AridNexusBadlands: Fyrestone Motel Roof",
    "Chest BadassCrater: Crater Rim Parkour Hut",
    "Chest CandlerakksCrag: Lower Bluff",
    "Chest CandlerakksCrag: Tracking Area",
    "Chest CandlerakksCrag: Before Terminus",
    "Chest HatredsShadow: Birds Nest", # and sprint
    "Chest ImmortalWoods: Graveyard Pillar", # 630
    "Chest ImmortalWoods: Ruins Parkour", # and sprint
    "Chest WingedStorm: Chest #54",
    "Chest WingedStorm: Chest #55",
    "Chest MarcusMercenaryShop: Station Rooftop",
]

locs_with_crouch_required = [
    "Enemy HatredsShadow: Handsome Dragon",
    "Symbol Opportunity: Construction Site",
    "Chest SouthernShelf: Boom Bewm Elevator",
]

# TODO list for crouch

# TODO list for vehicle fire (mostly just challenges)

def try_add_rule(place, rule):
    if place is None:
        return
    try:
        add_rule(place, rule)
    except:
        print(f"failed setting rule at {place}")


def set_rules(world: Borderlands2World):

    # items must be classified as progression to use in rules here
    try_add_rule(world.try_get_entrance("WindshearWaste to SouthernShelf"),
        lambda state: state.has("Melee", world.player) and state.has("Common Pistol", world.player))
    #add_rule(world.multiworld.get
    # add_rule(world.multiworld.get_entrance("SouthernShelf to ThreeHornsDivide", world.player),
    #     lambda state: state.has("Common Pistol", world.player))
    # add_rule(world.multiworld.get_location("Enemy WindshearWaste: Knuckle Dragger", world.player),
    #     lambda state: state.has("Melee", world.player))

    if world.options.jump_checks.value > 0:
        # ensure you can at least jump a little before wildlife preserve
        # try_add_rule(world.try_get_entrance("Highlands to WildlifeExploitationPreserve"),
        #     lambda state: state.has("Progressive Jump", world.player))
        try_add_rule(world.try_get_entrance("HerosPass to VaultOfTheWarrior"),
            lambda state: state.has("Progressive Jump", world.player))
        try_add_rule(world.try_get_entrance("BadassCrater to TorgueArena"), # 490 jump_z required
            lambda state: state.has("Progressive Jump", world.player))
        try_add_rule(world.try_get_entrance("BloodshotRamparts to Oasis"),
                 lambda state: state.has("Progressive Jump", world.player))

        for loc in locs_with_jump_required:
            try_add_rule(world.try_get_location(loc),
                lambda state: state.has("Progressive Jump", world.player)
            )

    #need melee to break vines to Hector
    try_add_rule(world.try_get_entrance("Mt.ScarabResearchCenter to FFSBossFight"),
             lambda state: state.has("Melee", world.player))

    try_add_rule(world.try_get_entrance("CandlerakksCrag to Terminus"),
            lambda state: state.has("Crouch", world.player))
    # If you die to the dragon, you need to crouch under the gate
    try_add_rule(world.try_get_entrance("HatredsShadow to LairOfInfiniteAgony"),
             lambda state: state.has("Crouch", world.player))

    for loc in locs_with_crouch_required:
        try_add_rule(world.try_get_location(loc),
            lambda state: state.has("Crouch", world.player)
        )



    if world.options.entrance_locks.value == 0:
        # skip if no entrance locks
        return

    for name, region_data in region_data_table.items():
        region = world.multiworld.get_region(name, world.player)
        for c_region_name in region_data.connecting_regions:
            c_region_data = region_data_table[c_region_name]
            ent_name = f"{region.name} to {c_region_name}"
            t_item = c_region_data.travel_item_name
            if t_item and isinstance(t_item, str):
                try_add_rule(
                    world.try_get_entrance(ent_name),
                    lambda state, travel_item=t_item: state.has(travel_item, world.player)
                )
            elif t_item and isinstance(t_item, list):
                try_add_rule(
                    world.try_get_entrance(ent_name),
                    lambda state, travel_item=t_item: state.has_all(travel_item, world.player)
                )


