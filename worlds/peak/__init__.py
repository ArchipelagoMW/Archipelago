import logging
import math
from collections import Counter
import typing

from BaseClasses import ItemClassification, CollectionState, LocationProgressType, Tutorial
from worlds.AutoWorld import World, WebWorld
from .Items import PeakItem, item_table, progression_table, useful_table, filler_table, trap_table, lookup_id_to_name, item_groups
from .Locations import LOCATION_TABLE, EXCLUDED_LOCATIONS
from .Options import PeakOptions, peak_option_groups
from .Rules import apply_rules, TROPICS_LOCATIONS, MESA_LOCATIONS, ALPINE_LOCATIONS, ROOTS_LOCATIONS, CALDERA_LOCATIONS, KILN_LOCATIONS

class PeakWeb(WebWorld):
    theme = "stone"
    setup_en = Tutorial(
        tutorial_name="Start Guide",
        description="A guide to playing Gato Roboto Archipelago",
        language="English",
        file_name="guide_en.md",
        link="guide/en",
        authors=["Pathkendle", "TheNickRyan"]
    )

    tutorials = [setup_en]
    option_groups = peak_option_groups

class PeakWorld(World):
    """
    PEAK is a multiplayer climbing game where you and your friends must reach the summit of a procedurally generated mountain.
    """
    game = "PEAK"
    web = PeakWeb()
    is_experimental = True
    options_dataclass = PeakOptions
    options: PeakOptions
    topology_present = False

    item_name_groups = item_groups
    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = LOCATION_TABLE.copy()
    
    # Add event locations to the mapping
    event_locations = [
        "Ascent 1 Completed",
        "Ascent 2 Completed",
        "Ascent 3 Completed",
        "Ascent 4 Completed",
        "Ascent 5 Completed",
        "Ascent 6 Completed",
        "Ascent 7 Completed",
        "Mesa Access",
        "Alpine Access",
        "Roots Access",
        "Tropics Access",
        "Caldera Access",
        "Kiln Access",
        "Idol Dunked",
        "All Badges Collected"

    ]
    for event_loc in event_locations:
        location_name_to_id[event_loc] = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.excluded_locations = set()

    def validate_ids(self):
        """Ensure that item and location IDs are unique."""
        item_ids = list(self.item_name_to_id.values())
        dupe_items = [item for item, count in Counter(item_ids).items() if count > 1]
        if dupe_items:
            raise Exception(f"Duplicate item IDs found: {dupe_items}")

        loc_ids = [loc_id for loc_id in self.location_name_to_id.values() if loc_id is not None]
        dupe_locs = [loc for loc, count in Counter(loc_ids).items() if count > 1]
        if dupe_locs:
            raise Exception(f"Duplicate location IDs found: {dupe_locs}")

    def create_regions(self):
        """Create regions using the location table."""
        from .Regions import create_peak_regions
        self.validate_ids()
        create_peak_regions(self)
    

    def create_item(self, name: str, classification: ItemClassification = None) -> PeakItem:
        """Create a Peak item from the given name."""
        if name not in item_table:
            raise ValueError(f"Item '{name}' not found in item_table")
        
        data = item_table[name]
        
        # Use provided classification or default to item's classification
        if classification is None:
            classification = data.classification
            
        return PeakItem(name, classification, data.code, self.player)

    def create_items(self):
        """Create the initial item pool based on the location table."""
        
        # Calculate total locations, accounting for excluded ascent levels
        goal_type = self.options.goal.value
        required_ascent = self.options.ascent_count.value
        
        # Start with all locations in LOCATION_TABLE
        total_locations = len(LOCATION_TABLE)
        
        # Add event locations
        #total_locations += 15  # 7 Ascent Completed + Mesa/Roots/Alpine/Tropics/Caldera/Kiln Access + Idol Dunked + All Badges Collected
        
        # Subtract excluded ascent locations if goal is Reach Peak
        if goal_type == 0 or goal_type == 3: # Reach Peak goal or Peak and Badges goal
            excluded_ascent_count = 7 - required_ascent  # Number of ascents to exclude
            # Each excluded ascent has 6 badge locations (Beachcomber, Trailblazer, Alpinist, Volcanology, Nomad, Forestry)
            # Plus 1 Scout Sashe location
            # Plus 1 Ascent Completed event
            locations_per_ascent = 7
            total_locations -= (excluded_ascent_count * locations_per_ascent)
            
            logging.debug(f"[Player {self.multiworld.player_name[self.player]}] Excluding {excluded_ascent_count} ascent levels, removing {excluded_ascent_count * locations_per_ascent} locations")
        if self.options.disable_multiplayer_badges.value:
            multiplayer_badge_count = 9
            total_locations -= multiplayer_badge_count
            logging.debug(f"[Player {self.multiworld.player_name[self.player]}] Excluding {multiplayer_badge_count} multiplayer badges")
        
        if self.options.disable_hard_badges.value:
            hard_badge_count = 5
            total_locations -= hard_badge_count
            logging.debug(f"[Player {self.multiworld.player_name[self.player]}] Excluding {hard_badge_count} hard badges")

        if self.options.disable_biome_badges.value:
            biome_badge_count = 10
            total_locations -= biome_badge_count
            logging.debug(f"[Player {self.multiworld.player_name[self.player]}] Excluding {biome_badge_count} biome specific badges")
    
        logging.debug(f"[Player {self.multiworld.player_name[self.player]}] Total locations after exclusions: {total_locations}")
        
        item_pool = []
        
        # Add Progressive Ascent items based on goal requirements
        if goal_type == 0 or goal_type == 3:  # Reach Peak goal - only add enough Progressive Ascent for the required level
            for _ in range(required_ascent):
                item_pool.append(self.create_item("Progressive Ascent"))
            logging.debug(f"[Player {self.multiworld.player_name[self.player]}] Added {required_ascent} Progressive Ascent items (Reach Peak goal)")
        else:  # Other goals - add all 7 Progressive Ascent items
            for _ in range(7):
                item_pool.append(self.create_item("Progressive Ascent"))
            logging.debug(f"[Player {self.multiworld.player_name[self.player]}] Added 7 Progressive Ascent items (non-Reach Peak goal)")

        for _ in range(4):
            item_pool.append(self.create_item("Progressive Mountain"))
        logging.debug(f"[Player {self.multiworld.player_name[self.player]}] Added 4 Progressive Mountain items")
    
        for _ in range(8):
            item_pool.append(self.create_item("Progressive Endurance"))
        logging.debug(f"[Player {self.multiworld.player_name[self.player]}] Added 8 Progressive Endurance items")
    

        # Add progressive stamina items if enabled
        if self.options.progressive_stamina.value:
            max_stamina_upgrades = 4
            if self.options.additional_stamina_bars.value:
                max_stamina_upgrades = 7
            
            for i in range(max_stamina_upgrades):
                item_pool.append(self.create_item("Progressive Stamina Bar"))
            
            logging.debug(f"[Player {self.multiworld.player_name[self.player]}] Added {max_stamina_upgrades} progressive stamina items")

        # Add useful items
        for item_name in useful_table.keys():
            if item_name != "Progressive Stamina Bar":  # Skip stamina bar since we handled it above
                item_pool.append(self.create_item(item_name))
                # Ensure all items needed for acquire locations are in the pool (one each)
        acquire_required_items = [
            "Rope Spool", "Rope Cannon", "Anti-Rope Spool", "Anti-Rope Cannon",
            "Chain Launcher", "Piton", "Rescue Claw", "Scout Cannon", "Flying Disc",
            "Guidebook", "Portable Stove", "Checkpoint Flag", "Compass", "Pirate's Compass",
            "Binoculars", "Parasol", "Balloon", "Balloon Bunch",
            "Lantern", "Flare", "Torch", "Faerie Lantern",
            "Bandages", "First-Aid Kit", "Antidote", "Heat Pack", "Cure-All",
            "Remedy Fungus", "Medicinal Root", "Aloe Vera", "Sunscreen",
            "Marshmallow", "Glizzy", "Fortified Milk", "Trail Mix", "Granola Bar",
            "Scout Cookies", "Airline Food", "Energy Drink", "Sports Drink", "Big Lollipop",
            "Big Egg", "Egg", "Cooked Bird", "Honeycomb", "Beehive", "Bing Bong",
            "Magic Bean", "Blowgun", "Cactus", "Scout Effigy", "Cursed Skull",
            "Pandora's Lunchbox", "Ancient Idol", "Strange Gem", "Book of Bones",
            "Bugle of Friendship", "Bugle", "Scoutmaster's Bugle", "Conch", "Dynamite",
            "Scorpion", "Tick", "Mandrake",
            "Cloud Fungus", "Shelf Shroom", "Bounce Shroom", "Button Shroom",
            "Bugle Shroom", "Cluster Shroom", "Chubby Shroom",
            "Red Crispberry", "Green Crispberry", "Yellow Crispberry",
            "Coconut", "Coconut Half",
            "Brown Berrynana", "Blue Berrynana", "Pink Berrynana", "Yellow Berrynana",
            "Orange Winterberry", "Yellow Winterberry", "Napberry",
            "Red Prickleberry", "Gold Prickleberry",
            "Red Shroomberry", "Blue Shroomberry", "Green Shroomberry",
            "Yellow Shroomberry", "Purple Shroomberry",
            "Purple Kingberry", "Yellow Kingberry", "Green Kingberry",
            "Black Clusterberry", "Red Clusterberry", "Yellow Clusterberry",
        ]

        for item_name in acquire_required_items:
            if item_name in item_table:
                item_pool.append(self.create_item(item_name, ItemClassification.progression))
            else:
                logging.warning(f"[Player {self.multiworld.player_name[self.player]}] Acquire item '{item_name}' not found in item_table")

        logging.debug(f"[Player {self.multiworld.player_name[self.player]}] Added {len(acquire_required_items)} acquire-required items")
        # Calculate how many slots are left for traps and fillers
        remaining_slots = total_locations - len(item_pool)
        
        # Build trap_weights list based on individual trap weights
        trap_weights = []
        trap_weights += (["Instant Death Trap"] * self.options.instant_death_trap_weight.value)
        trap_weights += (["Items to Bombs"] * self.options.items_to_bombs_weight.value)
        trap_weights += (["Pokemon Trivia Trap"] * self.options.pokemon_trivia_trap_weight.value)
        trap_weights += (["Blackout Trap"] * self.options.blackout_trap_weight.value)
        trap_weights += (["Spawn Bee Swarm"] * self.options.spawn_bee_swarm_weight.value)
        trap_weights += (["Banana Peel Trap"] * self.options.banana_peel_trap_weight.value)
        trap_weights += (["Minor Poison Trap"] * self.options.minor_poison_trap_weight.value)
        trap_weights += (["Poison Trap"] * self.options.poison_trap_weight.value)
        trap_weights += (["Deadly Poison Trap"] * self.options.deadly_poison_trap_weight.value)
        trap_weights += (["Tornado Trap"] * self.options.tornado_trap_weight.value)
        trap_weights += (["Swap Trap"] * self.options.swap_trap_weight.value)
        trap_weights += (["Nap Time Trap"] * self.options.nap_time_trap_weight.value)
        trap_weights += (["Hungry Hungry Camper Trap"] * self.options.hungry_hungry_camper_trap_weight.value)
        trap_weights += (["Balloon Trap"] * self.options.balloon_trap_weight.value)
        trap_weights += (["Slip Trap"] * self.options.slip_trap_weight.value)
        trap_weights += (["Freeze Trap"] * self.options.freeze_trap_weight.value)
        trap_weights += (["Cold Trap"] * self.options.cold_trap_weight.value)
        trap_weights += (["Hot Trap"] * self.options.hot_trap_weight.value)
        trap_weights += (["Injury Trap"] * self.options.injury_trap_weight.value)
        trap_weights += (["Cactus Ball Trap"] * self.options.cactus_ball_trap_weight.value)
        trap_weights += (["Yeet Trap"] * self.options.yeet_trap_weight.value)
        trap_weights += (["Tumbleweed Trap"] * self.options.tumbleweed_trap_weight.value)
        trap_weights += (["Zombie Horde Trap"] * self.options.zombie_horde_trap_weight.value)
        trap_weights += (["Gust Trap"] * self.options.gust_trap_weight.value)
        trap_weights += (["Mandrake Trap"] * self.options.mandrake_trap_weight.value)
        trap_weights += (["Fungal Infection Trap"] * self.options.fungal_infection_trap_weight.value)
        trap_weights += (["Fear Trap"] * self.options.fear_trap_weight.value)
        trap_weights += (["Scoutmaster Trap"] * self.options.scoutmaster_trap_weight.value)
        trap_weights += (["Zoom Trap"] * self.options.zoom_trap_weight.value)
        trap_weights += (["Screen Flip Trap"] * self.options.screen_flip_trap_weight.value)
        trap_weights += (["Drop Everything Trap"] * self.options.drop_everything_trap_weight.value)
        trap_weights += (["Pixel Trap"] * self.options.pixel_trap_weight.value)
        trap_weights += (["Eruption Trap"] * self.options.eruption_trap_weight.value)
        trap_weights += (["Beetle Horde Trap"] * self.options.beetle_horde_trap_weight.value)
        trap_weights += (["Custom Trivia Trap"] * self.options.custom_trivia_trap_weight.value)
        
        # Calculate number of trap items based on TrapPercentage
        trap_count = 0 if (len(trap_weights) == 0) else math.ceil(remaining_slots * (self.options.trap_percentage.value / 100.0))
        
        # Add trap items by randomly selecting from weighted list
        trap_pool = []
        for i in range(trap_count):
            trap_item = self.multiworld.random.choice(trap_weights)
            trap_pool.append(self.create_item(trap_item))
        
        item_pool += trap_pool
        
        # Fill remaining slots with filler items
        filler_items = list(filler_table.keys())
        while len(item_pool) < total_locations:
            filler_name = self.random.choice(filler_items)
            item_pool.append(self.create_item(filler_name))
        
        logging.debug(f"[Player {self.multiworld.player_name[self.player]}] Total item pool count: {len(item_pool)}")
        logging.debug(f"[Player {self.multiworld.player_name[self.player]}] Total locations: {total_locations}")
        logging.debug(f"[Player {self.multiworld.player_name[self.player]}] Trap items added: {trap_count}")
        
        self.multiworld.itempool.extend(item_pool)
    
    def output_active_traps(self) -> typing.Dict[str, int]:
        trap_data = {}

        trap_data["instant_death_trap"] = self.options.instant_death_trap_weight.value
        trap_data["items_to_bombs"] = self.options.items_to_bombs_weight.value
        trap_data["pokemon_trivia_trap"] = self.options.pokemon_trivia_trap_weight.value
        trap_data["blackout_trap"] = self.options.blackout_trap_weight.value
        trap_data["spawn_bee_swarm"] = self.options.spawn_bee_swarm_weight.value
        trap_data["banana_peel_trap"] = self.options.banana_peel_trap_weight.value
        trap_data["minor_poison_trap"] = self.options.minor_poison_trap_weight.value
        trap_data["poison_trap"] = self.options.poison_trap_weight.value
        trap_data["deadly_poison_trap"] = self.options.deadly_poison_trap_weight.value
        trap_data["tornado_trap"] = self.options.tornado_trap_weight.value
        trap_data["swap_trap"] = self.options.swap_trap_weight.value
        trap_data["nap_time_trap"] = self.options.nap_time_trap_weight.value
        trap_data["hungry_hungry_camper_trap"] = self.options.hungry_hungry_camper_trap_weight.value
        trap_data["balloon_trap"] = self.options.balloon_trap_weight.value
        trap_data["slip_trap"] = self.options.slip_trap_weight.value
        trap_data["freeze_trap"] = self.options.freeze_trap_weight.value
        trap_data["cold_trap"] = self.options.cold_trap_weight.value
        trap_data["hot_trap"] = self.options.hot_trap_weight.value
        trap_data["injury_trap"] = self.options.injury_trap_weight.value
        trap_data["cactus_ball_trap"] = self.options.cactus_ball_trap_weight.value
        trap_data["yeet_trap"] = self.options.yeet_trap_weight.value
        trap_data["tumbleweed_trap"] = self.options.tumbleweed_trap_weight.value
        trap_data["zombie_horde_trap"] = self.options.zombie_horde_trap_weight.value
        trap_data["gust_trap"] = self.options.gust_trap_weight.value
        trap_data["mandrake_trap"] = self.options.mandrake_trap_weight.value
        trap_data["fungal_infection_trap"] = self.options.fungal_infection_trap_weight.value
        trap_data["fear_trap"] = self.options.fear_trap_weight.value
        trap_data["scoutmaster_trap"] = self.options.scoutmaster_trap_weight.value
        trap_data["zoom_trap"] = self.options.zoom_trap_weight.value
        trap_data["screen_flip_trap"] = self.options.screen_flip_trap_weight.value
        trap_data["drop_everything_trap"] = self.options.drop_everything_trap_weight.value
        trap_data["pixel_trap"] = self.options.pixel_trap_weight.value
        trap_data["eruption_trap"] = self.options.eruption_trap_weight.value
        trap_data["beetle_horde_trap"] = self.options.beetle_horde_trap_weight.value
        trap_data["custom_trivia_trap"] = self.options.custom_trivia_trap_weight.value

        return trap_data

    def set_rules(self):
        """Set progression rules and top-up the item pool based on final locations."""

        apply_rules(self)

        player = self.player
        # Count total Progressive items we're placing
        prog_ascent_count = 7 if self.options.goal.value != 0 and self.options.goal.value != 3 else self.options.ascent_count.value
        prog_stamina_count = 0
        if self.options.progressive_stamina.value:
            prog_stamina_count = 7 if self.options.additional_stamina_bars.value else 4
        prog_endurance_count = 8
        
        shore_accessible_locations = []
        for location in self.multiworld.get_locations(player):
            if location.progress_type == LocationProgressType.EXCLUDED:
                continue
            
            # Skip event locations
            if location.address is None:
                continue
                
            # If it's not in a biome list, it's shore-accessible
            if (location.name not in TROPICS_LOCATIONS and 
                location.name not in ROOTS_LOCATIONS and
                location.name not in MESA_LOCATIONS and
                location.name not in ALPINE_LOCATIONS and
                location.name not in CALDERA_LOCATIONS and
                location.name not in KILN_LOCATIONS and
                "(Ascent" not in location.name):
                shore_accessible_locations.append(location)
        
        logging.info(f"[Player {self.multiworld.player_name[player]}] Found {len(shore_accessible_locations)} shore-accessible locations")
        
        # Set item placement rules
        for location in self.multiworld.get_locations(player):
            if location.progress_type == LocationProgressType.EXCLUDED:
                continue
                
            if "(Ascent" in location.name or "Scout sashe" in location.name:
                import re
                match = re.search(r'Ascent (\d+)', location.name)
                if match:
                    required_ascents = int(match.group(1))
                    def make_rule(req_asc, req_stam=0, req_end=0):
                        def rule(item):

                            # prevent these items entirely on high ascents
                            if item.player != player:
                                return True
                            
                            # NEVER place Progressive Mountain on ANY ascent location
                            if item.name == "Progressive Mountain":
                                return False
                            
                            # For high ascents, be conservative
                            if req_asc >= 5:
                                # Don't place any progression items here
                                if item.name in ["Progressive Ascent", "Progressive Stamina Bar", "Progressive Endurance"]:
                                    return False
                            elif req_asc >= 3:
                                # Don't place stamina or ascent here
                                if item.name in ["Progressive Ascent", "Progressive Stamina Bar"]:
                                    return False
                            elif req_asc >= 1:
                                # Don't place ascent here
                                if item.name == "Progressive Ascent":
                                    return False
                            
                            return True
                        return rule
                    
                    # Apply rules based on ascent requirements
                    if required_ascents >= 6:
                        location.item_rule = make_rule(required_ascents, 3, 4)
                    elif required_ascents >= 3:
                        location.item_rule = make_rule(required_ascents, 3, 0)
                    else:
                        location.item_rule = make_rule(required_ascents, 0, 0)

            if location.name in TROPICS_LOCATIONS or location.name in ROOTS_LOCATIONS:
                def biome_rule_1(item):
                    if item.player != player:
                        return True
                    if item.name == "Progressive Mountain":
                        if "napberry" not in location.name.lower():
                            if ("berry" in location.name.lower() or 
                                "conch" in location.name.lower() or 
                                "binoculars" in location.name.lower() or 
                                "guidebook" in location.name.lower()):
                                return False
                        mountains_in_pool = sum(1 for i in self.multiworld.itempool if i.player == player and i.name == "Progressive Mountain")
                        return mountains_in_pool >= 2  # Need at least 2 in pool to place 1 here
                    return True
                location.item_rule = biome_rule_1

            elif location.name in ALPINE_LOCATIONS or location.name in MESA_LOCATIONS:
                def biome_rule_2(item):
                    if item.player != player:
                        return True

                    # Can place Progressive Mountain here if at least 2 others exist elsewhere
                    if item.name == "Progressive Mountain":
                        if "napberry" not in location.name.lower():
                            if ("berry" in location.name.lower() or 
                                "conch" in location.name.lower() or 
                                "binoculars" in location.name.lower() or 
                                "guidebook" in location.name.lower()):
                                return False
                        mountains_in_pool = sum(1 for i in self.multiworld.itempool if i.player == player and i.name == "Progressive Mountain")
                        return mountains_in_pool >= 3  # Need at least 3 in pool to place 1 here
                    return True
                location.item_rule = biome_rule_2

            elif location.name in CALDERA_LOCATIONS:
                def biome_rule_3(item):
                    if item.player != player:
                        return True
                    if item.name == "Progressive Mountain":
                        if "napberry" not in location.name.lower():
                            if ("berry" in location.name.lower() or 
                                "conch" in location.name.lower() or 
                                "binoculars" in location.name.lower() or 
                                "guidebook" in location.name.lower()):
                                return False
                        mountains_in_pool = sum(1 for i in self.multiworld.itempool if i.player == player and i.name == "Progressive Mountain")
                        return mountains_in_pool >= 4  # Need all 4 in pool to place 1 here
                    return True
                location.item_rule = biome_rule_3

            elif location.name in KILN_LOCATIONS:
                def biome_rule_kiln(item):
                    if item.player != player:
                        return True
                    # NEVER place Progressive Mountain in Kiln locations
                    if item.name == "Progressive Mountain":
                        return False
                    return True
                location.item_rule = biome_rule_kiln
            
            # Limit Progressive Mountains in shore-accessible locations
            if location in shore_accessible_locations:
                old_rule = location.item_rule
                
                def shore_mountain_limit(item):
                    if item.player != player:
                        return True
                    
                    if item.name == "Progressive Mountain":
                        # Count how many mountains are already placed in shore locations
                        placed_count = sum(1 for loc in shore_accessible_locations 
                                        if loc.item and loc.item.name == "Progressive Mountain" and loc.item.player == player)
                        
                        # Only allow if we haven't hit the limit (max 2 in shore)
                        return placed_count < 2
                    
                    return True
                
                # Combine with existing rule if present
                if old_rule:
                    location.item_rule = lambda item, old=old_rule, shore_limit=shore_mountain_limit: old(item) and shore_limit(item)
                else:
                    location.item_rule = shore_mountain_limit

        # Access options directly via self.options
        goal = self.options.goal.value
        ascent_num = self.options.ascent_count.value

        # Set completion condition based on goal type
        if goal == 0:  # Reach Peak
            if 1 <= ascent_num <= 7:
                self.multiworld.completion_condition[self.player] = (
                    lambda state, n=ascent_num: state.has(f"Ascent {n} Completed", self.player)
                )
            else:
                return 

        elif goal == 1:  # Complete All Badges
            self.multiworld.completion_condition[self.player] = (
                lambda state: state.has("All Badges Collected", self.player)
            )

        elif goal == 2:  # 24 Karat Badge
            self.multiworld.completion_condition[self.player] = (
                lambda state: state.has("Idol Dunked", self.player)
            )
        elif goal == 3:  # Peak and Badges
            if 1 <= ascent_num <= 7:
                self.multiworld.completion_condition[self.player] = (
                    lambda state, n=ascent_num: state.has(f"Ascent {n} Completed", self.player) and state.has("All Badges Collected", self.player)
                )
        else:
            return  # Unsupported goal type, exit early

        # Ensure item pool matches number of locations
        final_locations = [loc for loc in self.multiworld.get_locations() 
                   if loc.player == self.player and loc.address is not None]
        current_items = [item for item in self.multiworld.itempool if item.player == self.player]
        missing = len(final_locations) - len(current_items)

        if missing > 0:
            logging.debug(
                f"[Player {self.multiworld.player_name[self.player]}] "
                f"Item pool is short by {missing} items. Adding filler items."
            )
            for _ in range(missing):
                filler_name = self.get_filler_item_name()
                self.multiworld.itempool.append(self.create_item(filler_name))

    def fill_slot_data(self):
        """Return slot data for this player."""
        session_id = f"{self.multiworld.seed_name}_{self.player}"
        
        # Calculate actual badge count from locations that exist in this seed
        badge_locations = [loc for loc in self.multiworld.get_locations(self.player) 
                        if loc.name.endswith(" Badge") and loc.address is not None]
        max_badges_available = len(badge_locations)
        
        # Respect the option but clamp to what's actually available
        requested_badge_count = self.options.badge_count.value
        actual_badge_count = min(requested_badge_count, max_badges_available)

        mountain_hints = []
        for location in self.multiworld.get_locations():
            if location.item and location.item.name == "Progressive Mountain" and location.item.player == self.player:
                mountain_hints.append({
                    "location": location.name,
                    "player": self.multiworld.get_player_name(location.player),
                    "game": self.multiworld.game[location.player],
                    "location_id": location.address,
                    "player_slot": location.player
                })
        
        slot_data = {
            "goal": self.options.goal.value,
            "ascent_count": self.options.ascent_count.value,
            "badge_count": actual_badge_count,
            "progressive_stamina": self.options.progressive_stamina.value,
            "additional_stamina_bars": self.options.additional_stamina_bars.value,
            "trap_percentage": self.options.trap_percentage.value,
            "ring_link": self.options.ring_link.value,
            "hard_ring_link": self.options.hard_ring_link.value,
            "energy_link": self.options.energy_link.value,
            "trap_link": self.options.trap_link.value,
            "death_link": self.options.death_link.value,
            "death_link_behavior": self.options.death_link_behavior.value,
            "death_link_send_behavior": self.options.death_link_send_behavior.value,
            "active_traps": self.output_active_traps(),
            "session_id": session_id,
            "mountain_hints": mountain_hints
        }
        
        # Log what we're sending
        logging.info(f"[Player {self.multiworld.player_name[self.player]}] Slot data being sent: {slot_data}")
        if requested_badge_count > max_badges_available:
            logging.warning(f"[Player {self.multiworld.player_name[self.player]}] Requested {requested_badge_count} badges but only {max_badges_available} available in seed. Clamped to {actual_badge_count}")
        
        return slot_data

    def get_filler_item_name(self):
        """Randomly select a filler item from the available candidates."""
        if not filler_table:
            raise Exception("No filler items available in item_table.")
        return self.random.choice(list(filler_table.keys()))
