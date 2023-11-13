from BaseClasses import Region, Entrance, Location, CollectionState


from .LADXR.checkMetadata import checkMetadataTable
from .Common import *
from worlds.generic.Rules import add_item_rule
from .Items import ladxr_item_to_la_item_name


prefilled_events = ["ANGLER_KEYHOLE", "RAFT", "MEDICINE2", "CASTLE_BUTTON"]

links_awakening_dungeon_names = [
    "Tail Cave",
    "Bottle Grotto",
    "Key Cavern",
    "Angler's Tunnel",
    "Catfish's Maw",
    "Face Shrine",
    "Eagle's Tower",
    "Turtle Rock",
    "Color Dungeon"
]


def meta_to_name(meta):
    return f"{meta.name} ({meta.area})"


def get_locations_to_id():
    ret = {

    }

    # Magic to generate unique ids
    for s, v in checkMetadataTable.items():
        if s == "None":
            continue
        splits = s.split("-")

        main_id = int(splits[0], 16)
        sub_id = 0
        if len(splits) > 1:
            sub_id = splits[1]
            if sub_id.isnumeric():
                sub_id = (int(sub_id) + 1) * 1000
            else:
                sub_id = 1000
        name = f"{v.name} ({v.area})"
        ret[name] = BASE_ID + main_id + sub_id

    return ret


locations_to_id = get_locations_to_id()


class LinksAwakeningLocation(Location):
    game = LINKS_AWAKENING
    dungeon = None

    def __init__(self, player: int, region, ladxr_item):
        name = meta_to_name(ladxr_item.metadata)

        self.event = ladxr_item.event is not None
        if self.event:
            name = ladxr_item.event

        address = None
        if not self.event:
            address = locations_to_id[name]
        super().__init__(player, name, address)
        self.parent_region = region
        self.ladxr_item = ladxr_item

        def filter_item(item):
            if not ladxr_item.MULTIWORLD and item.player != player:
                return False
            return True
        add_item_rule(self, filter_item)


def has_free_weapon(state: CollectionState, player: int) -> bool:
    return state.has("Progressive Sword", player) or state.has("Magic Rod", player) or state.has("Boomerang", player) or state.has("Hookshot", player)


# If the player has access to farm enough rupees to afford a game, we assume that they can keep beating the game
def can_farm_rupees(state: CollectionState, player: int) -> bool:
    return has_free_weapon(state, player) and (state.has("Can Play Trendy Game", player=player) or state.has("RAFT", player=player))


class LinksAwakeningRegion(Region):
    dungeon_index = None
    ladxr_region = None

    def __init__(self, name, ladxr_region, hint, player, world):
        super().__init__(name, player, world, hint)
        if ladxr_region:
            self.ladxr_region = ladxr_region
            if ladxr_region.dungeon:
                self.dungeon_index = ladxr_region.dungeon


def translate_item_name(item):
    if item in ladxr_item_to_la_item_name:
        return ladxr_item_to_la_item_name[item]

    return item


class GameStateAdapater:
    def __init__(self, state, player):
        self.state = state
        self.player = player

    def __contains__(self, item):
        if item.endswith("_USED"):
            return False
        if item in ladxr_item_to_la_item_name:
            item = ladxr_item_to_la_item_name[item]

        return self.state.has(item, self.player)

    def get(self, item, default):
        # Don't allow any money usage if you can't get back wasted rupees
        if item == "RUPEES":
            if can_farm_rupees(self.state, self.player):
                return self.state.prog_items[self.player]["RUPEES"]
            return 0
        elif item.endswith("_USED"):
            return 0
        else:
            item = ladxr_item_to_la_item_name[item]
        return self.state.prog_items[self.player].get(item, default)


class LinksAwakeningEntrance(Entrance):
    def __init__(self, player: int, name, region, condition):
        super().__init__(player, name, region)
        if isinstance(condition, str):
            if condition in ladxr_item_to_la_item_name:
                # Test if in inventory
                self.condition = ladxr_item_to_la_item_name[condition]
            else:
                # Event
                self.condition = condition
        elif condition:
            # rewrite condition
            # .copyWithModifiedItemNames(translate_item_name)
            self.condition = condition
        else:
            self.condition = None

    def access_rule(self, state):
        if isinstance(self.condition, str):
            return state.has(self.condition, self.player)
        if self.condition is None:
            return True

        return self.condition.test(GameStateAdapater(state, self.player))


