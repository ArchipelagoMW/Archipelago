from typing import Dict, List, Set, Any
from collections import Counter
from BaseClasses import Region, Location, Item, Tutorial, ItemClassification
from Options import OptionError
from worlds.AutoWorld import World, WebWorld
from .Items import base_id, item_table, group_table, tears_list, reliquary_set
from .Locations import location_names
from .Rules import BlasRules
from worlds.generic.Rules import set_rule
from .Options import BlasphemousOptions, blas_option_groups
from .Vanilla import unrandomized_dict, junk_locations, thorn_set, skill_dict
from .region_data import regions, locations

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
    option_groups = blas_option_groups


class BlasphemousWorld(World):
    """
    Blasphemous is a challenging Metroidvania set in the cursed land of Cvstodia. Play as the Penitent One, trapped
    in an endless cycle of death and rebirth, and free the world from its terrible fate in your quest to break
    your eternal damnation!
    """

    game = "Blasphemous"
    web = BlasphemousWeb()

    item_name_to_id = {item["name"]: (base_id + index) for index, item in enumerate(item_table)}
    location_name_to_id = {loc: (base_id + index) for index, loc in enumerate(location_names.values())}

    item_name_groups = group_table
    options_dataclass = BlasphemousOptions
    options: BlasphemousOptions

    required_client_version = (0, 4, 7)


    def __init__(self, multiworld, player):
        super(BlasphemousWorld, self).__init__(multiworld, player)
        self.start_room: str = "D17Z01S01"
        self.disabled_locations: List[str] = []


    def create_item(self, name: str) -> "BlasphemousItem":
        item_id: int = self.item_name_to_id[name]
        id = item_id - base_id

        return BlasphemousItem(name, item_table[id]["classification"], item_id, player=self.player)


    def create_event(self, event: str):
        return BlasphemousItem(event, ItemClassification.progression_skip_balancing, None, self.player)


    def get_filler_item_name(self) -> str:
        return self.random.choice(tears_list)


    def generate_early(self):
        if not self.options.starting_location.randomized:
            if self.options.starting_location == "mourning_havoc" and self.options.difficulty < 2:
                raise OptionError(f"[Blasphemous - '{self.player_name}'] "
                                f"{self.options.starting_location} cannot be chosen if Difficulty is lower than Hard.")

            if (self.options.starting_location == "brotherhood" or self.options.starting_location == "mourning_havoc") \
                and self.options.dash_shuffle:
                    raise OptionError(f"[Blasphemous - '{self.player_name}'] "
                                    f"{self.options.starting_location} cannot be chosen if Shuffle Dash is enabled.")
            
            if self.options.starting_location == "grievance" and self.options.wall_climb_shuffle:
                raise OptionError(f"[Blasphemous - '{self.player_name}'] "
                                f"{self.options.starting_location} cannot be chosen if Shuffle Wall Climb is enabled.")
        else:
            locations: List[int] = [ 0, 1, 2, 3, 4, 5, 6 ]

            if self.options.difficulty < 2:
                locations.remove(6)

            if self.options.dash_shuffle:
                locations.remove(0)
                if 6 in locations:
                    locations.remove(6)

            if self.options.wall_climb_shuffle:
                locations.remove(3)

            if self.options.starting_location.value not in locations:
                self.options.starting_location.value = self.random.choice(locations)
            
        
        if not self.options.dash_shuffle:
            self.multiworld.push_precollected(self.create_item("Dash Ability"))

        if not self.options.wall_climb_shuffle:
            self.multiworld.push_precollected(self.create_item("Wall Climb Ability"))

        if not self.options.boots_of_pleading:
            self.disabled_locations.append("RE401")

        if not self.options.purified_hand:
            self.disabled_locations.append("RE402")

        if self.options.skip_long_quests:
            for loc in junk_locations:
                self.options.exclude_locations.value.add(loc)

        start_rooms: Dict[int, str] = {
            0: "D17Z01S01",
            1: "D01Z02S01",
            2: "D02Z03S09",
            3: "D03Z03S11",
            4: "D04Z03S01",
            5: "D06Z01S09",
            6: "D20Z02S09"
        }

        self.start_room = start_rooms[self.options.starting_location.value]


    def create_items(self):
        removed: int = 0
        to_remove: List[str] = [
            "Tears of Atonement (250)",
            "Tears of Atonement (300)",
            "Tears of Atonement (500)",
            "Tears of Atonement (500)",
            "Tears of Atonement (500)"
        ]

        skipped_items = []

        skipped_items.extend(unrandomized_dict.values())

        if self.options.thorn_shuffle == "vanilla":
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

        self.multiworld.itempool += pool

        self.place_items_from_dict(unrandomized_dict)

        if self.options.thorn_shuffle == "vanilla":
            self.place_items_from_set(thorn_set, "Thorn Upgrade")

        if self.options.start_wheel:
            self.get_location("Beginning gift").place_locked_item(self.create_item("The Young Mason's Wheel"))

        if not self.options.skill_randomizer:
            self.place_items_from_dict(skill_dict)

        if self.options.thorn_shuffle == "local_only":
            self.options.local_items.value.add("Thorn Upgrade")
        

    def place_items_from_set(self, location_set: Set[str], name: str):
        for loc in location_set:
            self.get_location(loc).place_locked_item(self.create_item(name))

    
    def place_items_from_dict(self, option_dict: Dict[str, str]):
        for loc, item in option_dict.items():
            self.get_location(loc).place_locked_item(self.create_item(item))


    def create_regions(self) -> None:
        multiworld = self.multiworld
        player = self.player

        created_regions: List[str] = []

        for r in regions:
            multiworld.regions.append(Region(r["name"], player, multiworld))
            created_regions.append(r["name"])

        self.get_region("Menu").add_exits({self.start_room: "New Game"})

        blas_logic = BlasRules(self)

        for r in regions:
            region = self.get_region(r["name"])

            for e in r["exits"]:
                region.add_exits({e["target"]}, {e["target"]: blas_logic.load_rule(True, r["name"], e)})

            for l in [l for l in r["locations"] if l not in self.disabled_locations]:
                region.add_locations({location_names[l]: self.location_name_to_id[location_names[l]]}, BlasphemousLocation)

            for t in r["transitions"]:
                if t == r["name"]:
                    continue
                
                if t in created_regions:
                    region.add_exits({t})
                else:
                    multiworld.regions.append(Region(t, player, multiworld))
                    created_regions.append(t)
                    region.add_exits({t})


        for l in [l for l in locations if l["name"] not in self.disabled_locations]:
            location = self.get_location(location_names[l["name"]])
            set_rule(location, blas_logic.load_rule(False, l["name"], l))

        for rname, ename in blas_logic.indirect_conditions:
            self.multiworld.register_indirect_condition(self.get_region(rname), self.get_entrance(ename))
        #from Utils import visualize_regions
        #visualize_regions(self.get_region("Menu"), "blasphemous_regions.puml")
        
        victory = Location(player, "His Holiness Escribar", None, self.get_region("D07Z01S03[W]"))
        victory.place_locked_item(self.create_event("Victory"))
        self.get_region("D07Z01S03[W]").locations.append(victory)

        if self.options.ending == "ending_a":
            set_rule(victory, lambda state: state.has("Thorn Upgrade", player, 8))
        elif self.options.ending == "ending_c":
            set_rule(victory, lambda state: state.has("Thorn Upgrade", player, 8) and
                state.has("Holy Wound of Abnegation", player))

        multiworld.completion_condition[self.player] = lambda state: state.has("Victory", player)
    
    
    def fill_slot_data(self) -> Dict[str, Any]:
        slot_data: Dict[str, Any] = {}
        doors: Dict[str, str] = {}
        thorns: bool = True

        if self.options.thorn_shuffle == "vanilla":
            thorns = False

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
            "locationinfo": [{"gameId": loc, "apId": (base_id + index)} for index, loc in enumerate(location_names)],
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
