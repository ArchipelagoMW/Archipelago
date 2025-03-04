from BaseClasses import CollectionState, Region, ItemClassification
from worlds.pokepark_1 import PokeparkItem, PokeparkWorld
from worlds.pokepark_1.locations import PokeparkLocation
from worlds.pokepark_1.logic import Requirements, PokeparkRegion, REGIONS


def pokepark_requirements_satisfied(state: CollectionState, requirements: Requirements, world: PokeparkWorld):
    has_required_unlocks = all(state.has(unlock, world.player) for unlock in requirements.unlock_names)
    has_required_friends = all(state.has(friend, world.player) for friend in requirements.friendship_names)
    has_required_prismas = all(state.has(prisma, world.player) for prisma in requirements.prisma_names)
    has_enough_friends = requirements.friendcount <= state.count_group("Friendship Items", world.player)
    can_reach_required_locations = all(state.can_reach_location(location,world.player) for location in requirements.can_reach_locations)
    if requirements.oneof_item_names:
        has_any = any(
            all(state.has(item, world.player) for item in item_list)
            for item_list in requirements.oneof_item_names
        )
    else:
        has_any = True
    return has_required_unlocks and has_enough_friends and has_required_friends and has_required_prismas and has_any and can_reach_required_locations


def create_region(region: PokeparkRegion, world: PokeparkWorld):
    new_region = Region(region.name, world.player, world.multiworld)

    def create_location(location, location_type):
        new_location = PokeparkLocation(
            world.player,
            f"{region.display} - {location.name}",
            location.id,
            new_region
        )
        new_location.access_rule = lambda state: pokepark_requirements_satisfied(state, location.requirements, world)
        new_region.locations.append(new_location)
    for location in region.quest_locations:
        create_location(location, "quest")
    for location in region.unlock_location:
        create_location(location, "unlock")
    for location in region.friendship_locations:
        create_location(location, "friendship")
    for location in region.minigame_location:
        create_location(location, "minigame")


    if region.name == "Victory Region":
        new_location = PokeparkLocation(world.player, "Victory", None, new_region)
        new_location.access_rule = lambda state: pokepark_requirements_satisfied(state, region.requirements, world)
        new_region.locations.append(new_location)
        event_item = PokeparkItem("Victory", ItemClassification.progression, None, world.player)
        new_location.place_locked_item(event_item)
        world.multiworld.completion_condition[world.player] = lambda state: state.has("Victory", world.player)

    return new_region


def create_regions(world: PokeparkWorld):
    regions = {
        "Menu": Region("Menu", world.player, world.multiworld)
    }

    for region in REGIONS:
        regions[region.name] = create_region(region, world)

        for parent_name in region.parent_regions:
            if parent_name in regions:
                regions[parent_name].connect(regions[region.name], None,
                                               lambda state, r=region: pokepark_requirements_satisfied(state,
                                                                                                               r.requirements,
                                                                                                               world))

    world.multiworld.regions += regions.values()
