from collections.abc import Sequence
from collections import defaultdict
import json
from logging import warning
from typing import cast, Any, Callable, Dict, Set, List, Optional, TextIO, Union

from BaseClasses import CollectionState, MultiWorld, Region, Location, LocationProgressType, Entrance, Tutorial, ItemClassification
from worlds.AutoWorld import World, WebWorld
from worlds.generic.Rules import CollectionRule, ItemRule, add_rule, add_item_rule

from .items import ERItem, ERItemData, filler_item_names, item_descriptions, item_table, item_name_groups
from .locations import ERLocation, ERLocationData, location_tables, location_descriptions, location_dictionary, location_name_groups, region_order, region_order_dlc
from .options import EROptions, option_groups

#Web stuff
class EldenRingWeb(WebWorld):
    rich_text_options_doc = True
    theme = "stone"
    option_groups = option_groups
    item_descriptions = item_descriptions

#Main World
class EldenRing(World):
    """
    This is the description of the game that will be displayed on the AP website.
    """

    game = "EldenRing"
    options: EROptions
    options_dataclass = EROptions
    web = EldenRingWeb()
    base_id = 69000
    required_client_version = (0, 4, 2) # tbh idk what version is needed
    topology_present = True
    item_name_to_id = {data.name: data.ap_code for data in item_table.values() if data.ap_code is not None}
    location_name_to_id = {
        location.name: location.ap_code
        for locations in location_tables.values()
        for location in locations
        if location.ap_code is not None
    }
    location_name_groups = location_name_groups
    item_name_groups = item_name_groups
    location_descriptions = location_descriptions
    item_descriptions = item_descriptions

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)
        self.all_excluded_locations = set()

    def generate_early(self) -> None:
        self.created_regions = set()
        self.all_excluded_locations.update(self.options.exclude_locations.value)

    def create_regions(self) -> None:
        # Create Vanilla Regions
        regions: Dict[str, Region] = {"Menu": self.create_region("Menu", {})}
        regions.update({region_name: self.create_region(region_name, location_tables[region_name]) for region_name in region_order})
        """    "Chapel of Anticipation",
            "Stranded Graveyard",
        ]})""" #dont need the list just using region order

        # Create DLC Regions
        if self.options.enable_dlc:
            regions.update({region_name: self.create_region(region_name, location_tables[region_name]) for region_name in region_order_dlc})

        # Connect Regions
        def create_connection(from_region: str, to_region: str):
            connection = Entrance(self.player, f"Go To {to_region}", regions[from_region])
            regions[from_region].exits.append(connection)
            connection.connect(regions[to_region])

        regions["Menu"].exits.append(Entrance(self.player, "New Game", regions["Menu"]))
        self.multiworld.get_entrance("New Game", self.player).connect(regions["Chapel of Anticipation"])
        # Start #MARK: Connections
        create_connection("Chapel of Anticipation", "Stranded Graveyard")
        # Limgrave
        create_connection("Stranded Graveyard", "Limgrave")
        create_connection("Stranded Graveyard", "Fringefolk Hero's Grave")
        
        create_connection("Limgrave", "Church of Elleh")
        create_connection("Limgrave", "Coastal Cave")
        create_connection("Limgrave", "Groveside Cave")
        create_connection("Limgrave", "Stormfoot Catacombs")
        create_connection("Limgrave", "Gatefront Ruins")
        create_connection("Limgrave", "Limgrave Tunnels")
        create_connection("Limgrave", "Stormgate")
        create_connection("Limgrave", "Stormhill Shack")
        create_connection("Limgrave", "Waypoint Ruins")
        create_connection("Limgrave", "Dragon-Burnt Ruins")
        create_connection("Limgrave", "Murkwater Cave")
        create_connection("Limgrave", "Mistwood Ruins")
        create_connection("Limgrave", "Fort Haight")
        create_connection("Limgrave", "Third Church of Marika")
        create_connection("Limgrave", "LG Artist's Shack")
        create_connection("Limgrave", "Summonwater Village")
        create_connection("Limgrave", "Murkwater Catacombs")
        create_connection("Limgrave", "Highroad Cave")
        create_connection("Limgrave", "Deathtouched Catacombs",)
        


        
        
        # create_connection("Dragon-Burnt Ruins", "caelid crystal tunnels")
        create_connection("Coastal Cave", "Church of Dragon Communion")


        create_connection("Limgrave", "Liurnia of The Lakes")
        # Liurnia

        
        create_connection("Limgrave", "Caelid")
        # Caelid
        create_connection("Caelid", "Smoldering Church")


        
        #create_connection("Limgrave", "Siofra River")
        #create_connection("Limgrave", "Stormveil Castle")
        #create_connection("Limgrave", "Liurnia of The Lakes")
        # Liurnia of The Lakes
        #create_connection("Liurnia of The Lakes", "Chapel of Anticipation [Return]") # add real LL location for ca return


        #create_connection("Caelid", "Roundtable Hold") #only after getting to caelid area


        # Connect DLC Regions
        #if self.options.enable_dlc:
            #create_connection("Mohgwyn Palace", "Gravesite Plain")
        

    # For each region, add the associated locations retrieved from the corresponding location_table
    def create_region(self, region_name, location_table) -> Region:
        new_region = Region(region_name, self.player, self.multiworld)

        # Use this to un-exclude event locations so the fill doesn't complain about items behind
        # them being unreachable.
        excluded = self.options.exclude_locations.value

        for location in location_table:
            if self._is_location_available(location):
                new_location = ERLocation(self.player, location, new_region)
                if (
                    # Exclude missable locations that don't allow useful items
                    location.missable and self.options.missable_location_behavior == "randomize_unimportant"
                    and not (
                        # Unless they are excluded to a higher degree already
                        location.name in self.all_excluded_locations
                        and self.options.missable_location_behavior < self.options.excluded_location_behavior
                    )
                ):
                    new_location.progress_type = LocationProgressType.EXCLUDED
            else:
                # Replace non-randomized items with events that give the default item
                event_item = (
                    self.create_item(location.default_item_name) if location.default_item_name
                    else ERItem.event(location.name, self.player)
                )

                new_location = ERLocation(
                    self.player,
                    location,
                    parent = new_region,
                    event = True,
                )
                event_item.code = None
                new_location.place_locked_item(event_item)
                if location.name in excluded:
                    excluded.remove(location.name)
                    # Only remove from all_excluded if excluded does not have priority over missable
                    if not (self.options.missable_location_behavior < self.options.excluded_location_behavior):
                        self.all_excluded_locations.remove(location.name)

            new_region.locations.append(new_location)

        self.multiworld.regions.append(new_region)
        self.created_regions.add(region_name)
        return new_region
    
    def create_items(self) -> None:
        # Just used to efficiently deduplicate items
        item_set: Set[str] = set()

        # Gather all default items on randomized locations
        self.local_itempool = []
        num_required_extra_items = 0
        for location in cast(List[ERLocation], self.multiworld.get_unfilled_locations(self.player)):
            if not self._is_location_available(location.name):
                raise Exception("ER generation bug: Added an unavailable location.")

            default_item_name = cast(str, location.data.default_item_name)
            item = item_table[default_item_name]
            if item.skip:
                num_required_extra_items += 1
            else:
                # For unique items, make sure there aren't duplicates in the item set even if there
                # are multiple in-game locations that provide them.
                if default_item_name in item_set:
                    num_required_extra_items += 1
                else:
                    item_set.add(default_item_name)
                    self.local_itempool.append(self.create_item(default_item_name))

        injectables = self._create_injectable_items(num_required_extra_items)
        num_required_extra_items -= len(injectables)
        self.local_itempool.extend(injectables)

        # Extra filler items for locations containing skip items
        self.local_itempool.extend(self.create_item(self.get_filler_item_name()) for _ in range(num_required_extra_items))

        # Potentially fill some items locally and remove them from the itempool
        self._fill_local_items()

        # Add items to itempool
        self.multiworld.itempool += self.local_itempool

    def _create_injectable_items(self, num_required_extra_items: int) -> List[ERItem]:
        """Returns a list of items to inject into the multiworld instead of skipped items.

        If there isn't enough room to inject all the necessary progression items
        that are in missable locations by default, this adds them to the
        player's starting inventory.
        """

        all_injectable_items = [
            item for item
            in item_table.values()
        ]
        injectable_mandatory = [
            item for item in all_injectable_items
            if item.classification == ItemClassification.progression
        ]
        injectable_optional = [
            item for item in all_injectable_items
            if item.classification != ItemClassification.progression
        ]

        number_to_inject = min(num_required_extra_items, len(all_injectable_items))
        items = (
            self.random.sample(
                injectable_mandatory,
                k=min(len(injectable_mandatory), number_to_inject)
            )
            + self.random.sample(
                injectable_optional,
                k=max(0, number_to_inject - len(injectable_mandatory))
            )
        )

        if number_to_inject < len(injectable_mandatory):
            # It's worth considering the possibility of _removing_ unimportant
            # items from the pool to inject these instead rather than just
            # making them part of the starting health pack
            for item in injectable_mandatory:
                if item in items: continue
                self.multiworld.push_precollected(self.create_item(item))
                warning(
                    f"Couldn't add \"{item.name}\" to the item pool for " + 
                    f"{self.player_name}. Adding it to the starting " +
                    f"inventory instead."
                )

        return [self.create_item(item) for item in items]

    def _fill_local_items(self) -> None:
        """Removes certain items from the item pool and manually places them in the local world.

        We can't do this in pre_fill because the itempool may not be modified after create_items.
        """

    def _fill_local_item(
        self, name: str,
        regions: List[str],
        additional_condition: Optional[Callable[[ERLocationData], bool]] = None,
    ) -> None:
        """Chooses a valid location for the item with the given name and places it there.
        
        This always chooses a local location among the given regions. If additional_condition is
        passed, only locations meeting that condition will be considered.

        If the item could not be placed, it will be added to starting inventory.
        """
        item = next((item for item in self.local_itempool if item.name == name), None)
        if not item: return

        candidate_locations = [
            location for location in (
                self.multiworld.get_location(location.name, self.player)
                for region in regions
                for location in location_tables[region]
                if self._is_location_available(location)
                and not location.missable
                and not location.conditional
                and (not additional_condition or additional_condition(location))
            )
            # We can't use location.progress_type here because it's not set
            # until after `set_rules()` runs.
            if not location.item and location.name not in self.all_excluded_locations
            and location.item_rule(item)
        ]

        self.local_itempool.remove(item)

        if not candidate_locations:
            warning(f"Couldn't place \"{name}\" in a valid location for {self.player_name}. Adding it to starting inventory instead.")
            location = next(
                (location for location in self._get_our_locations() if location.data.default_item_name == item.name),
                None
            )
            if location: self._replace_with_filler(location)
            self.multiworld.push_precollected(self.create_item(name))
            return

        location = self.random.choice(candidate_locations)
        location.place_locked_item(item)

    def create_item(self, item: Union[str, ERItemData]) -> ERItem:
        data = item if isinstance(item, ERItemData) else item_table[item]
        return ERItem(self.player, data)

    def _replace_with_filler(self, location: ERLocation) -> None:
        """If possible, choose a filler item to replace location's current contents with."""
        if location.locked: return

        # Try 10 filler items. If none of them work, give up and leave it as-is.
        for _ in range(0, 10):
            candidate = self.create_filler()
            if location.item_rule(candidate):
                location.item = candidate
                return

    def get_filler_item_name(self) -> str:
        return self.random.choice(filler_item_names)

    def set_rules(self) -> None: #WIP #MARK: Rules

        #self._add_shop_rules()
        #self._add_npc_rules()
        #self._add_remembrance_rules()

        #smth like this for if an item and place is needed
        """self._add_entrance_rule("Leyndell, Royal Capital", lambda state: (
            self._has_enough_great_runes(state, self.options.great_runes_required)
            and self._can_get(state, "CO: Draconic Tree Sential")
        ))"""

        # Region locking
        #self._add_entrance_rule("Liurnia of The Lakes", lambda state: (self._has_enough_great_runes(state, 1)))
        #self._add_entrance_rule("Caelid", lambda state: ( self._has_enough_great_runes(state, 2) )) # 2 is runes required

        #do this for if an item or place is needed
        #self._add_entrance_rule("Mountain Top of the Giants", "Rold Medallion")

        self._add_entrance_rule("Fringefolk Hero's Grave", lambda state: state.has("Stonesword Key", self.player, 2))
        self._add_location_rule("LG/(SWV): Green Turtle Talisman - behind imp statue", lambda state: state.has("Stonesword Key", self.player))
        self._add_location_rule("LG/SR: Incantation Scarab - \"Homing Instinct\" Painting reward to NW", 
                                lambda state: state.has("\"Homing Instinct\" Painting", self.player))
        

        
        """
        # DLC Access Rules Below
        if self.options.enable_dlc:
            self._add_entrance_rule("Gravesite Plain", lambda state: self._can_get(state, "MP: Mohg Remembrance"))

            if self.options.late_dlc:
                self._add_entrance_rule(
                    "Gravesite Plain", 
                    lambda state: state.has("Rold Medallion", self.player) 
                    and state.has("Haligtree Secret Medallion (Left)", self.player) 
                    and state.has("Haligtree Secret Medallion (Right)", self.player) 
                    and self._can_get(state, "LRC: Morgott Remembrance"))
                    and self._can_get(state, "MP: Mohg Remembrance")
      
        

        if self.options.ending_condition >= 1 and self.options.enable_dlc:
            self.multiworld.completion_condition[self.player] = lambda state: self._can_get(state, "EI: Consort Radahn Remembrance")
        else:
            self.multiworld.completion_condition[self.player] = lambda state: self._can_get(state, "LAC: Elden Beast Remembrance")
        """

    def _has_enough_great_runes(self, state: CollectionState, runes_required: int) -> bool:
        """Returns whether the given state has enough great runes."""
        runeCount = 0
        if state.has("Godrick's Great Rune", self.player): runeCount += 1
        if state.has("Rykard's Great Rune", self.player): runeCount += 1
        if state.has("Radahn's Great Rune", self.player): runeCount += 1
        if state.has("Morgott's Great Rune", self.player): runeCount += 1
        if state.has("Mohg's Great Rune", self.player): runeCount += 1
        if state.has("Malenia's Great Rune", self.player): runeCount += 1
        if state.has("Great Rune of the Unborn", self.player): runeCount += 1
        return (
            runes_required >= runeCount
        )
    
    def _add_shop_rules(self) -> None: # this would be bell bearing stuff ig #MARK: Shop Rules
        """Adds rules for items unlocked in shops."""

        # Ashes
        ashes = {
            "Mortician's Ashes": ["Alluring Skull", "Ember", "Grave Key"],
            "Dreamchaser's Ashes": ["Life Ring", "Hidden Blessing"],
            "Paladin's Ashes": ["Lloyd's Shield Ring"],
            "Grave Warden's Ashes": ["Ember"],
            "Prisoner Chief's Ashes": [
                "Karla's Pointed Hat", "Karla's Coat", "Karla's Gloves", "Karla's Trousers"
            ],
            "Xanthous Ashes": ["Xanthous Overcoat", "Xanthous Gloves", "Xanthous Trousers"],
            "Dragon Chaser's Ashes": ["Ember"],
            "Easterner's Ashes": [
                "Washing Pole", "Eastern Helm", "Eastern Armor", "Eastern Gauntlets",
                "Eastern Leggings", "Wood Grain Ring",
            ],
            "Captain's Ashes": [
                "Millwood Knight Helm", "Millwood Knight Armor", "Millwood Knight Gauntlets",
                "Millwood Knight Leggings", "Refined Gem",
            ]
        }
        for (ash, items) in ashes.items():
            self._add_location_rule([f"FS: {item} - {ash}" for item in items], ash)

        # Shop unlocks
        shop_unlocks = {
            "Cornyx": [
                (
                    "Great Swamp Pyromancy Tome", "Great Swamp Tome",
                    ["Poison Mist", "Fire Orb", "Profuse Sweat", "Bursting Fireball"]
                ),
                (
                    "Carthus Pyromancy Tome", "Carthus Tome",
                    ["Acid Surge", "Carthus Flame Arc", "Carthus Beacon"]
                ),
                ("Izalith Pyromancy Tome", "Izalith Tome", ["Great Chaos Fire Orb", "Chaos Storm"]),
            ],
            "Irina": [
                (
                    "Braille Divine Tome of Carim", "Tome of Carim",
                    ["Med Heal", "Tears of Denial", "Force"]
                ),
                (
                    "Braille Divine Tome of Lothric", "Tome of Lothric",
                    ["Bountiful Light", "Magic Barrier", "Blessed Weapon"]
                ),
            ],
            "Orbeck": [
                ("Sage's Scroll", "Sage's Scroll", ["Great Farron Dart", "Farron Hail"]),
                (
                    "Golden Scroll", "Golden Scroll",
                    [
                        "Cast Light", "Repair", "Hidden Weapon", "Hidden Body",
                        "Twisted Wall of Light"
                    ],
                ),
                ("Logan's Scroll", "Logan's Scroll", ["Homing Soulmass", "Soul Spear"]),
                (
                    "Crystal Scroll", "Crystal Scroll",
                    ["Homing Crystal Soulmass", "Crystal Soul Spear", "Crystal Magic Weapon"]
                ),
            ],
            "Karla": [
                ("Quelana Pyromancy Tome", "Quelana Tome", ["Firestorm", "Rapport", "Fire Whip"]),
                (
                    "Grave Warden Pyromancy Tome", "Grave Warden Tome",
                    ["Black Flame", "Black Fire Orb"]
                ),
                ("Deep Braille Divine Tome", "Deep Braille Tome", ["Gnaw", "Deep Protection"]),
                (
                    "Londor Braille Divine Tome", "Londor Tome",
                    ["Vow of Silence", "Dark Blade", "Dead Again"]
                ),
            ],
        }
        for (shop, unlocks) in shop_unlocks.items():
            for (key, key_name, items) in unlocks:
                self._add_location_rule(
                    [f"FS: {item} - {shop} for {key_name}" for item in items], key)
                
    def _add_npc_rules(self) -> None: # npc quest stuff #MARK: Quest Rules
        """Adds rules for items accessible via NPC quests.

        We list missable locations here even though they never contain progression items so that the
        game knows what sphere they're in.

        Generally, for locations that can be accessed early by killing NPCs, we set up requirements
        assuming the player _doesn't_ so they aren't forced to start killing allies to advance the
        quest.
        """

        ## Patches

        # Patches will only set up shop in Firelink once he's tricked you in the bell tower. He'll
        # only do _that_ once you've spoken to Siegward after killing the Fire Demon and lit the
        # Rosaria's Bed Chamber bonfire. He _won't_ set up shop in the Cathedral if you light the
        # Rosaria's Bed Chamber bonfire before getting tricked by him, so we assume these locations
        # require the bell tower.
        self._add_location_rule([
            "CD: Shotel - Patches",
            "CD: Ember - Patches",
            "FS: Rusted Gold Coin - don't forgive Patches"
        ], lambda state: (
            self._can_go_to(state, "Firelink Shrine Bell Tower")
            and self._can_go_to(state, "Cathedral of the Deep")
        ))

        # Patches sells this after you tell him to search for Greirat in Grand Archives
        self._add_location_rule([
            "FS: Hidden Blessing - Patches after searching GA"
        ], lambda state: (
            self._can_get(state, "CD: Shotel - Patches")
            and self._can_get(state, "FS: Ember - shop for Greirat's Ashes")
        ))

        # Only make the player kill Patches once all his other items are available
        self._add_location_rule([
            "CD: Winged Spear - kill Patches",
            # You don't _have_ to kill him for this, but he has to be in Firelink at the same time
            # as Greirat to get it in the shop and that may not be feasible if the player progresses
            # Greirat's quest much faster.
            "CD: Horsehoof Ring - Patches",
        ], lambda state: (
            self._can_get(state, "FS: Hidden Blessing - Patches after searching GA")
            and self._can_get(state, "FS: Rusted Gold Coin - don't forgive Patches")
        ))
            
    def _add_remembrance_rules(self) -> None: # done? #MARK: Remembrance Rules
        """Adds rules for items obtainable for trading remembrances."""

        remembrances = [
            (
                "Remembrance of the Grafted", "Godrick",
                ["Axe of Godrick", "Grafted Dragon"]
            ),
            (
                "Remembrance of the Full Moon Queen", "Rennala", 
                ["Carian Regal Scepter", "Rennala's Full Moon"]
            ),
            (
                "Remembrance of the Starscourge", "Radahn",
                ["Starscourge Greatsword", "Lion Greatbow"]
            ),
            (
                "Remembrance of the Regal Ancestor", "Regal Ancestor Spirit",
                ["Winged Greathorn", "Ancestral Spirit's Horn"]
            ),
            (
                "Remembrance of the Omen King", "Morgott",
                ["Morgott's Cursed Sword", "Regal Omen Bairn"]
            ),
            (
                "Remembrance of the Naturalborn", "Astel",
                ["Waves of Darkness", "Bastard's Stars"]
            ),
            (
                "Remembrance of the Blasphemous", "Rykard",
                ["Rykard's Rancor", "Blasphemous Blade"]
            ),
            (
                "Remembrance of the Lichdragon", "Lichdragon",
                ["Fortissax's Lightning Spear", "Death Lightning"]
            ),
            (
                "Remembrance of the Fire Giant", "Fire Giant",
                ["Giant's Red Braid", "Burn, O Flame!"]
            ),
            (
                "Remembrance of the Blood Lord", "Mohg",
                ["Mohgwyn's Sacred Spear", "Bloodboon"]
            ),
            (
                "Remembrance of the Black Blade", "Maliketh",
                ["Maliketh's Black Blade", "Black Blade"]
            ),
            (
                "Remembrance of the Dragonlord", "Placidusax",
                ["Dragon King's Cragblade", "Placidusax's Ruin"]
            ),
            (
                "Remembrance of Hoarah Loux", "Hoarah Loux",
                ["Axe of Godfrey", "Hoarah Loux's Earthshaker"]
            ),
            (
                "Remembrance of the Rot Goddess", "Malenia",
                ["Hand of Malenia", "Scarlet Aeonia"]
            ),
            (
                "Elden Remembrance", "Elden Beast",
                ["Marika's Hammer", "Sacred Relic Sword"]
            ),
        ]

        dlc_remembrances = [
            (
                "Remembrance of the Dancing Lion", "Dancing Lion",
                ["Enraged Divine Beast", "Divine Beast Frost Stomp"]
            ),
            (
                "Remembrance of the Twin Moon Knight", "Rellana",
                ["Rellana's Twin Blades", "Rellana's Twin Moons"]
            ),
            (
                "Remembrance of Putrescence", "Putrescent Knight",
                ["Putrescence Cleaver", "Vortex of Putrescence"]
            ),
            (
                "Remembrance of the Wild Boar Rider", "Commander Gaius", 
                ["Sword Lance", "Blades of Stone"]
            ),
            (
                "Remembrance of the Shadow Sunflower", "Scadutree Avatar",
                ["Shadow Sunflower Blossom", "Land of Shadow"]
            ),
            (
                "Remembrance of the Impaler", "Messmer",
                ["Spear of the Impaler", "Messmer's Orb"]
            ),
            (
                "Remembrance of the Saint of the Bud", "Romina",
                ["Poleblade of the Bud", "Rotten Butterflies"]
            ),
            (
                "Remembrance of the Mother of Fingers", "Metyr",
                ["Staff of the Great Beyond", "Gazing Finger"]
            ),
            (
                "Remembrance of the Lord of Frenzied Flame", "Midra",
                ["Greatsword of Damnation", "Midra's Flame of Frenzy"]
            ),
            (
                "Remembrance of a God and a Lord", "Consort Radahn",
                ["Greatsword of Radahn (Lord) + (Light)", "Light of Miquella"]
            ),
        ]
            
        if self.options.enable_dlc:
            remembrances += dlc_remembrances
            self._add_location_rule("GADC: Bayle's Flame Lightning - Alter for Heart of Bayle", 
                                    lambda state: (state.has("Heart of Bayle", self.player) and state.can_reach("Grand Altar of Dragon Communion")))
            self._add_location_rule("GADC: Bayle's Tyranny - Alter for Heart of Bayle", 
                                    lambda state: (state.has("Heart of Bayle", self.player) and state.can_reach("Grand Altar of Dragon Communion")))

        for (remembrance, remembrance_name, items) in remembrances:
            self._add_location_rule([
                f"RH: {item} - Enia for {remembrance_name}" for item in items
            ], lambda state, r=remembrance: (state.has(r, self.player) and self._has_enough_great_runes(state, 1)
            ))
            
    def _add_location_rule(self, location: Union[str, List[str]], rule: Union[CollectionRule, str]) -> None:
        """Sets a rule for the given location if it that location is randomized.

        The rule can just be a single item/event name as well as an explicit rule lambda.
        """
        locations = location if isinstance(location, list) else [location]
        for location in locations:
            data = location_dictionary[location]
            if data.dlc and not self.options.enable_dlc: continue

            if not self._is_location_available(location): continue
            if isinstance(rule, str):
                assert item_table[rule].classification == ItemClassification.progression
                rule = lambda state, item=rule: state.has(item, self.player)
            add_rule(self.multiworld.get_location(location, self.player), rule)
    
    def _add_entrance_rule(self, region: str, rule: Union[CollectionRule, str]) -> None:
        """Sets a rule for the entrance to the given region."""
        assert region in location_tables
        if region not in self.created_regions: return
        if isinstance(rule, str):
            if " -> " not in rule:
                assert item_table[rule].classification == ItemClassification.progression
            rule = lambda state, item=rule: state.has(item, self.player)
        add_rule(self.multiworld.get_entrance("Go To " + region, self.player), rule)

    def _add_item_rule(self, location: str, rule: ItemRule) -> None:
        """Sets a rule for what items are allowed in a given location."""
        if not self._is_location_available(location): return
        add_item_rule(self.multiworld.get_location(location, self.player), rule)

    def _can_go_to(self, state, region) -> bool:
        """Returns whether state can access the given region name."""
        return state.can_reach_entrance(f"Go To {region}", self.player)

    def _can_get(self, state, location) -> bool:
        """Returns whether state can access the given location name."""
        return state.can_reach_location(location, self.player)
    
    def _is_location_available(
        self,
        location: Union[str, ERLocationData, ERLocation]
    ) -> bool:
        """Returns whether the given location is being randomized."""
        if isinstance(location, ERLocationData):
            data = location
        elif isinstance(location, ERLocation):
            data = location.data
        else:
            data = location_dictionary[location]

        return (
            not data.is_event
            and (not data.dlc or bool(self.options.enable_dlc))
            and not (
                self.options.excluded_location_behavior == "do_not_randomize"
                and data.name in self.all_excluded_locations
            )
            and not (
                self.options.missable_location_behavior == "do_not_randomize"
                and data.missable
            )
        )
    
    def write_spoiler(self, spoiler_handle: TextIO) -> None:
        text = ""

        if self.options.excluded_location_behavior == "randomize_unimportant":
            text += f"\n{self.player_name}'s world excluded: {sorted(self.all_excluded_locations)}\n"

        if text:
            text = "\n" + text + "\n"
            spoiler_handle.write(text)

    def _shuffle(self, seq: Sequence) -> List:
        """Returns a shuffled copy of a sequence."""
        copy = list(seq)
        self.random.shuffle(copy)
        return copy

    def _pop_item(
        self,
        location: Location,
        items: List[ERItem]
    ) -> ERItem:
        """Returns the next item in items that can be assigned to location."""
        for i, item in enumerate(items):
            if location.can_fill(self.multiworld.state, item, False):
                return items.pop(i)

        # If we can't find a suitable item, give up and assign an unsuitable one.
        return items.pop(0)

    def _get_our_locations(self) -> List[ERLocation]:
        return cast(List[ERLocation], self.multiworld.get_locations(self.player))
    
    def fill_slot_data(self) -> Dict[str, object]:
        slot_data: Dict[str, object] = {}

        # Once all clients support overlapping item IDs, adjust the ER AP item IDs to encode the
        # in-game ID as well as the count so that we don't need to send this information at all.
        #
        # We include all the items the game knows about so that users can manually request items
        # that aren't randomized, and then we _also_ include all the items that are placed in
        # practice.
        items_by_name = {
            location.item.name: cast(ERItem, location.item).data
            for location in self.multiworld.get_filled_locations()
            # item.code None is used for events, which we want to skip
            if location.item.code is not None and location.item.player == self.player
        }
        for item in item_table.values():
            if item.name not in items_by_name:
                items_by_name[item.name] = item

        ap_ids_to_er_ids: Dict[str, int] = {}
        item_counts: Dict[str, int] = {}
        for item in items_by_name.values():
            if item.ap_code is None: continue
            if item.er_code: ap_ids_to_er_ids[str(item.ap_code)] = item.er_code
            if item.count != 1: item_counts[str(item.ap_code)] = item.count

        # A map from Archipelago's location IDs to the keys the static randomizer uses to identify
        # locations.
        location_ids_to_keys: Dict[int, str] = {}
        for location in cast(List[ERLocation], self.multiworld.get_filled_locations(self.player)):
            # Skip events and only look at this world's locations
            if (location.address is not None and location.item.code is not None
                    and location.data.static):
                location_ids_to_keys[location.address] = location.data.static

        slot_data = {
            "options": {
                "ending_condition": self.options.ending_condition.value,
                "great_runes_required": self.options.great_runes_required.value,
                "enable_dlc": self.options.enable_dlc.value,
                "late_dlc": self.options.late_dlc.value,
                "death_link": self.options.death_link.value,
                "random_start": self.options.random_start.value,
                "auto_equip": self.options.auto_equip.value,
                "exclude_locations": self.options.exclude_locations.value,
                "excluded_location_behavior": self.options.excluded_location_behavior.value,
                "missable_location_behavior": self.options.missable_location_behavior.value,
            },
            "seed": self.multiworld.seed_name,  # to verify the server's multiworld
            "slot": self.multiworld.player_name[self.player],  # to connect to server
            "apIdsToItemIds": ap_ids_to_er_ids,
            "itemCounts": item_counts,
            "locationIdsToKeys": location_ids_to_keys,
        }

        return slot_data

    @staticmethod
    def interpret_slot_data(slot_data: Dict[str, Any]) -> Dict[str, Any]:
        return slot_data