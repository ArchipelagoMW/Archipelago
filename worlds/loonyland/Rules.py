from BaseClasses import CollectionState
from worlds.generic.Rules import add_item_rule, add_rule


def have_light_source(state: CollectionState, player: int) -> bool:
    return state.has("Lantern", player) or (state.has("Stick", player) and state.has("Boots", player))


def have_bombs(state: CollectionState, player: int) -> bool:
    return state.has("Bombs", player)
    # or werewolf badge when badges are added


def have_all_orbs(state: CollectionState, player: int) -> bool:
    return state.has("Orb", player, 4)


def have_all_bats(state: CollectionState, player: int) -> bool:
    return state.has("Bat Statue", player, 4)


def have_all_vamps(state: CollectionState, player: int) -> bool:
    return state.has("Vamp Statue", player, 8)


def have_special_weapon_damage(state: CollectionState, player: int) -> bool:
    return (
        state.has_any(("Bombs", "Shock Wand", "Cactus", "Boomerang", "Whoopee", "Hot Pants"), player)
    )


def have_special_weapon_bullet(state: CollectionState, player: int) -> bool:
    return (
        state.has_any(("Bombs", "Ice Spear", "Cactus", "Boomerang", "Whoopee", "Hot Pants"), player)
    )


# return lambda state: True slingshot counts

