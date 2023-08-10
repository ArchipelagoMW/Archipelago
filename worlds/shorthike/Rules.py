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
        if loc["purchase"]:
            forbid_items_for_player(world.get_location(loc["name"], player), self.item_name_groups['Coins'], player)
    forbid_item(world.get_location("Catch All Fish Reward", player), "Fishing Journal", player)
    forbid_item(world.get_location("Boat Challenge Reward", player), "Motorboat Key", player)
    forbid_item(world.get_location("Collect 15 Seashells", player), "Seashell", player)
    forbid_item(world.get_location("Wristwatch Trade", player), "Wristwatch", player)
    forbid_item(world.get_location("Sue the Rabbit Shoes Reward", player), "Headband", player)
