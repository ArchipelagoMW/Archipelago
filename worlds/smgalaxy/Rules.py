from sqlite3 import connect

from ..AutoWorld import LogicMixin
from ..generic.Rules import add_rule
from .regions import connect_regions
from .Options import EnablePurpleCoinStars
# main stage logic
def set_rules(world, player: int, self):
    connect_regions(world, player, "Menu", "Good Egg", lambda state: True)
    connect_regions(world, player, "Menu", "Bosses", lambda state: True)
    connect_regions(world, player, "Menu", "Hungry Lumas", lambda state: True)
    connect_regions(world, player, "Menu", "Honeyhive", lambda state: state.has("Power Star", player, 3))
    connect_regions(world, player, "Menu", "Fountain", lambda state: state.has("Grand Star Terrace", player))
    connect_regions(world, player, "Fountain", "Battlerock", lambda state: state.has("Power Star", player, 12))
    connect_regions(world, player, "Fountain", "Space Junk", lambda state: state.has("Power Star", player, 9))
    connect_regions(world, player, "Menu", "Kitchen", lambda state: state.has("Grand Star Fountain", player))
    connect_regions(world, player, "Kitchen", "Beach Bowl", lambda state: state.has("Power Star", player, 18))
    connect_regions(world, player, "Kitchen", "Ghostly", lambda state: state.has("Power Star", player, 20))
    connect_regions(world, player, "Menu", "Bedroom", lambda state: state.has("Grand Star Kitchen", player))
    connect_regions(world, player, "Bedroom", "Gusty Gardens", lambda state: state.has("Power Star", player, 24))
    connect_regions(world, player, "Bedroom", "Freezeflame", lambda state: state.has("Power Star", player, 26))
    connect_regions(world, player, "Bedroom", "Dusty Dune", lambda state: state.has("Power Star", player, 29))
    connect_regions(world, player, "Menu", "Engine Room", lambda state: state.has("Grand Star Bedroom", player))
    connect_regions(world, player, "Engine Room", "Gold Leaf", lambda state: state.has("Power Star", player, 34))
    connect_regions(world, player, "Engine Room", "Toy Time", lambda state: state.has("Power Star", player, 40))
    connect_regions(world, player, "Engine Room", "Sea Slide", lambda state: state.has("Power Star", player, 36))
    connect_regions(world, player, "Menu", "Garden", lambda state: state.has("Grand Star Engine Room", player))
    connect_regions(world, player, "Garden", "Deep Dark", lambda state: state.has("Power Star", player, 46))
    connect_regions(world, player, "Garden", "Dreadnaught", lambda state: state.has("Power Star", player, 48))
    connect_regions(world, player, "Garden", "Melty Molten", lambda state: state.has("Power Star", player, 52))
    connect_regions(world, player, "Menu", "Purple Coins", lambda state: True)
    
    # special stages logic
    add_rule(world.get_location("LDL: Surfing 101", player), lambda state: state.has("Power Star", player, 5))
    add_rule(world.get_location("FS: Painting the Planet Yellow", player), lambda state: state.has("Power Star", player, 7))
    add_rule(world.get_location("RG: Rolling in the Clouds", player), lambda state: state.has("Power Star", player, 11) and state.has("Grand Star Terrace", player))
    add_rule(world.get_location("HS: Shrinking Satellite", player), lambda state: state.has ("Power Star", player, 18) and state.has("Grand Star Terrace", player))
    add_rule(world.get_location("BUB: Through the Poison Swamp", player), lambda state: state.has ("Power Star", player, 19) and state.has("Grand Star Fountain", player))
    add_rule(world.get_location("BB: The Secret of Buoy Base", player), lambda state: state.has ("Power Star", player, 30) and state.has("Grand Star Fountain", player) and state.has("Grand Star Terrace", player))
    add_rule(world.get_location("BB: The Floating Fortress", player), lambda state: state.has ("Power Star", player, 30) and state.has("Grand Star Fountain", player) and state.has("Grand Star Terrace", player))
    add_rule(world.get_location("BF: Kingfin's Fearsome Waters", player), lambda state: state.has("Power Star", player, 55) and state.has("Grand Star Bedroom", player))
    add_rule(world.get_location("MS: Watch Your Step", player), lambda state: state.has("Power Star", player, 50) and state.has("Grand Star Engine Room", player) and state.has("Grand Star Bedroom", player))
    add_rule(world.get_location("DDR: Giant Eel Breakout", player), lambda state: state.has("Grand Star Fountain", player))
    add_rule(world.get_location("RGT: Gizmos, Gears, and Gadgets", player), lambda state: state.has("Grand Star Fountain", player) and state.has("Grand Star Terrace", player) and state.has("Green Star", player, 3))
    add_rule(world.get_location("LDT: The Galaxy's Greatest Wave", player), lambda state: state.has("Grand Star Fountain", player) and state.has("Grand Star Terrace", player) and state.has("Grand Star Kitchen", player) and state.has("Green Star", player, 3))
    add_rule(world.get_location("BBT: The Electric Labyrinth", player), lambda state: state.has("Grand Star Fountain", player) and state.has("Grand Star Terrace", player) and state.has("Grand Star Kitchen", player) and state.has("Green Star", player, 3))
    add_rule(world.get_location("SS: Rocky Road", player), lambda state: state.has("Power Star", player, 7))
    add_rule(world.get_location("SP: A Very Sticky Situation", player), lambda state: state.has("Grand Star Terrace", player) and state.has("Power Star", player, 9))
    add_rule(world.get_location("BM: Bigmouth's Gold Bait", player), lambda state: state.has("Grand Star Kitchen", player) and state.has("Power Star", player, 29))
    add_rule(world.get_location("Sandy Spiral: Choosing a Favorite Snack", player), lambda state: state.has("Grand Star Bedroom", player) and state.has("Power Star", player, 36) and state.has("Grand Star Fountain", player))
    add_rule(world.get_location("Bone's Boneyard: Racing the Spooky Speedster", player), lambda state: state.has("Grand Star Engine Room", player) and state.has("Grand Star Kitchen", player))
    add_rule(world.get_location("SC: Star Bunnies in the Snow", player), lambda state: state.has("Grand Star Engine Room", player) and state.has("Power Star", player, 52))
    # comet logic
    add_rule(world.get_location("GE: Dino Piranha Speed Run", player), lambda state: state.has("Power Star", player, 13))
    add_rule(world.get_location("HH: Honeyhive Cosmic Mario Race", player), lambda state: state.has("Power Star", player, 13))
    add_rule(world.get_location("SJ: Pull Star Path Speed Run", player), lambda state: state.has("Power Star", player, 13))
    add_rule(world.get_location("BR: Topmanic's Dardevil Run", player), lambda state: state.has("Power Star", player, 13))
    add_rule(world.get_location("BB: Fast Foes on the Cyclone Stone", player), lambda state: state.has("Power Star", player, 13))
    # boss stage logic 
    add_rule(world.get_location("BJ: Megaleg's Moon", player), lambda state: state.has("Power Star", player, 8))
    add_rule(world.get_location("B: The Firery Stronghold", player), lambda state: state.has("Power Star", player, 15) and state.has("Grand Star Terrace", player))
    add_rule(world.get_location("BJ: Sinking the Airships", player), lambda state: state.has("Power Star", player, 23) and state.has("Grand Star Fountain", player))
    add_rule(world.get_location("BJ: King Kaliente's Spicy Return", player), lambda state: state.has("Power Star", player, 45) and state.has("Grand Star Engine Room", player))
    add_rule(world.get_location("B:  Darkness on the Horizon", player), lambda state: state.has("Power Star", player, 33) and state.has("Grand Star Kitchen", player))
    add_rule(world.get_location("B: Bowser's Galaxy Reactor", player), lambda state: state.has("Power Star", player, world.Stars_to_finish[self.player].value) and state.has("Grand Star Bedroom", player))
    
    
    # purple coin star logic
    if self.multiworld.enable_purple_coin_stars[self.player] == EnablePurpleCoinStars.option_all:
        add_rule(world.get_location("DN: Battlestation's Purple Coins", player), lambda state: state.has("Peach", player))
        add_rule(world.get_location("MM: Red-Hot Purple Coins", player), lambda state: state.has("Peach", player))
        add_rule(world.get_location("TT: Luigi's Purple Coins", player), lambda state: state.has("Peach", player))
        add_rule(world.get_location("DD: Plunder the Purple Coins", player), lambda state: state.has("Peach", player))
        add_rule(world.get_location("GL: Purple Coins in the Woods", player), lambda state: state.has("Peach", player))
        add_rule(world.get_location("FF: Purple Coins on the Summit", player), lambda state: state.has("Peach", player))
        add_rule(world.get_location("SS: Purple Coins by the Seaside", player), lambda state: state.has("Peach", player))
        add_rule(world.get_location("GG: Purple Coins on the Puzzle Cube", player), lambda state: state.has("Peach", player))
        add_rule(world.get_location("G: Purple Coins in the Bone Pen", player), lambda state: state.has("Peach", player))
        add_rule(world.get_location("DDune: Purple Coin in the Desert", player), lambda state: state.has("Peach", player))
        add_rule(world.get_location("BR: Purple Coins on the Battlerock", player), lambda state: state.has("Peach", player))
        add_rule(world.get_location("GE: Purple Coin Omelet", player), lambda state: state.has("Peach", player))
        add_rule(world.get_location("HH: The Honeyhive's Purple Coins", player), lambda state: state.has("Peach", player))
        add_rule(world.get_location("SJ: Purple Coin Spacewalk", player), lambda state: state.has("Peach", player))
        add_rule(world.get_location("GG: Gateway's Purple coins", player), lambda state: state.has("Peach", player))
    elif self.multiworld.enable_purple_coin_stars[self.player] == EnablePurpleCoinStars.option_main_game_only:
          add_rule(world.get_location("GG: Gateway's Purple coins", player), lambda state: state.has("Grand Star Engine", player))
    else:
        return
    world.completion_condition[player] = lambda state: state.has("Peach", player)

