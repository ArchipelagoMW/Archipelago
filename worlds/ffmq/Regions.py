import yaml
from pathlib import Path
from BaseClasses import Region, MultiWorld, Entrance, Location, LocationProgressType
from worlds.generic.Rules import add_rule
from .Items import item_groups, yaml_item
from copy import deepcopy
import pkgutil

# base_path = Path(__file__).parent
# file_path = (base_path / "data/rooms.yaml").resolve()
rooms = yaml.load(pkgutil.get_data(__name__, "data/rooms.yaml"), yaml.Loader)

# battlefields = [
#     {"name": "Battlefield - Level Forest",
#      "object_id": 0x01,
#      "type": "Battlefield",
#      "region": "Earth Region"},
#     {"name": "Battlefield - West Sand",
#      "object_id": 0x02,
#      "type": "Battlefield",
#      "region": "Earth Region"},
#     {"name": "Battlefield - East Sand",
#      "object_id": 0x03,
#      "type": "Battlefield",
#      "region": "Earth Region"},
#     {"name": "Battlefield - Sand Door",
#      "object_id": 0x04,
#      "type": "Battlefield",
#      "region": "Water Region"},
#     {"name": "Battlefield - Lake Corner",
#      "object_id": 0x05,
#      "type": "Battlefield",
#      "region": "Water Region"},
#     {"name": "Battlefield - Aquaria",
#      "object_id": 0x06,
#      "type": "Battlefield",
#      "region": "Water Region"},
#     {"name": "Battlefield - Wintry Cave South",
#      "object_id": 0x07,
#      "type": "Battlefield",
#      "region": "Water Region"},
#     {"name": "Battlefield - Wintry Cave West",
#      "object_id": 0x08,
#      "type": "Battlefield",
#      "region": "Water Region"},
#     {"name": "Battlefield - Waterfall",
#      "object_id": 0x09,
#      "type": "Battlefield",
#      "region": "Water Region"},
#     {"name": "Battlefield - Frozen Strip East",
#      "object_id": 0x0A,
#      "type": "Battlefield",
#      "region": "Frozen Strip"},
#     {"name": "Battlefield - Frozen Strip West",
#      "object_id": 0x0B,
#      "type": "Battlefield",
#      "region": "Frozen Strip"},
#     {"name": "Battlefield - Earthquake Shelf South",
#      "object_id": 0x0C,
#      "type": "Battlefield",
#      "region": "Fire Region"},
#     {"name": "Battlefield - Earthquake Shelf Center",
#      "object_id": 0x0D,
#      "type": "Battlefield",
#      "region": "Fire Region"},
#     {"name": "Battlefield - Earthquake Shelf North",
#      "object_id": 0x0E,
#      "type": "Battlefield",
#      "region": "Fire Region"},
#     {"name": "Battlefield - Boulder Path",
#      "object_id": 0x0F,
#      "type": "Battlefield",
#      "region": "Fire Region"},
#     {"name": "Battlefield - Earthquake Plains",
#      "object_id": 0x10,
#      "type": "Battlefield",
#      "region": "Fire Region"},
#     {"name": "Battlefield - Earthquake Hills",
#      "object_id": 0x11,
#      "type": "Battlefield",
#      "region": "Fire Region"},
#     {"name": "Battlefield - Volcano",
#      "object_id": 0x12,
#      "type": "Battlefield",
#      "region": "Volcano Battlefield"},
#     {"name": "Battlefield - Ocean View West",
#      "object_id": 0x13,
#      "type": "Battlefield",
#      "region": "Wind Region"},
#     {"name": "Battlefield - Ocean View East",
#      "object_id": 0x14,
#      "type": "Battlefield",
#      "region": "Wind Region"},
#
# ]

