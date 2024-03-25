from typing import Dict, List, Set, Any, Callable
from collections import Counter
from BaseClasses import Region, Entrance, Location, Item, Tutorial, ItemClassification, CollectionState
from worlds.AutoWorld import World, WebWorld
from .Items import base_id, item_table, group_table, tears_set, reliquary_set
from .Locations import location_names
from .Rules import BlasRules
from worlds.generic.Rules import set_rule, add_rule
from .Options import BlasphemousOptions
from .Vanilla import unrandomized_dict, junk_locations, thorn_set, skill_dict
from .region_data import regions, locations, transitions

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
    location_name_to_id = {loc: (base_id + index) for index, loc in enumerate(location_names.values())}

    item_name_groups = group_table
    options_dataclass = BlasphemousOptions
    options: BlasphemousOptions

    required_client_version = (0, 4, 2)


    def __init__(self, multiworld, player):
        super(BlasphemousWorld, self).__init__(multiworld, player)
        self.start_room: str = "D17Z01S01"
        self.door_connections: Dict[str, str] = {}


    #def set_rules(self):
        #rules(self, self.door_connections)


    def create_item(self, name: str) -> "BlasphemousItem":
        item_id: int = self.item_name_to_id[name]
        id = item_id - base_id

        return BlasphemousItem(name, item_table[id]["classification"], item_id, player=self.player)


    def create_event(self, event: str):
        return BlasphemousItem(event, ItemClassification.progression_skip_balancing, None, self.player)


    def get_filler_item_name(self) -> str:
        return self.multiworld.random.choice(tears_set)


    def generate_early(self):
        multiworld = self.multiworld
        player = self.player

        if not self.options.starting_location.randomized:
            if self.options.starting_location == 6 and self.options.difficulty < 2:
                raise Exception(f"[Blasphemous - '{multiworld.get_player_name(player)}'] {self.options.starting_location}"
                                " cannot be chosen if Difficulty is lower than Hard.")

            if (self.options.starting_location == 0 or self.options.starting_location == 6) \
                and self.options.dash_shuffle:
                    raise Exception(f"[Blasphemous - '{multiworld.get_player_name(player)}'] {self.options.starting_location}"
                                    " cannot be chosen if Shuffle Dash is enabled.")
            
            if self.options.starting_location == 3 and self.options.wall_climb_shuffle:
                raise Exception(f"[Blasphemous - '{multiworld.get_player_name(player)}'] {self.options.starting_location}"
                                " cannot be chosen if Shuffle Wall Climb is enabled.")
        else:
            locations: List[int] = [ 0, 1, 2, 3, 4, 5, 6 ]
            invalid: bool = False

            if self.options.difficulty < 2:
                locations.remove(6)

            if self.options.dash_shuffle:
                locations.remove(0)
                if 6 in locations:
                    locations.remove(6)

            if self.options.wall_climb_shuffle:
                locations.remove(3)

            if self.options.starting_location == 6 and self.options.difficulty < 2:
                invalid = True

            if (self.options.starting_location == 0 or self.options.starting_location == 6) \
                and self.options.dash_shuffle:
                    invalid = True
            
            if self.options.starting_location == 3 and self.options.wall_climb_shuffle:
                invalid = True

            if invalid:
                self.options.starting_location = multiworld.random.choice(locations)
            
        
        if not self.options.dash_shuffle:
            multiworld.push_precollected(self.create_item("Dash Ability"))

        if not self.options.wall_climb_shuffle:
            multiworld.push_precollected(self.create_item("Wall Climb Ability"))

        if self.options.skip_long_quests:
            for loc in junk_locations:
                multiworld.exclude_locations[player].value.add(loc)

        start_rooms: Dict[int, str] = {
            0: "D17Z01S01",
            1: "D01Z02S01",
            2: "D02Z03S09",
            3: "D03Z03S11",
            4: "D04Z03S01",
            5: "D06Z01S09",
            6: "D20Z02S09"
        }

        self.start_room = start_rooms[self.options.starting_location]


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

        for item, count in self.options.start_inventory.value.items():
            for _ in range(count):
                skipped_items.append(item)
                junk += 1

        skipped_items.extend(unrandomized_dict.values())

        if self.options.thorn_shuffle == 2:
            for _ in range(8):
                skipped_items.append("Thorn Upgrade")

        if self.options.dash_shuffle:
            skipped_items.append(to_remove[removed])
            removed += 1
        elif not self.options.dash_shuffle:
            skipped_items.append("Dash Ability")

        if self.options.wall_climb_shuffle:
            skipped_items.append(to_remove[removed])
            removed += 1
        elif not self.options.wall_climb_shuffle:
            skipped_items.append("Wall Climb Ability")

        if not self.options.reliquary_shuffle:
            skipped_items.extend(reliquary_set)
        elif self.options.reliquary_shuffle:
            for _ in range(3):
                skipped_items.append(to_remove[removed])
                removed += 1

        if not self.options.boots_of_pleading:
            skipped_items.append("Boots of Pleading")

        if not self.options.purified_hand:
            skipped_items.append("Purified Hand of the Nun")

        if self.options.start_wheel:
            skipped_items.append("The Young Mason's Wheel")

        if not self.options.skill_randomizer:
            skipped_items.extend(skill_dict.values())

        counter = Counter(skipped_items)

        pool = []

        for item in item_table:
            count = item["count"] - counter[item["name"]]
            
            if count <= 0:
                continue
            else:
                for _ in range(count):
                    pool.append(self.create_item(item["name"]))

        for _ in range(junk):
            pool.append(self.create_item(self.get_filler_item_name()))

        world.itempool += pool


    def pre_fill(self):
        world = self.multiworld
        player = self.player

        self.place_items_from_dict(unrandomized_dict)

        if self.options.thorn_shuffle == 2:
            self.place_items_from_set(thorn_set, "Thorn Upgrade")

        if self.options.start_wheel:
            world.get_location("Beginning gift", player)\
                .place_locked_item(self.create_item("The Young Mason's Wheel"))

        if not self.options.skill_randomizer:
            self.place_items_from_dict(skill_dict)

        if self.options.thorn_shuffle == 1:
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
        multiworld = self.multiworld
        player = self.player


        for r in regions:
            multiworld.regions.append(Region(r["name"], player, multiworld))

        self.get_region("Menu").add_exits({self.start_room: "New Game"})

        blas_logic = BlasRules(self)

        for r in regions:
            region = multiworld.get_region(r["name"], player)

            for e in r["exits"]:
                region.add_exits({e["target"]})
                if len(e["logic"]) > 0:
                    for logic in e["logic"]:
                        rule: Callable[[CollectionState], bool] = None
                        for string in logic["item_requirements"]:
                            old_rule: Callable[[CollectionState], bool] = rule
                            new_rule: Callable[[CollectionState], bool] = None
                            if (string[0] == "D" and string[3] == "Z" and string[6] == "S")\
                            or (string[0] == "D" and string[3] == "B" and string[4] == "Z" and string[7] == "S"):
                                new_rule = lambda state: state.can_reach_region(string, self.player)
                            else:
                                new_rule = blas_logic.string_rules[string]

                            if rule == None:
                                rule = new_rule
                            else:
                                rule = lambda state: old_rule(state) and new_rule(state)

                        add_rule(self.get_entrance(f"{r['name']} -> {e['target']}"), rule, "or")

            for l in r["locations"]:
                if not self.options.boots_of_pleading and l == "RE401":
                    continue
                if not self.options.purified_hand and l == "RE402":
                    continue
                region.add_locations({location_names[l]: self.location_name_to_id[location_names[l]]}, BlasphemousLocation)

            for t in r["transitions"]:
                if t == r["name"]:
                    continue
                try:
                    region.add_exits({t})
                except KeyError:
                    multiworld.regions.append(Region(t, player, multiworld))
                    region.add_exits({t})


        for l in locations:
            if not self.options.boots_of_pleading and l["name"] == "RE401":
                continue
            if not self.options.purified_hand and l["name"] == "RE402":
                continue
            location = self.get_location(location_names[l["name"]])
            if len(l["logic"]) > 0:
                for index, logic in enumerate(l["logic"]):
                    rule: Callable[[CollectionState], bool] = None
                    for string in logic["item_requirements"]:
                        old_rule: Callable[[CollectionState], bool] = rule
                        new_rule: Callable[[CollectionState], bool] = None
                        if (string[0] == "D" and string[3] == "Z" and string[6] == "S")\
                        or (string[0] == "D" and string[3] == "B" and string[4] == "Z" and string[7] == "S"):
                            new_rule = lambda state: state.can_reach_region(string, self.player)
                        else:
                            new_rule = blas_logic.string_rules[string]

                        if rule == None:
                            rule = new_rule
                        else:
                            rule = lambda state: old_rule(state) and new_rule(state)
                    
                    if index == 0:
                        set_rule(location, rule)
                    else:
                        add_rule(location, rule, "or")

        for t in transitions:
            if len(t["logic"]) > 0:
                for index, logic in enumerate(t["logic"]):
                    rule: Callable[[CollectionState], bool] = None
                    for string in logic["item_requirements"]:
                        old_rule: Callable[[CollectionState], bool] = rule
                        new_rule: Callable[[CollectionState], bool] = None
                        if (string[0] == "D" and string[3] == "Z" and string[6] == "S")\
                        or (string[0] == "D" and string[3] == "B" and string[4] == "Z" and string[7] == "S"):
                            new_rule = lambda state: state.can_reach_region(string, self.player)
                        else:
                            new_rule = blas_logic.string_rules[string]

                        if rule == None:
                            rule = new_rule
                        else:
                            rule = lambda state: old_rule(state) and new_rule(state)

                    for entrance in self.get_region(t["name"]).entrances:
                        if index == 0:
                            set_rule(entrance, rule)
                        else:
                            add_rule(entrance, rule, "or")

        from Utils import visualize_regions
        visualize_regions(self.get_region("Menu"), "blasphemous_regions.puml")
        
        victory = Location(player, "His Holiness Escribar", None, self.get_region("D07Z01S03"))
        victory.place_locked_item(self.create_event("Victory"))
        self.get_region("D07Z01S03").locations.append(victory)

        if self.options.ending == 1:
            set_rule(victory, lambda state: state.has("Thorn Upgrade", player, 8))
        elif self.options.ending == 2:
            set_rule(victory, lambda state: state.has("Thorn Upgrade", player, 8) and
                state.has("Holy Wound of Abnegation", player))

        multiworld.completion_condition[self.player] = lambda state: state.has("Victory", player)
        

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

        if self.options.thorn_shuffle == 2:
            thorns = False

        for loc in world.get_filled_locations(player):
            if loc.item.code == None:
                continue
            else:
                data = {
                    "id": [i for i in location_names if location_names[i] == loc.name][0],
                    "ap_id": loc.address,
                    "name": loc.item.name,
                    "player_name": world.player_name[loc.item.player],
                    "type": int(loc.item.classification)
                }

                locations.append(data)

        config = {
            "LogicDifficulty": self.options.difficulty.value,
            "StartingLocation": self.options.starting_location.value,
            "VersionCreated": "AP",
            
            "UnlockTeleportation": bool(self.options.prie_dieu_warp.value),
            "AllowHints": bool(self.options.corpse_hints.value),
            "AllowPenitence": bool(self.options.penitence.value),
            
            "ShuffleReliquaries": bool(self.options.reliquary_shuffle.value),
            "ShuffleBootsOfPleading": bool(self.options.boots_of_pleading.value),
            "ShufflePurifiedHand": bool(self.options.purified_hand.value),
            "ShuffleDash": bool(self.options.dash_shuffle.value),
            "ShuffleWallClimb": bool(self.options.wall_climb_shuffle.value),
            
            "ShuffleSwordSkills": bool(self.options.wall_climb_shuffle.value),
            "ShuffleThorns": thorns,
            "JunkLongQuests": bool(self.options.skip_long_quests.value),
            "StartWithWheel": bool(self.options.start_wheel.value),

            "EnemyShuffleType": self.options.enemy_randomizer.value,
            "MaintainClass": bool(self.options.enemy_groups.value),
            "AreaScaling": bool(self.options.enemy_scaling.value),

            "BossShuffleType": 0,
            "DoorShuffleType": 0
        }
    
        slot_data = {
            "locations": locations,
            "doors": doors,
            "cfg": config,
            "ending": self.options.ending.value,
            "death_link": bool(self.options.death_link.value)
        }
    
        return slot_data


class BlasphemousItem(Item):
    game: str = "Blasphemous"


class BlasphemousLocation(Location):
    game: str = "Blasphemous"