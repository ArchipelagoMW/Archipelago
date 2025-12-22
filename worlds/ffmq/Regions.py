from BaseClasses import Region, MultiWorld, Entrance, Location, LocationProgressType, ItemClassification
from worlds.generic.Rules import add_rule
from .data.rooms import rooms, entrances
from .Items import item_groups, yaml_item

entrance_names = {entrance["id"]: entrance["name"] for entrance in entrances}

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
crest_warps = [51, 52, 53, 76, 96, 108, 158, 171, 175, 191, 275, 276, 277, 308, 334, 336, 396, 397]


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


def create_regions(self):

    menu_region = create_region(self.multiworld, self.player, "Menu")
    self.multiworld.regions.append(menu_region)

    for room in self.rooms:
        self.multiworld.regions.append(create_region(self.multiworld, self.player, room["name"], room["id"],
            [FFMQLocation(self.player, object["name"], location_table[object["name"]] if object["name"] in
            location_table else None, object["type"], object["access"],
            self.create_item(yaml_item(object["on_trigger"][0])) if object["type"] == "Trigger" else None) for object in
            room["game_objects"] if "Hero Chest" not in object["name"] and object["type"] not in ("BattlefieldGp",
            "BattlefieldXp") and not (object["name"] == "Kaeli Companion" and not object["on_trigger"])],
            room["links"]))

    dark_king_room = self.multiworld.get_region("Doom Castle Dark King Room", self.player)
    dark_king = FFMQLocation(self.player, "Dark King", None, "Trigger", [])
    dark_king.parent_region = dark_king_room
    dark_king.place_locked_item(self.create_item("Dark King"))
    dark_king_room.locations.append(dark_king)

    connection = Entrance(self.player, f"Enter Overworld", menu_region)
    connection.connect(self.multiworld.get_region("Overworld", self.player))
    menu_region.exits.append(connection)

    for region in self.multiworld.get_regions(self.player):
        for link in region.links:
            for connect_room in self.multiworld.get_regions(self.player):
                if connect_room.id == link["target_room"]:
                    connection = Entrance(self.player, entrance_names[link["entrance"]] if "entrance" in link and
                                          link["entrance"] != -1 else f"{region.name} to {connect_room.name}", region)
                    if "entrance" in link and link["entrance"] != -1:
                        if link["entrance"] in crest_warps:
                            if self.options.crest_shuffle:
                                self.multiworld.spoiler.set_entrance(entrance_names[link["entrance"]],
                                                                     connect_room.name, 'both', self.player)
                        elif "Subregion" in region.name and self.options.overworld_shuffle:
                            self.multiworld.spoiler.set_entrance(
                                entrance_names[link["entrance"]].replace("Overworld", f"Overworld {region.name}"),
                                connect_room.name, 'both', self.player)
                        elif self.options.map_shuffle:
                            self.multiworld.spoiler.set_entrance(entrance_names[link["entrance"]],
                                                                 connect_room.name, 'both', self.player)

                    if link["access"]:
                        process_rules(connection, link["access"])
                    region.exits.append(connection)
                    connection.connect(connect_room)
                    break


non_dead_end_crest_rooms = [
    'Libra Temple', 'Aquaria Gemini Room', "GrenadeMan's Mobius Room", 'Fireburg Gemini Room',
    'Sealed Temple', 'Alive Forest', 'Kaidge Temple Upper Ledge',
    'Windia Kid House Basement', 'Windia Old People House Basement'
]

non_dead_end_crest_warps = [
    'Libra Temple - Libra Tile Script', 'Aquaria Gemini Room - Gemini Script',
    'GrenadeMan Mobius Room - Mobius Teleporter Script', 'Fireburg Gemini Room - Gemini Teleporter Script',
    'Sealed Temple - Gemini Tile Script', 'Alive Forest - Libra Teleporter Script',
    'Alive Forest - Gemini Teleporter Script', 'Alive Forest - Mobius Teleporter Script',
    'Kaidge Temple - Mobius Teleporter Script', 'Windia Kid House Basement - Mobius Teleporter',
    'Windia Old People House Basement - Mobius Teleporter Script',
]


vendor_locations = ["Aquaria - Vendor", "Fireburg - Vendor", "Windia - Vendor"]