def have_special_weapon_range_damage(state: CollectionState, player: int) -> bool:
    return (
        state.has_any(("Bombs", "Shock Wand", "Cactus", "Boomerang"), player)
    )
    # return lambda state: True slingshot counts


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
        "Swamp: Mud Path": lambda state: state.has("Boots", player),
        # "Swamp: Bog Beast": lambda state: True,
        # "Rocky Cliffs: Upper Ledge": lambda state: True,
        "Swamp: Sapling Shrine": lambda state: state.has("Boots", player),
        # "Terror Glade: South Trees": lambda state: True,
        "Rocky Cliffs: Vine": lambda state: state.has("Fertilizer", player),
        # "Rocky Cliffs: Grand Pharoh": lambda state: True,
        "Rocky Cliffs: Rock Corner": lambda state: have_bombs(state, player),
        # "Swamp: Outside Luniton": lambda state: True,
        # "Swamp: East 1": lambda state: True,
        # "Swamp: Top Left dry": lambda state: True,
        # "Swamp: East 2": lambda state: True,
        # "Woods: Above Castle":  lambda state: True,
        # "Rocky Cliffs: Entrance Ledge": lambda state: True,
        # "Rocky Cliffs: Peak": lambda state: True,
        # "Woods: SW of Cabin": lambda state: True,
        "Witch's Cabin: Bedroom": lambda state: have_light_source(state, player),
        # "Witch's Cabin: Backroom" lambda state: True,
        # "Bonita's Cabin: Barrel Maze": lambda state: True,
        "Bog Pit: Top Door": lambda state: state.has("Skull Key", player),
        # "Bog Pit: Posts Room": lambda state: True,
        # "Bog Pit: Drippy Window": lambda state: True,
        # "Bog Pit: Green room":  lambda state: True,
        # "Bog Pit: Arena": lambda state: True,
        # "Bog Pit: SW Switch": lambda state: True,
        "Tunnel: Swampdog Pumpkin Door": lambda state: state.has("Pumpkin Key", player),
        "Tunnel: Scratch Wall": lambda state: have_special_weapon_bullet(state, player),
        # "Tunnel: Narrow Passage": lambda state: True,
        # "Tunnel: Top Frogs": lambda state: True,
        "Tunnel: Torch Island": lambda state: state.has("Boots", player),
        # "Tunnel: Small Room": lambda state: True,
        "Swamp Gas: Scratch Wall": lambda state: have_special_weapon_bullet(state, player),
        "Swamp Gas: Bat Door": lambda state: state.has("Bat Key", player),
        # "Swamp Gas: Stair room": lambda state: True,
        "Swamp Gas: Rock Prison": lambda state: have_bombs(state, player),
        # "A Tiny Cabin": lambda state: True,
        # "Seer: Bedside": lambda state: True
        "Dusty Crypt: Pumpkin Door": lambda state: state.has("Pumpkin Key", player),
        # "Dusty Crypt: Maze": lambda state: True,
        "Musty Crypt: Maze Room": lambda state: have_special_weapon_bullet(state, player),
        "Rusty Crypt: Vine": lambda state: state.has("Fertilizer", player),
        # "Rusty Crypt: Boulders": lambda state: True,
        # "A Messy Cabin": lambda state: True,
        # "Under The Lake: Behind Lightning Rod": True,
        "Under The Lake: Bat Door": lambda state: state.has("Bat Key", player),
        # "Deeper Lake: Corner":  lambda state: True,
        # "Deeper Lake: Rhombus": lambda state: True,
        # "Frankenjulie's Reward": lambda state: True,
        "Tower: Barracks": lambda state: state.has("Ghost Potion", player) and state.has("Bat Key", player),
        "Tower F2: Skull Puzzle": lambda state: state.has("Ghost Potion", player),
        # "PolterGuy's Reward": lambda state: True,
        "Tower Basement: DoorDoorDoorDoorDoorDoor": lambda state: state.has("Bat Key", player) and state.has(
            "Skull Key",
            player) and state.has(
            "Pumpkin Key", player),
        # "Abandoned Mine: Shaft": lambda state: True,
        # "Shrine of Bombulus: Prize": lambda state: True,
        # "Gloomy Cavern: Lockpick": lambda state: True,
        # "Happy Stick: Hidden": lambda state: True,
        # "Happy Stick: Reward": lambda state: True,
        # "Wolf Den: Top Left": lambda state: True,
        "Wolf Den: Pumpkin Door": lambda state: state.has("Pumpkin Key", player),
        "Wolf Den: Vine": lambda state: state.has("Fertilizer", player),
        "Upper Cavern: Three Gold Skeletons": lambda state: True,
        "Under The Ravine: Left Vine": lambda state: state.has("Fertilizer", player),
        "Under The Ravine: Right Vine": lambda state: state.has("Fertilizer", player),
        "Creepy Caverns M: Pharaoh Bat Door": lambda state: state.has("Bat Key", player),
        # "Creepy Caverns E: Top Pharaohs": lambda state: True,
        # "Creepy Caverns M: Gargoyles": lambda state: True,
        # "Castle Vampy: Top Room": lambda state: True,
        # "Castle Vampy: Maze": lambda state: True,
        # "Castle Vampy: Gauntlet": lambda state: True,
        # "Castle Vampy: Bat Closet": lambda state: True,
        # "Castle Vampy II: Candle Room": lambda state: True,
        # "Castle Vampy II: Bloodsucker Room": lambda state: True,
        # "Castle Vampy II: Vampire Lord": lambda state: True,
        # "Castle Vampy II: Bat Room": lambda state: True,
        # "Cabin in the Woods: Gold Skull": lambda state: True,
        # "Castle Vampy III: Center":   lambda state: True,
        # "Castle Vampy III: Behind the Pews": lambda state: True,
        # "Castle Vampy III: AMBUSH!": lambda state: True,
        # "Castle Vampy III: Halloween": lambda state: True,
        # "Castle Vampy III: Too Many Bats": lambda state: True,
        # "Castle Vampy IV: Right Path": lambda state: True,
        # "Castle Vampy IV: Left Path": lambda state: True,
        "Castle Vampy IV: Ballroom Right": lambda state: state.has("Ghost Potion", player) and state.has("Silver Sling",
                                                                                                         player),
        # "Castle Vampy IV: Right Secret Wall": lambda state: True,
        "Castle Vampy IV: Ballroom Left": lambda state: state.has("Ghost Potion", player) and state.has("Silver Sling",
                                                                                                        player),
        "Roof NW: Gutsy the Elder": lambda state: have_special_weapon_damage(state, player),
        # "Roof NE: Stoney the Elder": lambda state: True,
        # "Roof SW: Drippy the Elder": lambda state: True,
        # "Roof SE: Toasty the Elder": lambda state: True,
        # "Bonkula": lambda state: True,
        "Hidey-Hole: Bat Door": lambda state: state.has("Bat Key", player),
        # "Hidey-Hole: Pebbles":: lambda state: True,
        "Swampdog Lair: Entrance": lambda state: state.has("Boots", player),
        "Swampdog Lair: End": lambda state: state.has("Boots", player) and have_light_source(state,
                                                                                             player) and state.has(
            "Fertilizer", player),
        "Q: Ghostbusting": lambda state: state.has("Big Gem", player) and state.has("Doom Daisy", player) and state.has(
            "Mushroom", player, 10),
        "Q: Hairy Larry": lambda state: have_light_source(state, player) and state.has("Silver Sling",
                                                                                       player) and state.has("Boots",
                                                                                                             player),
        "Q: Scaredy Cat": lambda state: state.has("Cat", player),
        "Q: Silver Bullet": lambda state: state.has("Silver", player) and can_cleanse_crypts(state, player),
        "Q: Smashing Pumpkins": lambda state: can_cleanse_crypts(state, player),
        # "Q: Sticky Shoes": lambda state: True,
        "Q: The Collection": lambda state: state.has("Silver Sling", player) and state.has("Ghost Potion",
                                                                                           player) and can_enter_vampy(
            state, player),
        # "Q: The Rescue":  lambda state: True,
        # "Q: Tree Trimming": lambda state: True,
        "Q: Witch Mushrooms": lambda state: state.has("Mushroom", player, 10),
        "Q: Zombie Stomp": lambda state: can_cleanse_crypts(state, player),
        # "The Evilizer - Save Halloween Hill": lambda state: True
    }
    for loc in multiworld.get_locations(player):
        if loc.name in access_rules:
            add_rule(loc, access_rules[loc.name])
