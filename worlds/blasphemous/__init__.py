from typing import Dict, List, Set, Any
from collections import Counter
from BaseClasses import Region, Entrance, Location, Item, Tutorial, ItemClassification
from worlds.AutoWorld import World, WebWorld
from .Items import base_id, item_table, group_table, tears_set, reliquary_set, event_table
from .Locations import location_table
from .Rooms import room_table, door_table
from .Rules import rules
from worlds.generic.Rules import set_rule, add_rule
from .Options import blasphemous_options
from .Vanilla import unrandomized_dict, junk_locations, thorn_set, skill_dict


class BlasphemousWeb(WebWorld):
    theme = "stone"
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Blasphemous randomizer connected to an Archipelago Multiworld",
        "English",
        "setup_en.md",
        "setup/en",
        ["TRPG"]
    )]


class BlasphemousWorld(World):
    """
    Blasphemous is a challenging Metroidvania set in the cursed land of Cvstodia. Play as the Penitent One, trapped
    in an endless cycle of death and rebirth, and free the world from it's terrible fate in your quest to break
    your eternal damnation!
    """

    game: str = "Blasphemous"
    web = BlasphemousWeb()
    data_version = 2

    item_name_to_id = {item["name"]: (base_id + index) for index, item in enumerate(item_table)}
    location_name_to_id = {loc["name"]: (base_id + index) for index, loc in enumerate(location_table)}
    location_name_to_game_id = {loc["name"]: loc["game_id"] for loc in location_table}

    item_name_groups = group_table
    option_definitions = blasphemous_options

    required_client_version = (0, 4, 2)


    def __init__(self, multiworld, player):
        super(BlasphemousWorld, self).__init__(multiworld, player)
        self.start_room: str = "D17Z01S01"
        self.door_connections: Dict[str, str] = {}


    def set_rules(self):
        rules(self)
        for door in door_table:
            add_rule(self.multiworld.get_location(door["Id"], self.player),
                lambda state: state.can_reach(self.get_connected_door(door["Id"])), self.player)


    def create_item(self, name: str) -> "BlasphemousItem":
        item_id: int = self.item_name_to_id[name]
        id = item_id - base_id

        return BlasphemousItem(name, item_table[id]["classification"], item_id, player=self.player)


    def create_event(self, event: str):
        return BlasphemousItem(event, ItemClassification.progression_skip_balancing, None, self.player)


    def get_filler_item_name(self) -> str:
        return self.multiworld.random.choice(tears_set)


    def generate_early(self):
        world = self.multiworld
        player = self.player

        if not world.starting_location[player].randomized:
            if world.starting_location[player].value == 6 and world.difficulty[player].value < 2:
                raise Exception(f"[Blasphemous - '{world.get_player_name(player)}'] {world.starting_location[player]}"
                                " cannot be chosen if Difficulty is lower than Hard.")

            if (world.starting_location[player].value == 0 or world.starting_location[player].value == 6) \
                and world.dash_shuffle[player]:
                    raise Exception(f"[Blasphemous - '{world.get_player_name(player)}'] {world.starting_location[player]}"
                                    " cannot be chosen if Shuffle Dash is enabled.")
            
            if world.starting_location[player].value == 3 and world.wall_climb_shuffle[player]:
                raise Exception(f"[Blasphemous - '{world.get_player_name(player)}'] {world.starting_location[player]}"
                                " cannot be chosen if Shuffle Wall Climb is enabled.")
        else:
            locations: List[int] = [ 0, 1, 2, 3, 4, 5, 6 ]
            invalid: bool = False

            if world.difficulty[player].value < 2:
                locations.remove(6)

            if world.dash_shuffle[player]:
                locations.remove(0)
                if 6 in locations:
                    locations.remove(6)

            if world.wall_climb_shuffle[player]:
                locations.remove(3)

            if world.starting_location[player].value == 6 and world.difficulty[player].value < 2:
                invalid = True

            if (world.starting_location[player].value == 0 or world.starting_location[player].value == 6) \
                and world.dash_shuffle[player]:
                    invalid = True
            
            if world.starting_location[player].value == 3 and world.wall_climb_shuffle[player]:
                invalid = True

            if invalid:
                world.starting_location[player].value = world.random.choice(locations)
            
        
        if not world.dash_shuffle[player]:
            world.push_precollected(self.create_item("Dash Ability"))

        if not world.wall_climb_shuffle[player]:
            world.push_precollected(self.create_item("Wall Climb Ability"))

        if world.skip_long_quests[player]:
            for loc in junk_locations:
                world.exclude_locations[player].value.add(loc)

        start_rooms: Dict[int, str] = {
            0: "D17Z01S01",
            1: "D01Z02S01",
            2: "D02Z03S09",
            3: "D03Z03S11",
            4: "D04Z03S01",
            5: "D06Z01S09",
            6: "D20Z02S09"
        }

        self.start_room = start_rooms[world.starting_location[player].value]


    def create_items(self):
        world = self.multiworld
        player = self.player

        removed: int = 0
        to_remove: List[str] = [
            "Tears of Atonement (250)",
            "Tears of Atonement (300)",
            "Tears of Atonement (500)",
            "Tears of Atonement (500)",
            "Tears of Atonement (500)"
        ]

        skipped_items = []
        junk: int = 0

        for item, count in world.start_inventory[player].value.items():
            for _ in range(count):
                skipped_items.append(item)
                junk += 1

        skipped_items.extend(unrandomized_dict.values())

        if world.thorn_shuffle[player] == 2:
            for i in range(8):
                skipped_items.append("Thorn Upgrade")

        if world.dash_shuffle[player]:
            skipped_items.append(to_remove[removed])
            removed += 1
        elif not world.dash_shuffle[player]:
            skipped_items.append("Dash Ability")

        if world.wall_climb_shuffle[player]:
            skipped_items.append(to_remove[removed])
            removed += 1
        elif not world.wall_climb_shuffle[player]:
            skipped_items.append("Wall Climb Ability")

        if not world.reliquary_shuffle[player]:
            skipped_items.extend(reliquary_set)
        elif world.reliquary_shuffle[player]:
            for i in range(3):
                skipped_items.append(to_remove[removed])
                removed += 1

        if not world.boots_of_pleading[player]:
            skipped_items.append("Boots of Pleading")

        if not world.purified_hand[player]:
            skipped_items.append("Purified Hand of the Nun")

        if world.start_wheel[player]:
            skipped_items.append("The Young Mason's Wheel")

        if not world.skill_randomizer[player]:
            skipped_items.extend(skill_dict.values())

        counter = Counter(skipped_items)

        pool = []

        for item in item_table:
            count = item["count"] - counter[item["name"]]
            
            if count <= 0:
                continue
            else:
                for i in range(count):
                    pool.append(self.create_item(item["name"]))

        for _ in range(junk):
            pool.append(self.create_item(self.get_filler_item_name()))

        world.itempool += pool


    def pre_fill(self):
        world = self.multiworld
        player = self.player

        self.place_items_from_dict(unrandomized_dict)

        if world.thorn_shuffle[player] == 2:
            self.place_items_from_set(thorn_set, "Thorn Upgrade")

        if world.start_wheel[player]:
            world.get_location("Beginning gift", player)\
                .place_locked_item(self.create_item("The Young Mason's Wheel"))

        if not world.skill_randomizer[player]:
            self.place_items_from_dict(skill_dict)

        if world.thorn_shuffle[player] == 1:
            world.local_items[player].value.add("Thorn Upgrade")
        

    def place_items_from_set(self, location_set: Set[str], name: str):
        for loc in location_set:
            self.multiworld.get_location(loc, self.player)\
                .place_locked_item(self.create_item(name))

    
    def place_items_from_dict(self, option_dict: Dict[str, str]):
        for loc, item in option_dict.items():
            self.multiworld.get_location(loc, self.player)\
                .place_locked_item(self.create_item(item))


    def create_regions(self) -> None:
        player = self.player
        world = self.multiworld
        
        menu_region = Region("Menu", player, world)
        misc_region = Region("Misc", player, world)
        world.regions += [menu_region, misc_region]

        for room in room_table:
            region = Region(room, player, world)
            world.regions.append(region)

        menu_region.add_exits({self.start_room: "New Game"})
        world.get_region(self.start_room, player).add_exits({"Misc": "Misc"})

        for door in door_table:
            if door.get("OriginalDoor") is None:
                continue
            else:
                if not door["Id"] in self.door_connections.keys():
                    self.door_connections[door["Id"]] = door["OriginalDoor"]
                    self.door_connections[door["OriginalDoor"]] = door["Id"]

                parent_region: Region = self.get_room_from_door(door["Id"])
                target_region: Region = self.get_room_from_door(door["OriginalDoor"])
                parent_region.add_exits({
                    target_region.name: door["Id"]
                }, {
                    target_region.name: lambda x: door.get("VisibilityFlags") != 1
                })

        for index, loc in enumerate(location_table):
            if not world.boots_of_pleading[player] and loc["name"] == "BotSS: 2nd meeting with Redento":
                continue
            if not world.purified_hand[player] and loc["name"] == "MoM: Western room ledge":
                continue

            region: Region = world.get_region(loc["room"], player)
            region.add_locations({loc["name"]: base_id + index})
            #id = base_id + location_table.index(loc)
            #reg.locations.append(BlasphemousLocation(player, loc["name"], id, reg))

        for e, r in event_table.items():
            region: Region = world.get_region(r, player)
            event = BlasphemousLocation(player, e, None, region)
            event.show_in_spoiler = False
            event.place_locked_item(self.create_event(e))
            region.locations.append(event)

        for door in door_table:
            region: Region = self.get_room_from_door(self.door_connections[door["Id"]])
            event = BlasphemousLocation(player, door["Id"], None, region)
            event.show_in_spoiler = False
            event.place_locked_item(self.create_event(door["Id"]))
            region.locations.append(event)
        
        victory = Location(player, "His Holiness Escribar", None, world.get_region("D07Z01S03", player))
        victory.place_locked_item(self.create_event("Victory"))
        world.get_region("D07Z01S03", player).locations.append(victory)

        if world.ending[self.player].value == 1:
            set_rule(victory, lambda state: state.has("Thorn Upgrade", player, 8))
        elif world.ending[self.player].value == 2:
            set_rule(victory, lambda state: state.has("Thorn Upgrade", player, 8) and
                state.has("Holy Wound of Abnegation", player))

        world.completion_condition[self.player] = lambda state: state.has("Victory", player)
        

    def get_room_from_door(self, door: str) -> Region:
        return self.multiworld.get_region(door.split("[")[0], self.player)

    
    def get_connected_door(self, door: str) -> Entrance:
        return self.multiworld.get_entrance(self.door_connections[door], self.player)
    
    
    def fill_slot_data(self) -> Dict[str, Any]:
        slot_data: Dict[str, Any] = {}
        locations = []
        doors: Dict[str, str] = {}

        world = self.multiworld
        player = self.player
        thorns: bool = True

        if world.thorn_shuffle[player].value == 2:
            thorns = False

        for loc in world.get_filled_locations(player):
            if loc.item.code == None:
                continue
            else:
                data = {
                    "id": self.location_name_to_game_id[loc.name],
                    "ap_id": loc.address,
                    "name": loc.item.name,
                    "player_name": world.player_name[loc.item.player],
                    "type": int(loc.item.classification)
                }

                locations.append(data)

        config = {
            "LogicDifficulty": world.difficulty[player].value,
            "StartingLocation": world.starting_location[player].value,
            "VersionCreated": "AP",
            
            "UnlockTeleportation": bool(world.prie_dieu_warp[player].value),
            "AllowHints": bool(world.corpse_hints[player].value),
            "AllowPenitence": bool(world.penitence[player].value),
            
            "ShuffleReliquaries": bool(world.reliquary_shuffle[player].value),
            "ShuffleBootsOfPleading": bool(world.boots_of_pleading[player].value),
            "ShufflePurifiedHand": bool(world.purified_hand[player].value),
            "ShuffleDash": bool(world.dash_shuffle[player].value),
            "ShuffleWallClimb": bool(world.wall_climb_shuffle[player].value),
            
            "ShuffleSwordSkills": bool(world.skill_randomizer[player].value),
            "ShuffleThorns": thorns,
            "JunkLongQuests": bool(world.skip_long_quests[player].value),
            "StartWithWheel": bool(world.start_wheel[player].value),

            "EnemyShuffleType": world.enemy_randomizer[player].value,
            "MaintainClass": bool(world.enemy_groups[player].value),
            "AreaScaling": bool(world.enemy_scaling[player].value),

            "BossShuffleType": 0,
            "DoorShuffleType": 0
        }
    
        slot_data = {
            "locations": locations,
            "doors": doors,
            "cfg": config,
            "ending": world.ending[self.player].value,
            "death_link": bool(world.death_link[self.player].value)
        }
    
        return slot_data


class BlasphemousItem(Item):
    game: str = "Blasphemous"


class BlasphemousLocation(Location):
    game: str = "Blasphemous"