def ladxr_region_to_name(n):
    name = n.name
    if not name:
        if len(n.items) == 1:
            meta = n.items[0].metadata
            name = f"{meta.name} ({meta.area})"
        elif n.dungeon:
            name = f"D{n.dungeon} Room"
        else:
            name = "No Name"

    return name


def create_regions_from_ladxr(player, multiworld, logic):
    tmp = set()

    def print_items(n):
        print(f"Creating Region {ladxr_region_to_name(n)}")
        print("Has simple connections:")
        for region, info in n.simple_connections:
            print("  " + ladxr_region_to_name(region) + " | " + str(info))
        print("Has gated connections:")

        for region, info in n.gated_connections:
            print("  " + ladxr_region_to_name(region) + " | " + str(info))

        print("Has Locations:")
        for item in n.items:
            print("  " + str(item.metadata))
        print()

    used_names = {}

    regions = {}

    # Create regions
    for l in logic.location_list:
        # Temporarily uniqueify the name, until all regions are named
        name = ladxr_region_to_name(l)
        index = used_names.get(name, 0) + 1
        used_names[name] = index
        if index != 1:
            name += f" {index}"

        r = LinksAwakeningRegion(
            name=name, ladxr_region=l, hint="", player=player, world=multiworld)
        r.locations += [LinksAwakeningLocation(player, r, i) for i in l.items]
        regions[l] = r

    for ladxr_location in logic.location_list:
        for connection_location, connection_condition in ladxr_location.simple_connections + ladxr_location.gated_connections:
            region_a = regions[ladxr_location]
            region_b = regions[connection_location]
            # TODO: This name ain't gonna work for entrance rando, we need to cross reference with logic.world.overworld_entrance
            entrance = LinksAwakeningEntrance(
                player, f"{region_a.name} -> {region_b.name}", region_a, connection_condition)
            region_a.exits.append(entrance)
            entrance.connect(region_b)

    return list(regions.values())


class ConnectorInfo:
    def __init__(self, entrances, oneway=False, castle_button=False) -> None:
        self.entrances = entrances
        self.oneway = oneway
        self.castle_button = castle_button

connector_info = [
    ConnectorInfo(("fire_cave_entrance", "fire_cave_exit")),
    ConnectorInfo(("left_to_right_taltalentrance", "left_taltal_entrance"), True),
    ConnectorInfo(("obstacle_cave_entrance", "obstacle_cave_outside_chest", "obstacle_cave_exit")),
    ConnectorInfo(("papahl_entrance", "papahl_exit")),
    ConnectorInfo(("multichest_left", "multichest_right", "multichest_top")),
    ConnectorInfo(("right_taltal_connector1", "right_taltal_connector2")),
    ConnectorInfo(("right_taltal_connector3", "right_taltal_connector4"), True),
    ConnectorInfo(("right_taltal_connector5", "right_taltal_connector6")),
    ConnectorInfo(("writes_cave_left", "writes_cave_right")),
    ConnectorInfo(("raft_return_enter", "raft_return_exit"), True),
    ConnectorInfo(("toadstool_entrance", "toadstool_exit")),
    ConnectorInfo(("graveyard_cave_left", "graveyard_cave_right")),
    ConnectorInfo(("castle_main_entrance", "castle_upper_left"), castle_button=True),
    ConnectorInfo(("castle_secret_entrance", "castle_secret_exit")),
    ConnectorInfo(("papahl_house_left", "papahl_house_right")),
    ConnectorInfo(("prairie_right_cave_top", "prairie_right_cave_bottom", "prairie_right_cave_high")),
    ConnectorInfo(("prairie_to_animal_connector", "animal_to_prairie_connector")),
    ConnectorInfo(("d6_connector_entrance", "d6_connector_exit")),
    ConnectorInfo(("richard_house", "richard_maze")),
    ConnectorInfo(("prairie_madbatter_connector_entrance", "prairie_madbatter_connector_exit"))
    ]
