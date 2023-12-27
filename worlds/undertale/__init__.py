from .Items import UndertaleItem, item_table, required_armor, required_weapons, non_key_items, key_items, \
    junk_weights_all, plot_items, junk_weights_neutral, junk_weights_pacifist, junk_weights_genocide
from .Locations import UndertaleAdvancement, advancement_table, exclusion_table
from .Regions import undertale_regions, link_undertale_areas
from .Rules import set_rules, set_completion_rules
from worlds.generic.Rules import exclusion_rules
from BaseClasses import Region, Entrance, Tutorial, Item
from .Options import undertale_options
from worlds.AutoWorld import World, WebWorld
from worlds.LauncherComponents import Component, components, Type
from multiprocessing import Process


def run_client():
    print('running undertale client')
    from .UndertaleClient import main  # lazy import
    p = Process(target=main)
    p.start()


components.append(Component("Undertale Client", "UndertaleClient"))
# components.append(Component("Undertale Client", func=run_client))


def data_path(file_name: str):
    import pkgutil
    return pkgutil.get_data(__name__, "data/" + file_name)


class UndertaleWeb(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Tutorial",
        "A guide to setting up the Archipelago Undertale software on your computer. This guide covers "
        "single-player, multiworld, and related software.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Mewlif"]
    )]


