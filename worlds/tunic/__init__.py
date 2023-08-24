from typing import Dict

from BaseClasses import Region, Location, Item, Tutorial, ItemClassification
from .Items import filler_items, item_table, item_name_groups
from .Locations import location_table, location_name_groups
from .Rules import set_location_rules, set_region_rules, hexagon_quest_abilities, set_abilities
from .Regions import tunic_regions
from .Options import tunic_options
from ..AutoWorld import WebWorld, World


class TunicWeb(WebWorld):
    tutorials = [
        Tutorial(
            tutorial_name="Multiworld Setup Guide",
            description="A guide to setting up the TUNIC Randomizer for Archipelago multiworld games.",
            language="English",
            file_name="setup_en.md",
            link="guide/en",
            authors=["SilentDestroyer"]
        )
    ]
    theme = "grassFlowers"
    game = "Tunic"


class TunicItem(Item):
    game: str = "Tunic"


class TunicLocation(Location):
    game: str = "Tunic"


class TunicWorld(World):
    """
    Explore a land filled with lost legends, ancient powers, and ferocious monsters in TUNIC, an isometric action game
    about a small fox on a big adventure. Stranded on a mysterious beach, armed with only your own curiosity, you will
    confront colossal beasts, collect strange and powerful items, and unravel long-lost secrets. Be brave, tiny fox!
    """
    game = "Tunic"
    web = TunicWeb()

    data_version = 1
    tunic_items = item_table
    tunic_locations = location_table
    option_definitions = tunic_options
    item_name_groups = item_name_groups
    location_name_groups = location_name_groups

    item_name_to_id = {}
    location_name_to_id = {}
    item_base_id = 509342400
    location_base_id = 509342400

    for item_name, item_data in item_table.items():
        item_name_to_id[item_name] = item_base_id
        item_base_id += 1

    for location_name, location_data in location_table.items():
        location_name_to_id[location_name] = location_base_id
        location_base_id += 1

    def create_item(self, name: str) -> TunicItem:
        item_data = item_table[name]
        return TunicItem(name, item_data.classification, self.item_name_to_id[name], self.player)

    def create_items(self):
        hexagon_locations: Dict[str, str] = {
            "Red Hexagon": "Fortress Arena - Siege Engine/Vault Key Pickup",
            "Green Hexagon": "Librarian - Hexagon Green",
            "Blue Hexagon": "Rooted Ziggurat Lower - Hexagon Blue"
        }

        items = []
        for item_name in item_table:
            item_data = item_table[item_name]

            if item_name == "Gold Hexagon":
                # if hexagon quest is on, add the gold hexagons in
                if self.multiworld.hexagon_quest[self.player].value:
                    # if keys are behind bosses, place 3 manually
                    gold_hexes = item_data.quantity_in_item_pool
                    if self.multiworld.keys_behind_bosses[self.player].value:
                        for location in hexagon_locations.values():
                            self.multiworld.get_location(location, self.player)\
                                .place_locked_item(self.create_item("Gold Hexagon"))
                        gold_hexes -= 3

                    for i in range(0, gold_hexes):
                        items.append(self.create_item(item_name))
                    # adding a money x1 to even out the pool with this option
                    items.append(self.create_item("Money x1"))
                else:
                    # if not doing hexagon quest, just skip the gold hexagons
                    continue
            elif self.multiworld.hexagon_quest[self.player].value and \
                    ("Pages" in item_name or item_name in hexagon_locations.keys()):
                continue
            elif self.multiworld.keys_behind_bosses[self.player].value and item_name in hexagon_locations.keys():
                self.multiworld.get_location(hexagon_locations[item_name], self.player)\
                    .place_locked_item(self.create_item(item_name))
            elif (item_name == "Sword Upgrade" and not self.multiworld.sword_progression[self.player].value)\
                    or (item_name in ["Stick", "Sword"] and self.multiworld.sword_progression[self.player].value):
                continue
            else:
                for i in range(0, item_data.quantity_in_item_pool):
                    items.append(self.create_item(item_name))

        self.multiworld.random.shuffle(items)
        self.multiworld.itempool += items

    def create_regions(self):
        for region_name in tunic_regions.keys():
            region = Region(region_name, self.player, self.multiworld)
            self.multiworld.regions.append(region)

        for region_name in tunic_regions.keys():
            region = self.multiworld.get_region(region_name, self.player)
            region.add_exits(tunic_regions[region_name])

        for location_name in self.location_name_to_id:
            region = self.multiworld.get_region(location_table[location_name].region, self.player)
            location = TunicLocation(self.player, location_name, self.location_name_to_id[location_name], region)
            region.locations.append(location)

        victory_region = self.multiworld.get_region("Spirit Arena", self.player)
        victory_location = TunicLocation(self.player, "The Heir", None, victory_region)
        victory_location.place_locked_item(TunicItem("Victory", ItemClassification.progression, None, self.player))
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)
        victory_region.locations.append(victory_location)

    def set_rules(self) -> None:
        set_abilities(self.multiworld, self.player)
        set_region_rules(self.multiworld, self.player)
        set_location_rules(self.multiworld, self.player)

    def get_filler_item_name(self) -> str:
        return self.multiworld.random.choice(filler_items)

    def fill_slot_data(self) -> Dict[str, any]:
        # Find items for generating hints in-game
        stundagger = self.multiworld.find_item("Magic Dagger", self.player).item
        techbow = self.multiworld.find_item("Magic Wand", self.player).item
        grapple = self.multiworld.find_item("Magic Orb", self.player).item
        hyperdash = self.multiworld.find_item("Hero's Laurels", self.player).item
        lantern = self.multiworld.find_item("Lantern", self.player).item
        shotgun = self.multiworld.find_item("Shotgun", self.player).item
        scavenger_mask = self.multiworld.find_item("Scavenger Mask", self.player).item
        shield = self.multiworld.find_item("Shield", self.player).item
        dath_stone = self.multiworld.find_item("Dath Stone", self.player).item
        hourglass = self.multiworld.find_item("Hourglass", self.player).item
        house_key = self.multiworld.find_item("Old House Key", self.player).item
        vault_key = self.multiworld.find_item("Fortress Vault Key", self.player).item
        att_relic = self.multiworld.find_item("Hero Relic - ATT", self.player).item
        def_relic = self.multiworld.find_item("Hero Relic - DEF", self.player).item
        potion_relic = self.multiworld.find_item("Hero Relic - POTION", self.player).item
        hp_relic = self.multiworld.find_item("Hero Relic - HP", self.player).item
        sp_relic = self.multiworld.find_item("Hero Relic - MP", self.player).item
        mp_relic = self.multiworld.find_item("Hero Relic - SP", self.player).item

        slot_data: Dict[str, any] = {
            "seed": self.multiworld.per_slot_randoms[self.player].randint(0, 2147483647),
            "start_with_sword": self.multiworld.start_with_sword[self.player].value,
            "keys_behind_bosses": self.multiworld.keys_behind_bosses[self.player].value,
            "sword_progression": self.multiworld.sword_progression[self.player].value,
            "ability_shuffling": self.multiworld.ability_shuffling[self.player].value,
            "hexagon_quest": self.multiworld.hexagon_quest[self.player].value,
            "Magic Dagger": [stundagger.location.name, stundagger.location.player],
            "Magic Wand": [techbow.location.name, techbow.location.player],
            "Magic Orb": [grapple.location.name, grapple.location.player],
            "Hero's Laurels": [hyperdash.location.name, hyperdash.location.player],
            "Lantern": [lantern.location.name, lantern.location.player],
            "Shotgun": [shotgun.location.name, shotgun.location.player],
            "Scavenger Mask": [scavenger_mask.location.name, scavenger_mask.location.player],
            "Shield": [shield.location.name, shield.location.player],
            "Dath Stone": [dath_stone.location.name, dath_stone.location.player],
            "Hourglass": [hourglass.location.name, hourglass.location.player],
            "Old House Key": [house_key.location.name, house_key.location.player],
            "Fortress Vault Key": [vault_key.location.name, vault_key.location.player],
            "Hero Relic - ATT": [att_relic.location.name, att_relic.location.player],
            "Hero Relic - DEF": [def_relic.location.name, def_relic.location.player],
            "Hero Relic - POTION": [potion_relic.location.name, potion_relic.location.player],
            "Hero Relic - HP": [hp_relic.location.name, hp_relic.location.player],
            "Hero Relic - MP": [sp_relic.location.name, sp_relic.location.player],
            "Hero Relic - SP": [mp_relic.location.name, mp_relic.location.player],
        }

        if self.multiworld.sword_progression[self.player].value:
            swords = self.multiworld.find_item_locations("Sword Upgrade", self.player, False)
            slot_data["Sword Upgrade"] = [swords[0].item.location.name, swords[0].item.location.player,
                                          swords[1].item.location.name, swords[1].item.location.player,
                                          swords[2].item.location.name, swords[2].item.location.player,
                                          swords[3].item.location.name, swords[3].item.location.player]
        else:
            stick = self.multiworld.find_item("Stick", self.player).item
            swords = self.multiworld.find_item_locations("Sword", self.player, False)
            slot_data["Stick"] = [stick.location.name, stick.location.player],
            slot_data["Sword"] = [swords[0].item.location.name, swords[0].item.location.player,
                                  swords[1].item.location.name, swords[1].item.location.player,
                                  swords[2].item.location.name, swords[2].item.location.player],

        if not self.multiworld.hexagon_quest[self.player].value:
            hexagon_red = self.multiworld.find_item("Red Hexagon", self.player).item
            hexagon_green = self.multiworld.find_item("Green Hexagon", self.player).item
            hexagon_blue = self.multiworld.find_item("Blue Hexagon", self.player).item
            prayer_page = self.multiworld.find_item("Pages 24-25 (Prayer)", self.player).item
            holy_cross_page = self.multiworld.find_item("Pages 42-43 (Holy Cross)", self.player).item
            ice_rod_page = self.multiworld.find_item("Pages 52-53 (Ice Rod)", self.player).item
            slot_data["Red Hexagon"] = [hexagon_red.location.name, hexagon_red.location.player]
            slot_data["Green Hexagon"] = [hexagon_green.location.name, hexagon_green.location.player]
            slot_data["Blue Hexagon"] = [hexagon_blue.location.name, hexagon_blue.location.player]
            slot_data["Pages 24-25 (Prayer)"] = [prayer_page.location.name, prayer_page.location.player]
            slot_data["Pages 42-43 (Holy Cross)"] = [holy_cross_page.location.name, holy_cross_page.location.player]
            slot_data["Pages 52-53 (Ice Rod)"] = [ice_rod_page.location.name, ice_rod_page.location.player]
        else:
            golden_hexagons = self.multiworld.find_item_locations("Gold Hexagon", self.player, False)
            self.multiworld.per_slot_randoms[self.player].shuffle(golden_hexagons)
            hexagon_gold = golden_hexagons.pop()
            hexagon_gold2 = golden_hexagons.pop()
            hexagon_gold3 = golden_hexagons.pop()
            slot_data["Gold Hexagon"] = [hexagon_gold.name, hexagon_gold.player, hexagon_gold2.name,
                                         hexagon_gold2.player, hexagon_gold3.name, hexagon_gold3.player]
            slot_data["Hexagon Quest Prayer"] = hexagon_quest_abilities["prayer"]
            slot_data['Hexagon Quest Holy Cross'] = hexagon_quest_abilities["holy_cross"]
            slot_data['Hexagon Quest Ice Rod'] = hexagon_quest_abilities["ice_rod"]
        return slot_data