# file_path = (base_path / "data/shufflingdata.yaml").resolve()
# with open(file_path) as file:
#     shuffling_data = yaml.load(file, yaml.Loader)
# file_path = (base_path / "data/entrancespairs.yaml").resolve()
# with open(file_path) as file:
#     entrance_pairs = yaml.load(file, yaml.Loader)
#
# teleports_to = {}
# dead_ends = []
# connectors = []
# branches = []
#
#
# for room in rooms:
#     for link in room["links"]:
#         if "teleporter" in link:
#             if link["target_room"] not in teleports_to:
#                 teleports_to[link["target_room"]] = []
#             teleports_to[link["target_room"]].append(link["teleporter"])
#     # if len(room["links"]) == 1:
#     #     dead_ends.append(room["id"])
#     # elif len(room["links"]) == 2:
#     #     connectors.append(room["id"])
#     # else:
#     #     branches.append(room["id"])
#
# room_sets = []
# entrance_pairs_copy = deepcopy(entrance_pairs)
# def add_room(room_set, rooms, id):
#     for room in room_sets:
#         if id in room:
#             break
#     else:
#         for room in rooms:
#             if room["id"] == id:
#                 break
#         else:
#             raise Exception
#     if room in rooms:
#         rooms.remove(room)
#     room_set.append(room["id"])
#     for link in room["links"]:
#         if link["target_room"] not in room_set:
#             if "teleporter" not in link or link["entrance"] in shuffling_data["fixed_entrances"]:
#                 add_room(room_set, rooms, link["target_room"])
#         # for pair in entrance_pairs_copy:
#         #     if link["entrance"] in pair:
#         #         pair.remove(link["entrance"])
#         #         add_room()
#
#
# rooms_copy = deepcopy(rooms)
#
# while rooms_copy:
#     room_set = []
#     add_room(room_set, rooms_copy, rooms_copy[0]["id"])
#     room_sets.append(room_set)
#
# breakpoint()

object_id_table = {}
object_type_table = {}
offset = {"Chest": 0x420000, "Box": 0x420000, "NPC": 0x420000 + 300, "BattlefieldItem": 0x420000 + 350}
for room in rooms:
    for object in room["game_objects"]:
        if "Hero Chest" in object["name"] or object["type"] == "Trigger":
            continue
        if object["type"] in ("BattlefieldItem", "BattlefieldXp", "BattlefieldGp"):
            object_type_table[object["name"]] = "BattlefieldItem"
        elif object["type"] in ("Chest", "NPC", "Box"):
            #     location_table[object["name"]] = index
            object_type_table[object["name"]] = object["type"]
        object_id_table[object["name"]] = object["object_id"]
        #     index += 1
# for battlefield in battlefields:
    #location_table[battlefield["name"]] = offset["Battlefield"] + battlefield["object_id"]
    # object_id_table[battlefield["name"]] = battlefield["object_id"]
    # object_type_table[battlefield["name"]] = "Battlefield"
location_table = {loc_name: offset[object_type_table[loc_name]] + obj_id for loc_name, obj_id in
                  object_id_table.items()}


ow_regions = {
    "Earth Region": ([*range(445, 450)], ([2, 6], [25, 0], [31, 0], [36, 0], [37, 0]), [*range(1, 4)]),
    "Water Region": ([*range(450, 454), *range(455, 457)], ([4, 6], [13, 6], [8, 6], [49, 0], [53, 0], [56, 0]), [*range(4, 10)]),
    "Fire Region": ([*range(460, 466)], ([6, 6], [9, 6], [98, 0], [16, 6], [103, 0], [104, 0]), [*range(12, 18)]),
    "Wind Region": ([*range(466, 475)], ([3, 6], [140, 0], [142, 0], [18, 6], [173, 0], [174, 0], [10, 6], [184, 0]), [*range(19, 21)]),
    "Frozen Strip": ([*range(458, 460)], ([5, 6], [15, 6]), [*range(10, 12)]),
    "Volcano Battlefield": ([], [], [18]),
    "Spencer's Place": ([457], ([7, 6])),
    "Ship Dock Region": ([475, 477], ([17, 6])),
    "Life Temple Region": ([454], [[14, 6]]),
    "Light Temple Region": ([477], ([19, 6])),
    "Mac's Ship": ([*range(478, 480)], ([37, 8])),
    "Doom Castle": ([476], ([1, 6])),
}

weapons = ("Claw", "Bomb", "Sword", "Axe")


