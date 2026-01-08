import logging
import math
from collections import Counter

from BaseClasses import ItemClassification, CollectionState
from worlds.AutoWorld import World
from . import Web_World
from .Items import ITEMS, PlateUpItem
from .Locations import DISH_LOCATIONS, FRANCHISE_LOCATION_DICT, DAY_LOCATION_DICT, EXCLUDED_LOCATIONS
from .Options import PlateUpOptions, Goal
from .Rules import (
    filter_selected_dishes,
    apply_rules,
    restrict_locations_by_progression
)


class PlateUpWorld(World):
    game = "plateup"
    web = Web_World.PlateUpWebWorld()
    options_dataclass = PlateUpOptions
    options: PlateUpOptions

    # Pre-calculate mappings for items and locations.
    item_name_to_id = {name: data[0] for name, data in ITEMS.items()}
    location_name_to_id = {**FRANCHISE_LOCATION_DICT, **DAY_LOCATION_DICT, **DISH_LOCATIONS}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.excluded_locations = set()
        # Initialize attributes to avoid hasattr checks
        self.selected_dishes = []
        self.starting_dish = None
        self.valid_dish_locations = []

    def generate_location_table(self):
        """Plan locations based on goal/options and selected dishes."""
        goal = self.options.goal.value
        dish_count = self.options.dish.value
        if goal == 0:
            # Franchise goal: include per-run day/star locations up to required,
            # plus milestone locations up to required.
            required = self.options.franchise_count.value
            locs = {}

            def run_index_from_name(n: str):
                if not n.startswith("Franchise - "):
                    return None
                # Run 0 has no " After Franchised" suffix.
                if " After Franchised" not in n:
                    return 0
                # Extract suffix part
                suffix_part = n.split(" After Franchised", 1)[1]
                if suffix_part == "":
                    return 1  # exactly " After Franchised" => run 1
                suffix_part = suffix_part.strip()
                if suffix_part.isdigit():
                    return int(suffix_part)
                return None

            for name, loc in FRANCHISE_LOCATION_DICT.items():
                if name.startswith("Franchise ") and name.endswith(" times"):
                    # Milestone: include only up to required
                    try:
                        count = int(name.removeprefix("Franchise ").removesuffix(" times"))
                        if count <= required:
                            locs[name] = loc
                    except ValueError:
                        pass
                else:
                    run_idx = run_index_from_name(name)
                    if run_idx is not None and (run_idx + 1) <= required:
                        # Exclude post-day-15 checks (Day 16–20) from progression locations.
                        if "Complete Day " in name:
                            try:
                                day_str = name.split("Complete Day ", 1)[1].split(" ")[0].strip()
                                # day_str should be a number for days >=6; if it isn't, keep it
                                if day_str.isdigit() and int(day_str) > 15:
                                    continue
                            except Exception:
                                pass
                        locs[name] = loc
            # Include selected dish day locations as non-progression checks
            if dish_count > 0:
                if not self.selected_dishes or len(self.selected_dishes) != dish_count:
                    self.set_selected_dishes()
                for dish in self.selected_dishes:
                    for day in range(1, 15 + 1):
                        loc_name = f"{dish} - Day {day}"
                        loc_id = DISH_LOCATIONS.get(loc_name)
                        if loc_id:
                            locs[loc_name] = loc_id
            return locs
        else:
            required_days = self.options.day_count.value
            # Must match Regions star creation logic (floor)
            max_stars = required_days // 3
            locs = {}
            for name, loc in DAY_LOCATION_DICT.items():
                if name.startswith("Complete Day "):
                    day = int(name.removeprefix("Complete Day ").strip())
                    if day <= required_days:
                        locs[name] = loc
                elif name.startswith("Complete Star "):
                    star = int(name.removeprefix("Complete Star ").strip())
                    if star <= max_stars:
                        locs[name] = loc
            # Add dish locations when enabled; only those in selected_dishes
            if dish_count > 0:
                if not self.selected_dishes or len(self.selected_dishes) != dish_count:
                    self.set_selected_dishes()
                for dish in self.selected_dishes:
                    for day in range(1, 15 + 1):
                        loc_name = f"{dish} - Day {day}"
                        loc_id = DISH_LOCATIONS.get(loc_name)
                        if loc_id:
                            locs[loc_name] = loc_id
            return locs

    def validate_ids(self):
        """Ensure item and location IDs are unique."""
        item_ids = list(self.item_name_to_id.values())
        dupe_items = [item for item, count in Counter(item_ids).items() if count > 1]
        if dupe_items:
            raise Exception(f"Duplicate item IDs found: {dupe_items}")

        loc_ids = list(self.location_name_to_id.values())
        dupe_locs = [loc for loc, count in Counter(loc_ids).items() if count > 1]
        if dupe_locs:
            raise Exception(f"Duplicate location IDs found: {dupe_locs}")

    def create_regions(self):
        """Create regions using the planned location table."""
        from .Regions import create_plateup_regions
        # Ensure selected dishes are initialized
        self.set_selected_dishes()
        self._location_name_to_id = self.generate_location_table()
        self.validate_ids()
        create_plateup_regions(self)

    def create_item(self, name: str, classification: ItemClassification = ItemClassification.filler) -> PlateUpItem:
        """Create a PlateUp item from the given name."""
        if name in self.item_name_to_id:
            item_id = self.item_name_to_id[name]
        else:
            # Rebuild mapping from current ITEMS in case the class-level cache is stale
            from .Items import ITEMS as CURRENT_ITEMS
            self.item_name_to_id = {n: data[0] for n, data in CURRENT_ITEMS.items()}
            if name in self.item_name_to_id:
                item_id = self.item_name_to_id[name]
            else:
                raise ValueError(f"Item '{name}' not found in ITEMS")
        return PlateUpItem(name, classification, item_id, self.player)

    def create_items(self):
        self.set_selected_dishes()
        """Create the item pool for all planned locations."""
        # Base planned locations used by region creation
        base_locations = len(self.generate_location_table())
        # Dish locations are included in the base table
        total_locations = base_locations
        item_pool = []

        # Always remove one dish to be the starting dish (if any)
        self.starting_dish = self.selected_dishes[0] if self.selected_dishes else None
        unlock_dishes = self.selected_dishes[1:] if len(self.selected_dishes) > 1 else []

        # Add unlock items for the rest of the selected dishes (or all if none selected)
        for dish in unlock_dishes:
            unlock_name = f"{dish} Unlock"
            # Ensure mapping is current
            try:
                from .Items import ITEMS as CURRENT_ITEMS
                self.item_name_to_id = {n: data[0] for n, data in CURRENT_ITEMS.items()}
            except Exception:
                pass
            if unlock_name in self.item_name_to_id:
                item_pool.append(self.create_item(unlock_name, classification=ItemClassification.progression))
            else:
                logging.error(f"[Player {self.multiworld.player_name[self.player]}] Unlock item missing: {unlock_name}. ITEMS should include unlocks generated from Locations.dish_dictionary.")

        # Add progression items.
        # Add Player speed upgrades based on configured count
        player_speed_count = int(self.options.player_speed_upgrade_count.value)
        if player_speed_count > 0:
            item_pool.extend([
                self.create_item("Speed Upgrade Player", classification=ItemClassification.progression)
                for _ in range(player_speed_count)
            ])

        speed_mode = self.options.appliance_speed_mode.value
        appliance_speed_count = int(self.options.appliance_speed_upgrade_count.value)
        if appliance_speed_count > 0:
            if speed_mode == 0:
                item_pool.extend([
                    self.create_item("Speed Upgrade Appliance", classification=ItemClassification.progression)
                    for _ in range(appliance_speed_count)
                ])
            else:
                for _ in range(appliance_speed_count):
                    item_pool.extend([
                        self.create_item("Speed Upgrade Cook", classification=ItemClassification.progression),
                        self.create_item("Speed Upgrade Clean", classification=ItemClassification.progression),
                        self.create_item("Speed Upgrade Chop", classification=ItemClassification.progression)
                    ])

        # Determine total days to drive item counts
        if self.options.goal.value == Goal.option_franchise_x_times:
            total_days = 15 * int(self.options.franchise_count.value)
        else:
            total_days = int(self.options.day_count.value)

        # Place Money Cap Increase at ~1 per 10 days
        money_cap_items = max(1, total_days // 10)
        logging.debug(f"[Player {self.multiworld.player_name[self.player]}] Auto Money Cap items by cadence: total_days={total_days}, placing={money_cap_items}")
        if money_cap_items > 0:
            item_pool.extend([
                self.create_item("Money Cap Increase", classification=ItemClassification.filler)
                for _ in range(money_cap_items)
            ])

        # Number of Day Lease items required depends on configurable interval
        interval = max(1, int(self.options.day_lease_interval.value))
        lease_count = math.ceil(total_days / interval)
        item_pool.extend([
            self.create_item("Day Lease", classification=ItemClassification.progression)
            for _ in range(lease_count)
        ])

        # Add traps at ~10% of total locations, minimum 3
        remaining_capacity = max(0, total_locations - len(item_pool))
        desired_traps = max(3, total_days // 10)  # scale with run length
        trap_to_add = min(desired_traps, remaining_capacity)
        item_pool.extend([
            self.create_item("Random Customer Card", classification=ItemClassification.trap)
            for _ in range(trap_to_add)
        ])

        while len(item_pool) < total_locations:
            filler_name = self.get_filler_item_name()
            item_pool.append(self.create_item(filler_name))

        logging.debug(f"[Player {self.multiworld.player_name[self.player]}] Total item pool count: {len(item_pool)}")
        logging.debug(f"[Player {self.multiworld.player_name[self.player]}] Total locations: {total_locations}")
        self.multiworld.itempool.extend(item_pool)

    def set_rules(self):
        """Set progression rules and top-up the item pool based on final locations."""

        # Filter dishes only when enabled
        if self.options.dish.value > 0:
            filter_selected_dishes(self)
        else:
            self.selected_dishes = []
            self.valid_dish_locations = []

        restrict_locations_by_progression(self)

        if self.options.goal.value == Goal.option_franchise_x_times:
            required = self.options.franchise_count.value
            for i in range(required + 1, 51):  # expanded upper bound
                name = f"Franchise {i} times"
                if name in FRANCHISE_LOCATION_DICT:
                    EXCLUDED_LOCATIONS.add(FRANCHISE_LOCATION_DICT[name])

        def plateup_completion(state: CollectionState):
            if self.options.goal.value == Goal.option_franchise_x_times:
                count = self.options.franchise_count.value
                loc_name = f"Franchise {count} times"
            else:
                count = self.options.day_count.value
                loc_name = f"Complete Day {count}"
            return state.can_reach(loc_name, "Location", self.player)

        self.multiworld.completion_condition[self.player] = plateup_completion
        apply_rules(self)

        final_locations = [loc for loc in self.multiworld.get_locations() if loc.player == self.player]
        current_items = [item for item in self.multiworld.itempool if item.player == self.player]
        missing = len(final_locations) - len(current_items)
        if missing > 0:
            logging.debug(f"[Player {self.multiworld.player_name[self.player]}] Item pool is short by {missing} items. Adding filler items.")
            for _ in range(missing):
                filler_name = self.get_filler_item_name()
                self.multiworld.itempool.append(self.create_item(filler_name))

    def fill_slot_data(self):
        """Return slot data for this player."""
        options_dict = self.options.as_dict(
            "goal",
            "franchise_count",
            "day_count",
            "death_link",
            "death_link_behavior",
            "appliance_speed_mode",
            "day_lease_interval",
                "starting_money_cap"
        )
        options_dict["items_kept"] = self.options.appliances_kept.value
        if self.options.dish.value == 0:
            options_dict["selected_dishes"] = []
            options_dict["starting_dish"] = None
        else:
            options_dict["starting_dish"] = getattr(self, "starting_dish", None)
            options_dict["selected_dishes"] = getattr(self, "selected_dishes", [])
            # Diagnostics: count of planned dish day locations included
            planned = getattr(self, "_location_name_to_id", {})
            count = 0
            for dish in options_dict["selected_dishes"]:
                for day in range(1, 16):
                    name = f"{dish} - Day {day}"
                    if name in planned:
                        count += 1
            options_dict["dish_locations_present"] = count
        # Diagnostics
        options_dict["dish_unlocks"] = 0 if self.options.dish.value == 0 else 1
        return options_dict

    def get_filler_item_name(self):
        """Randomly select a filler item from the available candidates."""
        filler_candidates = [
            name for name, (code, classification) in ITEMS.items()
            if classification == ItemClassification.filler
        ]
        if not filler_candidates:
            raise Exception("No filler items available in ITEMS.")
        return self.random.choice(filler_candidates)

    def set_selected_dishes(self):
        dish_count = self.options.dish.value
        try:
            from .Locations import dish_dictionary
            all_dishes = list(dish_dictionary.values())
        except Exception:
            all_dishes = [
                "Salad", "Steak", "Burger", "Coffee", "Pizza", "Dumplings", "Turkey",
                "Pie", "Cakes", "Spaghetti", "Fish", "Tacos", "Hot Dogs", "Breakfast", "Stir Fry",
                "Sandwiches", "Sundaes"
            ]
        if dish_count <= 0:
            self.selected_dishes = []
            return
        # Sanitize any pre-set selection (e.g., plando)
        if self.selected_dishes:
            sanitized = [d for d in self.selected_dishes if d in all_dishes]
            if len(sanitized) >= dish_count:
                self.selected_dishes = sanitized[:dish_count]
                return
        # Deterministic per-seed random selection, without replacement
        self.selected_dishes = self.random.sample(all_dishes, k=min(dish_count, len(all_dishes)))