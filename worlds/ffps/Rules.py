from ..generic.Rules import set_rule, add_rule, add_item_rule
from BaseClasses import MultiWorld
from ..AutoWorld import LogicMixin


# Sets rules on entrances and advancements that are always applied
def set_rules(world: MultiWorld, player: int):
    set_rule(world.get_location(("Salvage Molten Freddy"), player), lambda state: True)
    set_rule(world.get_location(("Salvage ScrapTrap"), player), lambda state: state.has("Catalogue 2 Unlock", player))
    set_rule(world.get_location(("Salvage Scrap Baby"), player), lambda state: state.has("Catalogue 3 Unlock", player))
    set_rule(world.get_location(("Salvage Lefty"), player), lambda state: state.has("Catalogue 4 Unlock", player))
    set_rule(world.get_location(("Buy Fruit Maze Decor"), player), lambda state: state.has("Catalogue 2 Unlock", player))
    set_rule(world.get_location(("Buy Midnight Moterist Decor"), player), lambda state: state.has("Catalogue 2 Unlock", player))
    set_rule(world.get_location(("Buy Gumball Machine Decor"), player), lambda state: state.has("Catalogue 2 Unlock", player))
    set_rule(world.get_location(("Buy Stage Light Decor"), player), lambda state: state.has("Catalogue 2 Unlock", player))
    set_rule(world.get_location(("Buy Traffic Light Decor"), player), lambda state: state.has("Catalogue 2 Unlock", player))
    set_rule(world.get_location(("Buy Happy Frog Animatronic"), player), lambda state: state.has("Catalogue 2 Unlock", player))
    set_rule(world.get_location(("Buy Mr Hippo Animatronic"), player), lambda state: state.has("Catalogue 2 Unlock", player))
    set_rule(world.get_location(("Buy Nedd Bear Animatronic"), player), lambda state: state.has("Catalogue 2 Unlock", player))
    set_rule(world.get_location(("Buy Pig Patch Animatronic"), player), lambda state: state.has("Catalogue 2 Unlock", player))
    set_rule(world.get_location(("Buy Candy Cadet Decor"), player), lambda state: state.has("Catalogue 2 Unlock", player))
    set_rule(world.get_location(("Buy Stage Upgrade 3"), player), lambda state: state.has("Catalogue 2 Unlock", player))
    set_rule(world.get_location(("Buy Stage Upgrade 4"), player), lambda state: state.has("Catalogue 2 Unlock", player))
    set_rule(world.get_location(("Buy Cups Upgrade 3"), player), lambda state: state.has("Catalogue 2 Unlock", player))
    set_rule(world.get_location(("Buy Speaker Upgrade 1"), player), lambda state: state.has("Catalogue 2 Unlock", player))
    set_rule(world.get_location(("Buy Speaker Upgrade 2"), player), lambda state: state.has("Catalogue 2 Unlock", player))
    set_rule(world.get_location(("Buy Side Stage Upgrade"), player), lambda state: state.has("Catalogue 3 Unlock", player))
    set_rule(world.get_location(("Buy Ballpit Tower Decor"), player), lambda state: state.has("Catalogue 3 Unlock", player))
    set_rule(world.get_location(("Buy Ladder Tower Decor"), player), lambda state: state.has("Catalogue 3 Unlock", player))
    set_rule(world.get_location(("Buy Carnival Hoops Decor"), player), lambda state: state.has("Catalogue 3 Unlock", player))
    set_rule(world.get_location(("Buy Roller Coaster Decor"), player), lambda state: state.has("Catalogue 3 Unlock", player))
    set_rule(world.get_location(("Buy Lemonade Clown Decor"), player), lambda state: state.has("Catalogue 3 Unlock", player))
    set_rule(world.get_location(("Buy Punch Clown Decor"), player), lambda state: state.has("Catalogue 3 Unlock", player))
    set_rule(world.get_location(("Buy Jukebox Decor"), player), lambda state: state.has("Catalogue 3 Unlock", player))
    set_rule(world.get_location(("Buy Medical Station Decor"), player), lambda state: state.has("Catalogue 3 Unlock", player))
    set_rule(world.get_location(("Buy Security Door Decor"), player), lambda state: state.has("Catalogue 3 Unlock", player))
    set_rule(world.get_location(("Buy Rockstar Freddy Animatronic"), player), lambda state: state.has("Catalogue 3 Unlock", player))
    set_rule(world.get_location(("Buy Rockstar Bonnie Animatronic"), player), lambda state: state.has("Catalogue 3 Unlock", player))
    set_rule(world.get_location(("Buy Rockstar Chica Animatronic"), player), lambda state: state.has("Catalogue 3 Unlock", player))
    set_rule(world.get_location(("Buy Rockstar Foxy Animatronic"), player), lambda state: state.has("Catalogue 3 Unlock", player))
    set_rule(world.get_location(("Buy Stage Upgrade 5"), player), lambda state: state.has("Catalogue 3 Unlock", player))
    set_rule(world.get_location(("Buy Balloon Cart Decor"), player), lambda state: state.has("Catalogue 4 Unlock", player))
    set_rule(world.get_location(("Buy Confetti Floor"), player), lambda state: state.has("Catalogue 4 Unlock", player))
    set_rule(world.get_location(("Buy Deluxe Ballpit Decor"), player), lambda state: state.has("Catalogue 4 Unlock", player))
    set_rule(world.get_location(("Buy Pizza Light Decor"), player), lambda state: state.has("Catalogue 4 Unlock", player))
    set_rule(world.get_location(("Buy Data Archive Decor"), player), lambda state: state.has("Catalogue 4 Unlock", player))
    set_rule(world.get_location(("Buy Gravity Vortex Decor"), player), lambda state: state.has("Catalogue 4 Unlock", player))
    set_rule(world.get_location(("Buy Orville Elephant Animatronic"), player), lambda state: state.has("Catalogue 4 Unlock", player))
    set_rule(world.get_location(("Buy Prize King Decor"), player), lambda state: state.has("Catalogue 4 Unlock", player))
    set_rule(world.get_location(("Buy Security Puppet Decor"), player), lambda state: state.has("Catalogue 4 Unlock", player))
    set_rule(world.get_location(("Buy Lefty Animatronic"), player), lambda state: state.has("Catalogue 4 Unlock", player))
    set_rule(world.get_location(("Buy Music Man Animatronic"), player), lambda state: state.has("Catalogue 4 Unlock", player))
    set_rule(world.get_location(("Buy El Chip Animatronic"), player), lambda state: state.has("Catalogue 4 Unlock", player))
    set_rule(world.get_location(("Buy Funtime Chica Animatronic"), player), lambda state: state.has("Catalogue 4 Unlock", player))
    set_rule(world.get_location(("Buy Pickles Decor"), player), lambda state: state.has("Catalogue 4 Unlock", player))
    set_rule(world.get_location(("Buy Cups Upgrade 4"), player), lambda state: state.has("Catalogue 4 Unlock", player))
    set_rule(world.get_location(("Unlocked Catalogue 3"), player), lambda state: state.has("Catalogue 2 Unlock", player))
    set_rule(world.get_location(("Unlocked Catalogue 4"), player), lambda state: state.has("Catalogue 3 Unlock", player))


# Sets rules on completion condition
def set_completion_rules(world: MultiWorld, player: int):
    completion_requirements = lambda state: \
        state.has("ScrapTrap", player) and \
        state.has("Scrap Baby", player) and \
        state.has("Lefty", player) and \
        state.has("Molten Freddy", player)
    world.completion_condition[player] = lambda state: completion_requirements(state)
