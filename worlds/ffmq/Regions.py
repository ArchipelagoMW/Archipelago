
from BaseClasses import Region, MultiWorld, Entrance, Location, LocationProgressType
from worlds.generic.Rules import add_rule
from .Items import item_groups, yaml_item
import pkgutil
import yaml

rooms = yaml.load(pkgutil.get_data(__name__, "data/rooms.yaml"), yaml.Loader)

entrance_pairs = yaml.load(pkgutil.get_data(__name__, "data/entrancespairs.yaml"), yaml.Loader)

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
            object_type_table[object["name"]] = object["type"]
        object_id_table[object["name"]] = object["object_id"]

location_table = {loc_name: offset[object_type_table[loc_name]] + obj_id for loc_name, obj_id in
                  object_id_table.items()}

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


def get_entrance_to(entrance_to):
    for room in rooms:
        if room["id"] == entrance_to["target_room"]:
            for link in room["links"]:
                if link["target_room"] == entrance_to["room"]:
                    return link
    else:
        raise Exception(f"Did not find entrance {entrance_to}")


crest_dead_ends = (51, 52, 53, 108, 158, 396, 397)
dupe_rooms = ((336, 171), (175, 96))


def crest_shuffle(self):
    def pair(entrance_a, entrance_b, access_rule, barred=False):
        entrance_a_to = get_entrance_to(entrance_a)
        entrance_b_to = get_entrance_to(entrance_b)
        entrance_a["teleporter"] = entrance_b_to["teleporter"]
        entrance_b["teleporter"] = entrance_a_to["teleporter"]
        entrance_a["target_room"] = entrance_b_to["target_room"]
        entrance_b["target_room"] = entrance_a_to["target_room"]
        entrance_a["access"][0] = access_rule
        entrance_b["access"][0] = access_rule
        if barred:
            entrance_a["access"].append("Barred")
            entrance_b["access"].append("Barred")
        if "room" in entrance_a:
            del entrance_a["room"]
        if "room" in entrance_b:
            del entrance_b["room"]

    if self.multiworld.crest_shuffle[self.player]:
        crest_tiles = (["MobiusCrest"] * 4) + (["LibraCrest"] * 2) + (["GeminiCrest"] * 3)
        self.multiworld.random.shuffle(crest_tiles)
        crest_dead_end_entrances = []
        crest_open_entrances = []
        for room in self.rooms:
            for link in room["links"]:
                if ("GeminiCrest" in link["access"] or "LibraCrest" in link["access"] or "MobiusCrest" in
                        link["access"]) and "Spencer" not in room["name"]:
                    link["room"] = room["id"]
                    if link["entrance"] in crest_dead_ends:
                        crest_dead_end_entrances.append(link)
                    else:
                        crest_open_entrances.append(link)
        dupe_room_crests = [self.multiworld.random.choice(crest_tiles), self.multiworld.random.choice(crest_tiles)]
        while dupe_room_crests == ["GeminiCrest", "GeminiCrest"] or dupe_room_crests == ["LibraCrest", "LibraCrest"]:
            dupe_room_crests = [self.multiworld.random.choice(crest_tiles), self.multiworld.random.choice(crest_tiles)]
        self.multiworld.random.shuffle(crest_open_entrances)
        # there are two different sets of "dupe rooms" - rooms which use the same tile map. These must have the same
        # crest tiles set up for both instances. We have chosen two sets of crest tiles to be used for the dupe room
        # sets. If these are not the same crest, then we need to ensure we aren't going to try to connect a room from
        # one set to another.
        if dupe_room_crests[0] != dupe_room_crests[1]:
            while ((crest_open_entrances[-1]["entrance"] in dupe_rooms[0] and crest_open_entrances[-2]["entrance"]
                    in dupe_rooms[1]) or (crest_open_entrances[-1]["entrance"] in dupe_rooms[1] and
                    crest_open_entrances[-2]["entrance"] in dupe_rooms[0]) or (crest_open_entrances[-3]["entrance"]
                    in dupe_rooms[0] and crest_open_entrances[-4]["entrance"] in dupe_rooms[1]) or
                    (crest_open_entrances[-3]["entrance"] in dupe_rooms[1] and crest_open_entrances[-4]["entrance"]
                    in dupe_rooms[0])):
                self.multiworld.random.shuffle(crest_open_entrances)

        crest_tiles.remove(dupe_room_crests[0])
        crest_tiles.remove(dupe_room_crests[1])
        # we need to remove a second copy of the chosen dupe room crests unless two dupe rooms from the same set are
        # going to be connected.
        for x, dupe_room in enumerate(dupe_rooms):
            for i in (-1, -3):
                if crest_open_entrances[i]["entrance"] in dupe_room and crest_open_entrances[i-1]["entrance"] in dupe_room:
                    break
            else:
                crest_tiles.remove(dupe_room_crests[x])
        # crest_open_entrances.sort(key=lambda i: i["entrance"] not in dupe_rooms[0]
        #                               and i["entrance"] not in dupe_rooms[1])
        for entrance_a in crest_dead_end_entrances:
            entrance_b = crest_open_entrances.pop(0)
            for i, dupe_room in enumerate(dupe_rooms):
                if entrance_b["entrance"] in dupe_room:
                    crest_tile = dupe_room_crests[i]
                    break
            else:
                crest_tile = crest_tiles.pop()
            pair(entrance_a, entrance_b, crest_tile)
        for _ in range(2):
            entrance_a = crest_open_entrances.pop(0)
            entrance_b = crest_open_entrances.pop(0)
            for i, dupe_room in enumerate(dupe_rooms):
                if entrance_a["entrance"] in dupe_room or entrance_b["entrance"] in dupe_room:
                    crest_tile = dupe_room_crests[i]
                    break
            else:
                crest_tile = crest_tiles.pop()
            pair(entrance_a, entrance_b, crest_tile, barred=self.multiworld.logic[self.player] != "expert")


