from typing import List

from BaseClasses import Item, ItemClassification, Region, Tutorial, LocationProgressType, MultiWorld
from worlds.AutoWorld import WebWorld, World
from worlds.LauncherComponents import components, Component, launch_subprocess, Type
from .Rules import set_world_rules, get_level_region_name
from .Locations import Borderlands2Location, location_data_table, location_name_to_id, location_descriptions, bl2_base_id
from .Items import Borderlands2Item
from .Options import Borderlands2Options
from .Regions import region_data_table
from .archi_defs import loc_name_to_id, item_id_to_name, gear_data_table, item_data_table, max_level, item_name_to_id as item_name_to_raw_id
import random

VERSION = "0.5"



class Borderlands2WebWorld(WebWorld):
    theme = "ice"

    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Borderlands 2 for Multiworld.",
        "English",
        "guide_en.md",
        "guide/en",
        ["EdricY"]
    )]


def launch_client():
    from .Client import launch
    launch_subprocess(launch, name='Borderlands 2 Client')


components.append(Component("Borderlands 2 Client",
                            func=launch_client,
                            component_type=Type.CLIENT))


class Borderlands2World(World):
    """
     Borderlands 2 is a looter shooter we all love.
    """

    game = "Borderlands 2"
    web = Borderlands2WebWorld()
    options_dataclass = Borderlands2Options
    options: Borderlands2Options
    location_name_to_id = location_name_to_id
    location_descriptions = location_descriptions
    item_name_to_id = {name: bl2_base_id + id for name, id in item_name_to_raw_id.items()}
    item_name_groups = {
        "GrenadeMod": { "Common GrenadeMod", "Uncommon GrenadeMod", "Rare GrenadeMod", "VeryRare GrenadeMod", "Legendary GrenadeMod", "Seraph GrenadeMod", "Rainbow GrenadeMod", "Unique GrenadeMod" },
        "Shield": { "Common Shield", "Uncommon Shield", "Rare Shield", "VeryRare Shield", "Legendary Shield", "Seraph Shield", "Rainbow Shield", "Unique Shield" },
        "Pistol": { "Common Pistol", "Uncommon Pistol", "Rare Pistol", "VeryRare Pistol", "E-Tech Pistol", "Legendary Pistol", "Seraph Pistol", "Pearlescent Pistol", "Unique Pistol" },
        "Shotgun": { "Common Shotgun", "Uncommon Shotgun", "Rare Shotgun", "VeryRare Shotgun", "E-Tech Shotgun", "Legendary Shotgun", "Seraph Shotgun", "Rainbow Shotgun", "Pearlescent Shotgun", "Unique Shotgun" },
        "SMG": { "Common SMG", "Uncommon SMG", "Rare SMG", "VeryRare SMG", "E-Tech SMG", "Legendary SMG", "Seraph SMG", "Rainbow SMG", "Pearlescent SMG", "Unique SMG" },
        "SniperRifle": { "Common SniperRifle", "Uncommon SniperRifle", "Rare SniperRifle", "VeryRare SniperRifle", "E-Tech SniperRifle", "Legendary SniperRifle", "Seraph SniperRifle", "Rainbow SniperRifle", "Pearlescent SniperRifle", "Unique SniperRifle" },
        "AssaultRifle": { "Common AssaultRifle", "Uncommon AssaultRifle", "Rare AssaultRifle", "VeryRare AssaultRifle", "E-Tech AssaultRifle", "Legendary AssaultRifle", "Seraph AssaultRifle", "Rainbow AssaultRifle", "Pearlescent AssaultRifle", "Unique AssaultRifle" },
        "RocketLauncher": { "Common RocketLauncher", "Uncommon RocketLauncher", "Rare RocketLauncher", "VeryRare RocketLauncher", "E-Tech RocketLauncher", "Legendary RocketLauncher", "Seraph RocketLauncher", "Rainbow RocketLauncher", "Pearlescent RocketLauncher", "Unique RocketLauncher" },
    }

    # explicit_indirect_conditions = False # testing with this, hopefully can remove it later

    def __init__(self, multiworld: MultiWorld, player: int):
        super(Borderlands2World, self).__init__(multiworld, player)
        self.filler_gear_names = []
        self.restricted_regions = set()
        self.goal = loc_name_to_id["Enemy: W4R-D3N"]  # without base id
        self.skill_pts_total = 0
        self.filler_counter = 0
        
        self.filler_sdu_dict = {
            "Max Ammo Pistol": 7,
            "Max Ammo Shotgun": 7,
            "Max Ammo SMG": 7,
            "Max Ammo SniperRifle": 7,
            "Max Ammo AssaultRifle": 7,
            "Max Ammo RocketLauncher": 7,
            "Max Grenade Count": 7,
            "Backpack Upgrade": 9,
            # "Bank Storage Upgrade": 9,
        }

    def try_get_entrance(self, entrance_name):
        try:
            return self.multiworld.get_entrance(entrance_name, self.player)
        except KeyError:
            # print("couldn't find entrance: " + entrance_name)
            return None

    def try_get_location(self, loc_name):
        try:
            return self.multiworld.get_location(loc_name, self.player)
        except KeyError:
            # print("couldn't find location: " + loc_name)
            return None

    def try_get_region(self, reg_name):
        try:
            return self.multiworld.get_region(reg_name, self.player)
        except KeyError:
            # print("couldn't find location: " + reg_name)
            return None


    def generate_early(self):
        if self.options.remove_ffs_checks.value == 1:
            self.restricted_regions.update([region for region in region_data_table if region_data_table[region].dlc_group == "ffs"])

        if self.options.remove_tina_checks.value == 1:
            self.restricted_regions.update([region for region in region_data_table if region_data_table[region].dlc_group == "tina"])

        if self.options.remove_torgue_checks.value == 1:
            self.restricted_regions.update([region for region in region_data_table if region_data_table[region].dlc_group == "torgue"])

        if self.options.remove_scarlett_checks.value == 1:
            self.restricted_regions.update([region for region in region_data_table if region_data_table[region].dlc_group == "scarlett"])

        if self.options.remove_hammerlock_checks.value == 1:
            self.restricted_regions.update([region for region in region_data_table if region_data_table[region].dlc_group == "hammerlock"])

        if self.options.remove_digi_peak_checks.value == 1:
            self.restricted_regions.update([region for region in region_data_table if region_data_table[region].dlc_group == "digi"])

        if self.options.remove_base_game_checks.value == 1:
            self.restricted_regions.update([region for region in region_data_table if region_data_table[region].dlc_group == "basegame"])

        if self.options.remove_headhunter_checks.value == 1:
            self.restricted_regions.update([region for region in region_data_table if region_data_table[region].dlc_group == "headhunter"])

        if self.options.remove_specific_region_checks:
            self.restricted_regions.update(self.options.remove_specific_region_checks.value)

        all_filler_gear = [key for key in item_data_table.keys() if key.startswith("Filler Gear: ")]
        unique_filler = [key for key in all_filler_gear if key.replace("Filler Gear: ", "") not in gear_data_table]
        non_unique_filler = [key for key in all_filler_gear if key.replace("Filler Gear: ", "") in gear_data_table]

        if self.options.filler_gear.value == 1:  # unique
            self.filler_gear_names = unique_filler
        elif self.options.filler_gear.value == 2:  # rarity_groups
            self.filler_gear_names = non_unique_filler
        elif self.options.filler_gear.value == 3:  # both
            self.filler_gear_names = all_filler_gear
        else:  # none
            self.filler_gear_names = []

        self.filler_gear_names = [f for f in self.filler_gear_names if item_data_table[f].region not in self.restricted_regions]

        # if self.options.remove_raidboss_checks.value == 1:
        #     self.restricted_regions.update(["WingedStorm", "WrithingDeep","TerramorphousPeak"])

        # goal setup
        goal_name = self.options.goal.value
        self.goal = loc_name_to_id[goal_name] # without base id
        # self.options.exclude_locations.value.add(goal_name)

        # TODO: maybe add regions beyond the goal to restricted regions, or we can just expect the yaml to add them to remove_specific_region_checks
        # TODO: add regions to restricted regions if it requires another restricted region

    def create_item(self, name: str) -> Borderlands2Item:
        item_data = item_data_table[name]
        kind_str = item_data.item_kind
        kind = ItemClassification[kind_str]
        # if item_data.is_gear and "common" in name.lower():
        if item_data.is_gear:
            kind = ItemClassification.progression
        return Borderlands2Item(name, kind, self.item_name_to_id[name], self.player) # note: self.item_name_to_id includes bl2_base_id

    def create_filler(self) -> Borderlands2Item:
        self.filler_counter += 1
        branch = self.filler_counter % 5

        if branch == 1: # skill points
            if self.skill_pts_total < 126:  # max at 126 skill points
                self.skill_pts_total += 3
                return self.create_item("3 Skill Points")
            else:
                branch = 2

        if branch == 2: # sdu upgrade
            # select the filler sdu with the most remaining
            max_value = max(self.filler_sdu_dict.values())
            if max_value > 0:
                max_items = [item for item, value in self.filler_sdu_dict.items() if value == max_value]
                filler_sdu = random.choice(max_items)
                self.filler_sdu_dict[filler_sdu] -= 1
                return self.create_item(filler_sdu)
            else:
                branch = 3

        if branch == 3: # gear
            if self.filler_gear_names:
                gear_name = random.choice(self.filler_gear_names)
                self.filler_gear_names.remove(gear_name)
                return self.create_item(gear_name)
            else:
                branch = 4

        if branch == 4: # candy
            candy_name = random.choice(["YellowCandy", "RedCandy", "GreenCandy", "BlueCandy"])
            return self.create_item(candy_name)

        return self.create_item(random.choice(["$100", "10 Eridium", "10% Exp"]))

    def create_items(self) -> None:
        item_pool: List[Borderlands2Item] = []
        item_pool += [self.create_item(name) for name in item_data_table.keys()]  # 1 of everything to start
        item_pool += [self.create_item("Progressive Weapon Slot")]  # 2 total weapon slots
        item_pool += [self.create_item("Progressive Money Cap") for _ in range(7)]  # money cap is 8 stages
        item_pool += [self.create_item("3 Skill Points") for _ in range(7)]  # hit 27 at least
        self.skill_pts_total += 3 * 9 # 1 progressive + 8 filler
        self.filler_sdu_dict = { k : v-1 for k, v in self.filler_sdu_dict.items() } # decrement filler sdus by 1

        # setup jump checks
        if self.options.jump_checks.value == 0:
            # remove jump check
            item_pool = [item for item in item_pool if not item.name == "Progressive Jump"]
        else:
            # add num checks - 1
            jumps_to_add = self.options.jump_checks.value - 1
            item_pool += [self.create_item("Progressive Jump") for _ in range(jumps_to_add)]

        # setup sprint checks
        if self.options.sprint_checks.value == 0:
            # remove sprint check
            item_pool = [item for item in item_pool if not item.name == "Progressive Sprint"]
        else:
            # add num checks - 1
            sprints_to_add = self.options.sprint_checks.value - 1
            item_pool += [self.create_item("Progressive Sprint") for _ in range(sprints_to_add)]

        restricted_travel_items = [region_data_table[r].travel_item_name for r in self.restricted_regions]
        new_pool = []

        # reconstruct pool based on options
        for item in item_pool:
            item_data = item_data_table[item.name]

            # skip filler gear for now
            if item.name.startswith("Filler Gear"):
                continue
            # skip override items (should only be used in yaml)
            if item.name.startswith("Override"):
                continue

            # skip travel items (entrance locks)
            if self.options.entrance_locks.value == 0 and item.name.startswith("Travel: "):
                continue
            # skip trap items
            if self.options.spawn_traps.value == 0 and item.name.startswith("Trap Spawn"):
                continue

            if item.name.startswith("Reward"):
                # skip quest rewards
                if self.options.quest_reward_items.value == 0:
                    continue
                # skip non-gear quest rewards
                if self.options.quest_reward_items.value == 2 or self.options.quest_reward_items.value == 4:
                    if item_data_table[item.name].is_non_gear_reward:
                        continue
                # skip quest rewards from restricted regions
                if self.options.quest_reward_items.value == 3 or self.options.quest_reward_items.value == 4:
                    if item_data_table[item.name].region in self.restricted_regions:
                        continue

            # skip gear rewards
            if self.options.gear_rarity_item_pool.value != 4:
                if self.options.gear_rarity_item_pool.value <= 3 and item.name.startswith("Rainbow"):
                    continue
                if self.options.gear_rarity_item_pool.value <= 2 and item.name.startswith("Pearlescent"):
                    continue
                if self.options.gear_rarity_item_pool.value <= 1 and item.name.startswith("Seraph"):
                    continue
                if self.options.gear_rarity_item_pool.value == 0 and item.name in gear_data_table:
                    continue

            # skip restricted region Travel Items
            if item.name in restricted_travel_items:
                continue


            # item should be included
            new_pool.append(item)

        item_pool = new_pool

        # fill leftovers
        location_count = len(self.multiworld.get_unfilled_locations(self.player))
        leftover = location_count - len(item_pool)
        # print("Adding Filler Checks: " + str(leftover))
        for _ in range(leftover):
            item_pool += [self.create_filler()]

        self.multiworld.itempool += item_pool

    def create_regions(self) -> None:
        loc_dict = {
            location_name: location_id for location_name, location_id in self.location_name_to_id.items()
        }

        # remove symbols
        if self.options.vault_symbols.value == 0:
            for location_name, location_data in location_data_table.items():
                if location_name.startswith("Symbol"):
                    loc_dict[location_name] = None

        # remove vending machines
        if self.options.vending_machines.value == 0:
            for location_name, location_data in location_data_table.items():
                if location_name.startswith("Vending"):
                    loc_dict[location_name] = None

        # remove quests
        if self.options.quest_completion_checks.value == 0:
            for location_name, location_data in location_data_table.items():
                if location_name.startswith("Quest"):
                    loc_dict[location_name] = None

        # remove generic mob checks
        if self.options.generic_mob_checks.value == 0:
            for location_name, location_data in location_data_table.items():
                if location_name.startswith("Generic"):
                    loc_dict[location_name] = None

        # remove rarity checks
        if self.options.gear_rarity_checks.value != 4:
            for location_name, location_data in gear_data_table.items():
                if self.options.gear_rarity_checks.value <= 3 and location_name.startswith("Rainbow"):
                    loc_dict[location_name] = None
                elif self.options.gear_rarity_checks.value <= 2 and location_name.startswith("Pearlescent"):
                    loc_dict[location_name] = None
                elif self.options.gear_rarity_checks.value <= 1 and location_name.startswith("Seraph"):
                    loc_dict[location_name] = None
                elif self.options.gear_rarity_checks.value == 0 and location_data.is_gear:
                    loc_dict[location_name] = None

        # remove challenge checks
        if self.options.challenge_checks.value == 0:
            for location_name, location_data in location_data_table.items():
                if location_name.startswith("Challenge"):
                    loc_dict[location_name] = None

        # remove chest checks
        if self.options.chest_checks.value == 0:
            for location_name, location_data in location_data_table.items():
                if location_name.startswith("Chest "):
                    loc_dict[location_name] = None

        # remove co-op checks
        if self.options.remove_coop_checks.value != 0:
            for location_name, location_data in location_data_table.items():
                v = location_data.coop_type
                if v and v <= self.options.remove_coop_checks.value:
                    loc_dict[location_name] = None

        # remove raidboss checks
        if self.options.remove_raidboss_checks.value == 1:
            for location_name, location_data in location_data_table.items():
                if location_data.is_raidboss:
                    loc_dict[location_name] = None

        # remove checks above max level
        if self.options.max_level_checks.value != 0:
            for location_name, location_data in location_data_table.items():
                if location_data.level > self.options.max_level_checks.value:
                    loc_dict[location_name] = None

        # remove level checks below override level
        if "Override Level 15" in self.options.start_inventory.value:
            for location_name, location_data in location_data_table.items():
                if location_name.startswith("Level ") and location_data.level <= 15:
                    loc_dict[location_name] = None
        if "Override Level 30" in self.options.start_inventory.value:
            for location_name, location_data in location_data_table.items():
                if location_name.startswith("Level ") and location_data.level <= 30:
                    loc_dict[location_name] = None

        # create regions
        for name, region_data in region_data_table.items():
            region = Region(name, self.player, self.multiworld)
            self.multiworld.regions.append(region)
            # # attempting to use events for region detection
            # event_loc = world.try_get_location(f"Story Location - {story_req_reg_name}")
            # if not event_loc:
            # event_loc = Borderlands2Location(self.player, f"Story Location - {name}", None, region)
            # event_loc.place_locked_item(Borderlands2Item(f"Story Reached {name}", ItemClassification.progression, None, self.player))
            # region.locations.append(event_loc)


        # connect regions
        for name, region_data in region_data_table.items():
            region = self.multiworld.get_region(name, self.player)
            for c_region_name in region_data.connecting_regions:
                c_region = self.multiworld.get_region(c_region_name, self.player)
                exit_name = f"{region.name} to {c_region.name}"
                # TODO: do you have to (or is it better to) add all the exits in one go?
                region.add_exits({c_region.name: exit_name})


        # add locations to regions
        for name, addr in loc_dict.items():
            if addr is None:
                continue
            loc_data = location_data_table[name]
            region_name = loc_data.region
            if region_name in self.restricted_regions:
                continue
            # TODO also skip if it requires another restricted region (but not gear)
            region = self.multiworld.get_region(region_name, self.player)
            region.add_locations({name: addr}, Borderlands2Location)

        # create level regions
        menu_reg = self.multiworld.get_region("Menu", self.player)
        prev_reg = menu_reg
        for i in range(max_level + 2):
            level_reg_name = get_level_region_name(i)
            if self.try_get_region(level_reg_name):
                # region is not new, skip
                continue
            level_region = Region(level_reg_name, self.player, self.multiworld)
            self.multiworld.regions.append(level_region)
            prev_reg.add_exits({level_reg_name: f"{prev_reg.name} to {level_reg_name}"})
            # print(f"{prev_reg.name} to {level_reg_name}")
            prev_reg = level_region

        # level_0_reg = Region("Level 0", self.player, self.multiworld) # pre-damage region
        # self.multiworld.regions.append(level_0_reg)
        # menu_reg = self.multiworld.get_region("Menu", self.player)
        # menu_reg.add_exits({"Level 0": "Menu to Level 0"}) # no rule associated
        # level_groups = [f"Level {i}-{i+4}" for i in range(1, 31, 5)] # stratify by 5s

        # for i, reg_name in enumerate(level_groups):
        #     print(reg_name)
        #     level_region = Region(reg_name, self.player, self.multiworld)
        #     self.multiworld.regions.append(level_region)
        #     if i == 0:
        #         continue
        #     prev_reg_name = level_groups[i-1]
        #     prev_reg = self.multiworld.get_region(prev_reg_name, self.player)
        #     prev_reg.add_exits({reg_name: f"{prev_reg_name} to {reg_name}"})
        # level_0_reg.add_exits({"Level 1-5": "Level 0 to Level 1-5"})

        # setup victory condition (as "event" with None address/code)
        # v_region_name = location_data_table[goal_name].region
        # victory_region = self.multiworld.get_region(v_region_name, self.player)
        # victory_location = Borderlands2Location(self.player, "Victory Location", None, victory_region)
        # victory_item = Borderlands2Item("Victory: " + goal_name, ItemClassification.progression, None, self.player)
        # victory_location.place_locked_item(victory_item)
        # victory_region.locations.append(victory_location)

        # setup goal location. place local filler item there. TODO: maybe replace with "Nothing"?
        goal_name = self.options.goal.value
        self.multiworld.get_location(goal_name, self.player).place_locked_item(self.create_item("$100"))
        self.multiworld.completion_condition[self.player] = lambda state: (
            state.can_reach_location(goal_name, self.player)
        )

        # from Utils import visualize_regions
        # print("visualize_regions")
        # visualize_regions(self.multiworld.get_region("Menu", self.player), "my_world.puml")

    def get_filler_item_name(self) -> str:
        return "$100"

    def set_rules(self) -> None:
        set_world_rules(self)

    # def pre_fill(self) -> None:
    #     pass

    def fill_slot_data(self):
        return {
            "version": VERSION,
            "goal": self.goal,
            "delete_starting_gear": self.options.delete_starting_gear.value,
            "gear_rarity_item_pool": self.options.gear_rarity_item_pool.value,
            "filler_gear": self.options.filler_gear.value,
            "receive_gear": self.options.receive_gear.value,
            "vault_symbols": self.options.vault_symbols.value,
            "vending_machines": self.options.vending_machines.value,
            "entrance_locks": self.options.entrance_locks.value,
            "jump_checks": self.options.jump_checks.value,
            "max_jump_height": self.options.max_jump_height.value,
            "sprint_checks": self.options.sprint_checks.value,
            "max_sprint_speed": self.options.max_sprint_speed.value,
            "spawn_traps": self.options.spawn_traps.value,
            "quest_completion_checks": self.options.quest_completion_checks.value,
            "quest_reward_items": self.options.quest_reward_items.value,
            "generic_mob_checks": self.options.generic_mob_checks.value,
            "gear_rarity_checks": self.options.gear_rarity_checks.value,
            "challenge_checks": self.options.challenge_checks.value,
            "chest_checks": self.options.chest_checks.value,
            "death_link": self.options.death_link.value,
            "death_link_punishment": self.options.death_link_punishment.value,
            "death_link_send_mode": self.options.death_link_send_mode.value,
        }
