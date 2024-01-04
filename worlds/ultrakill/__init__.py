from typing import Dict, Set, List, Any
from BaseClasses import Region, Entrance, Location, Item, Tutorial, ItemClassification
from worlds.AutoWorld import World, WebWorld
from .Items import base_id, item_table, group_table
from .Locations import location_table, event_table, ext_bosses
from .Regions import region_table, secret_levels
from .Rules import rules
from .Options import ultrakill_options, Goal, UnlockType, StartingWeapon
from .Music import multilayer_music, singlelayer_music
from worlds.generic.Rules import set_rule


class UltrakillWeb(WebWorld):
    # theme = ""
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up ULTRAKILL randomizer and connecting to an Archipelago Multiworld",
        "English",
        "setup_en.md",
        "setup/en",
        ["TRPG"]
    )]


class UltrakillWorld(World):
    """description"""

    game = "ULTRAKILL"
    web = UltrakillWeb()

    item_name_to_id = {item["name"]: (base_id + index) for index, item in enumerate(item_table)}
    item_name_to_type = {item["name"]: item["type"] for item in item_table}
    location_name_to_id = {loc["name"]: (base_id + index) for index, loc in enumerate(location_table)}
    location_name_to_game_id = {loc["name"]: loc["game_id"] for loc in location_table}

    item_name_groups = group_table
    option_definitions = ultrakill_options

    goal_name = "6-2"
    start_weapon = "Revolver - Piercer"
    music: Dict[str, str] = {}

    def set_rules(self):    
        rules(self)


    def create_item(self, name: str) -> "UltrakillItem":
        item_id: int = self.item_name_to_id[name]
        id = item_id - base_id

        return UltrakillItem(name, item_table[id]["classification"], item_id, self.player)
    

    def create_event(self, event: str):
        return UltrakillItem(event, ItemClassification.progression_skip_balancing, None, self.player)
    

    def generate_early(self):
        world = self.multiworld
        player = self.player
        
        if not world.include_secret_mission_completion[self.player] and world.goal_requirement[self.player].value > 24:
            print(f"[ULTRAKILL - '{world.get_player_name(player)}'] Secret mission completion is disabled. Goal requirement lowered to 24.")
            world.goal_requirement[self.player].value = 24

        if self.multiworld.starting_weapon[self.player] != StartingWeapon.option_revolver:
            weapons: Set[str] = group_table["start_weapons"]

            if self.multiworld.starting_weapon[self.player] != StartingWeapon.option_revolver and not self.multiworld.start_with_arm[self.player]:
                if "Railcannon - Electric" in weapons:
                    weapons.remove("Railcannon - Electric")
                if "Railcannon - Screwdriver" in weapons:
                    weapons.remove("Railcannon - Screwdriver")
                if "Railcannon - Malicious" in weapons:
                    weapons.remove("Railcannon - Malicious")
                if "Rocket Launcher - Freezeframe" in weapons:
                    weapons.remove("Rocket Launcher - Freezeframe")

            if self.multiworld.start_with_arm[self.player]:
                if "Feedbacker" in weapons:
                    weapons.remove("Feedbacker")

            if not self.multiworld.start_with_arm[self.player] and self.multiworld.starting_weapon[self.player] != StartingWeapon.option_any_weapon_or_arm:
                if "Feedbacker" in weapons:
                    weapons.remove("Feedbacker")

            if self.multiworld.starting_weapon[self.player] != StartingWeapon.option_any_weapon_or_arm:
                if "Knuckleblaster" in weapons:
                    weapons.remove("Knuckleblaster")

            if self.multiworld.randomize_secondary_fire[self.player]:
                if "Rocket Launcher - S.R.S. Cannon" in weapons:
                    weapons.remove("Rocket Launcher - S.R.S. Cannon")
            
            self.start_weapon = self.multiworld.random.choice(weapons)

        if self.multiworld.music_randomizer[self.player]:
            tempDict: Dict[str, str] = {}
            multi1 = []
            multi1.extend(multilayer_music.keys())
            multi2 = [] 
            multi2.extend(multilayer_music.keys())

            while len(multi1) > 0:
                id1 = self.multiworld.random.choice(multi1)
                id2 = self.multiworld.random.choice(multi2)

                tempDict[id1] = id2
                multi1.remove(id1)
                multi2.remove(id2)

            single1 = []
            single1.extend(singlelayer_music.keys())
            single2 = []
            single2.extend(singlelayer_music.keys())

            while len(single1) > 0:
                id1 = self.multiworld.random.choice(single1)
                id2 = self.multiworld.random.choice(single2)

                tempDict[id1] = id2
                single1.remove(id1)
                single2.remove(id2)
            
            tempKeys = list(tempDict.keys())
            tempKeys.sort()
            self.music = {i: tempDict[i] for i in tempKeys}
            #print(self.music)

    
    def write_spoiler_header(self, spoiler_handle):
        if self.multiworld.music_randomizer[self.player]:
            spoiler_handle.write("\nMusic:\n")
            for i, j in self.music.items():
                original: str
                changed: str
                if i in multilayer_music.keys():
                    original = multilayer_music[i]
                elif i in singlelayer_music.keys():
                    original = singlelayer_music[i]
                if j in multilayer_music.keys():
                    changed = multilayer_music[j]
                elif j in singlelayer_music.keys():
                    changed = singlelayer_music[j]
                spoiler_handle.write(f"({i}) {original} -> {changed}\n")


    def create_items(self):
        pool = []

        for item in item_table:
            count = 1

            if item["name"] == self.start_weapon:
                continue
            if self.multiworld.unlock_type[self.player] == UnlockType.option_levels and \
                item["name"] in group_table["layers"] or \
                    (self.goal_name in item["name"] and not "Skull" in item["name"]):
                        continue
            elif self.multiworld.unlock_type[self.player] == UnlockType.option_layers and item["name"] in group_table["levels"]:
                continue
            if not self.multiworld.randomize_skulls[self.player] and "Skull" in item["name"]:
                continue
            if not self.multiworld.randomize_secondary_fire[self.player] and "Secondary Fire" in item["name"]:
                continue
            if self.multiworld.start_with_arm[self.player] and item["name"] == "Feedbacker":
                continue
            if self.multiworld.start_with_slide[self.player] and item["name"] == "Slide":
                continue
            if self.multiworld.start_with_slam[self.player] and item["name"] == "Slam":
                continue
            if item["name"] in group_table["junk"]:
                continue

            if item["name"] == "Stamina Bar":
                count = 3 - self.multiworld.starting_stamina[self.player].value
            if item["name"] == "Wall Jump":
                count = 3 - self.multiworld.starting_walljumps[self.player].value
            if self.multiworld.randomize_skulls[self.player] and item["name"] == "Blue Skull (1-4)":
                count = 4
            if self.multiworld.randomize_skulls[self.player] and item["name"] == "Blue Skull (5-1)":
                count = 3

            if count <= 0:
                continue
            else:
                for i in range(count):
                    pool.append(self.create_item(item["name"]))
        
        junk: int = len(self.multiworld.get_unfilled_locations(self.player)) - (len(pool) + 1)
        #print("unfilled = " + str(len(self.multiworld.get_unfilled_locations(self.player))))
        #print("junk = " + str(junk))

        trap: int = round(junk * (self.multiworld.trap_percent[self.player] / 100))
        filler: int = junk - trap
        #print("trap = " + str(trap))
        #print("filler = " + str(filler))

        for i in range(trap):
            pool.append(self.create_item(self.multiworld.random.choice(group_table["trap"])))

        for i in range(filler):
            pool.append(self.create_item(self.multiworld.random.choice(group_table["filler"])))
            
        self.multiworld.itempool += pool


    def pre_fill(self):
        world = self.multiworld
        player = self.player

        first_loc = world.get_location("0-1: Weapon", player)

        if first_loc.item != None:
            if not first_loc.item.name in group_table["start_weapons"]:
                raise Exception(f"[ULTRAKILL - {world.get_player_name(player)}] "
                                f"'{first_loc.item.name}' is not a valid starting weapon.")
            
            if first_loc.item.name != self.start_weapon:
                print(f"[ULTRAKILL - '{world.get_player_name(player)}'] An item already exists at \"0-1: Weapon\". "
                    "Selected starting weapon is being returned to the item pool.")
                
                world.itempool.append(self.create_item(self.start_weapon))
        else:
            first_loc.place_locked_item(self.create_item(self.start_weapon))


    def create_regions(self):
        
        player = self.player
        world = self.multiworld

        menu = Region("Menu", player, world)

        for number, name in region_table.items():
            r = Region(name, player, world)
            entrance = Entrance(player, "To " + number, menu)
            entrance.connect(r)
            if "S" in number:
                world.get_region(region_table[secret_levels[number]], player).exits.append(entrance)
            else:
                menu.exits.append(entrance)
            exit = Entrance(player, "To Menu", r)
            exit.connect(menu)
            r.exits.append(exit)
            world.regions.append(r)

        world.regions.append(menu)

        if world.goal[player] == Goal.option_1_4:
            self.goal_name = "1-4"
        elif world.goal[player] == Goal.option_2_4:
            self.goal_name = "2-4"
        elif world.goal[player] == Goal.option_3_2:
            self.goal_name = "3-2"
        elif world.goal[player] == Goal.option_4_4:
            self.goal_name = "4-4"
        elif world.goal[player] == Goal.option_5_4:
            self.goal_name = "5-4"
        elif world.goal[player] == Goal.option_6_2:
            self.goal_name = "6-2"
        elif world.goal[player] == Goal.option_P_1:
            self.goal_name = "P-1"
        elif world.goal[player] == Goal.option_P_2:
            self.goal_name = "P-2"

        for loc in location_table:
            if self.goal_name in loc["name"] and not "_w" in loc["game_id"]:
                continue
            elif "_b" in loc["game_id"] and world.boss_rewards[player].value == 0:
                continue
            elif loc["name"] in ext_bosses and world.boss_rewards[player].value < 2:
                continue
            elif "_c" in loc["game_id"] and not world.challenge_rewards[player]:
                continue
            elif "_p" in loc["game_id"] and not world.p_rank_rewards[player]:
                continue
            elif "fish" in loc["game_id"] and not world.fish_rewards[player]:
                continue
            else:
                id = base_id + location_table.index(loc)
                region: Region = world.get_region(region_table[loc["region"]], player)
                location: UltrakillLocation = UltrakillLocation(player, loc["name"], id, region)
                #print(location.name + ", " + region.name)
                region.locations.append(location)

        for loc in event_table:
            if "P-" in loc["name"] and not self.goal_name in loc["name"]:
                continue

            if "-S" in loc["name"] and not world.include_secret_mission_completion[self.player]:
                continue

            region: Region = world.get_region(region_table[loc["region"]], player)

            location: UltrakillLocation = UltrakillLocation(player, loc["name"], None, region)
            if not self.goal_name in loc["name"]:
                location.place_locked_item(self.create_event("Level Completed"))
            region.locations.append(location)

        victory: Location = world.get_location("Cleared " + self.goal_name, player)
        victory.place_locked_item(self.create_event("Victory"))

        world.completion_condition[player] = lambda state: state.has("Victory", player)


    def fill_slot_data(self) -> Dict[str, Any]:
        world = self.multiworld
        player = self.player

        locations = []

        color_int_to_enum: Dict[int, str] = {
            0: "Off",
            1: "Once",
            2: "EveryLoad"
        }

        for loc in world.get_filled_locations(player):
            if "Cleared" in loc.name:
                continue
            else:
                data = {
                    "id": self.location_name_to_game_id[loc.name],
                    "ap_id": loc.address,
                    "item_name": loc.item.name,
                    "player_name": world.player_name[loc.item.player]
                }

                if loc.item.game == "ULTRAKILL":
                    data["item_type"] = self.item_name_to_type[loc.item.name].name
                    data["ukitem"] = True
                else:
                    data["item_type"] = loc.item.classification.name
                    data["ukitem"] = False

                locations.append(data)

        slot_data: Dict[str, Any] = {
            "locations": locations,
            "goal": world.goal[player].value,
            "goal_requirement": world.goal_requirement[player].value,
            "boss_rewards": world.boss_rewards[player].value,
            "challenge_rewards": bool(world.challenge_rewards[player]),
            "p_rank_rewards": bool(world.p_rank_rewards[player]),
            "fish_rewards": bool(world.fish_rewards[player]),
            "randomize_secondary_fire": bool(world.randomize_secondary_fire[player]),
            "start_with_arm": bool(world.start_with_arm[player]),
            "starting_stamina": world.starting_stamina[player].value,
            "starting_walljumps": world.starting_walljumps[player].value,
            "start_with_slide": bool(world.start_with_slide[player]),
            "start_with_slam": bool(world.start_with_slam[player]),
            "randomize_skulls": bool(world.randomize_skulls[player]),
            "point_multiplier": world.point_multiplier[player].value,
            "ui_color_randomizer": color_int_to_enum[world.ui_color_randomizer[player].value],
            "gun_color_randomizer": color_int_to_enum[world.gun_color_randomizer[player].value],
            "music_randomizer": bool(world.music_randomizer[player]),
            "music": self.music,
            "cybergrind_hints": bool(world.cybergrind_hints[player]),
            "death_link": bool(world.death_link[player]),
        }
        return slot_data


class UltrakillItem(Item):
    game: str = "ULTRAKILL"


class UltrakillLocation(Location):
    game: str = "ULTRAKILL"

