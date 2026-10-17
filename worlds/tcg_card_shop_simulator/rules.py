from BaseClasses import ItemClassification
def set_goal(world):

    if world.options.goal.value == world.options.goal.option_reach_max_level:
        world.multiworld.get_location(f"Level {world.options.max_level.value}", world.player).place_locked_item(
            Item("Victory", ItemClassification.progression, None, world.player))
        world.multiworld.completion_condition[world.player] = lambda state: state.has("Victory", world.player)

    if world.options.goal.value == world.options.goal.option_collection_builder:
        world.multiworld.completion_condition[world.player] = (
            lambda state: all(
                has_card_pack(world, state, region)
                for region in CardRegion
            )
        )

    if world.options.goal.value == world.options.goal.option_sell_ghost_cards:
        lambdas = {}
        for bagsize, amount in world.ghost_item_counts.items():
            plural = "s" if bagsize > 1 else ""
            item_name = f"{bagsize} Ghost Card{plural}"
            lambdas[bagsize] = (lambda state, item=item_name, count=amount: state.has(item, world.player, count))
        world.multiworld.completion_condition[world.player] = lambda state: all(check(state) for check in lambdas.values())