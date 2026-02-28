def create_events(world, player):
    world.get_location("Credits", player).place_locked_item(world.create_item("Victory", player))
