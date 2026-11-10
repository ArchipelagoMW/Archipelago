from .Items import UndertaleItem, item_table, required_armor, required_weapons, non_key_items, key_items, \
    junk_weights_all, junk_weights_neutral, junk_weights_pacifist, junk_weights_genocide, \
    junk_weights_cut_items, spells_attack, spells_heal, spells_gimmicks, spells_pacifist, spells_violent
from .Locations import advancement_table, exclusion_table
from .er_rules import set_er_location_rules
from .er_scripts import create_er_regions_vanilla, UndertaleERLocation
from .er_data import door_name_list, genocide_missing_rooms
from worlds.generic.Rules import exclusion_rules
from BaseClasses import Tutorial, Item, MultiWorld
from .Options import UndertaleOptions
from worlds.AutoWorld import World, WebWorld
from worlds.LauncherComponents import Component, components
from multiprocessing import Process
from typing import Dict, List, Any
import math
import typing


def run_client():
    print('running undertale client')
    from .UndertaleClient import main  # lazy import
    p = Process(target=main)
    p.start()


# components.append(Component("Undertale Client", "UndertaleClient"))
components.append(Component("Undertale Client", func=run_client))


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
    topology_present = True
    glitches_item_name = "Out of Logic Access"

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = {name: data.id for name, data in advancement_table.items()}

    data_version = 7
    er_portal_hints: Dict[int, str]
    
    all_door_locks: List[str] = []

    def interpret_slot_data(self, slot_data: dict[str, Any]) -> None:
        if "Locked Doors" in slot_data:
            self.all_door_locks = slot_data["Locked Doors"]
            return slot_data

    def __init__(self, multiworld: "MultiWorld", player: int):
        super().__init__(multiworld, player)

    def _get_undertale_data(self):
        return {
            "world_seed": self.random.getrandbits(32),
            "seed_name": self.multiworld.seed_name,
            "player_name": self.multiworld.get_player_name(self.player),
            "player_id": self.player,
            "client_version": self.required_client_version,
            "race": self.multiworld.is_race,
            "route_required": self.options.route_required.current_key,
            "starting_area": self.options.starting_area.current_key,
            "temy_include": bool(self.options.temy_include.value),
            "only_flakes": bool(self.options.only_flakes.value),
            "no_equips": bool(self.options.no_equips.value),
            "key_hunt": bool(self.options.key_hunt.value),
            "key_pieces": self.options.key_pieces.value,
            "extra_key_pieces": self.options.extra_key_pieces.value,
            "rando_love": bool(self.options.rando_love.value),
            "rando_stats": bool(self.options.rando_stats.value),
            "prog_armor": bool(self.options.prog_armor.value),
            "prog_weapons": bool(self.options.prog_weapons.value),
            "rando_item_button": bool(self.options.rando_item_button.value),
            "kill_sanity": self.options.kill_sanity.current_key,
            "rando_jump": bool(self.options.rando_jump.value),
            "cut_items": bool(self.options.cut_items.value),
            "kill_sanity_pack_size": self.options.kill_sanity_pack_size.value,
            "ice_traps": self.options.ice_traps.value,
            "spare_sanity": self.options.spare_sanity.current_key,
            "gifting": False,
            # "gifting": bool(self.options.gifting.value),
            "entrance_rando": False,
            # "entrance_rando": bool(self.options.entrance_rando.value),
            "spare_sanity_max": self.options.spare_sanity_max.value,
            "spare_sanity_pack_size": self.options.spare_sanity_pack_size.value,
            "bonus_locations": bool(self.options.bonus_locations.value),
            "guaranteed_filler": self.options.guaranteed_filler.value,
            "hub_shop_cost": self.options.hub_shop_cost.value,
            "enabled_spells": set(self.options.enabled_spells.value),
            "door_locks": self.options.door_locks.value,
            "mandatory_door_locks": set(self.options.mandatory_door_locks.value),
            "excluded_door_locks": set(self.options.excluded_door_locks.value),
            "love_reduction_traps": self.options.love_reduction_traps.value,
            "max_hp_reduction_traps": self.options.max_hp_reduction_traps.value,
            "atk_reduction_traps": self.options.atk_reduction_traps.value,
            "def_reduction_traps": self.options.def_reduction_traps.value,
            "sans_req_hp": self.options.sans_req_hp.value,
            "sans_req_inv_tier": self.options.sans_req_inv_tier.value,
            "undying_req_hp": self.options.undying_req_hp.value,
            "undying_req_atk": self.options.undying_req_atk.value,
            "undying_req_def": self.options.undying_req_def.value,
            "asgore_req_atk": self.options.asgore_req_atk.value,
            "asgore_req_def": self.options.asgore_req_def.value,
            "start_inventory_from_pool": self.options.start_inventory_from_pool.value
        }

    def get_filler_item_name(self):
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
        if self.options.cut_items:
            junk_pool = junk_pool | junk_weights_cut_items.copy()
        if not self.options.only_flakes:
            return self.random.choices(list(junk_pool.keys()), weights=list(junk_pool.values()))[0]
        else:
            return "Temmie Flakes"

        # if self.options.entrance_rando:
            # self.undertale_portal_pairs = assemble_er(self)
        # else:

    def generate_early(self):
        if self.options.route_required.current_key != "genocide" and \
                self.options.route_required.current_key != "all_routes":
            self.options.kill_sanity.value = 0
            self.options.rando_love.value = 0
            self.options.rando_stats.value = 0
        if self.options.route_required.current_key == "genocide":
            self.options.spare_sanity.value = 0
        if self.options.kill_sanity.value != 2:
            self.options.kill_sanity_pack_size.value = 40
        if self.options.spare_sanity.value == 1:
            self.options.spare_sanity_pack_size.value = self.options.spare_sanity_max.value
            
        re_gen_passthrough = getattr(self.multiworld, "re_gen_passthrough", {})
        if re_gen_passthrough and self.game in re_gen_passthrough:
            slot_data: dict[str, Any] = re_gen_passthrough[self.game]
            self.all_door_locks = []
            if "Locked Doors" in slot_data:
                self.all_door_locks = slot_data["Locked Doors"]
        else:
            self.all_door_locks = []
            if self.options.door_locks.value > 0:
                rand_door_list = door_name_list.copy()
                if self.options.route_required.current_key == "genocide":
                    rand_door_list = [item for item in rand_door_list if (item.split(" <-> ")[0] not in genocide_missing_rooms and item.split(" <-> ")[1] not in genocide_missing_rooms)]
                rand_door_list = [item for item in rand_door_list if (item not in self.options.excluded_door_locks.value and item not in self.options.mandatory_door_locks.value and item.split(" <-> ")[1]+" <->"+item.split(" <-> ")[0] not in self.options.mandatory_door_locks.value and item.split(" <-> ")[1]+" <->"+item.split(" <-> ")[0] not in self.options.excluded_door_locks.value)]
                amount_to_add = min(len(rand_door_list), self.options.door_locks.value)
                # print("actually added = "+str(amount_to_add))
                self.random.shuffle(rand_door_list)
                for i in range(amount_to_add):
                    self.all_door_locks.append(rand_door_list.pop())
            if len(self.options.mandatory_door_locks.value) > 0:
                rand_door_list = door_name_list.copy()
                self.all_door_locks.extend([do for do in rand_door_list if do in self.options.mandatory_door_locks.value or do.split(" <-> ")[1]+" <->"+do.split(" <-> ")[0] in self.options.mandatory_door_locks.value])

    def create_items(self):
        exclusion_pool = set()
        # Generate item pool
        itempool = []
        # Add all required progression items
        for name, num in key_items.items():
            itempool += [name] * num
        for name, num in required_armor.items():
            itempool += [name] * num
        for name, num in required_weapons.items():
            itempool += [name] * num
        for name, num in non_key_items.items():
            itempool += [name] * num
            
        for door in self.all_door_locks:
            itempool += ["Door Unlock - "+door]

        if "attack" in self.options.enabled_spells:
            for name, num in spells_attack.items():
                itempool += [name] * num
        if "heal" in self.options.enabled_spells:
            for name, num in spells_heal.items():
                itempool += [name] * num
        if "pacifist" in self.options.enabled_spells:
            for name, num in spells_pacifist.items():
                itempool += [name] * num
        if "violent" in self.options.enabled_spells:
            for name, num in spells_violent.items():
                itempool += [name] * num
        if "gimmick" in self.options.enabled_spells:
            for name, num in spells_gimmicks.items():
                itempool += [name] * num
        if self.options.rando_item_button:
            itempool += ["ITEM"]
        else:
            self.multiworld.push_precollected(self.create_item("ITEM"))
        if not self.options.rando_jump:
            itempool.remove("Jump")
            self.multiworld.push_precollected(self.create_item("Jump"))
        if self.options.route_required == "genocide":
            itempool = [item for item in itempool if item != "Stained Apron"
                        and item != "Hot Dog...?" and item != "Punch Card"]
        elif self.options.route_required == "neutral":
            itempool = [item for item in itempool if item != "Hot Dog...?"]
        if self.options.route_required == "pacifist" or self.options.route_required == "all_routes":
            itempool += ["Undyne Letter EX"]
        else:
            itempool.remove("Complete Skeleton")
            itempool.remove("Fish")
            itempool.remove("DT Extractor")
        if self.options.key_hunt:
            itempool += ["Key Piece"] * (self.options.key_pieces.value + self.options.extra_key_pieces.value)
        else:
            itempool += ["Left Home Key"]
            itempool += ["Right Home Key"]
        if not self.options.rando_love or \
                (self.options.route_required != "genocide" and
                 self.options.route_required != "all_routes"):
            itempool = [item for item in itempool if not item == "LOVE"]
        if self.options.rando_love or \
                (self.options.route_required == "genocide" or
                 self.options.route_required == "all_routes"):
            itempool += ["LOVE Reduction Trap"] * self.options.love_reduction_traps.value
        if self.options.rando_stats or \
                (self.options.route_required == "genocide" or
                 self.options.route_required == "all_routes"):
            itempool += ["Max HP Reduction Trap"] * self.options.max_hp_reduction_traps.value
            itempool += ["ATK Reduction Trap"] * self.options.atk_reduction_traps.value
            itempool += ["DEF Reduction Trap"] * self.options.def_reduction_traps.value
        if self.options.spare_sanity == 2 and self.options.route_required != "genocide":
            itempool += ["Ruins Spare"] * math.ceil(self.options.spare_sanity_max.value /
                                                    self.options.spare_sanity_pack_size.value)
            itempool += ["Snowdin Spare"] * math.ceil(self.options.spare_sanity_max.value /
                                                      self.options.spare_sanity_pack_size.value)
            itempool += ["Waterfall Spare"] * math.ceil(self.options.spare_sanity_max.value /
                                                        self.options.spare_sanity_pack_size.value)
            itempool += ["Hotland Spare"] * math.ceil(self.options.spare_sanity_max.value /
                                                      self.options.spare_sanity_pack_size.value)
        elif self.options.spare_sanity == 1:
            self.multiworld.push_precollected(self.create_item("Ruins Spare"))
            self.multiworld.push_precollected(self.create_item("Snowdin Spare"))
            self.multiworld.push_precollected(self.create_item("Waterfall Spare"))
            self.multiworld.push_precollected(self.create_item("Hotland Spare"))
        if self.options.kill_sanity != 2 or \
                (self.options.route_required != "genocide" and
                 self.options.route_required != "all_routes"):
            self.multiworld.push_precollected(self.create_item("Ruins Population Pack"))
            self.multiworld.push_precollected(self.create_item("Snowdin Population Pack"))
            self.multiworld.push_precollected(self.create_item("Waterfall Population Pack"))
            self.multiworld.push_precollected(self.create_item("Hotland Population Pack"))
            exclusion_pool.update(exclusion_table["NoKills"])
        else:
            itempool += ["Ruins Population Pack"] * math.ceil(20/self.options.kill_sanity_pack_size.value)
            itempool += ["Snowdin Population Pack"] * math.ceil(16/self.options.kill_sanity_pack_size.value)
            itempool += ["Waterfall Population Pack"] * math.ceil(18/self.options.kill_sanity_pack_size.value)
            itempool += ["Hotland Population Pack"] * math.ceil(40/self.options.kill_sanity_pack_size.value)
        if self.options.ice_traps.value > 0:
            itempool += ["Ice Trap"] * self.options.ice_traps.value
        if not self.options.rando_stats or \
                (self.options.route_required != "genocide" and
                 self.options.route_required != "all_routes"):
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

        if self.options.starting_area.current_key.title() == "None":
            pass
        elif self.options.starting_area.current_key.title() == "All":
            all_keys = ["Ruins Key", "Snowdin Key", "Waterfall Key", "Hotland Key"]
            for item in all_keys:
                itempool.remove(item)
                self.multiworld.push_precollected(self.create_item(item))
        else:
            starting_key = self.options.starting_area.current_key.title() + " Key"
            itempool.remove(starting_key)
            self.multiworld.push_precollected(self.create_item(starting_key))
        # Choose locations to automatically exclude based on settings
        exclusion_pool.update(exclusion_table[self.options.route_required.current_key])
        if not self.options.rando_love or \
                (self.options.route_required != "genocide" and
                 self.options.route_required != "all_routes"):
            exclusion_pool.update(exclusion_table["NoLove"])
        if not self.options.rando_stats or \
                (self.options.route_required != "genocide" and
                 self.options.route_required != "all_routes"):
            exclusion_pool.update(exclusion_table["NoStats"])

        # Choose locations to automatically exclude based on settings
        exclusion_checks = set()
        exclusion_checks.update([])
        exclusion_rules(self.multiworld, self.player, exclusion_checks)

        # Convert itempool into real items
        completed_itempool = [item for item in map(lambda itm_name: self.create_item(itm_name), itempool)]
        # Fill remaining items with randomly generated junk or Temmie Flakes
        counter = 1
        while len(completed_itempool)+self.options.guaranteed_filler.value > len(self.multiworld.get_unfilled_locations(self.player)):
            region = self.get_region("room_area1")
            location = UndertaleERLocation(self.player, "Hub Shop "+str(counter), counter, region)
            region.locations.append(location)
            counter += 1
        while len(completed_itempool) < len(self.multiworld.get_unfilled_locations(self.player)):
            completed_itempool.append(self.create_filler())

        self.multiworld.itempool += completed_itempool
    
    def set_rules(self) -> None:
        set_er_location_rules(self)

    def create_regions(self):
        create_er_regions_vanilla(self)

    def fill_slot_data(self):
        slot_data = self._get_undertale_data()
        slot_data["Locked Doors"] = self.all_door_locks
        return slot_data

    def create_item(self, name: str) -> Item:
        from .Items import item_table
        item_data = item_table[name]
        item = UndertaleItem(name, item_data.classification, item_data.code, self.player)
        return item

    def write_spoiler(self, spoiler_handle: typing.TextIO) -> None:
        player_name = self.multiworld.get_player_name(self.player)
        spoiler_handle.write(f"\n\nLocked Doors ({player_name}): ")
        list_as_string = ""
        for item in self.all_door_locks:
            list_as_string += f"{item}, "
        list_as_string = list_as_string.removesuffix(", ")
        spoiler_handle.write(list_as_string)
