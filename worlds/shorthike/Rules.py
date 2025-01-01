from worlds.generic.Rules import forbid_items_for_player, add_rule
from .Options import Goal, GoldenFeatherProgression, MinShopCheckLogic, ShopCheckLogic


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

        # Shop Rules
        if loc["purchase"] and not options.coins_in_shops:
            forbid_items_for_player(multiworld.get_location(loc["name"], player), self.item_name_groups['Coins'], player)
        if loc["purchase"] >= get_min_shop_logic_cost(self) and options.shop_check_logic != ShopCheckLogic.option_nothing:
            if options.shop_check_logic in {ShopCheckLogic.option_fishing_rod, ShopCheckLogic.option_fishing_rod_and_shovel}:
                add_rule(multiworld.get_location(loc["name"], player),
                    lambda state: state.has("Progressive Fishing Rod", player))
            if options.shop_check_logic in {ShopCheckLogic.option_golden_fishing_rod, ShopCheckLogic.option_golden_fishing_rod_and_shovel}:
                add_rule(multiworld.get_location(loc["name"], player),
                    lambda state: state.has("Progressive Fishing Rod", player, 2))
            if options.shop_check_logic in {ShopCheckLogic.option_shovel, ShopCheckLogic.option_fishing_rod_and_shovel, ShopCheckLogic.option_golden_fishing_rod_and_shovel}:
                add_rule(multiworld.get_location(loc["name"], player),
                    lambda state: state.has("Shovel", player))

        # Minimum Feather Rules
        if options.golden_feather_progression != GoldenFeatherProgression.option_hard:
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
        lambda state: state.has("Progressive Fishing Rod", player))
    add_rule(multiworld.get_location("Catch Fish with Permit", player),
        lambda state: state.has("Progressive Fishing Rod", player))
    add_rule(multiworld.get_location("Catch All Fish Reward", player),
        lambda state: state.has("Progressive Fishing Rod", player, 2))

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
    
    # Race Rules
    if options.easier_races:
        add_rule(multiworld.get_location("Lighthouse Race Reward", player),
            lambda state: state.has("Running Shoes", player))
        add_rule(multiworld.get_location("Old Building Race Reward", player),
            lambda state: state.has("Running Shoes", player))
        add_rule(multiworld.get_location("Hawk Peak Race Reward", player),
            lambda state: state.has("Running Shoes", player))

def get_min_feathers(self, min_golden_feathers, min_golden_feathers_easy):
    options = self.options

    min_feathers = min_golden_feathers
    if options.golden_feather_progression == GoldenFeatherProgression.option_easy:
        min_feathers = min_golden_feathers_easy
    if min_feathers > options.golden_feathers:
        if options.goal not in {Goal.option_help_everyone, Goal.option_photo}:
            min_feathers = options.golden_feathers

    return min_feathers

def get_min_shop_logic_cost(self):
    options = self.options

    if options.min_shop_check_logic == MinShopCheckLogic.option_40_coins:
        return 40
    elif options.min_shop_check_logic == MinShopCheckLogic.option_100_coins:
        return 100
    elif options.min_shop_check_logic == MinShopCheckLogic.option_400_coins:
        return 400
