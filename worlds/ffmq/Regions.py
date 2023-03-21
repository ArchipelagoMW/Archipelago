import yaml
from pathlib import Path
from BaseClasses import Region, MultiWorld, Entrance, Location, LocationProgressType
from worlds.generic.Rules import add_rule, exclusion_rules
from .Items import item_groups

base_path = Path(__file__).parent
file_path = (base_path / "data/rooms.yaml").resolve()
with open(file_path) as file:
    rooms = yaml.load(file, yaml.Loader)

location_table = {}
index = 0x420000
for room in rooms:
    for object in room["game_objects"]:
        if object["type"] in ("Chest", "NPC", "Battlefield", "Box") and "Hero Chest" not in object["name"]:
            location_table[object["name"]] = index
            index += 1


def add_spaces(text):
    return "".join([(" " + c if (c.isupper() or c.isnumeric()) and not (text[i-1].isnumeric() and c == "F") else c) for
                    i, c in enumerate(text)]).strip()


ow_regions = {
    "Earth Region": ([*range(445, 450)], ([2, 6], [25, 0], [31, 0], [36, 0], [37, 0]), [2]),
    "Water Region": ([*range(450, 454), *range(455, 457)], ([4, 6], [13, 6], [8, 6], [49, 0], [53, 0], [56, 0]), (6, 10)),
    "Fire Region": ([*range(460, 466)], ([6, 6], [9, 6], [98, 0], [16, 6], [103, 0], [104, 0]), (13, 16)),
    "Wind Region": ([*range(466, 475)], ([3, 6], [140, 0], [142, 0], [18, 6], [173, 0], [174, 0], [10, 6], [184, 0]), ()),
    "Frozen Strip": ([*range(458, 460)], ([5, 6], [15, 6]), ()),
    "Spencer's Place": ([457], ([7, 6]), ()),
    "Inaccessible": ([454, 475, 477], ([19, 6], [17, 6], [14, 6]), ()),
    "Mac's Ship": ([*range(478, 480)], ([37, 8]), ()),
    "Doom Castle": ([476], ([1, 6]), ())
}

weapons = ("Claw", "Bomb", "Sword", "Axe")


def process_rules(spot, access):
    for weapon in weapons:
        if weapon in access:
            add_rule(spot, lambda state, w=weapon: state.has_any(item_groups[w + "s"], spot.player))
    access = [add_spaces(rule) for rule in access if rule not in weapons]
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
    self.multiworld.regions.append(create_region(self.multiworld, self.player, "Menu"))

    for room in rooms:
        if room["id"] == 0:
            for region in ow_regions:
                self.multiworld.regions.append(create_region(self.multiworld, self.player, region, 0,
                    [FFMQLocation(self.player, object["name"], object["object_id"], object["type"]) for object in
                    room["game_objects"] if object["object_id"] in ow_regions[region][2]], [link for link in
                    room["links"] if link["entrance"] in ow_regions[region][0]]))
        else:
            if self.multiworld.doom_castle[self.player] != "standard" and room["name"] in ("Doom Castle Ice Floor",
                                                                                           "Doom Castle Lava Floor",
                                                                                           "Doom Castle Sky Floor"):
                continue
            self.multiworld.regions.append(create_region(self.multiworld, self.player, room["name"], room["id"],
                 [FFMQLocation(self.player, object["name"], location_table[object["name"]] if object["name"] in
                 location_table else None, object["type"], object["access"],
                 self.create_item(add_spaces(object["on_trigger"][0])) if object["type"] == "Trigger" else None) for
                 object in room["game_objects"] if "Hero Chest" not in object["name"] and (object["type"] != "Box" or
                 self.multiworld.brown_boxes[self.player] == "include")], room["links"]))

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
        "Frozen Strip": lambda state: state.has_all(["Sand Coin", "Wake Water", "Summer Aquaria"], self.player) \
            or state.has_all(["River Coin", "Dualhead Hydra", "Summer Aquaria"], self.player),
        "Fire Region": lambda state: state.has("River Coin", self.player) or state.has_all(
            ["Sand Coin", "Dualhead Hydra", "Summer Aquaria"], self.player),
        "Wind Region": lambda state: state.has("Sun Coin", self.player),
        "Mac's Ship": lambda state: state.has_all(["Ship Dock Access", "Ship Liberated"], self.player),
        "Inaccessible": lambda state: False,
        "Doom Castle": lambda state: state.has_all(
            ["Ship Dock Access", "Ship Steering Wheel", "Ship Loaned"], self.player),
        }

    menu_region = self.multiworld.get_region("Menu", self.player)
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

    prioritized_locations = []
    non_prioritized_locations = []
    for location in self.multiworld.get_locations(self.player):
        if (location.type == "Battlefield" and self.multiworld.prioritize_battlefields[self.player] or location.type ==
                "NPC" and self.multiworld.prioritize_npcs[self.player] or location.type == "Chest" and
                self.multiworld.prioritize_chests[self.player]):
            prioritized_locations.append(location)
        elif location.type == "Box":
            non_prioritized_locations.append(location)
    if prioritized_locations:
        self.multiworld.random.shuffle(prioritized_locations)
        self.multiworld.random.shuffle(non_prioritized_locations)
        non_prioritized_locations = non_prioritized_locations[:len(prioritized_locations) * 3]
        friendly = 2 if self.multiworld.logic[self.player] == "friendly" else 0
        useful_locations = prioritized_locations[int(len(prioritized_locations) / 2) + friendly:]
        prioritized_locations = prioritized_locations[:int(len(prioritized_locations) / 2) + friendly]
        for location in prioritized_locations:
            location.progress_type = LocationProgressType.PRIORITY
        for location in non_prioritized_locations:
            location.progress_type = LocationProgressType.EXCLUDED
        self.multiworld.ffmq_useful_locations += useful_locations