def process_rules(spot, access):
    for weapon in weapons:
        if weapon in access:
            add_rule(spot, lambda state, w=weapon: state.has_any(item_groups[w + "s"], spot.player))
    access = [yaml_item(rule) for rule in access if rule not in weapons]
    add_rule(spot, lambda state: state.has_all(access, spot.player))


def create_region(world: MultiWorld, player: int, name: str, room_id=None, locations=None, links=None):
    if links is None:
        links = []
    ret = Region(name, player, world)
    if locations:
        for location in locations:
            location.parent_region = ret
            ret.locations.append(location)
    ret.links = links
    ret.id = room_id
    return ret


def create_regions(self):
    menu_region = create_region(self.multiworld, self.player, "Menu")
    self.multiworld.regions.append(menu_region)
    # menu_region.locations.append(FFMQLocation(self.player, "Starting Weapon", None, "Trigger",
    #     event=self.create_item(self.multiworld.starting_weapon[self.player].current_key.title().replace("_", " "))))
    # menu_region.locations[-1].parent_region = menu_region
    # menu_region.locations.append(FFMQLocation(self.player, "Starting Armor", None, "Trigger",
    #                                           event=self.create_item("Steel Armor")))
    # menu_region.locations[-1].parent_region = menu_region
    # if self.multiworld.sky_coin_mode[self.player] == "start_with":
    #     menu_region.locations.append(FFMQLocation(self.player, "Starting Coin", None, "Trigger",
    #                                               event=self.create_item("Sky Coin")))
    #     menu_region.locations[-1].parent_region = menu_region
    # if self.multiworld.map_shuffle[self.player]:
    #     self.rooms = rooms.deepcopy()
    #     local_connectors = connectors.copy()
    #     local_branches = branches.copy()
    #     local_dead_ends = dead_ends.copy()
    #
    #     # dungeon floor shuffle
    #     if self.multiworld.map_shuffle[self.player] in ("everything", "dungeons", "overworld_and_dungeons"):
    #         map_sets = [[] for _ in range(35)]
    #         while branches:
    #             map = self.random.randint(len(map_sets))


    for room in rooms:
        if room["id"] == 0:
            for region in ow_regions:
                self.multiworld.regions.append(create_region(self.multiworld, self.player, region, 0,
                    [], [link for link in room["links"] if link["entrance"] in ow_regions[region][0]]))
        else:
            self.multiworld.regions.append(create_region(self.multiworld, self.player, room["name"], room["id"],
                [FFMQLocation(self.player, object["name"], location_table[object["name"]] if object["name"] in
                location_table else None, object["type"], object["access"],
                self.create_item(yaml_item(object["on_trigger"][0])) if object["type"] == "Trigger" else None) for
                object in room["game_objects"] if "Hero Chest" not in object["name"] and (object["type"] != "Box" or
                self.multiworld.brown_boxes[self.player] == "include")], room["links"]))

    if self.multiworld.shuffle_battlefield_rewards[self.player]:
        item_battlefields = self.multiworld.random.sample(list(range(1, 21)), 5)
    else:
        item_battlefields = [2, 6, 10, 13, 16]

    for battlefield in rooms[0]["game_objects"]:
        if battlefield["object_id"] in item_battlefields:
            for region_name in ow_regions:
                if battlefield["object_id"] in ow_regions[region_name][2]:
                    break
            location = FFMQLocation(self.player, battlefield["name"], location_table[battlefield["name"]], "BattlefieldItem")
            region = self.multiworld.get_region(region_name, self.player)
            location.parent_region = region
            region.locations.append(location)

    dark_king_room = self.multiworld.get_region("Doom Castle Dark King Room", self.player)
    dark_king = FFMQLocation(self.player, "Dark King", None, "Trigger", [])
    dark_king.parent_region = dark_king_room
    dark_king.place_locked_item(self.create_item("Dark King"))
    dark_king_room.locations.append(dark_king)

    ow_rules = {
        "Earth Region": lambda state: True,
        "Water Region": lambda state: state.has("Sand Coin", self.player) or state.has_all(
            ["River Coin", "Dualhead Hydra", "Summer Aquaria"], self.player),
        "Spencer's Place": lambda state: state.has_all(["Sun Coin", "Rainbow Bridge"], self.player),
        "Frozen Strip": lambda state: state.has_all(["Sand Coin", "Wakewater", "Summer Aquaria"], self.player) \
            or state.has_all(["River Coin", "Dualhead Hydra", "Summer Aquaria"], self.player),
        "Fire Region": lambda state: state.has("River Coin", self.player) or state.has_all(
            ["Sand Coin", "Dualhead Hydra", "Summer Aquaria"], self.player),
        "Wind Region": lambda state: state.has("Sun Coin", self.player),
        "Mac's Ship": lambda state: state.has_all(["Ship Dock Access", "Ship Liberated"], self.player),
        "Life Temple Region": lambda state: False,
        "Light Temple Region": lambda state: False,
        "Ship Dock Region": lambda state: False,
        "Doom Castle": lambda state: state.has_all(
            ["Ship Dock Access", "Ship Steering Wheel", "Ship Loaned"], self.player),
        "Volcano Battlefield": lambda state: state.has_all(["River Coin", "Dualhead Hydra"], self.player) or
                                             state.has_all(["Sand Coin", "Summer Aquaria"], self.player)
    }

    for region in ow_regions:
        connection = Entrance(self.player, f"Enter Overworld Subregion: {region}", menu_region)
        connection.connect(self.multiworld.get_region(region, self.player))
        connection.access_rule = ow_rules[region]
        menu_region.exits.append(connection)

    for region in self.multiworld.get_regions(self.player):
        for link in region.links:
            if link["target_room"] == 0:
                for sub_region, c in ow_regions.items():
                    if link["teleporter"] in c[1]:
                        connection = Entrance(self.player, f"{region.name} to {sub_region}", region)
                        region.exits.append(connection)
                        connection.connect(self.multiworld.get_region(sub_region, self.player))
                        if link["access"]:
                            process_rules(connection, link["access"])
                        continue
            for connect_room in self.multiworld.get_regions(self.player):
                if connect_room.id == link["target_room"]:
                    connection = Entrance(self.player, f"{region.name} to {connect_room.name}", region)

                    if link["access"]:
                        process_rules(connection, link["access"])
                    region.exits.append(connection)
                    connection.connect(connect_room)
                    break

    # prioritized_locations = []
    # non_prioritized_locations = []
    # for location in self.multiworld.get_locations(self.player):
    #     if (location.type == "Battlefield" and self.multiworld.prioritize_battlefields[self.player] or location.type ==
    #             "NPC" and self.multiworld.prioritize_npcs[self.player] or location.type == "Chest" and
    #             self.multiworld.prioritize_chests[self.player]):
    #         prioritized_locations.append(location)
    #     elif location.type == "Box":
    #         non_prioritized_locations.append(location)
    # if prioritized_locations:
    #     self.multiworld.random.shuffle(prioritized_locations)
    #     self.multiworld.random.shuffle(non_prioritized_locations)
    #     non_prioritized_locations = non_prioritized_locations[:len(prioritized_locations) * 3]
    #     friendly = 2 if self.multiworld.logic[self.player] == "friendly" else 0
    #     useful_locations = prioritized_locations[int(len(prioritized_locations) / 2) + friendly:]
    #     prioritized_locations = prioritized_locations[:int(len(prioritized_locations) / 2) + friendly]
    #     for location in prioritized_locations:
    #         location.progress_type = LocationProgressType.PRIORITY
    #     for location in non_prioritized_locations:
    #         location.progress_type = LocationProgressType.EXCLUDED
    #     self.multiworld.ffmq_useful_locations += useful_locations


