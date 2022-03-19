import json
import os
import shutil
import threading
from typing import NamedTuple, Union
import logging

from BaseClasses import Item, Location, Region, Entrance, MultiWorld
from . import Logic
from ..generic.Rules import add_rule, set_rule, forbid_item, add_item_rule
from ..AutoWorld import World, LogicMixin
from NetUtils import SlotType
from .Locations import location_table
from .Items import item_table
from .Options import ff6wc_options


class FF6WCWorld(World):
    options = ff6wc_options
    game = "Final Fantasy 6 Worlds Collide"
    topology_present = False
    data_version = 1
    base_id = 6000


    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = location_table

    item_name_groups = {
        'characters': [
            'TERRA', 'LOCKE', 'CYAN', 'SHADOW', 'EDGAR',
            'SABIN', 'CELES', 'STRAGO', 'RELM', 'SETZER',
            'MOG', 'GAU', 'GOGO', 'UMARO'
        ],
        'espers': [
            "Ramuh", "Ifrit", "Shiva", "Siren", "Terrato", "Shoat", "Maduin",
            "Bismark", "Stray", "Palidor", "Tritoch", "Odin", "Raiden", "Bahamut",
            "Alexandr", "Crusader", "Ragnarok", "Kirin", "ZoneSeek", "Carbunkl",
            "Phantom", "Sraphim", "Golem", "Unicorn", "Fenrir", "Starlet", "Phoenix",
        ],
        "dragons": [
            "Removed!", "Stomped!",
            "Blasted!", "Ditched!",
            "Wiped!", "Incinerated!",
            "Skunked!", "Gone!"
        ]
    }

    for k, v in item_name_to_id.items():
        item_name_to_id[k] = v + base_id

    for k, v in location_name_to_id.items():
        if v is not None:
            location_name_to_id[k] = v + base_id

    def __init__(self, world: MultiWorld, player: int):
        super().__init__(world, player)
        self.starting_characters = None
        self.generator_in_use = threading.Event()
        self.wc = None

    def create_item(self, name: str):
        return FF6WCItem(name, True, self.item_name_to_id[name], self.player)

    def create_event(self, event: str):
        return FF6WCItem(event, True, None, self.player)

    def create_location(self, name, id, parent, event=False):
        return_location = FF6WCLocation(self.player, name, id, parent)
        return_location.event = event
        return return_location

    def generate_early(self):
        chosen_starting_characters = [
            str.upper(self.world.StartingCharacter1[self.player].current_key),
            str.upper(self.world.StartingCharacter2[self.player].current_key),
            str.upper(self.world.StartingCharacter3[self.player].current_key),
            str.upper(self.world.StartingCharacter4[self.player].current_key)
        ]
        chosen_starting_characters = chosen_starting_characters[0:self.world.StartingCharacterCount[self.player]]

        filtered_starting_characters = []
        for character in chosen_starting_characters:
            if character not in filtered_starting_characters:
                filtered_starting_characters.append(character)

        self.starting_characters = filtered_starting_characters

    def create_regions(self):
        menu = Region("Menu", None, "Menu", self.player, self.world)
        world_map = Region("World Map", None, "World Map", self.player, self.world)
        final_dungeon = Region("Kefka's Tower", None, "Kefka's Tower", self.player, self.world)

        for name, id in self.location_name_to_id.items():
            if name in Locations.dragon_events:
                id = None
            if name in Locations.kefka_checks.keys():
                final_dungeon.locations.append(self.create_location(name, id, final_dungeon))
            elif name in Locations.accomplishment_data.keys():
                final_dungeon.locations.append(self.create_location(name, None, final_dungeon, True))
            else:
                world_map.locations.append(self.create_location(name, id, world_map))

        airship = Entrance(self.player, "Airship", menu)
        final_dungeon_entrance = Entrance(self.player, "Kefka's Tower Landing", world_map)
        # airship.connect(menu)
        airship.connect(world_map)
        menu.exits.append(airship)
        world_map.exits.append(airship)
        self.world.regions.append(menu)
        final_dungeon_entrance.connect(world_map)
        final_dungeon_entrance.connect(final_dungeon)
        world_map.exits.append(final_dungeon_entrance)
        final_dungeon.exits.append(final_dungeon_entrance)
        self.world.regions.append(world_map)
        self.world.regions.append(final_dungeon)

    def create_items(self):
        for item in map(self.create_item, self.item_name_to_id):
            if item.name in self.starting_characters:
                self.world.push_precollected(item)
            else:
                self.world.itempool.append(item)

    def set_rules(self):
        check_list = {
            "TERRA": Locations.terra_checks,
            "LOCKE": Locations.locke_checks,
            "CYAN": Locations.cyan_checks,
            "SHADOW": Locations.shadow_checks,
            "EDGAR": Locations.edgar_checks,
            "SABIN": Locations.sabin_checks,
            "CELES": Locations.celes_checks,
            "STRAGO": Locations.strago_checks,
            "RELM": Locations.relm_checks,
            "SETZER": Locations.setzer_checks,
            "MOG": Locations.mog_checks,
            "GAU": Locations.gau_checks,
            "GOGO": Locations.gogo_checks,
            "UMARO": Locations.umaro_checks,
        }
        # Set every character locked check to require that character.
        for check_name, checks in check_list.items():
            for check, id in checks.items():
                if check_name == "TERRA":
                    set_rule(self.world.get_location(check, self.player),
                        lambda state: state._ff6wc_has_terra(self.player))
                elif check_name == "LOCKE":
                    set_rule(self.world.get_location(check, self.player),
                        lambda state: state._ff6wc_has_locke(self.player))
                elif check_name == "CYAN":
                    set_rule(self.world.get_location(check, self.player),
                        lambda state: state._ff6wc_has_cyan(self.player))
                elif check_name == "SHADOW":
                    set_rule(self.world.get_location(check, self.player),
                        lambda state: state._ff6wc_has_shadow(self.player))
                elif check_name == "EDGAR":
                    set_rule(self.world.get_location(check, self.player),
                        lambda state: state._ff6wc_has_edgar(self.player))
                elif check_name == "SABIN":
                    set_rule(self.world.get_location(check, self.player),
                        lambda state: state._ff6wc_has_sabin(self.player))
                elif check_name == "CELES":
                    set_rule(self.world.get_location(check, self.player),
                        lambda state: state._ff6wc_has_celes(self.player))
                elif check_name == "STRAGO":
                    set_rule(self.world.get_location(check, self.player),
                        lambda state: state._ff6wc_has_strago(self.player))
                elif check_name == "RELM":
                    set_rule(self.world.get_location(check, self.player),
                        lambda state: state._ff6wc_has_relm(self.player))
                elif check_name == "SETZER":
                    set_rule(self.world.get_location(check, self.player),
                        lambda state: state._ff6wc_has_setzer(self.player))
                elif check_name == "GAU":
                    set_rule(self.world.get_location(check, self.player),
                        lambda state: state._ff6wc_has_gau(self.player))
                elif check_name == "MOG":
                    set_rule(self.world.get_location(check, self.player),
                        lambda state: state._ff6wc_has_mog(self.player))
                elif check_name == "GOGO":
                    set_rule(self.world.get_location(check, self.player),
                        lambda state: state._ff6wc_has_gogo(self.player))
                elif check_name == "UMARO":
                    set_rule(self.world.get_location(check, self.player),
                        lambda state: state._ff6wc_has_umaro(self.player))

        for check in Locations.item_only_checks:
            add_item_rule(self.world.get_location(check, self.player),
                          lambda item: item.name not in self.item_name_groups["characters"]
                                       and item.name not in self.item_name_groups['espers']
                                        or item.player != self.player)

        for check in Locations.no_character_checks:
            add_item_rule(self.world.get_location(check, self.player),
                          lambda item: item.name not in self.item_name_groups["characters"]
                                        or item.player != self.player)

        for check in Locations.no_item_checks:
            add_item_rule(self.world.get_location(check, self.player),
                          lambda item: item.name in self.item_name_groups["characters"]
                                        or item.name in self.item_name_groups['espers']
                                        or item.player != self.player)

        for dragon in Locations.dragons:
            dragon_event = Locations.dragon_events_link[dragon]
            add_item_rule(self.world.get_location(dragon_event, self.player),
                          lambda state: state.can_reach(str(dragon), 'Location', self.player))

        set_rule(self.world.get_region("Menu", self.player), lambda state: True)
        set_rule(self.world.get_region("World Map", self.player), lambda state: True)
        set_rule(self.world.get_entrance("Airship", self.player), lambda state: True)
        set_rule(self.world.get_entrance("Kefka's Tower Landing", self.player),
                 lambda state: state._ff6wc_has_enough_characters(self.world, self.player)
                               and state._ff6wc_has_enough_espers(self.world, self.player))
        set_rule(self.world.get_region("Kefka's Tower", self.player),
                 lambda state: state._ff6wc_has_enough_characters(self.world, self.player)
                               and state._ff6wc_has_enough_espers(self.world, self.player))
        set_rule(self.world.get_location("Beat Final Kefka", self.player),
                 lambda state: state.can_reach("Kefka's Tower", 'Location', self.player)
                                and state._ff6wc_has_enough_dragons(self.world, self.player))

    def generate_basic(self):
        self.world.get_location("Kefka's Tower", self.player).place_locked_item(
            self.create_event("Kefka's Tower Access"))
        self.world.get_location("Beat Final Kefka", self.player).place_locked_item(self.create_event("Victory"))
        self.world.completion_condition[self.player] = lambda state: state.has("Victory", self.player)

        for index, dragon in enumerate(Locations.dragons):
            dragon_event = Locations.dragon_events_link[dragon]
            self.world.get_location(dragon_event, self.player).place_locked_item(
                self.create_event(self.item_name_groups["dragons"][index]))

        filler_item = self.create_item("Junk")
        filler_count = len(
            self.world.get_unfilled_locations(self.player)) - len(
                [item for item in self.world.itempool if item.player == self.player])
        self.world.itempool += [filler_item for i in range(0, filler_count)]

    def generate_output(self, output_directory: str):
        locations = dict()
        # get all locations
        for region in self.world.regions:
            if region.player == self.player:
                for location in region.locations:
                    locations[location.name] = "Archipelago"
                    if location.item.player == self.player:
                        locations[location.name] = location.item.name
        options = self.options
        other = self.world
        character_arg_string = ""
        for index, character in enumerate(self.starting_characters):
            character_arg_string += f"-sc{index + 1}={str.lower(character)}"
        char_c = str(self.world.CharacterCount[self.player]) + "." + str(self.world.CharacterCount[self.player])
        esper_c = str(self.world.EsperCount[self.player]) + "." + str(self.world.EsperCount[self.player])
        drag_c = str(self.world.DragonCount[self.player]) + "." + str(self.world.DragonCount[self.player])
        objective_flag = f'-oa=2.3.3.2.{char_c}.4.{esper_c}.6.{drag_c}'
        filename = os.path.join(os.path.abspath('.'), 'output', 'ff6wc' + self.world.seed_name + str(self.player) + '.json')
        with open(filename, "w") as file:
            json.dump(locations, file, indent=2)
        argtest = [
            "-i=ff3.sfc",
            f"-ap={filename}",
            objective_flag,
            "-ob=30.8.8.1.1.11.8",
            "-nro",
            "-sl",
            "-cg",
            character_arg_string,
            "-debug"
        ]

        arglist = " ".join(argtest)
        print(arglist)
        # -oa 2.3.3.2.4.12.4.10.26.6.1.8 is characters/espers/dragons
        # (2.4.12 is Characters, 4-12; 4.10.26 is Espers, 10-26, 6.1.8 is Dragons, 1-8)
        # -ob 30.8.8.1.1.11.8 is Get All SwdTechs after Doma.
        os.system(f"python ./worlds/ff6wc/WorldsCollide/wc.py {arglist}")
        os.remove(filename)
        return "test"


class FF6WCItem(Item):
    game = 'Final Fantasy 6 Worlds Collide'


class FF6WCLocation(Location):
    game = 'Final Fantasy 6 Worlds Collide'


class PlandoItem(NamedTuple):
    item: str
    location: str
    world: Union[bool, str] = False  # False -> own world, True -> not own world
    from_pool: bool = True  # if item should be removed from item pool
    force: str = 'silent'  # false -> warns if item not successfully placed. true -> errors out on failure to place item.

    def warn(self, warning: str):
        if self.force in ['true', 'fail', 'failure', 'none', 'false', 'warn', 'warning']:
            logging.warning(f'{warning}')
        else:
            logging.debug(f'{warning}')

    def failed(self, warning: str, exception=Exception):
        if self.force in ['true', 'fail', 'failure']:
            raise exception(warning)
        else:
            self.warn(warning)


class PlandoConnection(NamedTuple):
    entrance: str
    exit: str
    direction: str  # entrance, exit or both
