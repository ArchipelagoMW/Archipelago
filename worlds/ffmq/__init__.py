import Utils
import settings
import base64
import threading
import requests
import yaml
from worlds.AutoWorld import World, WebWorld
from BaseClasses import Tutorial
from .Regions import create_regions, location_table, set_rules, stage_set_rules, rooms, non_dead_end_crest_rooms,\
    non_dead_end_crest_warps
from .Items import item_table, item_groups, create_items, FFMQItem, fillers
from .Output import generate_output
from .Options import option_definitions
from .Client import FFMQClient


# removed until lists are supported
# class FFMQSettings(settings.Group):
#     class APIUrls(list):
#         """A list of API URLs to get map shuffle, crest shuffle, and battlefield reward shuffle data from."""
#     api_urls: APIUrls = [
#         "https://api.ffmqrando.net/",
#         "http://ffmqr.jalchavware.com:5271/"
#     ]


class FFMQWebWorld(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to playing Final Fantasy Mystic Quest with Archipelago.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Alchav"]
    )]


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
    stage_set_rules = stage_set_rules

    data_version = 1
    
    web = FFMQWebWorld()
    # settings: FFMQSettings

    def __init__(self, world, player: int):
        self.rom_name_available_event = threading.Event()
        self.rom_name = None
        self.rooms = None
        super().__init__(world, player)

    def generate_early(self):
        if self.multiworld.sky_coin_mode[self.player] == "shattered_sky_coin":
            self.multiworld.brown_boxes[self.player].value = 1
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

    @classmethod
    def stage_generate_early(cls, multiworld):

        # api_urls = Utils.get_options()["ffmq_options"].get("api_urls", None)
        api_urls = [
            "https://api.ffmqrando.net/",
            "http://ffmqr.jalchavware.com:5271/"
        ]

        rooms_data = {}

        for world in multiworld.get_game_worlds("Final Fantasy Mystic Quest"):
            if (world.multiworld.map_shuffle[world.player] or world.multiworld.crest_shuffle[world.player] or
                    world.multiworld.crest_shuffle[world.player]):
                if world.multiworld.map_shuffle_seed[world.player].value.isdigit():
                    multiworld.random.seed(int(world.multiworld.map_shuffle_seed[world.player].value))
                elif world.multiworld.map_shuffle_seed[world.player].value != "random":
                    multiworld.random.seed(int(hash(world.multiworld.map_shuffle_seed[world.player].value))
                                                + int(world.multiworld.seed))

                seed = hex(multiworld.random.randint(0, 0xFFFFFFFF)).split("0x")[1].upper()
                map_shuffle = multiworld.map_shuffle[world.player].value
                crest_shuffle = multiworld.crest_shuffle[world.player].current_key
                battlefield_shuffle = multiworld.shuffle_battlefield_rewards[world.player].current_key
                companion_shuffle = multiworld.companions_locations[world.player].value
                kaeli_mom = multiworld.kaelis_mom_fight_minotaur[world.player].current_key

                query = f"s={seed}&m={map_shuffle}&c={crest_shuffle}&b={battlefield_shuffle}&cs={companion_shuffle}&km={kaeli_mom}"

                if query in rooms_data:
                    world.rooms = rooms_data[query]
                    continue

                if not api_urls:
                    raise Exception("No FFMQR API URLs specified in host.yaml")

                errors = []
                for api_url in api_urls.copy():
                    try:
                        response = requests.get(f"{api_url}GenerateRooms?{query}")
                    except (ConnectionError, requests.exceptions.HTTPError, requests.exceptions.ConnectionError,
                            requests.exceptions.RequestException) as err:
                        api_urls.remove(api_url)
                        errors.append([api_url, err])
                    else:
                        if response.ok:
                            world.rooms = rooms_data[query] = yaml.load(response.text, yaml.Loader)
                            break
                        else:
                            api_urls.remove(api_url)
                            errors.append([api_url, response])
                else:
                    error_text = f"Failed to fetch map shuffle data for FFMQ player {world.player}"
                    for error in errors:
                        error_text += f"\n{error[0]} - got error {error[1].status_code} {error[1].reason} {error[1].text}"
                    raise Exception(error_text)
                api_urls.append(api_urls.pop(0))
            else:
                world.rooms = rooms

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
        for item, count in fillers.items():
            r -= count
            r -= fillers[item]
            if r <= 0:
                return item

    def extend_hint_information(self, hint_data):
        hint_data[self.player] = {}
        if self.multiworld.map_shuffle[self.player]:
            single_location_regions = ["Subregion Volcano Battlefield", "Subregion Mac's Ship", "Subregion Doom Castle"]
            for subregion in ["Subregion Foresta", "Subregion Aquaria", "Subregion Frozen Fields", "Subregion Fireburg",
                              "Subregion Volcano Battlefield", "Subregion Windia", "Subregion Mac's Ship",
                              "Subregion Doom Castle"]:
                region = self.multiworld.get_region(subregion, self.player)
                for location in region.locations:
                    if location.address and self.multiworld.map_shuffle[self.player] != "dungeons":
                        hint_data[self.player][location.address] = (subregion.split("Subregion ")[-1]
                                                                    + (" Region" if subregion not in
                                                                       single_location_regions else ""))
                for overworld_spot in region.exits:
                    if ("Subregion" in overworld_spot.connected_region.name or
                            overworld_spot.name == "Overworld - Mac Ship Doom" or "Focus Tower" in overworld_spot.name
                            or "Doom Castle" in overworld_spot.name or overworld_spot.name == "Overworld - Giant Tree"):
                        continue
                    exits = list(overworld_spot.connected_region.exits) + [overworld_spot]
                    checked_regions = set()
                    while exits:
                        exit_check = exits.pop()
                        if (exit_check.connected_region not in checked_regions and "Subregion" not in
                                exit_check.connected_region.name):
                            checked_regions.add(exit_check.connected_region)
                            exits.extend(exit_check.connected_region.exits)
                            for location in exit_check.connected_region.locations:
                                if location.address:
                                    hint = []
                                    if self.multiworld.map_shuffle[self.player] != "dungeons":
                                        hint.append((subregion.split("Subregion ")[-1] + (" Region" if subregion not
                                                    in single_location_regions else "")))
                                    if self.multiworld.map_shuffle[self.player] != "overworld" and subregion not in \
                                            ("Subregion Mac's Ship", "Subregion Doom Castle"):
                                        hint.append(overworld_spot.name.split("Overworld - ")[-1].replace("Pazuzu",
                                            "Pazuzu's"))
                                    hint = " - ".join(hint)
                                    if location.address in hint_data[self.player]:
                                        hint_data[self.player][location.address] += f"/{hint}"
                                    else:
                                        hint_data[self.player][location.address] = hint

