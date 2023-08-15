from typing import Dict, List, Set
from worlds.generic.Rules import forbid_item, forbid_items_for_player, set_rule, add_rule
from BaseClasses import CollectionState


def create_rules(self, location_table):
    world = self.multiworld
    player = self.player
    for loc in location_table:
        if loc["needsShovel"]:
            forbid_item(world.get_location(loc["name"], player), "Shovel", player)
            forbid_item(world.get_location(loc["name"], player), "Toy Shovel", player)
            forbid_items_for_player(world.get_location(loc["name"], player), self.item_name_groups['Maps'], player)
            set_rule(world.get_location(loc["name"], self.player),
                lambda state: state.has("Shovel", self.player))
        if loc["purchase"]:
            forbid_items_for_player(world.get_location(loc["name"], player), self.item_name_groups['Coins'], player)
    forbid_item(world.get_location("Catch All Fish Reward", player), "Fishing Journal", player)
    set_rule(world.get_location("Catch All Fish Reward", player),
        lambda state: state.has("Fishing Journal", self.player))
    forbid_item(world.get_location("Catch 3 Fish Reward", player), "Fishing Rod", player)
    set_rule(world.get_location("Catch 3 Fish Reward", player),
        lambda state: state.has("Fishing Rod", self.player))
    forbid_item(world.get_location("Catch Fish with Permit", player), "Fishing Rod", player)
    set_rule(world.get_location("Catch Fish with Permit", player),
        lambda state: state.has("Fishing Rod", self.player))
    forbid_item(world.get_location("Return Camping Permit", player), "Camping Permit", player)
    set_rule(world.get_location("Return Camping Permit", player),
        lambda state: state.has("Camping Permit", self.player))
    forbid_item(world.get_location("Boat Challenge Reward", player), "Motorboat Key", player)
    set_rule(world.get_location("Boat Challenge Reward", player),
        lambda state: state.has("Motorboat Key", self.player))
    forbid_item(world.get_location("Collect 15 Seashells", player), "Seashell", player)
    set_rule(world.get_location("Collect 15 Seashells", player),
        lambda state: state.has("Seashell", self.player, 15))
    forbid_item(world.get_location("Wristwatch Trade", player), "Wristwatch", player)
    set_rule(world.get_location("Wristwatch Trade", player),
        lambda state: state.has("Wristwatch", self.player))
    forbid_item(world.get_location("Sue the Rabbit Shoes Reward", player), "Headband", player)
    set_rule(world.get_location("Sue the Rabbit Shoes Reward", player),
        lambda state: state.has("Headband", self.player))
    forbid_item(world.get_location("Return to Shell Kid", player), "Shell Necklace", player)
    set_rule(world.get_location("Return to Shell Kid", player),
        lambda state: state.has("Shell Necklace", self.player))