def set_rules(self) -> None:
    self.multiworld.completion_condition[self.player] = lambda state: state.has("Dark King", self.player)

    # need to add this to aquaria and fireburg bosses if they're in foresta region when entrance shuffle added
    def hard_boss_logic(state):
        return state.has_all(["River Coin", "Sand Coin"], self.player)

    add_rule(self.multiworld.get_location("Pazuzu 1F", self.player), hard_boss_logic)
    add_rule(self.multiworld.get_location("Gidrah", self.player), hard_boss_logic)
    add_rule(self.multiworld.get_location("Dullahan", self.player), hard_boss_logic)

    if self.multiworld.logic[self.player] == "friendly":
        process_rules(self.multiworld.get_entrance("Earth Region to Bone Dungeon 1F", self.player),
                      ["Bomb"])
        process_rules(self.multiworld.get_entrance("Water Region to Wintry Cave 1F - East Ledge", self.player),
                      ["Bomb", "Claw"])
        process_rules(self.multiworld.get_entrance("Water Region to Ice Pyramid 1F Maze Lobby", self.player),
                      ["Bomb", "Claw"])
        process_rules(self.multiworld.get_entrance("Fire Region to Mine Exterior North West Platforms", self.player),
                      ["MegaGrenade", "Claw", "Reuben1"])
        process_rules(self.multiworld.get_entrance("Fire Region to Lava Dome Inner Ring Main Loop", self.player),
                      ["MegaGrenade"])
        process_rules(self.multiworld.get_entrance("Wind Region to Giant Tree 1F Main Area", self.player),
                      ["DragonClaw", "Axe"])
        process_rules(self.multiworld.get_entrance("Wind Region to Mount Gale", self.player),
                      ["DragonClaw"])
        process_rules(self.multiworld.get_entrance("Wind Region to Pazuzu Tower 1F Main Lobby", self.player),
                      ["DragonClaw", "Bomb"])
        # currently these entrances have the same name. probably should fix that
        process_rules(self.multiworld.get_region("Mac's Ship", self.player).exits[0],
                 ["DragonClaw", "CaptainCap"])
        process_rules(self.multiworld.get_region("Mac's Ship", self.player).exits[1],
                 ["DragonClaw", "CaptainCap"])
        for region in self.multiworld.get_regions(self.player):
            if "Ice Pyramid" in region.name:
                new_rule = "Magic Mirror"
            elif "Volcano" in region.name:
                new_rule = "Mask"
            else:
                continue
            for location in region.locations:
                add_rule(location, lambda state, item=new_rule: state.has(item, self.player))
            for entrance in region.exits:
                add_rule(entrance, lambda state, item=new_rule: state.has(item, self.player))
    elif self.multiworld.logic[self.player] == "expert":
        if self.multiworld.map_shuffle[self.player] == "none" and not self.multiworld.crest_shuffle[self.player]:
            inner_room = self.multiworld.get_region("Wintry Temple Inner Room", self.player)
            connection = Entrance(self.player, "Sealed Temple Exit Trick", inner_room)
            connection.connect(self.multiworld.get_region("Wintry Temple Outer Room", self.player))
            connection.access_rule = lambda state: state.has("Exit Book", self.player)
            inner_room.exits.append(connection)
        for region in ow_regions:
            for entrance in self.multiworld.get_region(region, self.player).entrances:
                if entrance.parent_region.name != "Menu":
                    entrance.access_rule = lambda state: False

    if self.multiworld.sky_coin_mode[self.player] == "shattered_sky_coin":
        logic_coins = [16, 24, 32, 32, 38][self.multiworld.shattered_sky_coin_quantity[self.player].value]
        self.multiworld.get_entrance("Focus Tower 1F SkyCoin Room to Doom Castle Corridor of Destiny", self.player).access_rule = \
            lambda state: state.has("Sky Fragment", self.player, logic_coins)
    elif self.multiworld.sky_coin_mode[self.player] == "save_the_crystals":
        self.multiworld.get_entrance("Focus Tower 1F SkyCoin Room to Doom Castle Corridor of Destiny", self.player).access_rule = \
            lambda state: state.can_reach("Bone Dungeon B2 - Flamerus Rex Chest", "Location", self.player) and \
            state.has("Dualhead Hydra", self.player) and state.has("Ice Golem", self.player) and \
            state.can_reach("Pazuzu's Tower 7F - Pazuzu Chest", "Location", self.player)


class FFMQLocation(Location):
    game = "Final Fantasy Mystic Quest"

    def __init__(self, player, name, address, loc_type, access=None, event=None):
        super(FFMQLocation, self).__init__(
            player, name,
            address
        )
        self.type = loc_type
        if access:
            process_rules(self, access)
        if event:
            self.place_locked_item(event)
