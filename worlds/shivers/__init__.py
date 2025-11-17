from typing import Dict, List, Optional

from BaseClasses import Item, ItemClassification, Location, Region, Tutorial
from Fill import fill_restrictive
from worlds.AutoWorld import WebWorld, World
from . import Constants, Rules
from .Items import ItemType, SHIVERS_ITEM_ID_OFFSET, ShiversItem, item_table
from .Options import ShiversOptions, shivers_option_groups
from .Rules import set_rules


class ShiversWeb(WebWorld):
    tutorials = [Tutorial(
        "Shivers Setup Guide",
        "A guide to setting up Shivers for Multiworld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["GodlFire", "Cynbel_Terreus"]
    )]
    option_groups = shivers_option_groups


class ShiversWorld(World):
    """
    Shivers is a horror themed point and click adventure.
    Explore the mysteries of Windlenot's Museum of the Strange and Unusual.
    """

    game = "Shivers"
    topology_present = False
    web = ShiversWeb()
    options_dataclass = ShiversOptions
    options: ShiversOptions
    set_rules = set_rules
    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = Constants.location_name_to_id
    storage_placements = []
    pot_completed_list: List[int]

    def generate_early(self):
        self.pot_completed_list = []

        # Pot piece shuffle location:
        if self.options.location_pot_pieces == "own_world":
            self.options.local_items.value |= {name for name, data in item_table.items() if
                                               data.type in [ItemType.POT, ItemType.POT_COMPLETE]}
        elif self.options.location_pot_pieces == "different_world":
            self.options.non_local_items.value |= {name for name, data in item_table.items() if
                                                   data.type in [ItemType.POT, ItemType.POT_COMPLETE]}

        # Ixupi captures priority locations:
        if self.options.ixupi_captures_priority:
            self.options.priority_locations.value |= (
                {name for name in self.location_names if name.startswith('Ixupi Captured')}
            )

    def create_item(self, name: str) -> Item:
        data = item_table[name]
        return ShiversItem(name, data.classification, data.code, self.player)

    def create_event_location(self, region_name: str, location_name: str, event_name: Optional[str] = None) -> None:
        region = self.get_region(region_name)
        loc = ShiversLocation(self.player, location_name, None, region)
        if event_name is not None:
            loc.place_locked_item(ShiversItem(event_name, ItemClassification.progression, None, self.player))
        else:
            loc.place_locked_item(ShiversItem(location_name, ItemClassification.progression, None, self.player))
        loc.show_in_spoiler = False
        region.locations.append(loc)

    def create_regions(self) -> None:
        # Create regions
        for region_name, exits in Constants.region_info["regions"]:
            r = Region(region_name, self.player, self.multiworld)
            self.multiworld.regions.append(r)
            for exit_name in exits:
                r.create_exit(exit_name)

        # Bind mandatory connections
        for entr_name, region_name in Constants.region_info["mandatory_connections"]:
            e = self.get_entrance(entr_name)
            r = self.get_region(region_name)
            e.connect(r)
        
        # Locations
        # Build exclusion list
        removed_locations = set()
        if not self.options.include_information_plaques:
            removed_locations.update(Constants.exclusion_info["plaques"])
        if not self.options.elevators_stay_solved:
            removed_locations.update(Constants.exclusion_info["elevators"])
        if not self.options.early_lightning:
            removed_locations.update(Constants.exclusion_info["lightning"])

        # Add locations
        for region_name, locations in Constants.location_info["locations_by_region"].items():
            region = self.get_region(region_name)
            for loc_name in locations:
                if loc_name not in removed_locations:
                    loc = ShiversLocation(self.player, loc_name, self.location_name_to_id.get(loc_name, None), region)
                    region.locations.append(loc)

        self.create_event_location("Prehistoric", "Set Skull Dial: Prehistoric")
        self.create_event_location("Tar River", "Set Skull Dial: Tar River")
        self.create_event_location("Egypt", "Set Skull Dial: Egypt")
        self.create_event_location("Burial", "Set Skull Dial: Burial")
        self.create_event_location("Gods Room", "Set Skull Dial: Gods Room")
        self.create_event_location("Werewolf", "Set Skull Dial: Werewolf")
        self.create_event_location("Projector Room", "Viewed Theater Movie")
        self.create_event_location("Clock Chains", "Clock Chains", "Set Time")
        self.create_event_location("Clock Tower", "Jukebox", "Set Song")
        self.create_event_location("Fortune Teller", "Viewed Fortune")
        self.create_event_location("Orrery", "Orrery", "Aligned Planets")
        self.create_event_location("Norse Stone", "Norse Stone", "Viewed Norse Stone")
        self.create_event_location("Beth's Body", "Beth's Body", "Viewed Page 17")
        self.create_event_location("Windlenot's Body", "Windlenot's Body", "Viewed Egyptian Hieroglyphics Explained")
        self.create_event_location("Guillotine", "Guillotine", "Lost Your Head")

    def create_items(self) -> None:
        # Add items to item pool
        item_pool = []
        for name, data in item_table.items():
            if data.type in [ItemType.KEY, ItemType.ABILITY, ItemType.IXUPI_AVAILABILITY]:
                item_pool.append(self.create_item(name))

        # Pot pieces/Completed/Mixed:
        if self.options.full_pots == "pieces":
            item_pool += [self.create_item(name) for name, data in item_table.items() if data.type == ItemType.POT]
        elif self.options.full_pots == "complete":
            item_pool += [self.create_item(name) for name, data in item_table.items() if
                          data.type == ItemType.POT_COMPLETE]
        else:
            # Roll for if pieces or a complete pot will be used.
            # Pot Pieces
            pieces = [self.create_item(name) for name, data in item_table.items() if data.type == ItemType.POT]
            complete = [self.create_item(name) for name, data in item_table.items() if
                        data.type == ItemType.POT_COMPLETE]
            for i in range(10):
                if self.random.randint(0, 1) == 0:
                    self.pot_completed_list.append(0)
                    item_pool.append(pieces[i])
                    item_pool.append(pieces[i + 10])
                # Completed Pot
                else:
                    self.pot_completed_list.append(1)
                    item_pool.append(complete[i])

        # Add Easier Lyre
        item_pool += [self.create_item("Easier Lyre") for _ in range(9)]

        # Place library escape items. Choose a location to place the escape item
        library_region = self.get_region("Library")
        library_location = self.random.choice(
            [loc for loc in library_region.locations if not loc.name.startswith("Storage: ")]
        )

        # Roll for which escape items will be placed in the Library
        library_random = self.random.randint(1, 3)
        if library_random == 1:
            library_location.place_locked_item(self.create_item("Crawling"))
            item_pool = [item for item in item_pool if item.name != "Crawling"]
        elif library_random == 2:
            library_location.place_locked_item(self.create_item("Key for Library"))
            item_pool = [item for item in item_pool if item.name != "Key for Library"]
        elif library_random == 3:
            library_location.place_locked_item(self.create_item("Key for Three Floor Elevator"))
            library_location_2 = self.random.choice(
                [loc for loc in library_region.locations if
                 not loc.name.startswith("Storage: ") and loc != library_location]
            )
            library_location_2.place_locked_item(self.create_item("Key for Egypt Room"))
            item_pool = [item for item in item_pool if
                         item.name not in ["Key for Three Floor Elevator", "Key for Egypt Room"]]

        # If front door option is on, determine which set of keys will
        # be used for lobby access and add front door key to item pool
        lobby_access_keys = 0
        if self.options.front_door_usable:
            lobby_access_keys = self.random.randint(0, 1)
            item_pool.append(self.create_item("Key for Front Door"))
        else:
            item_pool.append(self.create_item("Heal"))

        def set_lobby_access_keys(items: Dict[str, int]):
            if lobby_access_keys == 0:
                items["Key for Underground Lake"] = 1
                items["Key for Office Elevator"] = 1
                items["Key for Office"] = 1
            else:
                items["Key for Front Door"] = 1

        # Lobby access:
        if self.options.lobby_access == "early":
            set_lobby_access_keys(self.multiworld.early_items[self.player])
        elif self.options.lobby_access == "local":
            set_lobby_access_keys(self.multiworld.local_early_items[self.player])

        goal_item_code = SHIVERS_ITEM_ID_OFFSET + 100 + Constants.years_since_sep_30_1980
        for name, data in item_table.items():
            if data.type == ItemType.GOAL and data.code == goal_item_code:
                goal = self.create_item(name)
                self.get_location("Mystery Solved").place_locked_item(goal)

        # Extra filler is random between Heals and Easier Lyre. Heals weighted 95%.
        filler_needed = len(self.multiworld.get_unfilled_locations(self.player)) - len(item_pool) - 23
        item_pool += map(self.create_item, self.random.choices(
            ["Heal", "Easier Lyre"], weights=[95, 5], k=filler_needed
        ))

        self.multiworld.itempool += item_pool

    def pre_fill(self) -> None:
        # Prefills event storage locations with duplicate pots
        storage_locs = []
        storage_items = []

        for locations in Constants.location_info["locations_by_region"].values():
            for loc_name in locations:
                if loc_name.startswith("Storage: "):
                    storage_locs.append(self.get_location(loc_name))

        # Pot pieces/Completed/Mixed:
        if self.options.full_pots == "pieces":
            storage_items += [self.create_item(name) for name, data in item_table.items() if
                              data.type == ItemType.POT_DUPLICATE]
        elif self.options.full_pots == "complete":
            storage_items += [self.create_item(name) for name, data in item_table.items() if
                              data.type == ItemType.POT_COMPLETE_DUPLICATE]
            storage_items += [self.create_item("Empty") for _ in range(10)]
        else:
            pieces = [self.create_item(name) for name, data in item_table.items() if
                      data.type == ItemType.POT_DUPLICATE]
            complete = [self.create_item(name) for name, data in item_table.items() if
                        data.type == ItemType.POT_COMPLETE_DUPLICATE]
            for i in range(10):
                # Pieces
                if self.pot_completed_list[i] == 0:
                    storage_items.append(pieces[i])
                    storage_items.append(pieces[i + 10])
                # Complete
                else:
                    storage_items.append(complete[i])
                    storage_items.append(self.create_item("Empty"))

        storage_items += [self.create_item("Empty") for _ in range(3)]

        state = self.multiworld.get_all_state(False, True, False)

        self.random.shuffle(storage_locs)
        self.random.shuffle(storage_items)

        fill_restrictive(self.multiworld, state, storage_locs.copy(), storage_items, True, True)

        self.storage_placements = {location.name.replace("Storage: ", ""): location.item.name.replace(" DUPE", "") for
                                   location in storage_locs}

    def get_pre_fill_items(self) -> List[Item]:
        if self.options.full_pots == "pieces":
            return [self.create_item(name) for name, data in item_table.items() if
                    data.type == ItemType.POT_DUPLICATE]
        elif self.options.full_pots == "complete":
            return [self.create_item(name) for name, data in item_table.items() if
                    data.type == ItemType.POT_COMPLETE_DUPLICATE]
        else:
            pool = []
            pieces = [self.create_item(name) for name, data in item_table.items() if
                      data.type == ItemType.POT_DUPLICATE]
            complete = [self.create_item(name) for name, data in item_table.items() if
                        data.type == ItemType.POT_COMPLETE_DUPLICATE]
            for i in range(10):
                if self.pot_completed_list[i] == 0:
                    pool.append(pieces[i])
                    pool.append(pieces[i + 10])
                else:
                    pool.append(complete[i])
            return pool

    def fill_slot_data(self) -> dict:
        return {
            "StoragePlacements": self.storage_placements,
            "ExcludedLocations": list(self.options.exclude_locations.value),
            "IxupiCapturesNeeded": self.options.ixupi_captures_needed.value,
            "ElevatorsStaySolved": self.options.elevators_stay_solved.value,
            "EarlyBeth": self.options.early_beth.value,
            "EarlyLightning": self.options.early_lightning.value,
            "FrontDoorUsable": self.options.front_door_usable.value,
            "PuzzleCollectBehavior": self.options.puzzle_collect_behavior.value,
        }


class ShiversLocation(Location):
    game = "Shivers"