def set_rules(self) -> None:
    self.multiworld.completion_condition[self.player] = lambda state: state.has("Dark King", self.player)

    def hard_boss_logic(state):
        return state.has_all(["River Coin", "Sand Coin"], self.player)

    add_rule(self.multiworld.get_location("Pazuzu 1F", self.player), hard_boss_logic)
    add_rule(self.multiworld.get_location("Gidrah", self.player), hard_boss_logic)
    add_rule(self.multiworld.get_location("Dullahan", self.player), hard_boss_logic)

    if self.options.map_shuffle:
        for boss in ("SnowCrab", "Ice Golem", "Jinn", "Medusa", "Dualhead Hydra"):
            if boss == "SnowCrab":
                if "SnowCrab" not in self.multiworld.regions.location_cache[self.player]:
                    boss = "Freezer Crab"
            loc = self.multiworld.get_location(boss, self.player)
            checked_regions = {loc.parent_region}

            def check_foresta(region):
                if region.name == "Subregion Foresta":
                    add_rule(loc, hard_boss_logic)
                    return True
                elif "Subregion" in region.name:
                    return True
                for entrance in region.entrances:
                    if entrance.parent_region not in checked_regions:
                        checked_regions.add(entrance.parent_region)
                        if check_foresta(entrance.parent_region):
                            return True
            check_foresta(loc.parent_region)

    if self.options.map_shuffle or self.options.crest_shuffle:
        process_rules(self.multiworld.get_entrance("Subregion Frozen Fields to Subregion Aquaria", self.player),
                      ["SummerAquaria"])

    if self.options.logic == "friendly":
        process_rules(self.multiworld.get_entrance("Overworld - Ice Pyramid", self.player),
                      ["MagicMirror"])
        process_rules(self.multiworld.get_entrance("Overworld - Volcano", self.player),
                      ["Mask"])
        if self.options.map_shuffle:
            process_rules(self.multiworld.get_entrance("Overworld - Bone Dungeon", self.player),
                          ["Bomb"])
            process_rules(self.multiworld.get_entrance("Overworld - Wintry Cave", self.player),
                          ["Bomb", "Claw"])
            process_rules(self.multiworld.get_entrance("Overworld - Ice Pyramid", self.player),
                          ["Bomb", "Claw"])
            process_rules(self.multiworld.get_entrance("Overworld - Mine", self.player),
                          ["MegaGrenade", "Claw"])
            process_rules(self.multiworld.get_entrance("Overworld - Lava Dome", self.player),
                          ["MegaGrenade"])
            process_rules(self.multiworld.get_entrance("Overworld - Giant Tree", self.player),
                          ["DragonClaw", "Axe"])
            process_rules(self.multiworld.get_entrance("Overworld - Mount Gale", self.player),
                          ["DragonClaw"])
            process_rules(self.multiworld.get_entrance("Overworld - Pazuzu Tower", self.player),
                          ["DragonClaw", "Bomb"])
            process_rules(self.multiworld.get_entrance("Overworld - Mac Ship", self.player),
                          ["DragonClaw", "CaptainCap"])
            process_rules(self.multiworld.get_entrance("Overworld - Mac Ship Doom", self.player),
                          ["DragonClaw", "CaptainCap"])

    if self.options.logic == "expert":
        if self.options.map_shuffle == "none" and not self.options.crest_shuffle:
            inner_room = self.multiworld.get_region("Wintry Temple Inner Room", self.player)
            connection = Entrance(self.player, "Sealed Temple Exit Trick", inner_room)
            connection.connect(self.multiworld.get_region("Wintry Temple Outer Room", self.player))
            connection.access_rule = lambda state: state.has("Exit Book", self.player)
            inner_room.exits.append(connection)
    else:
        for crest_warp in non_dead_end_crest_warps:
            entrance = self.multiworld.get_entrance(crest_warp, self.player)
            if entrance.connected_region.name in non_dead_end_crest_rooms:
                entrance.access_rule = lambda state: False

    if self.options.sky_coin_mode == "shattered_sky_coin":
        logic_coins = [16, 24, 32, 32, 38][self.options.shattered_sky_coin_quantity.value]
        self.multiworld.get_entrance("Focus Tower 1F - Sky Door", self.player).access_rule = \
            lambda state: state.has("Sky Fragment", self.player, logic_coins)
    elif self.options.sky_coin_mode == "save_the_crystals":
        self.multiworld.get_entrance("Focus Tower 1F - Sky Door", self.player).access_rule = \
            lambda state: state.has_all(["Flamerus Rex", "Dualhead Hydra", "Ice Golem", "Pazuzu"], self.player)
    elif self.options.sky_coin_mode in ("standard", "start_with"):
        self.multiworld.get_entrance("Focus Tower 1F - Sky Door", self.player).access_rule = \
            lambda state: state.has("Sky Coin", self.player)

    if self.options.enemies_density == "none":
        for location in vendor_locations:
            if self.options.accessibility == "full":
                self.multiworld.get_location(location, self.player).progress_type = LocationProgressType.EXCLUDED
            else:
                self.multiworld.get_location(location, self.player).access_rule = lambda state: False


def stage_set_rules(multiworld):
    # If there's no enemies, there's no repeatable income sources
    no_enemies_players = [player for player in multiworld.get_game_players("Final Fantasy Mystic Quest")
                          if multiworld.worlds[player].options.enemies_density == "none"]
    if (len([item for item in multiworld.itempool if item.excludable]) >
        len([player for player in no_enemies_players
             if multiworld.worlds[player].options.accessibility != "minimal"]) * 3):
        for player in no_enemies_players:
            for location in vendor_locations:
                if multiworld.worlds[player].options.accessibility == "full":
                    multiworld.get_location(location, player).progress_type = LocationProgressType.EXCLUDED
                else:
                    multiworld.get_location(location, player).access_rule = lambda state: False


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
