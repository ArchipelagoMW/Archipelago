from .Items import UndertaleItem, item_table, required_armor, required_weapons, non_key_items, key_items, \
    junk_weights_all, plot_items, junk_weights_neutral, junk_weights_pacifist, junk_weights_genocide
from .Locations import UndertaleAdvancement, advancement_table, exclusion_table
from .Regions import undertale_regions, link_undertale_areas
from .Rules import set_rules, set_completion_rules
from worlds.generic.Rules import exclusion_rules
from BaseClasses import Region, Entrance, Tutorial, Item
from .Options import UndertaleOptions
from worlds.AutoWorld import World, WebWorld
from worlds.LauncherComponents import Component, components
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
        "Multiworld Setup Guide",
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
    options_dataclass = UndertaleOptions
    options: UndertaleOptions
    web = UndertaleWeb()

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = {name: data.id for name, data in advancement_table.items()}

    def _get_undertale_data(self):
        return {
            "world_seed": self.random.getrandbits(32),
            "seed_name": self.multiworld.seed_name,
            "player_name": self.multiworld.get_player_name(self.player),
            "player_id": self.player,
            "client_version": self.required_client_version,
            "race": self.multiworld.is_race,
            "route": self.options.route_required.current_key,
            "starting_area": self.options.starting_area.current_key,
            "temy_armor_include": bool(self.options.temy_include.value),
            "only_flakes": bool(self.options.only_flakes.value),
            "no_equips": bool(self.options.no_equips.value),
            "key_hunt": bool(self.options.key_hunt.value),
            "key_pieces": int(self.options.key_pieces.value),
            "rando_love": bool(self.options.rando_love and (self.options.route_required == "genocide" or self.options.route_required == "all_routes")),
            "rando_stats": bool(self.options.rando_stats and (self.options.route_required == "genocide" or self.options.route_required == "all_routes")),
            "prog_armor": bool(self.options.prog_armor.value),
            "prog_weapons": bool(self.options.prog_weapons.value),
            "rando_item_button": bool(self.options.rando_item_button.value),
            "route_required": int(self.options.route_required.value),
            "temy_include": int(self.options.temy_include.value)

        }

    def get_filler_item_name(self):
        if self.options.route_required == "all_routes":
            junk_pool = junk_weights_all
        elif self.options.route_required == "genocide":
            junk_pool = junk_weights_genocide
        elif self.options.route_required == "neutral":
            junk_pool = junk_weights_neutral
        elif self.options.route_required == "pacifist":
            junk_pool = junk_weights_pacifist
        else:
            junk_pool = junk_weights_all
        if not self.options.only_flakes:
            return self.random.choices(list(junk_pool.keys()), weights=list(junk_pool.values()))[0]
        else:
            return "Temmie Flakes"

    def create_items(self):
        self.multiworld.get_location("Undyne Date", self.player).place_locked_item(self.create_item("Undyne Date"))
        self.multiworld.get_location("Alphys Date", self.player).place_locked_item(self.create_item("Alphys Date"))
        self.multiworld.get_location("Papyrus Date", self.player).place_locked_item(self.create_item("Papyrus Date"))
        # Generate item pool
        itempool = []
        if self.options.route_required == "all_routes":
            junk_pool = junk_weights_all.copy()
        elif self.options.route_required == "genocide":
            junk_pool = junk_weights_genocide.copy()
        elif self.options.route_required == "neutral":
            junk_pool = junk_weights_neutral.copy()
        elif self.options.route_required == "pacifist":
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
        if self.options.rando_item_button:
            itempool += ["ITEM"]
        else:
            self.multiworld.push_precollected(self.create_item("ITEM"))
        self.multiworld.push_precollected(self.create_item("FIGHT"))
        self.multiworld.push_precollected(self.create_item("ACT"))
        self.multiworld.push_precollected(self.create_item("MERCY"))
        if self.options.route_required == "genocide":
            itempool = [item for item in itempool if item != "Popato Chisps" and item != "Stained Apron" and
                        item != "Nice Cream" and item != "Hot Cat" and item != "Hot Dog...?" and item != "Punch Card"]
        elif self.options.route_required == "neutral":
            itempool = [item for item in itempool if item != "Popato Chisps" and item != "Hot Cat" and
                        item != "Hot Dog...?"]
        if self.options.route_required == "pacifist" or self.options.route_required == "all_routes":
            itempool += ["Undyne Letter EX"]
        else:
            itempool.remove("Complete Skeleton")
            itempool.remove("Fish")
            itempool.remove("DT Extractor")
            itempool.remove("Hush Puppy")
        if self.options.key_hunt:
            itempool += ["Key Piece"] * self.options.key_pieces.value
        else:
            itempool += ["Left Home Key"]
            itempool += ["Right Home Key"]
        if not self.options.rando_love or \
                (self.options.route_required != "genocide" and self.options.route_required != "all_routes"):
            itempool = [item for item in itempool if not item == "LOVE"]
        if not self.options.rando_stats or \
                (self.options.route_required != "genocide" and self.options.route_required != "all_routes"):
            itempool = [item for item in itempool if not (item == "ATK Up" or item == "DEF Up" or item == "HP Up")]
        if self.options.temy_include:
            itempool += ["temy armor"]
        if self.options.no_equips:
            itempool = [item for item in itempool if item not in required_armor and item not in required_weapons]
        else:
            if self.options.prog_armor:
                itempool = [item if (item not in required_armor and not item == "temy armor") else
                            "Progressive Armor" for item in itempool]
            if self.options.prog_weapons:
                itempool = [item if item not in required_weapons else "Progressive Weapons" for item in itempool]
        if self.options.route_required == "genocide" or \
                self.options.route_required == "all_routes":
            if not self.options.only_flakes:
                itempool += ["Snowman Piece"] * 2
            if not self.options.no_equips:
                itempool = ["Real Knife" if item == "Worn Dagger" else "The Locket"
                            if item == "Heart Locket" else item for item in itempool]
        if self.options.only_flakes:
            itempool = [item for item in itempool if item not in non_key_items]

        starting_key = self.options.starting_area.current_key.title() + " Key"
        itempool.remove(starting_key)
        self.multiworld.push_precollected(self.create_item(starting_key))
        # Choose locations to automatically exclude based on settings
        exclusion_pool = set()
        exclusion_pool.update(exclusion_table[self.options.route_required.current_key])
        if not self.options.rando_love or \
                (self.options.route_required != "genocide" and self.options.route_required != "all_routes"):
            exclusion_pool.update(exclusion_table["NoLove"])
        if not self.options.rando_stats or \
                (self.options.route_required != "genocide" and self.options.route_required != "all_routes"):
            exclusion_pool.update(exclusion_table["NoStats"])

        # Choose locations to automatically exclude based on settings
        exclusion_checks = set()
        exclusion_checks.update(["Nicecream Punch Card", "Hush Trade"])
        exclusion_rules(self.multiworld, self.player, exclusion_checks)

        # Convert itempool into real items
        itempool = [item for item in map(lambda name: self.create_item(name), itempool)]
        # Fill remaining items with randomly generated junk or Temmie Flakes
        while len(itempool) < len(self.multiworld.get_unfilled_locations(self.player)):
            itempool.append(self.create_filler())

        self.multiworld.itempool += itempool

    def set_rules(self):
        set_rules(self)
        set_completion_rules(self)

    def create_regions(self):
        def UndertaleRegion(region_name: str, exits=[]):
            ret = Region(region_name, self.player, self.multiworld)
            ret.locations += [UndertaleAdvancement(self.player, loc_name, loc_data.id, ret)
                              for loc_name, loc_data in advancement_table.items()
                              if loc_data.region == region_name and
                              (loc_name not in exclusion_table["NoStats"] or
                              (self.options.rando_stats and
                               (self.options.route_required == "genocide" or
                                self.options.route_required == "all_routes"))) and
                              (loc_name not in exclusion_table["NoLove"] or
                              (self.options.rando_love and
                               (self.options.route_required == "genocide" or
                                self.options.route_required == "all_routes"))) and
                              loc_name not in exclusion_table[self.options.route_required.current_key]]
            for exit in exits:
                ret.exits.append(Entrance(self.player, exit, ret))
            return ret

        self.multiworld.regions += [UndertaleRegion(*r) for r in undertale_regions]
        link_undertale_areas(self.multiworld, self.player)

    def fill_slot_data(self):
        return self._get_undertale_data()

    def create_item(self, name: str) -> Item:
        item_data = item_table[name]
        item = UndertaleItem(name, item_data.classification, item_data.code, self.player)
        return item