non_shuffled_things = ("FocusTowerForesta", "FocusTowerAquaria", "LifeTemple", "FocusTowerFrozen", "FocusTowerFireburg",
                       "FocusTowerWindia", "GiantTree", "SpencersPlace", "ShipDock", "MacsShip", "LightTemple",
                       "DoomCastle", "MacsShipDoom")


def overworld_shuffle(self):

    overworld_things = []

    for room in self.rooms:
        if "type" in room and room["type"] == "Subregion":
            if "game_objects" in room:
                for object in room["game_objects"]:
                    if "location" in object:
                        overworld_things.append(object.copy())
            for object in room["links"]:
                if "location" in object and object["location"] not in non_shuffled_things:
                    overworld_things.append(object.copy())
    self.multiworld.random.shuffle(overworld_things)

    def swap_ow_things(room_id, links, objects):
        thing = overworld_things.pop()
        thing["location_slot"] = object["location_slot"]
        if "target_room" in thing:
            links.append(thing)
            target_room = thing["target_room"]
            for room in self.rooms:
                if room["id"] == target_room:
                    for link in room["links"]:
                        if link["target_room"] >= 220 <= 231:
                            link["target_room"] = room_id
        else:
            objects.append(thing)

    for room in self.rooms:
        if "type" in room and room["type"] == "Subregion":
            modified_objects = []
            modified_links = []
            if "game_objects" in room:
                for object in room["game_objects"]:
                    if "location" in object:
                        swap_ow_things(room["id"], modified_links, modified_objects)

                    else:
                        modified_objects.append(object)
            for link in room["links"]:
                if "location" in link and link["location"] not in non_shuffled_things:
                    swap_ow_things(room["id"], modified_links, modified_objects)
                else:
                    modified_links.append(link)
            room["game_objects"] = modified_objects
            room["links"] = modified_links

def create_regions(self):

    crest_shuffle(self)

    overworld_shuffle(self)

    menu_region = create_region(self.multiworld, self.player, "Menu")
    self.multiworld.regions.append(menu_region)

    battlefields = []
    if self.multiworld.shuffle_battlefield_rewards[self.player]:
        battlefield_types = (["BattlefieldItem"] * 5) + (["BattlefieldXp"] * 10) + (["BattlefieldGp"] * 5)
        self.multiworld.random.shuffle(battlefield_types)

    for room in self.rooms:
        if "type" not in room or room["type"] != "Subregion":
            continue
        for object in room["game_objects"]:
            if object["type"].startswith("Battlefield"):
                if self.multiworld.shuffle_battlefield_rewards[self.player]:
                    object["type"] = battlefield_types.pop()
                battlefields.append(object)

    for room in self.rooms:
        self.multiworld.regions.append(create_region(self.multiworld, self.player, room["name"], room["id"],
            [FFMQLocation(self.player, object["name"], location_table[object["name"]] if object["name"] in
            location_table else None, object["type"], object["access"],
            self.create_item(yaml_item(object["on_trigger"][0])) if object["type"] == "Trigger" else None) for
            object in room["game_objects"] if "Hero Chest" not in object["name"] and (object["type"] != "Box" or
            self.multiworld.brown_boxes[self.player] == "include")], room["links"]))

    for battlefield in battlefields:
        if battlefield["type"] == "BattlefieldItem":
            continue
        elif battlefield["type"] == "BattlefieldXp":
            item = self.create_item("XP")
        elif battlefield["type"] == "BattlefieldGp":
            item = self.create_item("GP")
        self.multiworld.get_location(battlefield["name"], self.player).place_locked_item(item)

    dark_king_room = self.multiworld.get_region("Doom Castle Dark King Room", self.player)
    dark_king = FFMQLocation(self.player, "Dark King", None, "Trigger", [])
    dark_king.parent_region = dark_king_room
    dark_king.place_locked_item(self.create_item("Dark King"))
    dark_king_room.locations.append(dark_king)

    connection = Entrance(self.player, f"Enter Overworld", menu_region)
    connection.connect(self.multiworld.get_region("Subregion Foresta", self.player))
    menu_region.exits.append(connection)

    for region in self.multiworld.get_regions(self.player):
        for link in region.links:
            for connect_room in self.multiworld.get_regions(self.player):
                if connect_room.id == link["target_room"]:
                    connection = Entrance(self.player, f"{region.name} to {connect_room.name}", region)

                    if link["access"]:
                        process_rules(connection, link["access"])
                    region.exits.append(connection)
                    connection.connect(connect_room)
                    break



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
