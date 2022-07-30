import os
import json
from base64 import b64encode, b64decode
from math import ceil
from .Items import UndertaleItem, item_table, required_armor, required_weapons, non_key_items, key_items, junk_weights_all, plot_items, junk_weights_neutral, junk_weights_pacifist, junk_weights_genocide
from .Locations import UndertaleAdvancement, advancement_table, exclusion_table
from .Regions import undertale_regions, link_undertale_areas
from .Rules import set_rules, set_completion_rules
from worlds.generic.Rules import exclusion_rules

from BaseClasses import Region, Entrance, Item, ItemClassification
from .Options import undertale_options
from ..AutoWorld import World

client_version = 7


def data_path(*args):
    return os.path.join(os.path.dirname(__file__), 'data', *args)


class UndertaleWorld(World):
    """
    Undertale is an RPG where every choice you make matters. You could choose to hurt all the enemies, eventually
    causing genocide of the monster species. Or you can spare all the enemies, befriending them and freeing them
    from their underground prison.
    """
    game: str = "Undertale"
    options = undertale_options
    topology_present = True

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = {name: data.id for name, data in advancement_table.items()}

    data_version = 4

    def _get_undertale_data(self):
        return {
            'world_seed': self.world.slot_seeds[self.player].getrandbits(32),
            'seed_name': self.world.seed_name,
            'player_name': self.world.get_player_name(self.player),
            'player_id': self.player,
            'client_version': client_version,
            'race': self.world.is_race,
            'route': self.world.route_required[self.player].current_key,
            'temy_armor_include': bool(self.world.temy_include[self.player].value),
            'only_flakes': bool(self.world.only_flakes[self.player].value),
            'no_equips': bool(self.world.no_equips[self.player].value),
            'key_hunt': bool(self.world.key_hunt[self.player].value),
            'key_pieces': self.world.key_pieces[self.player].value,
            'prog_plot': bool(self.world.prog_plot[self.player].value),
            'rando_love': bool(self.world.rando_love[self.player].value),
            'rando_area': bool(self.world.rando_area[self.player].value),
            'rando_stats': bool(self.world.rando_stats[self.player].value),
            'prog_armor': bool(self.world.prog_armor[self.player].value),
            'prog_weapons': bool(self.world.prog_weapons[self.player].value)
        }

    def generate_basic(self):
        self.world.get_location("Undyne Date", self.player).place_locked_item(self.create_item("Undyne Date"))
        self.world.get_location("Alphys Date", self.player).place_locked_item(self.create_item("Alphys Date"))
        self.world.get_location("Papyrus Date", self.player).place_locked_item(self.create_item("Papyrus Date"))
        # Generate item pool
        itempool = []
        if self.world.route_required[self.player].current_key == "all_routes":
            junk_pool = junk_weights_all.copy()
        elif self.world.route_required[self.player].current_key == "genocide":
            junk_pool = junk_weights_genocide.copy()
        elif self.world.route_required[self.player].current_key == "neutral":
            junk_pool = junk_weights_neutral.copy()
        elif self.world.route_required[self.player].current_key == "pacifist":
            junk_pool = junk_weights_pacifist.copy()
        else:
            junk_pool = junk_weights_all.copy()
        # Add all required progression items
        for (name, num) in key_items.items():
            itempool += [name] * num
        if not self.world.only_flakes[self.player]:
            for (name, num) in non_key_items.items():
                itempool += [name] * num
        if not self.world.no_equips[self.player]:
            for (name, num) in required_armor.items():
                itempool += [name] * num
            for (name, num) in required_weapons.items():
                itempool += [name] * num
        if not self.world.temy_include[self.player]:
            if "temy armor" in itempool:
                itempool.remove("temy armor")
        if self.world.prog_armor[self.player]:
            itempool = [item if item not in required_armor else "Progressive Armor" for item in itempool]
        if self.world.prog_weapons[self.player]:
            itempool = [item if item not in required_weapons else "Progressive Weapons" for item in itempool]
        if self.world.route_required[self.player].current_key == "genocide" or self.world.route_required[self.player].current_key == "all_routes":
            if not self.world.only_flakes[self.player]:
                itempool += ["Snowman Piece"] * 2
            if not self.world.no_equips[self.player]:
                itempool = ["Real Knife" if item == "Worn Dagger" else "The Locket" if item == "Heart Locket" else item for item in itempool]
        if self.world.route_required[self.player].current_key == "pacifist" or self.world.route_required[self.player].current_key == "all_routes":
            itempool += ["Undyne Letter EX"]
            itempool += ["Hush Puppy"]
        else:
            itempool.remove("Complete Skeleton")
            itempool.remove("Fish")
            itempool.remove("DT Extractor")
        if self.world.route_required[self.player].current_key == "genocide":
            itempool.remove("Cooking Set")
            itempool.remove("Microphone")
        if self.world.key_hunt[self.player]:
            itempool += ["Key Piece"] * self.world.key_pieces[self.player].value
        else:
            itempool += ["Left Home Key"]
            itempool += ["Right Home Key"]
        if not self.world.rando_love[self.player] or (self.world.route_required[self.player].current_key != "genocide" and self.world.route_required[self.player].current_key != "all_routes"):
            itempool = [item for item in itempool if not item == "LOVE"]
        if not self.world.rando_stats[self.player] or (self.world.route_required[self.player].current_key != "genocide" and self.world.route_required[self.player].current_key != "all_routes"):
            itempool = [item for item in itempool if not (item == "ATK Up" or item == "DEF Up" or item == "HP Up")]
        if self.world.prog_plot[self.player]:
            itempool = [item if item not in plot_items else "Progressive Plot" for item in itempool]
        if self.world.route_required[self.player].current_key == "genocide":
            itempool = [item for item in itempool if item != "Popato Chisps" and item != "Stained Apron" and item != "Nice Cream" and item != "Hot Cat" and item != "Hot Dog...?" and item != "Punch Card"]
        elif self.world.route_required[self.player].current_key == "neutral":
            itempool = [item for item in itempool if item != "Popato Chisps" and item != "Hot Cat" and item != "Hot Dog...?"]
        # Choose locations to automatically exclude based on settings
        exclusion_pool = set()
        exclusion_pool.update(exclusion_table[self.world.route_required[self.player].current_key])
        if not self.world.rando_love[self.player] or (self.world.route_required[self.player].current_key != "genocide" and self.world.route_required[self.player].current_key != "all_routes"):
            exclusion_pool.update(exclusion_table["NoLove"])
        if not self.world.rando_stats[self.player] or (self.world.route_required[self.player].current_key != "genocide" and self.world.route_required[self.player].current_key != "all_routes"):
            exclusion_pool.update(exclusion_table["NoStats"])

        # Choose locations to automatically exclude based on settings
        exclusion_checks = set()
        exclusion_checks.update(["Nicecream Punch Card", "Hush Trade"])
        exclusion_rules(self.world, self.player, exclusion_checks)

        # Fill remaining items with randomly generated junk or Temmie Flakes
        if not self.world.only_flakes[self.player]:
            itempool += self.world.random.choices(list(junk_pool.keys()), weights=list(junk_pool.values()), k=len(self.location_names)-len(itempool)-len(exclusion_pool))
        else:
            itempool += ["Temmie Flakes"] * (len(self.location_names) - len(itempool) - len(exclusion_pool))
        # Convert itempool into real items
        itempool = [item for item in map(lambda name: self.create_item(name), itempool)]

        self.world.random.shuffle(itempool)

        self.world.itempool += itempool

    def set_rules(self):
        set_rules(self.world, self.player)
        set_completion_rules(self.world, self.player)

    def create_regions(self):
        def UndertaleRegion(region_name: str, exits=[]):
            ret = Region(region_name, None, region_name, self.player, self.world)
            ret.locations = [UndertaleAdvancement(self.player, loc_name, loc_data.id, ret)
                for loc_name, loc_data in advancement_table.items()
                if loc_data.region == region_name and (loc_name not in exclusion_table["NoStats"] or (self.world.rando_stats[self.player] and (self.world.route_required[self.player].current_key == "genocide" or self.world.route_required[self.player].current_key == "all_routes"))) and (loc_name not in exclusion_table["NoLove"] or (self.world.rando_love[self.player] and (self.world.route_required[self.player].current_key == "genocide" or self.world.route_required[self.player].current_key == "all_routes"))) and not loc_name in exclusion_table[self.world.route_required[self.player].current_key]]
            for exit in exits:
                ret.exits.append(Entrance(self.player, exit, ret))
            return ret

        self.world.regions += [UndertaleRegion(*r) for r in undertale_regions]
        link_undertale_areas(self.world, self.player)

    def fill_slot_data(self):
        slot_data = self._get_undertale_data()
        for option_name in undertale_options:
            option = getattr(self.world, option_name)[self.player]
            if (option_name == "rando_love" or option_name == "rando_stats") and self.world.route_required[self.player].current_key != "genocide" and self.world.route_required[self.player].current_key != "all_routes":
                option.value = False
            if slot_data.get(option_name, None) is None and type(option.value) in {str, int}:
                slot_data[option_name] = int(option.value)
        for (exit, region) in Regions.randomized_connections:
            slot_data[exit] = self.world.get_entrance(exit, self.player).connected_region.name
            slot_data[region] = self.world.get_region(region, self.player).entrances[0].name
        return slot_data

    def create_item(self, name: str) -> Item:
        item_data = item_table[name]
        item = UndertaleItem(name,
                                ItemClassification.progression if item_data.progression else ItemClassification.filler,
                                item_data.code, self.player)
        return item