def set_rules(self) -> None:

    self.multiworld.completion_condition[self.player] = lambda state: state.has("Dark King", self.player)
    # if self.multiworld.doom_castle[self.player] != "Standard"
    # self.multiworld.

    if self.multiworld.logic[self.player] == "friendly":
        for region in self.multiworld.get_regions(self.player):
            new_rules = []
            if "Ice Pyramid" in region.name:
                new_rules.append("Magic Mirror")
            elif "Volcano" in region.name:
                new_rules.append("Mask")

            if self.multiworld.map_shuffle[self.player] != "none" and self.multiworld.map_shuffle[self.player] != "overworld":
                if "Bone Dungeon" in region.name:
                    new_rules.append("Bomb")
                elif "Wintry Cave" in region.name or "Ice Pyramid" in region.name:
                    new_rules += ["Bomb", "Claw"]
                elif "Mine" in region.name:
                    new_rules += ["Mega Grenade", "Claw", "Reuben 1"]
                elif "Lava Dome" in region.name:
                    new_rules.append("Mega Grenade")
                elif "Giant Tree" in region.name:
                    new_rules += ["Axe", "Dragon Claw"]
                elif "Mount Gale" in region.name:
                    new_rules.append("Dragon Claw")
                elif "Pazuzu" in region.name:
                    new_rules += ["Dragon Claw", "Bomb"]
                elif "Mac" in region.name:
                    new_rules += ["Dragon Claw", "Captain Cap"]
            for location in region.locations:
                process_rules(location, new_rules)
    elif self.multiworld.logic[self.player] == "expert":
        if self.multiworld.map_shuffle[self.player] == "none" and not self.multiworld.crest_shuffle[self.player]:
            inner_room = self.multiworld.get_region("Wintry Temple Inner Room", self.player)
            connection = Entrance(self.player, "Sealed Temple Exit Trick", inner_room)
            connection.connect(self.multiworld.get_region("Wintry Temple Outer Room", self.player))
            connection.access_rule = lambda state: state.has("Exit Book", self.player)
            inner_room.exits.append(connection)
        for region in ow_regions:
            for entrance in self.multiworld.get_region(region, self.player).entrances:
                if entrance.parent_region != "Menu":
                    entrance.access_rule = lambda state: False

    if self.multiworld.sky_coin_mode[self.player] == "shattered":
        logic_coins = [16, 24, 32, 32, 38][self.multiworld.shattered_sky_coin_quantity[self.player].value]
        self.multiworld.get_entrance("Focus Tower 1F SkyCoin Room to Doom Castle Corridor of Destiny").access_rule = \
            lambda state: state.has("Sky Fragment", self.player, logic_coins)
    elif self.multiworld.sky_coin_mode[self.player] == "save_the_crystals":
        self.multiworld.get_entrance("Focus Tower 1F SkyCoin Room to Doom Castle Corridor of Destiny").access_rule = \
            lambda state: state.can_reach("Rex Chest", "Location", self.player) and \
                          state.has("DualheadHydra", self.player) and \
                          state.can_reach("Pazuzu Chest", "Location", self.player) and \
                          state.has("IceGolem", self.player)




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
