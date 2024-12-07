from BaseClasses import CollectionState
from worlds.generic.Rules import add_item_rule, add_rule


def have_light_source(state: CollectionState, player: int) -> bool:
    return state.has("Lantern", player) or (state.has("Stick", player) and state.has("Boots", player))


def have_bombs(state: CollectionState, player: int) -> bool:
    return state.has("Bombs", player)
    # or werewolf badge when badges are added


def have_all_orbs(state: CollectionState, player: int) -> bool:
    return state.count("Orb", player) >= 4


def have_all_bats(state: CollectionState, player: int) -> bool:
    return state.count("Bat Statue", player) >= 4


def have_all_vamps(state: CollectionState, player: int) -> bool:
    return state.count("Vampire Statue", player) >= 8


def have_special_weapon_damage(state: CollectionState, player: int) -> bool:
    return (
        state.has_any(("Bombs", "Shock Wand", "Cactus", "Boomerang", "Whoopee", "Hot Pants"), player)
    )


def have_special_weapon_bullet(state: CollectionState, player: int) -> bool:
    return (
        state.has_any(("Bombs", "Ice Spear", "Cactus", "Boomerang", "Whoopee", "Hot Pants"), player)
    )


# return true slingshot counts

def have_special_weapon_range_damage(state: CollectionState, player: int) -> bool:
    return (
        state.has_any(("Bombs", "Shock Wand", "Cactus", "Boomerang"), player)
    )
    # return true slingshot counts


def have_special_weapon_through_walls(state: CollectionState, player: int) -> bool:
    return (
        state.has_any(("Bombs", "Shock Wand", "Whoopee"), player)
        # state.has("Hot Pants")
    )


def can_cleanse_crypts(state: CollectionState, player: int) -> bool:
    return (have_light_source(state, player) and can_enter_zombiton(state, player) and have_special_weapon_range_damage(
        state, player))


# these will get removed in favor of region access reqs eventually
def can_enter_zombiton(state: CollectionState, player: int) -> bool:
    return state.has("Boots", player)


def can_enter_rocky_cliffs(state: CollectionState, player: int) -> bool:
    return state.has("Big Gem", player)


def can_enter_vampy(state: CollectionState, player: int) -> bool:
    return can_enter_rocky_cliffs(state, player) and have_light_source(state, player)


def can_enter_vampy_ii(state: CollectionState, player: int) -> bool:
    return can_enter_vampy(state, player) and state.has("Skull Key", player)


def can_enter_vampy_iii(state: CollectionState, player: int) -> bool:
    return can_enter_vampy_ii(state, player) and state.has("Bat Key", player)


def can_enter_vampy_iv(state: CollectionState, player: int) -> bool:
    return can_enter_vampy_iii(state, player) and state.has("Pumpkin Key", player)

