from worlds.AutoWorld import World
from .Regions import create_regions, location_table, set_rules, rooms, non_dead_end_crest_rooms,\
    non_dead_end_crest_warps
from .Items import item_table, item_groups, create_items, FFMQItem, fillers
from .Output import generate_output
from .Options import option_definitions
from .Client import FFMQClient
import base64
import threading
import requests
import yaml


class FFMQWorld(World):
    """Final Fantasy: Mystic Quest is a simple, humorous RPG for the Super Nintendo. You travel across four continents,
    linked in the middle of the world by the Focus Tower, which has been locked by four magical coins. Make your way to
    the bottom of the Focus Tower, then straight up through the top!"""
    # -Giga Otomia

    game = "Final Fantasy Mystic Quest"

    item_name_to_id = {name: data.id for name, data in item_table.items() if data.id is not None}
    location_name_to_id = location_table
    option_definitions = option_definitions

    topology_present = True

    item_name_groups = item_groups

    generate_output = generate_output
    create_items = create_items
    create_regions = create_regions
    set_rules = set_rules

    def __init__(self, world, player: int):
        self.rom_name_available_event = threading.Event()
        self.rom_name = None
        self.rooms = None
        super().__init__(world, player)

    def generate_early(self):
        if self.multiworld.sky_coin_mode[self.player] == "shattered_sky_coin":
            self.multiworld.brown_boxes[self.player] = self.multiworld.brown_boxes[self.player].from_text("include")
        if self.multiworld.enemies_scaling_lower[self.player].value > \
                self.multiworld.enemies_scaling_upper[self.player].value:
            (self.multiworld.enemies_scaling_lower[self.player].value,
             self.multiworld.enemies_scaling_upper[self.player].value) =\
                (self.multiworld.enemies_scaling_upper[self.player].value,
                 self.multiworld.enemies_scaling_lower[self.player].value)
        if self.multiworld.bosses_scaling_lower[self.player].value > \
                self.multiworld.bosses_scaling_upper[self.player].value:
            (self.multiworld.bosses_scaling_lower[self.player].value,
             self.multiworld.bosses_scaling_upper[self.player].value) =\
                (self.multiworld.bosses_scaling_upper[self.player].value,
                 self.multiworld.bosses_scaling_lower[self.player].value)

        if (self.multiworld.map_shuffle[self.player] or self.multiworld.crest_shuffle[self.player] or
                self.multiworld.crest_shuffle[self.player]):
            if self.multiworld.map_shuffle_seed[self.player].value.isdigit():
                self.multiworld.random.seed(int(self.multiworld.map_shuffle_seed[self.player].value))
            elif self.multiworld.map_shuffle_seed[self.player].value != "random":
                self.multiworld.random.seed(int(hash(self.multiworld.map_shuffle_seed[self.player].value))
                                            + int(self.multiworld.seed))

            seed = hex(self.multiworld.random.randint(0, 0xFFFFFFFF)).split("0x")[1].upper()
            map_shuffle = self.multiworld.map_shuffle[self.player].value
            crest_shuffle = self.multiworld.crest_shuffle[self.player].current_key
            battlefield_shuffle = self.multiworld.shuffle_battlefield_rewards[self.player].current_key

            url = f"https://ffmqrapi.azurewebsites.net/GenerateRooms?s={seed}&m={map_shuffle}&c={crest_shuffle}&b={battlefield_shuffle}"
            response = requests.get(url)
            if response.ok:
                self.rooms = yaml.load(response.text, yaml.Loader)
            else:
                raise Exception(f"Got error {response.status_code} {response.reason} {response.text} from trying to "
                                f"fetch map shuffle data for FFMQ player {self.player}")
        else:
            self.rooms = rooms

    def create_item(self, name: str):
        return FFMQItem(name, self.player)

    def collect_item(self, state, item, remove=False):
        if "Progressive" in item.name:
            i = item.code - 256
            if state.has(self.item_id_to_name[i], self.player):
                if state.has(self.item_id_to_name[i+1], self.player):
                    return self.item_id_to_name[i+2]
                return self.item_id_to_name[i+1]
            return self.item_id_to_name[i]
        return item.name if item.advancement else None

    def modify_multidata(self, multidata):
        # wait for self.rom_name to be available.
        self.rom_name_available_event.wait()
        rom_name = getattr(self, "rom_name", None)
        # we skip in case of error, so that the original error in the output thread is the one that gets raised
        if rom_name:
            new_name = base64.b64encode(bytes(self.rom_name)).decode()
            payload = multidata["connect_names"][self.multiworld.player_name[self.player]]
            multidata["connect_names"][new_name] = payload

    def get_filler_item_name(self):
        r = self.multiworld.random.randint(0, 201)
        for item in fillers:
            r -= fillers[item]
            if r <= 0:
                return item

    def extend_hint_information(self, hint_data):
        hint_data[self.player] = {}
        if True: #self.multiworld.map_shuffle[self.player]:
            for subregion in ["Subregion Foresta", "Subregion Aquaria", "Subregion Frozen Fields", "Subregion Fireburg",
                              "Subregion Volcano Battlefield", "Subregion Windia", "Subregion Mac's Ship",
                              "Subregion Doom Castle"]:
                region = self.multiworld.get_region(subregion, self.player)
                # exits = region.exits
                for location in region.locations:
                    if location.address:
                        hint_data[self.player][location.address] = subregion.split("Subregion ")[-1]
                for overworld_spot in region.exits:
                    if ("Subregion" in overworld_spot.connected_region.name or
                            overworld_spot.name == "Overworld - Mac Ship Doom" or "Focus Tower" in overworld_spot.name
                            or "Doom Castle" in overworld_spot.name or overworld_spot.name == "Overworld - Giant Tree"):
                        continue
                    exits = overworld_spot.connected_region.exits + [overworld_spot]
                    checked_regions = set()
                    while exits:
                        exit_check = exits.pop()
                        if (exit_check.connected_region not in checked_regions and "Subregion" not in
                                exit_check.connected_region.name and (exit_check.name not in
                                non_dead_end_crest_warps or exit_check.connected_region.name not in
                                non_dead_end_crest_rooms)):
                            checked_regions.add(exit_check.connected_region)
                            exits.extend(exit_check.connected_region.exits)
                            for location in exit_check.connected_region.locations:
                                if location.address:
                                    if location.address in hint_data[self.player]:
                                        print("dupe")
                                    hint_data[self.player][location.address] = \
                                        overworld_spot.name.split("Overworld - ")[-1].replace("Pazuzu", "Pazuzu's")
