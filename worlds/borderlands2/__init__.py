from typing import List

from BaseClasses import ItemClassification, Region, Tutorial, LocationProgressType
from worlds.AutoWorld import WebWorld, World
from worlds.LauncherComponents import components, Component, launch_subprocess, Type
from .Items import Borderlands2Item, item_data_table, bl2_base_id, item_name_to_id, item_descriptions
from .Locations import Borderlands2Location, location_data_table, location_name_to_id, location_descriptions, get_region_from_loc_name, coop_locations
from .Options import Borderlands2Options
from .Regions import region_data_table
from .archi_defs import loc_name_to_id, item_id_to_name, gear_kind_to_id
import random

class Borderlands2WebWorld(WebWorld):
    theme = "ice"

    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Borderlands 2 for Multiworld.",
        "English",
        "setup_en.md",
        "setup/en",
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
    item_name_to_id = item_name_to_id
    item_descriptions = item_descriptions
    goal = loc_name_to_id["Enemy BloodshotRamparts: W4R-D3N"]  # without base id
    skill_pts_total = 0
    filler_counter = 0

    restricted_regions = set()

    def try_get_entrance(self, entrance_name):
        try:
            return self.multiworld.get_entrance(entrance_name, self.player)
        except KeyError:
            print("couldn't find entrance: " + entrance_name)
            return None

    def try_get_location(self, loc_name):
        try:
            return self.multiworld.get_location(loc_name, self.player)
        except KeyError:
            print("couldn't find location: " + loc_name)
            return None

    def generate_early(self):
        if self.options.remove_dlc_checks.value == 1:
            self.restricted_regions.update([
                "FFSIntroSanctuary", "Burrows", "Backburner", "DahlAbandon", "HeliosFallen", "WrithingDeep", "Mt.ScarabResearchCenter", "FFSBossFight",
                "UnassumingDocks", "FlamerockRefuge", "HatredsShadow", "LairOfInfiniteAgony", "ImmortalWoods", "Forest", "MinesOfAvarice", "MurderlinsTemple", "WingedStorm", "DragonKeep",
                "BadassCrater","Beatdown","TorgueArena","TorgueArenaRing","BadassCraterBar","Forge","SouthernRaceway","PyroPetesBar", "Oasis", "HaytersFolly", "Wurmwater", "WashburneRefinery", "Rustyards", "MagnysLighthouse", "LeviathansLair",
                "HuntersGrotto", "CandlerakksCrag", "ArdortonStation", "ScyllasGrove", "Terminus",
            ])

        if self.options.remove_digi_peak_checks.value == 1:
            self.restricted_regions.update(["DigistructPeak", "DigistructPeakInner"])

        if self.options.remove_headhunter_checks.value == 1:
            self.restricted_regions.update([
                "MarcusMercenaryShop", "GluttonyGulch", "RotgutDistillery", "WamBamIsland", "HallowedHollow"
            ])


    def create_item(self, name: str) -> Borderlands2Item:
        return Borderlands2Item(name, item_data_table[name].type, item_data_table[name].code, self.player)

    def create_filler(self) -> Borderlands2Item:
        self.filler_counter += 1
        branch = self.filler_counter % 7
        if branch == 1:
            if self.skill_pts_total < 126:  # max at 126 skill points
                self.skill_pts_total += 3
                return self.create_item("3 Skill Points")

        if branch == 2:
            return self.create_item("10 Eridium")

        if branch == 3:
            return self.create_item("10% Exp")

        if branch == 4:
            # white and green gear
            gear_name = random.choice([k for k in gear_kind_to_id.keys() if "common" in k.lower()])
            gear_name = "Filler Gear: " + gear_name
            return self.create_item(gear_name)

        if branch == 5:
            candy_name = random.choice(["YellowCandy", "RedCandy", "GreenCandy", "BlueCandy"])
            return self.create_item(candy_name)

        if branch == 6:
            gemstone_name = random.choice(["Filler Gear: Gemstone Pistol", "Filler Gear: Gemstone Shotgun",
                                           "Filler Gear: Gemstone SMG", "Filler Gear: Gemstone SniperRifle",
                                           "Filler Gear: Gemstone AssaultRifle"])
            return self.create_item(gemstone_name)

        return self.create_item("$100")

    def create_items(self) -> None:
        item_pool: List[Borderlands2Item] = []
        item_pool += [self.create_item(name) for name in item_data_table.keys()]  # 1 of everything to start
        item_pool += [self.create_item("Weapon Slot")]  # 2 total weapon slots
        item_pool += [self.create_item("Progressive Money Cap") for _ in range(7)]  # money cap is 8 stages
        item_pool += [self.create_item("3 Skill Points") for _ in range(8)]  # hit 27 at least
        self.skill_pts_total += 3 * 9

        # remove filler gear for now
        item_pool = [item for item in item_pool if not item.name.startswith("Filler Gear")]

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

        restricted_travel_items = [region_data_table[r].primary_travel_item for r in self.restricted_regions]
        new_pool = []
        for item in item_pool:
            # skip travel items (entrance locks)
            if self.options.entrance_locks.value == 0 and item.name.startswith("Travel: "):
                continue
            # skip trap items
            if self.options.spawn_traps.value == 0 and item.name.startswith("Trap Spawn"):
                continue
            # skip quest rewards
            if self.options.quest_reward_rando.value == 0 and item.name.startswith("Quest"):
                continue

            # skip gear rewards
            if self.options.gear_rarity_item_pool.value != 4:
                if self.options.gear_rarity_checks.value <= 3 and item.name.startswith("Rainbow"):
                    continue
                if self.options.gear_rarity_checks.value <= 2 and item.name.startswith("Pearlescent"):
                    continue
                if self.options.gear_rarity_checks.value <= 1 and item.name.startswith("Seraph"):
                    continue
                if self.options.gear_rarity_checks.value == 0 and item.code - bl2_base_id <= 199 and item.code - bl2_base_id >= 100:
                    continue

            # skip restricted region Travel Items
            if item.name in restricted_travel_items:
                continue
            # skip items from restricted regions (mostly quests)
            if get_region_from_loc_name(item.name) in self.restricted_regions:
                continue

            # item should be included
            new_pool.append(item)

        item_pool = new_pool

        # fill leftovers
        location_count = len(self.multiworld.get_locations(self.player))
        leftover = location_count - len(item_pool)
        for _ in range(leftover - 1):
            item_pool += [self.create_filler()]

        self.multiworld.itempool += item_pool

    def create_regions(self) -> None:
        if self.options.goal.value == 0:
            goal_name = "Enemy BloodshotRamparts: W4R-D3N"
        elif self.options.goal.value == 1:
            goal_name = "Enemy AridNexusBadlands: Saturn"
        elif self.options.goal.value == 2:
            goal_name = "Enemy VaultOfTheWarrior: Warrior"
        self.goal = loc_name_to_id[goal_name]

        loc_dict = {
            location_name: location_data.address for location_name, location_data in location_data_table.items()
        }

        # remove goal from locations
        del loc_dict[goal_name]

        # remove symbols
        if self.options.vault_symbols.value == 0:
            for location_name, location_data in location_data_table.items():
                if location_name.startswith("Symbol"):
                    del loc_dict[location_name]

        # remove vending machines
        if self.options.vending_machines.value == 0:
            for location_name, location_data in location_data_table.items():
                if location_name.startswith("Vending"):
                    del loc_dict[location_name]

        # remove quests
        if self.options.quest_reward_rando.value == 0:
            for location_name, location_data in location_data_table.items():
                if location_name.startswith("Quest"):
                    del loc_dict[location_name]

        # remove generic mob checks
        if self.options.generic_mob_checks.value == 0:
            for location_name, location_data in location_data_table.items():
                if location_name.startswith("Generic"):
                    del loc_dict[location_name]

        # remove rarity checks
        if self.options.gear_rarity_checks.value != 4:
            for location_name, location_data in location_data_table.items():
                if self.options.gear_rarity_checks.value <= 3 and location_name.startswith("Rainbow"):
                    del loc_dict[location_name]
                elif self.options.gear_rarity_checks.value <= 2 and location_name.startswith("Pearlescent"):
                    del loc_dict[location_name]
                elif self.options.gear_rarity_checks.value <= 1 and location_name.startswith("Seraph"):
                    del loc_dict[location_name]
                elif self.options.gear_rarity_checks.value == 0 and location_data.address - bl2_base_id <= 199 and location_data.address - bl2_base_id >= 100:
                    del loc_dict[location_name]

        # remove challenge checks
        if self.options.challenge_checks.value == 0:
            for location_name, location_data in location_data_table.items():
                if location_name.startswith("Challenge"):
                    del loc_dict[location_name]

        # remove chest checks
        if self.options.chest_checks.value == 0:
            for location_name, location_data in location_data_table.items():
                if location_name.startswith("Chest "):
                    del loc_dict[location_name]

        # remove co-op checks
        if self.options.remove_coop_checks.value != 0:
            for location_name, location_data in location_data_table.items():
                v = coop_locations.get(location_name)
                if v and v <= self.options.remove_coop_checks.value:
                    del loc_dict[location_name]

        # create regions
        for name, region_data in region_data_table.items():
            region = Region(name, self.player, self.multiworld)
            self.multiworld.regions.append(region)

        # connect regions
        for name, region_data in region_data_table.items():
            region = self.multiworld.get_region(name, self.player)
            for c_region_name in region_data.connecting_regions:
                if c_region_name in self.restricted_regions:
                    continue
                c_region = self.multiworld.get_region(c_region_name, self.player)
                exit_name = f"{region.name} to {c_region.name}"
                # TODO: do you have to (or is it better to) add all the exits in one go?
                region.add_exits({c_region.name: exit_name})


        # add locations to regions
        for name, addr in loc_dict.items():
            loc_data = location_data_table[name]
            region_name = loc_data.region
            if region_name in self.restricted_regions:
                continue
            region = self.multiworld.get_region(region_name, self.player)
            region.add_locations({name: addr}, Borderlands2Location)

        # setup victory condition (as "event" with None address/code)
        v_region_name = get_region_from_loc_name(goal_name)
        victory_region = self.multiworld.get_region(v_region_name, self.player)
        victory_location = Borderlands2Location(self.player, "Victory Location", None, victory_region)
        victory_item = Borderlands2Item("Victory: " + goal_name, ItemClassification.progression, None, self.player)
        victory_location.place_locked_item(victory_item)
        victory_region.locations.append(victory_location)

        self.multiworld.completion_condition[self.player] = lambda state: (
            state.has("Victory: " + goal_name, self.player)
        )

        from Utils import visualize_regions
        visualize_regions(self.multiworld.get_region("Menu", self.player), "my_world.puml")
        print("visualize_regions")

    def get_filler_item_name(self) -> str:
        return "$100"

    def set_rules(self) -> None:
        from .Rules import set_rules
        set_rules(self)

    def fill_slot_data(self):
        return {
            "goal": self.goal,
            "delete_starting_gear": self.options.delete_starting_gear.value,
            "gear_rarity_item_pool": self.options.gear_rarity_item_pool.value,
            "receive_gear": self.options.receive_gear.value,
            "vault_symbols": self.options.vault_symbols.value,
            "vending_machines": self.options.vending_machines.value,
            "entrance_locks": self.options.entrance_locks.value,
            "jump_checks": self.options.jump_checks.value,
            "max_jump_height": self.options.max_jump_height.value,
            "sprint_checks": self.options.sprint_checks.value,
            "max_sprint_speed": self.options.max_sprint_speed.value,
            "spawn_traps": self.options.spawn_traps.value,
            "quest_reward_rando": self.options.quest_reward_rando.value,
            "generic_mob_checks": self.options.generic_mob_checks.value,
            "gear_rarity_checks": self.options.gear_rarity_checks.value,
            "challenge_checks": self.options.challenge_checks.value,
            "chest_checks": self.options.chest_checks.value,
            "death_link": self.options.death_link.value,
            "death_link_punishment": self.options.death_link_punishment.value,
            "death_link_send_mode": self.options.death_link_send_mode.value,
        }