def set_rules(multiworld, world, player):

    access_rules = {
        "Halloween Hill - Swamp Mud Path": lambda state: state.has("Boots", player),
        "Halloween Hill - Bog Beast Home": True,
        "Halloween Hill - Rocky Cliffs below Upper Caverns": lambda state: can_enter_rocky_cliffs(state, player),
        "Halloween Hill - Sapling Shrine": lambda state: state.has("Boots", player),
        "Halloween Hill - Terror Glade": True,
        "Halloween Hill - Rocky Cliffs Vine": lambda state: state.has("Fertilizer", player),
        "Halloween Hill - Rocky Cliffs Grand Pharoh": lambda state: can_enter_rocky_cliffs(state, player),
        "Halloween Hill - Rocky Cliffs Rock Corner": lambda state: can_enter_rocky_cliffs(state, player) and have_bombs(state, player),
        "Halloween Hill - Mushroom outside town": True,
        "Halloween Hill - North of UG Passage": True,
        "Halloween Hill - Top left mushroom spot": True,
        "Halloween Hill - NE of UG Passage": True,
        "Halloween Hill - East Woods": True,
        "Halloween Hill - Rocky Cliffs Ledge": lambda state: can_enter_rocky_cliffs(state, player),
        "Halloween Hill - Rocky Cliffs Peak": lambda state: can_enter_rocky_cliffs(state, player),
        "Halloween Hill - Cat Tree": True,
        "The Witch's Cabin - Bedroom": lambda state: have_light_source(state, player),
        "The Witch's Cabin - Backroom": True,
        "Bonita's Cabin - Barrel Maze": True,
        "The Bog Pit - Top Door": lambda state: state.has("Skull Key", player),
        "The Bog Pit - Post Room": True,
        "The Bog Pit - Window Drip": True,
        "The Bog Pit - Green room": True,
        "The Bog Pit - Arena": True,
        "The Bog Pit - Kill Wall": True,
        "Underground Tunnel - Swampdog Door": lambda state: state.has("Pumpkin Key", player),
        "Underground Tunnel - Scribble Wall": lambda state: have_special_weapon_bullet(state, player),
        "Underground Tunnel - Tiny Passage": True,
        "Underground Tunnel - fire frogs": True,
        "Underground Tunnel - Torch Island": lambda state: state.has("Boots", player),
        "Underground Tunnel - Small Room": True,
        "Swamp Gas Cavern - Scratch Wall": lambda state: state.has("Boots", player) and have_special_weapon_bullet(state, player),
        "Swamp Gas Cavern - Bat Mound": lambda state: state.has("Boots", player) and state.has("Bat Key", player),
        "Swamp Gas Cavern - Stair room": lambda state: state.has("Boots", player),
        "Swamp Gas Cavern - Rock Prison": lambda state: state.has("Boots", player) and have_bombs(state, player),
        "A Tiny Cabin - Tiny Cabin": lambda state: state.has("Skull Key", player),
        "A Cabin - Bedside ": lambda state: can_enter_zombiton(state, player),
        "Dusty Crypt - Pumpkin Door": lambda state: have_light_source(state, player) and state.has("Pumpkin Key", player),
        "Dusty Crypt - Maze": lambda state: have_light_source(state, player),
        "Musty Crypt - Big Closed Room": lambda state: have_light_source(state, player) and can_enter_zombiton(state, player) and have_special_weapon_bullet(state, player),
        "Rusty Crypt - Spike Vine": lambda state: have_light_source(state, player) and state.has("Fertilizer", player),
        "Rusty Crypt - Boulders": lambda state: have_light_source(state, player),
        "A Messy Cabin - Barrel Mess": lambda state: can_enter_zombiton(state, player),
        "Under the Lake - Lightning Rod Secret": lambda state: have_light_source(state, player) and have_all_orbs(state, player),
        "Under the Lake - Bat Door": lambda state: have_light_source(state, player) and have_all_orbs(state, player) and state.has("Bat Key", player),
        "Deeper Under the Lake - SE corner": lambda state: have_light_source(state, player) and have_all_orbs(state, player),
        "Deeper Under the Lake - Rhombus": lambda state: have_light_source(state, player) and have_all_orbs(state, player),
        "Frankenjulie's Laboratory - Boss Reward": lambda state: have_light_source(state, player) and have_all_orbs(state, player),
        "Haunted Tower - Barracks": lambda state: state.has("Ghost Potion", player) and state.has("Bat Key", player),
        "Haunted Tower, Floor 2 - Top Left": lambda state: state.has("Ghost Potion", player),
        "Haunted Tower Roof - Boss Reward": lambda state: state.has("Ghost Potion", player),
        "Haunted Basement - DoorDoorDoorDoorDoorDoor": lambda state: state.has("Ghost Potion", player) and have_light_source(state, player) and state.has("Bat Key", player) and state.has("Skull Key", player) and state.has("Pumpkin Key", player),
        "Abandoned Mines - Shaft": lambda state: have_light_source(state, player) and can_enter_rocky_cliffs(state, player),
        "The Shrine of Bombulus - Bombulus": lambda state: can_enter_rocky_cliffs(state, player),
        "A Gloomy Cavern - Lockpick": lambda state: have_light_source(state, player) and can_enter_rocky_cliffs(state, player),
        "Happy Stick Woods - Happy Stick Hidden": lambda state: state.has("Talisman", player),
        "Happy Stick Woods - Happy Stick Reward": lambda state: state.has("Talisman", player),
        "The Wolf Den - Wolf Top Left": lambda state: have_light_source(state, player) and state.has("Silver Sling", player),
        "The Wolf Den - Pumpkin Door": lambda state: have_light_source(state, player) and state.has("Silver Sling", player) and state.has("Pumpkin Key", player),
        "The Wolf Den - Grow Room": lambda state: have_light_source(state, player) and state.has("Silver Sling", player) and state.has("Fertilizer", player),
        "Upper Creepy Cavern - The Three ombres": lambda state: have_light_source(state, player) and can_enter_rocky_cliffs(state, player),
        "Under the Ravine - Left Vine": lambda state: have_light_source(state, player) and can_enter_rocky_cliffs(state, player) and state.has("Fertilizer", player),
        "Under the Ravine - Right Vine": lambda state: have_light_source(state, player) and can_enter_rocky_cliffs(state, player) and state.has("Fertilizer", player),
        "Creepy Caverns - M Pharoh bat Room": lambda state: have_light_source(state, player) and can_enter_rocky_cliffs(state, player) and state.has("Bat Key", player),
        "Creepy Caverns - E 2 blue Pharos": lambda state: have_light_source(state, player) and can_enter_rocky_cliffs(state, player),
        "Creepy Caverns - M GARGOYLE ROOM": lambda state: have_light_source(state, player) and can_enter_rocky_cliffs(state, player),
        "Castle Vampy - Vampire Guard": lambda state: can_enter_vampy(state, player),
        "Castle Vampy - maze top left": lambda state: can_enter_vampy(state, player),
        "Castle Vampy - Top Right Gauntlet": lambda state: can_enter_vampy(state, player),
        "Castle Vampy - Bat Closet": lambda state: can_enter_vampy(state, player),
        "Castle Vampy II - Candle Room": lambda state: can_enter_vampy_ii(state, player),
        "Castle Vampy II - Top Right Top": lambda state: can_enter_vampy_ii(state, player),
        "Castle Vampy II - Bottom Right Middle": lambda state: can_enter_vampy_ii(state, player),
        "Castle Vampy II - Bat room": lambda state: can_enter_vampy_ii(state, player) and have_special_weapon_bullet(state, player),
        "Cabin in the woods - Gold Skull": True,
        "Castle Vampy III - Middle": lambda state: can_enter_vampy_iii(state, player),
        "Castle Vampy III - Behind the Pews": lambda state: can_enter_vampy_iii(state, player),
        "Castle Vampy III - AMBUSH!": lambda state: can_enter_vampy_iii(state, player),
        "Castle Vampy III - Halloween": lambda state: can_enter_vampy_iii(state, player),
        "Castle Vampy III - So many bats": lambda state: can_enter_vampy_iii(state, player),
        "Castle Vampy IV - Right Path": lambda state: can_enter_vampy_iv(state, player),
        "Castle Vampy IV - Left Path": lambda state: can_enter_vampy_iv(state, player),
        "Castle Vampy IV - Ballroom Right": lambda state: can_enter_vampy_iv(state, player) and state.has("Ghost Potion", player) and state.has("Silver Sling", player),
        "Castle Vampy IV - Right Secret Wall": lambda state: can_enter_vampy_iv(state, player),
        "Castle Vampy IV - Ballroom Left": lambda state: can_enter_vampy_iv(state, player) and state.has("Ghost Potion", player) and state.has("Silver Sling", player),
        "Castle Vampy Roof - Gutsy the Elder": lambda state: can_enter_vampy(state, player) and have_all_bats(state, player) and have_special_weapon_damage(state, player),
        "Castle Vampy Roof - Stoney the Elder": lambda state: can_enter_vampy(state, player) and have_all_bats(state, player),
        "Castle Vampy Roof - Drippy the Elder": lambda state: can_enter_vampy(state, player) and have_all_bats(state, player),
        "Castle Vampy Roof - Toasty the Elder": lambda state: can_enter_vampy(state, player) and have_all_bats(state, player),
        "Heart of Terror - Bonkula": lambda state: can_enter_vampy_iv(state, player) and have_all_vamps(state, player),
        "A Hidey Hole - Bat Door": lambda state: state.has("Bat Key", player),
        "A Hidey Hole - Pebbles": True,
        "Swampdog Lair - Entrance": lambda state: state.has("Boots", player),
        "Swampdog Lair - End": lambda state: state.has("Boots", player) and have_light_source(state, player) and state.has("Fertilizer", player),
        "The Witch's Cabin - Ghostbusting": lambda state: state.has("Big Gem", player) and state.has("Daisy", player) and state.has("Mushroom", player, 10),
        "A Cabin3 - Hairy Larry": lambda state: have_light_source(state, player) and state.has("Silver Sling", player) and state.has("Boots", player) ,
        "Halloween Hill - Scaredy Cat": lambda state: state.has("Cat", player),
        "Halloween Hill - Silver Bullet": lambda state: state.has("Silver", player) and can_cleanse_crypts(state, player),
        "Halloween Hill - Smashing Pumpkins": lambda state: can_cleanse_crypts(state, player),
        "Halloween Hill - Sticky Shoes": True,
        "A Cabin4 - The Collection": lambda state: state.has("Silver Sling", player) and state.has("Ghost Potion", player) and can_enter_vampy(state, player),
        "A Gloomy Cavern - The Rescue": lambda state: have_light_source(state, player) and can_enter_rocky_cliffs(state, player),
        "A Cabin - Tree Trimming": True,
        "The Witch's Cabin - Witch Mushrooms": lambda state: state.has("Mushroom", player, 10),
        "Halloween Hill - Zombie Stomp": lambda state: can_cleanse_crypts(state, player)
        }
    for loc in multiworld.get_locations(player):
        if loc.name in access_rules:
            add_rule(loc, access_rules[loc.name])

