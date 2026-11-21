from typing import TYPE_CHECKING
from worlds.generic.Rules import set_rule

if TYPE_CHECKING:
    from . import FaxanaduWorld


def can_buy_in_eolis(state, player):
    # Sword or Deluge so we can farm for gold.
    # Ring of Elf so we can get 1500 from the King.
    return state.has_any(["Progressive Sword", "Deluge", "Ring of Elf"], player)


def has_any_magic(state, player):
    return state.has_any(["Deluge", "Thunder", "Fire", "Death", "Tilte"], player)


def set_rules(faxanadu_world: "FaxanaduWorld"):
    player = faxanadu_world.player
    multiworld = faxanadu_world.multiworld

    # Region rules
    set_rule(multiworld.get_entrance("Eolis -> Path to Apolune", player), lambda state:
             state.has_all(["Key Jack", "Progressive Sword"], player))  # You can't go far with magic only
    set_rule(multiworld.get_entrance("Apolune -> Tower of Trunk", player), lambda state: state.has("Key Jack", player))
    set_rule(multiworld.get_entrance("Apolune -> Path to Forepaw", player), lambda state: state.has("Mattock", player))
    set_rule(multiworld.get_entrance("Trunk -> Joker Spring", player), lambda state: state.has("Key Joker", player))
    set_rule(multiworld.get_entrance("Trunk -> Tower of Fortress", player), lambda state: state.has("Key Jack", player))
    set_rule(multiworld.get_entrance("Trunk -> Path to Mascon", player), lambda state: 
             state.has_all(["Key Queen", "Ring of Ruby", "Sky Spring Flow", "Tower of Fortress Spring Flow", "Joker Spring Flow"], player) and 
             state.has("Progressive Sword", player, 2))
    set_rule(multiworld.get_entrance("Path to Mascon -> Tower of Red Potion", player), lambda state:
             state.has("Key Queen", player) and
             state.has("Red Potion", player, 4))  # It's impossible to go through the tower of Red Potion without at least 1-2 potions. Give them 4 for good measure.
    set_rule(multiworld.get_entrance("Path to Victim -> Tower of Suffer", player), lambda state: state.has("Key Queen", player))
    set_rule(multiworld.get_entrance("Path to Victim -> Victim", player), lambda state: state.has("Unlock Wingboots", player))
    set_rule(multiworld.get_entrance("Mist -> Useless Tower", player), lambda state:
             state.has_all(["Key King", "Unlock Wingboots"], player))
    set_rule(multiworld.get_entrance("Mist -> Tower of Mist", player), lambda state: state.has("Key King", player))
    set_rule(multiworld.get_entrance("Mist -> Path to Conflate", player), lambda state: state.has("Key Ace", player))
    set_rule(multiworld.get_entrance("Path to Conflate -> Helm Branch", player), lambda state: state.has("Key King", player))
    set_rule(multiworld.get_entrance("Path to Conflate -> Branches", player), lambda state: state.has("Key King", player))
    set_rule(multiworld.get_entrance("Daybreak -> Dartmoor Castle", player), lambda state: state.has("Ring of Dworf", player))
    set_rule(multiworld.get_entrance("Dartmoor Castle -> Evil Fortress", player), lambda state: state.has("Demons Ring", player))

    # Location rules
    set_rule(multiworld.get_location("Eolis Key Jack", player), lambda state: can_buy_in_eolis(state, player))
    set_rule(multiworld.get_location("Eolis Hand Dagger", player), lambda state: can_buy_in_eolis(state, player))
    set_rule(multiworld.get_location("Eolis Elixir", player), lambda state: can_buy_in_eolis(state, player))
    set_rule(multiworld.get_location("Eolis Deluge", player), lambda state: can_buy_in_eolis(state, player))
    set_rule(multiworld.get_location("Eolis Red Potion", player), lambda state: can_buy_in_eolis(state, player))
    set_rule(multiworld.get_location("Path to Apolune Magic Shield", player), lambda state: state.has("Key King", player))  # Mid-late cost, make sure we've progressed
    set_rule(multiworld.get_location("Path to Apolune Death", player), lambda state: state.has("Key Ace", player))  # Mid-late cost, make sure we've progressed
    set_rule(multiworld.get_location("Tower of Trunk Hidden Mattock", player), lambda state:
             # This is actually possible if the monster drop into the stairs and kill it with dagger. But it's a "pro move"
             state.has("Deluge", player, 1) or
             state.has("Progressive Sword", player, 2))
    set_rule(multiworld.get_location("Path to Forepaw Glove", player), lambda state:
             state.has_all(["Deluge", "Unlock Wingboots"], player))
    set_rule(multiworld.get_location("Trunk Red Potion", player), lambda state: state.has("Unlock Wingboots", player))
    set_rule(multiworld.get_location("Sky Spring", player), lambda state: state.has("Unlock Wingboots", player))
    set_rule(multiworld.get_location("Tower of Fortress Spring", player), lambda state: state.has("Spring Elixir", player))
    set_rule(multiworld.get_location("Tower of Fortress Guru", player), lambda state: state.has("Sky Spring Flow", player))
    set_rule(multiworld.get_location("Tower of Suffer Hidden Wingboots", player), lambda state: 
             state.has("Deluge", player) or
             state.has("Progressive Sword", player, 2))
    set_rule(multiworld.get_location("Misty House", player), lambda state: state.has("Black Onyx", player))
    set_rule(multiworld.get_location("Misty Doctor Office", player), lambda state: has_any_magic(state, player))
    set_rule(multiworld.get_location("Conflate Guru", player), lambda state: state.has("Progressive Armor", player, 3))
    set_rule(multiworld.get_location("Branches Hidden Mattock", player), lambda state: state.has("Unlock Wingboots", player))
    set_rule(multiworld.get_location("Path to Daybreak Glove", player), lambda state: state.has("Unlock Wingboots", player))
    set_rule(multiworld.get_location("Dartmoor Castle Hidden Hourglass", player), lambda state: state.has("Unlock Wingboots", player))
    set_rule(multiworld.get_location("Dartmoor Castle Hidden Red Potion", player), lambda state: has_any_magic(state, player))
    set_rule(multiworld.get_location("Fraternal Castle Guru", player), lambda state: state.has("Progressive Sword", player, 4))
    set_rule(multiworld.get_location("Fraternal Castle Shop Hidden Ointment", player), lambda state: has_any_magic(state, player))

    if faxanadu_world.options.require_dragon_slayer.value:
        set_rule(multiworld.get_location("Evil One", player), lambda state: 
                 state.has_all_counts({"Progressive Sword": 4, "Progressive Armor": 3, "Progressive Shield": 4}, player))