class UndertaleWorld(World):
    """
    Undertale is an RPG where every choice you make matters. You could choose to hurt all the enemies, eventually
    causing genocide of the monster species. Or you can spare all the enemies, befriending them and freeing them
    from their underground prison.
    """
    game = "Undertale"
    option_definitions = undertale_options
    web = UndertaleWeb()

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = {name: data.id for name, data in advancement_table.items()}

    data_version = 7

    def _get_undertale_data(self):
        return {
            "world_seed": self.multiworld.per_slot_randoms[self.player].getrandbits(32),
            "seed_name": self.multiworld.seed_name,
            "player_name": self.multiworld.get_player_name(self.player),
            "player_id": self.player,
            "client_version": self.required_client_version,
            "race": self.multiworld.is_race,
            "route": self.multiworld.route_required[self.player].current_key,
            "starting_area": self.multiworld.starting_area[self.player].current_key,
            "temy_armor_include": bool(self.multiworld.temy_include[self.player].value),
            "only_flakes": bool(self.multiworld.only_flakes[self.player].value),
            "no_equips": bool(self.multiworld.no_equips[self.player].value),
            "key_hunt": bool(self.multiworld.key_hunt[self.player].value),
            "key_pieces": self.multiworld.key_pieces[self.player].value,
            "rando_love": bool(self.multiworld.rando_love[self.player].value),
            "rando_stats": bool(self.multiworld.rando_stats[self.player].value),
            "prog_armor": bool(self.multiworld.prog_armor[self.player].value),
            "prog_weapons": bool(self.multiworld.prog_weapons[self.player].value),
            "rando_item_button": bool(self.multiworld.rando_item_button[self.player].value)
        }

    def create_items(self):
        self.multiworld.get_location("Undyne Date", self.player).place_locked_item(self.create_item("Undyne Date"))
        self.multiworld.get_location("Alphys Date", self.player).place_locked_item(self.create_item("Alphys Date"))
        self.multiworld.get_location("Papyrus Date", self.player).place_locked_item(self.create_item("Papyrus Date"))
        # Generate item pool
        itempool = []
        if self.multiworld.route_required[self.player] == "all_routes":
            junk_pool = junk_weights_all.copy()
        elif self.multiworld.route_required[self.player] == "genocide":
            junk_pool = junk_weights_genocide.copy()
        elif self.multiworld.route_required[self.player] == "neutral":
            junk_pool = junk_weights_neutral.copy()
        elif self.multiworld.route_required[self.player] == "pacifist":
            junk_pool = junk_weights_pacifist.copy()
        else:
            junk_pool = junk_weights_all.copy()
        # Add all required progression items
        for name, num in key_items.items():
            itempool += [name] * num
        for name, num in required_armor.items():
            itempool += [name] * num
        for name, num in required_weapons.items():
            itempool += [name] * num
        for name, num in non_key_items.items():
            itempool += [name] * num
        if self.multiworld.rando_item_button[self.player]:
            itempool += ["ITEM"]
        else:
            self.multiworld.push_precollected(self.create_item("ITEM"))
        self.multiworld.push_precollected(self.create_item("FIGHT"))
        self.multiworld.push_precollected(self.create_item("ACT"))
        self.multiworld.push_precollected(self.create_item("MERCY"))
        if self.multiworld.route_required[self.player] == "genocide":
            itempool = [item for item in itempool if item != "Popato Chisps" and item != "Stained Apron" and
                        item != "Nice Cream" and item != "Hot Cat" and item != "Hot Dog...?" and item != "Punch Card"]
        elif self.multiworld.route_required[self.player] == "neutral":
            itempool = [item for item in itempool if item != "Popato Chisps" and item != "Hot Cat" and
                        item != "Hot Dog...?"]
        if self.multiworld.route_required[self.player] == "pacifist" or \
                self.multiworld.route_required[self.player] == "all_routes":
            itempool += ["Undyne Letter EX"]
        else:
            itempool.remove("Complete Skeleton")
            itempool.remove("Fish")
            itempool.remove("DT Extractor")
            itempool.remove("Hush Puppy")
        if self.multiworld.key_hunt[self.player]:
            itempool += ["Key Piece"] * self.multiworld.key_pieces[self.player].value
        else:
            itempool += ["Left Home Key"]
            itempool += ["Right Home Key"]
        if not self.multiworld.rando_love[self.player] or \
                (self.multiworld.route_required[self.player] != "genocide" and
                 self.multiworld.route_required[self.player] != "all_routes"):
            itempool = [item for item in itempool if not item == "LOVE"]
        if not self.multiworld.rando_stats[self.player] or \
                (self.multiworld.route_required[self.player] != "genocide" and
                 self.multiworld.route_required[self.player] != "all_routes"):
            itempool = [item for item in itempool if not (item == "ATK Up" or item == "DEF Up" or item == "HP Up")]
        if self.multiworld.temy_include[self.player]:
            itempool += ["temy armor"]
        if self.multiworld.no_equips[self.player]:
            itempool = [item for item in itempool if item not in required_armor and item not in required_weapons]
        else:
            if self.multiworld.prog_armor[self.player]:
                itempool = [item if (item not in required_armor and not item == "temy armor") else
                            "Progressive Armor" for item in itempool]
            if self.multiworld.prog_weapons[self.player]:
                itempool = [item if item not in required_weapons else "Progressive Weapons" for item in itempool]
        if self.multiworld.route_required[self.player] == "genocide" or \
                self.multiworld.route_required[self.player] == "all_routes":
            if not self.multiworld.only_flakes[self.player]:
                itempool += ["Snowman Piece"] * 2
            if not self.multiworld.no_equips[self.player]:
                itempool = ["Real Knife" if item == "Worn Dagger" else "The Locket"
                            if item == "Heart Locket" else item for item in itempool]
        if self.multiworld.only_flakes[self.player]:
            itempool = [item for item in itempool if item not in non_key_items]

        starting_key = self.multiworld.starting_area[self.player].current_key.title() + " Key"
        itempool.remove(starting_key)
        self.multiworld.push_precollected(self.create_item(starting_key))
        # Choose locations to automatically exclude based on settings
        exclusion_pool = set()
        exclusion_pool.update(exclusion_table[self.multiworld.route_required[self.player].current_key])
        if not self.multiworld.rando_love[self.player] or \
                (self.multiworld.route_required[self.player] != "genocide" and
                 self.multiworld.route_required[self.player] != "all_routes"):
            exclusion_pool.update(exclusion_table["NoLove"])
        if not self.multiworld.rando_stats[self.player] or \
                (self.multiworld.route_required[self.player] != "genocide" and
                 self.multiworld.route_required[self.player] != "all_routes"):
            exclusion_pool.update(exclusion_table["NoStats"])

        # Choose locations to automatically exclude based on settings
        exclusion_checks = set()
        exclusion_checks.update(["Nicecream Punch Card", "Hush Trade"])
        exclusion_rules(self.multiworld, self.player, exclusion_checks)

        # Fill remaining items with randomly generated junk or Temmie Flakes
        if not self.multiworld.only_flakes[self.player]:
            itempool += self.multiworld.random.choices(list(junk_pool.keys()), weights=list(junk_pool.values()),
                                                       k=len(self.location_names)-len(itempool)-len(exclusion_pool))
        else:
            itempool += ["Temmie Flakes"] * (len(self.location_names) - len(itempool) - len(exclusion_pool))
        # Convert itempool into real items
        itempool = [item for item in map(lambda name: self.create_item(name), itempool)]

        self.multiworld.itempool += itempool

    def set_rules(self):
        set_rules(self.multiworld, self.player)
        set_completion_rules(self.multiworld, self.player)

    def create_regions(self):
        def UndertaleRegion(region_name: str, exits=[]):
            ret = Region(region_name, self.player, self.multiworld)
            ret.locations += [UndertaleAdvancement(self.player, loc_name, loc_data.id, ret)
                             for loc_name, loc_data in advancement_table.items()
                             if loc_data.region == region_name and
                             (loc_name not in exclusion_table["NoStats"] or
                              (self.multiworld.rando_stats[self.player] and
                               (self.multiworld.route_required[self.player] == "genocide" or
                                self.multiworld.route_required[self.player] == "all_routes"))) and
                             (loc_name not in exclusion_table["NoLove"] or
                              (self.multiworld.rando_love[self.player] and
                               (self.multiworld.route_required[self.player] == "genocide" or
                                self.multiworld.route_required[self.player] == "all_routes"))) and
                             loc_name not in exclusion_table[self.multiworld.route_required[self.player].current_key]]
            for exit in exits:
                ret.exits.append(Entrance(self.player, exit, ret))
            return ret

        self.multiworld.regions += [UndertaleRegion(*r) for r in undertale_regions]
        link_undertale_areas(self.multiworld, self.player)

    def fill_slot_data(self):
        slot_data = self._get_undertale_data()
        for option_name in undertale_options:
            option = getattr(self.multiworld, option_name)[self.player]
            if (option_name == "rando_love" or option_name == "rando_stats") and \
                    self.multiworld.route_required[self.player] != "genocide" and \
                    self.multiworld.route_required[self.player] != "all_routes":
                option.value = False
            if slot_data.get(option_name, None) is None and type(option.value) in {str, int}:
                slot_data[option_name] = int(option.value)
        return slot_data

    def create_item(self, name: str) -> Item:
        item_data = item_table[name]
        item = UndertaleItem(name, item_data.classification, item_data.code, self.player)
        return item
