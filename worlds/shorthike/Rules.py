from worlds.generic.Rules import forbid_items_for_player, add_rule


def create_rules(self, location_table):
    world = self.multiworld
    player = self.player

    # Shovel Rules
    for loc in location_table:
        if loc["needsShovel"]:
            forbid_items_for_player(world.get_location(loc["name"], player), self.item_name_groups['Maps'], player)
            add_rule(world.get_location(loc["name"], self.player),
                lambda state: state.has("Shovel", self.player))
        if loc["purchase"] and not world.coins_in_shops[player].value:
            forbid_items_for_player(world.get_location(loc["name"], player), self.item_name_groups['Coins'], player)

        # Minimum Feather Rules
        if world.golden_feather_progression[player].value != 2  and loc["minGoldenFeathers"] != 0:
            min_feathers = loc["minGoldenFeathers"]
            if world.golden_feather_progression[player].value == 0:
                min_feathers = loc["minGoldenFeathersEasy"]
            if min_feathers > world.golden_feathers[player].value:
                min_feathers = world.golden_feathers[player].value

            if world.buckets[player].value > 0 and min_feathers > loc["minGoldenFeathersBucket"]:
                add_rule(world.get_location(loc["name"], self.player),
                    lambda state: state.has("Golden Feather", self.player, min_feathers)
                        or (state.has("Golden Feather", self.player, loc["minGoldenFeathersBucket"])
                        and state.has("Bucket", self.player)))
            else:
                add_rule(world.get_location(loc["name"], self.player),
                    lambda state: state.has("Golden Feather", self.player, min_feathers))
    add_rule(world.get_location("Shovel Kid Trade", player),
        lambda state: state.has("Toy Shovel", self.player))

    # Fishing Rules
    add_rule(world.get_location("Catch All Fish Reward", player),
        lambda state: state.has("Fishing Journal", self.player))
    add_rule(world.get_location("Catch 3 Fish Reward", player),
        lambda state: state.has("Fishing Rod", self.player))
    add_rule(world.get_location("Catch Fish with Permit", player),
        lambda state: state.has("Fishing Rod", self.player))
    add_rule(world.get_location("Catch All Fish Reward", player),
        lambda state: state.has("Fishing Rod", self.player))

    # Misc Rules
    add_rule(world.get_location("Return Camping Permit", player),
        lambda state: state.has("Camping Permit", self.player))
    add_rule(world.get_location("Boat Challenge Reward", player),
        lambda state: state.has("Motorboat Key", self.player))
    add_rule(world.get_location("Collect 15 Seashells", player),
        lambda state: state.has("Seashell", self.player, 15))
    add_rule(world.get_location("Wristwatch Trade", player),
        lambda state: state.has("Wristwatch", self.player))
    add_rule(world.get_location("Sue the Rabbit Shoes Reward", player),
        lambda state: state.has("Headband", self.player))
    add_rule(world.get_location("Return to Shell Kid", player),
        lambda state: state.has("Shell Necklace", self.player))
    add_rule(world.get_location("Beachstickball (10 Hits)", player),
        lambda state: state.has("Stick", self.player))
    add_rule(world.get_location("Beachstickball (20 Hits)", player),
        lambda state: state.has("Stick", self.player))
    add_rule(world.get_location("Beachstickball (30 Hits)", player),
        lambda state: state.has("Stick", self.player))
