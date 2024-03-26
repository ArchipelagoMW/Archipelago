from worlds.generic.Rules import forbid_items_for_player, add_rule

def create_rules(self, location_table):
    multiworld = self.multiworld
    player = self.player
    options = self.options

    # Shovel Rules
    for loc in location_table:
        if loc["needsShovel"]:
            forbid_items_for_player(multiworld.get_location(loc["name"], player), self.item_name_groups['Maps'], player)
            add_rule(multiworld.get_location(loc["name"], player),
                lambda state: state.has("Shovel", player))
        if loc["purchase"] and not options.coins_in_shops:
            forbid_items_for_player(multiworld.get_location(loc["name"], player), self.item_name_groups['Coins'], player)

        # Minimum Feather Rules
        if options.golden_feather_progression != 2:
            min_feathers = get_min_feathers(self, loc["minGoldenFeathers"], loc["minGoldenFeathersEasy"])

            if options.buckets > 0 and loc["minGoldenFeathersBucket"] < min_feathers:
                add_rule(multiworld.get_location(loc["name"], player),
                    lambda state, loc=loc, min_feathers=min_feathers: state.has("Golden Feather", player, min_feathers)
                        or (state.has("Bucket", player) and state.has("Golden Feather", player, loc["minGoldenFeathersBucket"])))
            elif min_feathers > 0:
                add_rule(multiworld.get_location(loc["name"], player),
                    lambda state, min_feathers=min_feathers: state.has("Golden Feather", player, min_feathers))
    add_rule(multiworld.get_location("Shovel Kid Trade", player),
        lambda state: state.has("Toy Shovel", player))
    add_rule(multiworld.get_location("Sand Castle Golden Feather", player),
        lambda state: state.has("Toy Shovel", player))

    # Fishing Rules
    add_rule(multiworld.get_location("Catch 3 Fish Reward", player),
        lambda state: state.has("Fishing Rod", player))
    add_rule(multiworld.get_location("Catch Fish with Permit", player),
        lambda state: state.has("Fishing Rod", player))
    add_rule(multiworld.get_location("Catch All Fish Reward", player),
        lambda state: state.has("Fishing Rod", player))

    # Misc Rules
    add_rule(multiworld.get_location("Return Camping Permit", player),
        lambda state: state.has("Camping Permit", player))
    add_rule(multiworld.get_location("Boat Challenge Reward", player),
        lambda state: state.has("Motorboat Key", player))
    add_rule(multiworld.get_location("Collect 15 Seashells", player),
        lambda state: state.has("Seashell", player, 15))
    add_rule(multiworld.get_location("Wristwatch Trade", player),
        lambda state: state.has("Wristwatch", player))
    add_rule(multiworld.get_location("Sue the Rabbit Shoes Reward", player),
        lambda state: state.has("Headband", player))
    add_rule(multiworld.get_location("Return to Shell Kid", player),
        lambda state: state.has("Shell Necklace", player) and state.has("Seashell", player, 15))
    add_rule(multiworld.get_location("Ranger May Shell Necklace Golden Feather", player),
        lambda state: state.has("Shell Necklace", player))
    add_rule(multiworld.get_location("Beachstickball (10 Hits)", player),
        lambda state: state.has("Stick", player))
    add_rule(multiworld.get_location("Beachstickball (20 Hits)", player),
        lambda state: state.has("Stick", player))
    add_rule(multiworld.get_location("Beachstickball (30 Hits)", player),
        lambda state: state.has("Stick", player))

def get_min_feathers(self, min_golden_feathers, min_golden_feathers_easy):
    options = self.options

    min_feathers = min_golden_feathers
    if options.golden_feather_progression == 0:
        min_feathers = min_golden_feathers_easy
    if min_feathers > options.golden_feathers:
        if options.goal != 1 and options.goal != 3:
            min_feathers = options.golden_feathers

    return min_feathers
