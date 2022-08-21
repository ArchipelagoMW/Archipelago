from ..generic.Rules import set_rule
from BaseClasses import MultiWorld

def set_location_rules(world: MultiWorld, player: int):

    set_rule(world.get_location("Afterlife: TV", player), 
        lambda state: state.has("CAVE KEY", player))

    # New Muldul
    set_rule(world.get_location("New Muldul: Underground Chest", player), 
        lambda state: state.has("PNEUMATOPHORE", player))
    set_rule(world.get_location("New Muldul: Upper House Chest 1", player), 
        lambda state: state.has("UPPER HOUSE KEY", player))
    set_rule(world.get_location("New Muldul: Upper House Chest 2", player), 
        lambda state: state.has("UPPER HOUSE KEY", player))
    set_rule(world.get_location("New Muldul: TV", player), 
        lambda state: state.has("HOUSE KEY", player))
    set_rule(world.get_location("New Muldul: Rescued Blerol", player), 
        lambda state: (state.has("JAIL KEY", player) and state.has("PNEUMATOPHORE", player)))
    set_rule(world.get_location("New Muldul: Rescued Blerol 2", player), 
        lambda state: (state.has("JAIL KEY", player) and state.has("PNEUMATOPHORE", player)))
    set_rule(world.get_location("New Muldul: Vault Left Chest", player), 
        lambda state: (state.has("WORM ROOM KEY", player) and state.has("BRIDGE KEY", player) and state.has("DOCK KEY", player)))
    set_rule(world.get_location("New Muldul: Vault Right Chest", player), 
        lambda state: (state.has("WORM ROOM KEY", player) and state.has("BRIDGE KEY", player) and state.has("DOCK KEY", player)))
    set_rule(world.get_location("New Muldul: Vault Bomb", player), 
        lambda state: (state.has("WORM ROOM KEY", player) and state.has("BRIDGE KEY", player) and state.has("DOCK KEY", player)))

    # Viewax's Edifice
    set_rule(world.get_location("Viewax's Edifice: Fountain Banana", player), 
        lambda state: state.has("PNEUMATOPHORE", player))
    set_rule(world.get_location("Viewax's Edifice: Dedusmuln's Suitcase", player), 
        lambda state: state.has("PNEUMATOPHORE", player))
    set_rule(world.get_location("Viewax's Edifice: Dedusmuln's Campfire", player), 
        lambda state: state.has("PNEUMATOPHORE", player))
    set_rule(world.get_location("Viewax's Edifice: Talk to Dedusmuln", player), 
        lambda state: state.has("PNEUMATOPHORE", player))
    set_rule(world.get_location("Viewax's Edifice: Canopic Jar", player), 
        lambda state: (state.has("PADDLE", player) and state.has("PNEUMATOPHORE", player)))
    set_rule(world.get_location("Viewax's Edifice: Cave Sarcophagus", player), 
        lambda state: (state.has("PADDLE", player) and state.has("PNEUMATOPHORE", player)))
    set_rule(world.get_location("Viewax's Edifice: Shielded Key", player), 
        lambda state: (state.has("PADDLE", player) and state.has("PNEUMATOPHORE", player)))
    set_rule(world.get_location("Viewax's Edifice: Tower Pot", player), 
        lambda state: (state.has("PADDLE", player) and state.has("PNEUMATOPHORE", player)))
    set_rule(world.get_location("Viewax's Edifice: Tower Jar", player), 
        lambda state: (state.has("PADDLE", player) and state.has("PNEUMATOPHORE", player)))
    set_rule(world.get_location("Viewax's Edifice: Tower Chest", player), 
        lambda state: (state.has("TOWER KEY", player) and state.has("PADDLE", player) and state.has("PNEUMATOPHORE", player)))
    set_rule(world.get_location("Viewax's Edifice: Sage Fridge", player), 
        lambda state: state.has("PNEUMATOPHORE", player))
    set_rule(world.get_location("Viewax's Edifice: Sage Item 1", player), 
        lambda state: state.has("PNEUMATOPHORE", player))
    set_rule(world.get_location("Viewax's Edifice: Sage Item 2", player), 
        lambda state: state.has("PNEUMATOPHORE", player))
    set_rule(world.get_location("Viewax's Edifice: Viewax Pot", player), 
        lambda state: (state.has("PADDLE", player) and state.has("PNEUMATOPHORE", player)))
    set_rule(world.get_location("Viewax's Edifice: Defeat Viewax", player), 
        lambda state: (state.has("PADDLE", player) and state.has("PNEUMATOPHORE", player)))
    set_rule(world.get_location("Viewax's Edifice: TV", player), 
        lambda state: (state.has("PADDLE", player) and state.has("JAIL KEY", player) and state.has("PNEUMATOPHORE", player)))

    # Arcade 1
    set_rule(world.get_location("Arcade 1: Key", player), 
        lambda state: (state.has("PADDLE", player) and state.has("PNEUMATOPHORE", player)))
    set_rule(world.get_location("Arcade 1: Coin Dash", player), 
        lambda state: (state.has("PADDLE", player) and state.has("PNEUMATOPHORE", player)))
    set_rule(world.get_location("Arcade 1: Burrito Alcove 1", player), 
        lambda state: (state.has("PADDLE", player) and state.has("PNEUMATOPHORE", player)))
    set_rule(world.get_location("Arcade 1: Burrito Alcove 2", player), 
        lambda state: (state.has("PADDLE", player) and state.has("PNEUMATOPHORE", player)))
    set_rule(world.get_location("Arcade 1: Behind Spikes Banana", player), 
        lambda state: (state.has("PADDLE", player) and state.has("PNEUMATOPHORE", player)))
    set_rule(world.get_location("Arcade 1: Pyramid Banana", player), 
        lambda state: (state.has("PADDLE", player) and state.has("PNEUMATOPHORE", player)))
    set_rule(world.get_location("Arcade 1: Moving Platforms Muscle Applique", player), 
        lambda state: (state.has("PADDLE", player) and state.has("PNEUMATOPHORE", player)))
    set_rule(world.get_location("Arcade 1: Bed Banana", player), 
        lambda state: (state.has("PADDLE", player) and state.has("PNEUMATOPHORE", player)))

    # Airship
    set_rule(world.get_location("Airship: Talk to Somsnosa", player), 
        lambda state: (state.has("WORM ROOM KEY", player) and state.has("DOCK KEY", player)))

    # Arcade Island
    set_rule(world.get_location("Arcade Island: Shielded Key", player), 
        lambda state: (state.has("PNEUMATOPHORE", player) and state.has("DOCK KEY", player)))
    set_rule(world.get_location("Arcade 2: Flying Machine Banana", player), 
        lambda state: (state.has("PNEUMATOPHORE", player) and state.has("DOCK KEY", player)))
    set_rule(world.get_location("Arcade 2: Paper Cup Detour", player), 
        lambda state: (state.has("PNEUMATOPHORE", player) and state.has("DOCK KEY", player)))
    set_rule(world.get_location("Arcade 2: Peak Muscle Applique", player), 
        lambda state: (state.has("PNEUMATOPHORE", player) and state.has("DOCK KEY", player)))
    set_rule(world.get_location("Arcade 2: Double Banana 1", player), 
        lambda state: (state.has("PNEUMATOPHORE", player) and state.has("DOCK KEY", player)))
    set_rule(world.get_location("Arcade 2: Double Banana 2", player), 
        lambda state: (state.has("PNEUMATOPHORE", player) and state.has("DOCK KEY", player)))
    set_rule(world.get_location("Arcade 2: Cave Burrito", player), 
        lambda state: (state.has("PNEUMATOPHORE", player) and state.has("DOCK KEY", player)))

    # TV Island
    set_rule(world.get_location("TV Island: TV", player), 
        lambda state: state.has("DOCK KEY", player))

    # Juice Ranch
    set_rule(world.get_location("Juice Ranch: Juice 1", player), 
        lambda state: state.has("DOCK KEY", player))
    set_rule(world.get_location("Juice Ranch: Juice 2", player), 
        lambda state: state.has("DOCK KEY", player))
    set_rule(world.get_location("Juice Ranch: Juice 3", player), 
        lambda state: state.has("DOCK KEY", player))
    set_rule(world.get_location("Juice Ranch: Ledge Rancher", player), 
        lambda state: state.has("DOCK KEY", player))
    set_rule(world.get_location("Juice Ranch: Battle with Somsnosa", player), 
        lambda state: state.has("DOCK KEY", player))
    set_rule(world.get_location("Juice Ranch: Fridge", player), 
        lambda state: state.has("DOCK KEY", player))
    set_rule(world.get_location("Juice Ranch: TV", player), 
        lambda state: state.has("DOCK KEY", player))

    # Worm Pod
    set_rule(world.get_location("Worm Pod: Key", player), 
        lambda state: (state.has("DOCK KEY", player) and state.has("WORM ROOM KEY", player)))

    # Foglast
    set_rule(world.get_location("Foglast: West Sarcophagus", player), 
        lambda state: state.has("DOCK KEY", player))
    set_rule(world.get_location("Foglast: Underground Sarcophagus", player), 
        lambda state: state.has("DOCK KEY", player))
    set_rule(world.get_location("Foglast: Shielded Key", player), 
        lambda state: state.has("DOCK KEY", player))
    set_rule(world.get_location("Foglast: Buy Clicker", player), 
        lambda state: state.has("DOCK KEY", player))
    set_rule(world.get_location("Foglast: TV", player), 
        lambda state: (state.has("CLICKER", player) and state.has("DOCK KEY", player)))
    set_rule(world.get_location("Foglast: Shielded Chest", player), 
        lambda state: state.has("DOCK KEY", player))
    set_rule(world.get_location("Foglast: Cave Fridge", player), 
        lambda state: (state.has("DOCK KEY", player) and state.has("PNEUMATOPHORE", player)))
    set_rule(world.get_location("Foglast: Roof Sarcophagus", player), 
        lambda state: (state.has("BRIDGE KEY", player) and state.has("DOCK KEY", player) and state.has("PNEUMATOPHORE", player)))
    set_rule(world.get_location("Foglast: Under Lair Sarcophagus 1", player), 
        lambda state: (state.has("BRIDGE KEY", player) and state.has("DOCK KEY", player) and state.has("PNEUMATOPHORE", player)))
    set_rule(world.get_location("Foglast: Under Lair Sarcophagus 2", player), 
        lambda state: (state.has("BRIDGE KEY", player) and state.has("DOCK KEY", player) and state.has("PNEUMATOPHORE", player)))
    set_rule(world.get_location("Foglast: Under Lair Sarcophagus 3", player), 
        lambda state: (state.has("BRIDGE KEY", player) and state.has("DOCK KEY", player) and state.has("PNEUMATOPHORE", player)))
    set_rule(world.get_location("Foglast: Sage Sarcophagus", player), 
        lambda state: (state.has("BRIDGE KEY", player) and state.has("DOCK KEY", player) and state.has("PNEUMATOPHORE", player)))
    set_rule(world.get_location("Foglast: Sage Item 1", player), 
        lambda state: (state.has("BRIDGE KEY", player) and state.has("DOCK KEY", player) and state.has("PNEUMATOPHORE", player)))
    set_rule(world.get_location("Foglast: Sage Item 2", player), 
        lambda state: (state.has("BRIDGE KEY", player) and state.has("DOCK KEY", player) and state.has("PNEUMATOPHORE", player)))

    # Drill Castle
    set_rule(world.get_location("Drill Castle: Island Banana", player), 
        lambda state: state.has("PNEUMATOPHORE", player))
    set_rule(world.get_location("Drill Castle: Island Pot", player), 
        lambda state: state.has("PNEUMATOPHORE", player))
    set_rule(world.get_location("Drill Castle: Cave Sarcophagus", player), 
        lambda state: state.has("PNEUMATOPHORE", player))
    set_rule(world.get_location("Drill Castle: Roof Banana", player), 
        lambda state: state.has("PNEUMATOPHORE", player))
    set_rule(world.get_location("Drill Castle: TV", player), 
        lambda state: state.has("PNEUMATOPHORE", player))

    # Sage Labyrinth
    set_rule(world.get_location("Sage Labyrinth: 1F Chest Near Fountain", player), 
        lambda state: state.has("SKULL BOMB", player))
    set_rule(world.get_location("Sage Labyrinth: 1F Hidden Sarcophagus", player), 
        lambda state: state.has("SKULL BOMB", player))
    set_rule(world.get_location("Sage Labyrinth: 1F Four Statues Chest 1", player), 
        lambda state: state.has("SKULL BOMB", player))
    set_rule(world.get_location("Sage Labyrinth: 1F Four Statues Chest 2", player), 
        lambda state: state.has("SKULL BOMB", player))
    set_rule(world.get_location("Sage Labyrinth: B1 Double Chest 1", player), 
        lambda state: state.has("SKULL BOMB", player))
    set_rule(world.get_location("Sage Labyrinth: B1 Double Chest 2", player), 
        lambda state: state.has("SKULL BOMB", player))
    set_rule(world.get_location("Sage Labyrinth: B1 Single Chest", player), 
        lambda state: state.has("SKULL BOMB", player))
    set_rule(world.get_location("Sage Labyrinth: B1 Enemy Chest", player), 
        lambda state: state.has("SKULL BOMB", player))
    set_rule(world.get_location("Sage Labyrinth: B1 Hidden Sarcophagus", player), 
        lambda state: state.has("SKULL BOMB", player))
    set_rule(world.get_location("Sage Labyrinth: B1 Hole Chest", player), 
        lambda state: state.has("SKULL BOMB", player))
    set_rule(world.get_location("Sage Labyrinth: B2 Hidden Sarcophagus 1", player), 
        lambda state: state.has("SKULL BOMB", player))
    set_rule(world.get_location("Sage Labyrinth: B2 Hidden Sarcophagus 2", player), 
        lambda state: state.has("SKULL BOMB", player))
    set_rule(world.get_location("Sage Labyrinth: Motor Hunter Sarcophagus", player), 
        lambda state: state.has("SKULL BOMB", player))
    set_rule(world.get_location("Sage Labyrinth: Sage Item 1", player), 
        lambda state: (state.has("DEEP KEY", player) and state.has("SKULL BOMB", player)))
    set_rule(world.get_location("Sage Labyrinth: Sage Item 2", player), 
        lambda state: (state.has("DEEP KEY", player) and state.has("SKULL BOMB", player)))
    set_rule(world.get_location("Sage Labyrinth: Sage Left Arm", player), 
        lambda state: (state.has("DEEP KEY", player) and state.has("SKULL BOMB", player)))
    set_rule(world.get_location("Sage Labyrinth: Sage Right Arm", player), 
        lambda state: (state.has("DEEP KEY", player) and state.has("SKULL BOMB", player)))
    set_rule(world.get_location("Sage Labyrinth: Sage Left Leg", player), 
        lambda state: (state.has("DEEP KEY", player) and state.has("SKULL BOMB", player)))
    set_rule(world.get_location("Sage Labyrinth: Sage Right Leg", player), 
        lambda state: (state.has("DEEP KEY", player) and state.has("SKULL BOMB", player)))

    # Sage Airship
    set_rule(world.get_location("Sage Airship: Bottom Level Pot", player), 
        lambda state: state.has("SKULL BOMB", player))
    set_rule(world.get_location("Sage Airship: Flesh Pot", player), 
        lambda state: state.has("SKULL BOMB", player))
    set_rule(world.get_location("Sage Airship: Top Jar", player), 
        lambda state: state.has("SKULL BOMB", player))
    set_rule(world.get_location("Sage Airship: TV", player), 
        lambda state: state.has("SAGE TOKEN", player, 3))

    # Hylemxylem
    set_rule(world.get_location("Hylemxylem: Jar", player), 
        lambda state: (state.has("DOCK KEY", player) and state.has("BRIDGE KEY", player) and state.has("WORM ROOM KEY", player)))
    set_rule(world.get_location("Hylemxylem: Lower Reservoir Key", player), 
        lambda state: (state.has("DOCK KEY", player) and state.has("BRIDGE KEY", player) and state.has("WORM ROOM KEY", player)))
    set_rule(world.get_location("Hylemxylem: Fountain Banana", player), 
        lambda state: (state.has("DOCK KEY", player) and state.has("BRIDGE KEY", player) and state.has("WORM ROOM KEY", player)))
    set_rule(world.get_location("Hylemxylem: East Island Banana", player), 
        lambda state: (state.has("DOCK KEY", player) and state.has("BRIDGE KEY", player) and state.has("WORM ROOM KEY", player) and state.has("PNEUMATOPHORE", player)))
    set_rule(world.get_location("Hylemxylem: East Island Chest", player), 
        lambda state: (state.has("DOCK KEY", player) and state.has("BRIDGE KEY", player) and state.has("WORM ROOM KEY", player) and state.has("PNEUMATOPHORE", player)))
    set_rule(world.get_location("Hylemxylem: Upper Chamber Banana", player), 
        lambda state: (state.has("DOCK KEY", player) and state.has("BRIDGE KEY", player) and state.has("WORM ROOM KEY", player) and state.has("UPPER CHAMBER KEY", player)))
    set_rule(world.get_location("Hylemxylem: Across Upper Reservoir Chest", player), 
        lambda state: (state.has("DOCK KEY", player) and state.has("BRIDGE KEY", player) and state.has("WORM ROOM KEY", player) and state.has("UPPER CHAMBER KEY", player)))
    set_rule(world.get_location("Hylemxylem: Drained Lower Reservoir Chest", player), 
        lambda state: (state.has("DOCK KEY", player) and state.has("BRIDGE KEY", player) and state.has("WORM ROOM KEY", player) and state.has("UPPER CHAMBER KEY", player)))
    set_rule(world.get_location("Hylemxylem: Drained Lower Reservoir Burrito 1", player), 
        lambda state: (state.has("DOCK KEY", player) and state.has("BRIDGE KEY", player) and state.has("WORM ROOM KEY", player) and state.has("UPPER CHAMBER KEY", player)))
    set_rule(world.get_location("Hylemxylem: Drained Lower Reservoir Burrito 2", player), 
        lambda state: (state.has("DOCK KEY", player) and state.has("BRIDGE KEY", player) and state.has("WORM ROOM KEY", player) and state.has("UPPER CHAMBER KEY", player)))
    set_rule(world.get_location("Hylemxylem: Lower Reservoir Hole Pot 1", player), 
        lambda state: (state.has("DOCK KEY", player) and state.has("BRIDGE KEY", player) and state.has("WORM ROOM KEY", player) and state.has("UPPER CHAMBER KEY", player)))
    set_rule(world.get_location("Hylemxylem: Lower Reservoir Hole Pot 2", player), 
        lambda state: (state.has("DOCK KEY", player) and state.has("BRIDGE KEY", player) and state.has("WORM ROOM KEY", player) and state.has("UPPER CHAMBER KEY", player)))
    set_rule(world.get_location("Hylemxylem: Lower Reservoir Hole Pot 3", player), 
        lambda state: (state.has("DOCK KEY", player) and state.has("BRIDGE KEY", player) and state.has("WORM ROOM KEY", player) and state.has("UPPER CHAMBER KEY", player)))
    set_rule(world.get_location("Hylemxylem: Lower Reservoir Hole Sarcophagus", player), 
        lambda state: (state.has("DOCK KEY", player) and state.has("BRIDGE KEY", player) and state.has("WORM ROOM KEY", player) and state.has("UPPER CHAMBER KEY", player)))
    set_rule(world.get_location("Hylemxylem: Drained Upper Reservoir Burrito 1", player), 
        lambda state: (state.has("DOCK KEY", player) and state.has("BRIDGE KEY", player) and state.has("WORM ROOM KEY", player) and state.has("UPPER CHAMBER KEY", player)))
    set_rule(world.get_location("Hylemxylem: Drained Upper Reservoir Burrito 2", player), 
        lambda state: (state.has("DOCK KEY", player) and state.has("BRIDGE KEY", player) and state.has("WORM ROOM KEY", player) and state.has("UPPER CHAMBER KEY", player)))
    set_rule(world.get_location("Hylemxylem: Drained Upper Reservoir Burrito 3", player), 
        lambda state: (state.has("DOCK KEY", player) and state.has("BRIDGE KEY", player) and state.has("WORM ROOM KEY", player) and state.has("UPPER CHAMBER KEY", player)))
    set_rule(world.get_location("Hylemxylem: Upper Reservoir Hole Key", player), 
        lambda state: (state.has("DOCK KEY", player) and state.has("BRIDGE KEY", player) and state.has("WORM ROOM KEY", player) and state.has("UPPER CHAMBER KEY", player)))
