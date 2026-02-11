import os
from threading import Event
from typing import List, ClassVar, Any, Optional, Type, TextIO

from BaseClasses import Item, ItemClassification, MultiWorld, CollectionState
from Options import Option
from worlds.AutoWorld import World
from .Options import *
from .Settings import OracleOfSeasonsSettings
from .Util import *
from .WebWorld import OracleOfSeasonsWeb
from .data import LOCATIONS_DATA
from .data.Constants import *
from .data.Items import ITEMS_DATA
from .generation.Hints import create_region_hints, create_item_hints
from .generation.LogicMixin import OracleOfSeasonsState


class OracleOfSeasonsWorld(World):
    """
    The Legend of Zelda: Oracles of Seasons is one of the rare Capcom entries to the series.
    The seasons in the world of Holodrum have been a mess since Onox captured Din, the Oracle of Seasons.
    Gather the Essences of Nature, confront Onox and rescue Din to give nature some rest in Holodrum.
    """
    game = "The Legend of Zelda - Oracle of Seasons"
    options_dataclass = OracleOfSeasonsOptions
    options: OracleOfSeasonsOptions
    web = OracleOfSeasonsWeb()
    topology_present = True

    settings: ClassVar[OracleOfSeasonsSettings]
    settings_key = "tloz_oos_options"

    location_name_to_id = build_location_name_to_id_dict()
    item_name_to_id = build_item_name_to_id_dict()
    item_name_groups = ITEM_GROUPS
    location_name_groups = LOCATION_GROUPS
    origin_region_name = "impa's house"

    @classmethod
    def version(cls) -> str:
        return cls.world_version.as_simple_string()

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)

        self.pre_fill_items: List[Item] = []
        self.default_seasons: Dict[str, str] = DEFAULT_SEASONS.copy()
        self.dungeon_entrances: Dict[str, str] = DUNGEON_CONNECTIONS.copy()
        self.portal_connections: Dict[str, str] = PORTAL_CONNECTIONS.copy()
        self.lost_woods_item_sequence: List[List] = LOST_WOODS_ITEM_SEQUENCE.copy()
        self.lost_woods_main_sequence: List[List] = LOST_WOODS_MAIN_SEQUENCE.copy()
        self.old_man_rupee_values: Dict[str, int] = OLD_MAN_RUPEE_VALUES.copy()
        self.samasa_gate_code: List[int] = SAMASA_GATE_CODE.copy()
        self.shop_prices: Dict[str, int] = VANILLA_SHOP_PRICES.copy()
        self.shop_order: List[List[str]] = []
        self.shop_rupee_requirements: Dict[str, int] = {}
        self.essences_in_game: List[str] = ITEM_GROUPS["Essences"].copy()
        self.random_rings_pool: List[str] = []
        self.remaining_progressive_gasha_seeds = 0

        self.made_hints = Event()
        self.region_hints: list[tuple[str, str | int]] = []
        self.item_hints: list[Item | None] = []

    def generate_early(self) -> None:
        if self.interpret_slot_data(None):
            return
        from .generation.GenerateEarly import generate_early
        generate_early(self)

    def create_regions(self) -> None:
        from worlds.tloz_oos.generation.CreateRegions import create_regions
        create_regions(self)

    def set_rules(self) -> None:
        from worlds.tloz_oos.generation.Logic import create_connections, apply_self_locking_rules
        create_connections(self, self.player, self.origin_region_name, self.options)
        apply_self_locking_rules(self.multiworld, self.player)
        self.multiworld.completion_condition[self.player] = lambda state: state.has("_beaten_game", self.player)

        self.multiworld.register_indirect_condition(self.get_region("lost woods top statue"), self.get_entrance("lost woods -> lost woods deku"))
        self.multiworld.register_indirect_condition(self.get_region("lost woods phonograph"), self.get_entrance("lost woods stump -> lost woods"))
        self.multiworld.register_indirect_condition(self.get_region("lost woods phonograph"), self.get_entrance("d6 sector -> lost woods"))
        self.multiworld.register_indirect_condition(self.get_region("lost woods deku"), self.get_entrance("lost woods -> d6 sector"))
        self.multiworld.register_indirect_condition(self.get_region("lost woods deku"), self.get_entrance("lost woods stump -> d6 sector"))

        if self.options.linked_heros_cave:
            for i in range(1, 9):
                self.multiworld.register_indirect_condition(self.get_region(f"enter d{i}"), self.get_entrance("d11 floor 4 chest -> d11 final chest"))

        if self.options.logic_difficulty == OracleOfSeasonsLogicDifficulty.option_hell:
            cucco_region = self.get_region("rooster adventure")
            # This saves using an event which is slightly more efficient
            self.multiworld.register_indirect_condition(cucco_region, self.get_entrance("d6 sector -> old man near d6"))
            self.multiworld.register_indirect_condition(cucco_region, self.get_entrance("d6 sector -> d6 entrance"))
            self.multiworld.register_indirect_condition(self.get_region("lost woods top statue"), self.get_entrance("rooster adventure -> lost woods deku"))

    def create_item(self, name: str) -> Item:
        # If item name has a "!PROG" suffix, force it to be progression. This is typically used to create the right
        # amount of progression rupees while keeping them a filler item as default
        if name.endswith("!PROG"):
            name = name.removesuffix("!PROG")
            classification = ItemClassification.progression_deprioritized_skip_balancing
        elif name.endswith("!USEFUL"):
            # Same for above but with useful. This is typically used for Required Rings,
            # as we don't want those locked in a barren dungeon
            name = name.removesuffix("!USEFUL")
            classification = ITEMS_DATA[name]["classification"]
            if classification == ItemClassification.filler:
                classification = ItemClassification.useful
        elif name.endswith("!FILLER"):
            name = name.removesuffix("!FILLER")
            classification = ItemClassification.filler
        else:
            classification = ITEMS_DATA[name]["classification"]
        ap_code = self.item_name_to_id[name]

        # A few items become progression only in hard logic
        progression_items_in_medium_logic = ["Expert's Ring", "Fist Ring", "Swimmer's Ring", "Energy Ring", "Heart Ring L-2"]
        if self.options.logic_difficulty >= OracleOfSeasonsLogicDifficulty.option_medium and name in progression_items_in_medium_logic:
            classification = ItemClassification.progression
        if self.options.logic_difficulty >= OracleOfSeasonsLogicDifficulty.option_hard and name == "Heart Ring L-1":
            classification = ItemClassification.progression
        # As many Gasha Seeds become progression as the number of deterministic Gasha Nuts
        if self.remaining_progressive_gasha_seeds > 0 and name == "Gasha Seed":
            self.remaining_progressive_gasha_seeds -= 1
            classification = ItemClassification.progression_deprioritized

        # Players in Medium+ are expected to know the default paths through Lost Woods, Phonograph becomes filler
        if self.options.logic_difficulty >= OracleOfSeasonsLogicDifficulty.option_medium and not self.options.randomize_lost_woods_item_sequence and name == "Phonograph":
            classification = ItemClassification.filler

        # UT doesn't let us know if the item is progression or not, so it is always progression
        if hasattr(self.multiworld, "generation_is_fake"):
            classification = ItemClassification.progression

        return Item(name, classification, ap_code, self.player)

    def create_items(self) -> None:
        from worlds.tloz_oos.generation.CreateItems import create_items
        create_items(self)

    def get_pre_fill_items(self) -> None:
        return self.pre_fill_items

    @classmethod
    def stage_pre_fill(cls, multiworld: MultiWorld):
        from worlds.tloz_oos.generation.PreFill import stage_pre_fill_dungeon_items
        stage_pre_fill_dungeon_items(multiworld)

    def get_filler_item_name(self) -> str:
        FILLER_ITEM_NAMES = [
            "Rupees (1)", "Rupees (5)", "Rupees (10)", "Rupees (10)",
            "Rupees (20)", "Rupees (30)",
            "Ore Chunks (10)", "Ore Chunks (10)", "Ore Chunks (25)",
            "Random Ring", "Random Ring", "Random Ring",
            "Gasha Seed", "Gasha Seed",
            "Potion"
        ]

        item_name = self.random.choice(FILLER_ITEM_NAMES)
        if item_name == "Random Ring":
            return self.get_random_ring_name()
        return item_name

    def get_random_ring_name(self) -> str:
        if len(self.random_rings_pool) > 0:
            return self.random_rings_pool.pop()
        return self.get_filler_item_name()  # It might loop but not enough to really matter

    def connect_entrances(self) -> None:
        from .generation.ER import oos_randomize_entrances
        oos_randomize_entrances(self)

    # noinspection PyUnusedLocal
    @classmethod
    def stage_fill_hook(cls, multiworld: MultiWorld, progitempool: list[Item], usefulitempool: list[Item], filleritempool: list[Item], fill_locations):
        from worlds.tloz_oos.generation.OrderPool import order_pool
        order_pool(multiworld, progitempool)

    def generate_output(self, output_directory: str):
        from worlds.tloz_oos.generation.PatchWriter import oos_create_ap_procedure_patch

        if self.options.bird_hint.know_it_all():
            self.region_hints = create_region_hints(self)

        if self.options.bird_hint.owl():
            self.item_hints = create_item_hints(self)
        self.made_hints.set()
        patch = oos_create_ap_procedure_patch(self)
        rom_path = os.path.join(output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}"
                                                  f"{patch.patch_file_ending}")
        patch.write(rom_path)

    def fill_slot_data(self) -> dict:
        slot_data = {
            "version": f"{self.version()}",
            "options": self.options.as_dict(
                *[option_name for option_name in OracleOfSeasonsOptions.type_hints
                  if hasattr(OracleOfSeasonsOptions.type_hints[option_name], "include_in_slot_data")]),
            # "samasa_gate_sequence": ' '.join([str(x) for x in self.samasa_gate_code]),
            "lost_woods_item_sequence": self.lost_woods_item_sequence,
            "lost_woods_main_sequence": self.lost_woods_main_sequence,
            "default_seasons": self.default_seasons,
            "old_man_rupee_values": self.old_man_rupee_values,
            "dungeon_entrances": {a.replace(" entrance", ""): b.replace("enter ", "")
                                  for a, b in self.dungeon_entrances.items()},
            "essences_in_game": self.essences_in_game,
            "subrosia_portals": self.portal_connections,
            "shop_rupee_requirements": self.shop_rupee_requirements,
            "shop_costs": self.shop_prices,
        }

        self.made_hints.wait()
        # The structure is made to make it easy to call CreateHints
        slot_data_item_hints = []
        for item_hint in self.item_hints:
            if item_hint is None:
                # Joke hint
                slot_data_item_hints.append(None)
                continue
            location = item_hint.location
            slot_data_item_hints.append((location.address, location.player))
        slot_data["item_hints"] = slot_data_item_hints

        return slot_data

    def write_spoiler(self, spoiler_handle: TextIO):
        from worlds.tloz_oos.generation.CreateRegions import location_is_active
        spoiler_handle.write(f"\n\nDefault Seasons ({self.multiworld.player_name[self.player]}):\n")
        for region_name, season in self.default_seasons.items():
            spoiler_handle.write(f"\t- {region_name} --> {SEASON_NAMES[season]}\n")

        if self.options.shuffle_dungeons:
            spoiler_handle.write(f"\nDungeon Entrances ({self.multiworld.player_name[self.player]}):\n")
            for entrance, dungeon in self.dungeon_entrances.items():
                spoiler_handle.write(f"\t- {entrance} --> {dungeon.replace('enter ', '')}\n")

        if self.options.shuffle_portals != "vanilla":
            spoiler_handle.write(f"\nSubrosia Portals ({self.multiworld.player_name[self.player]}):\n")
            for portal_holo, portal_sub in self.portal_connections.items():
                spoiler_handle.write(f"\t- {portal_holo} --> {portal_sub}\n")

        spoiler_handle.write(f"\nShop Prices ({self.multiworld.player_name[self.player]}):\n")
        shop_codes = [code for shop in self.shop_order for code in shop]
        shop_codes.extend(MARKET_LOCATIONS)
        for shop_code in shop_codes:
            price = self.shop_prices[shop_code]
            for loc_name, loc_data in LOCATIONS_DATA.items():
                if loc_data.get("symbolic_name", None) is None or loc_data["symbolic_name"] != shop_code:
                    continue
                if location_is_active(self, loc_name, loc_data):
                    currency = "Ore Chunks" if shop_code.startswith("subrosia") else "Rupees"
                    spoiler_handle.write(f"\t- {loc_name}: {price} {currency}\n")
                break

    def collect(self, state: CollectionState | OracleOfSeasonsState, item: Item) -> bool:
        change = super().collect(state, item)
        if not change:
            return False

        if item.name == "Bombs (10)":
            state.prog_items[self.player]["Bombs"] += 1
        elif item.name == "Bombs (20)":
            state.prog_items[self.player]["Bombs"] += 2
        elif item.name == "Bombchus (10)":
            state.prog_items[self.player]["Bombchus"] += 1
        elif item.name == "Bombchus (20)":
            state.prog_items[self.player]["Bombchus"] += 2

        if self.options.logic_difficulty < OracleOfSeasonsLogicDifficulty.option_hell:
            return True
        if item.code is None or item.code >= 0x2100 and item.code != 0x2e00:  # Not usable item nor ember nor flippers
            return True
        state.tloz_oos_available_cuccos[self.player] = None
        return True

    def remove(self, state: CollectionState | OracleOfSeasonsState, item: Item) -> bool:
        change = super().remove(state, item)
        if not change:
            return False

        if item.name == "Bombs (10)":
            state.prog_items[self.player]["Bombs"] -= 1
        elif item.name == "Bombs (20)":
            state.prog_items[self.player]["Bombs"] -= 2
        elif item.name == "Bombchus (10)":
            state.prog_items[self.player]["Bombchus"] -= 1
        elif item.name == "Bombchus (20)":
            state.prog_items[self.player]["Bombchus"] -= 2

        if self.options.logic_difficulty < OracleOfSeasonsLogicDifficulty.option_hell:
            return True
        if item.code is None or item.code >= 0x2100 and item.code != 0x2e00:  # Not usable item nor ember nor flippers
            return True
        state.tloz_oos_available_cuccos[self.player] = None
        return True

    # UT stuff
    def interpret_slot_data(self, slot_data: Optional[dict[str, Any]]) -> Any:
        if slot_data is not None:
            return slot_data

        if not hasattr(self.multiworld, "re_gen_passthrough") or self.game not in self.multiworld.re_gen_passthrough:
            return False

        slot_data = self.multiworld.re_gen_passthrough[self.game]

        for option in [option_name for option_name in OracleOfSeasonsOptions.type_hints
                       if hasattr(OracleOfSeasonsOptions.type_hints[option_name], "include_in_slot_data")]:
            option_class: Type[Option] = OracleOfSeasonsOptions.type_hints[option]
            self.options.__setattr__(option, option_class.from_any(slot_data["options"][option]))

        self.lost_woods_item_sequence = slot_data["lost_woods_item_sequence"]
        self.lost_woods_main_sequence = slot_data["lost_woods_main_sequence"]
        self.default_seasons = slot_data["default_seasons"]
        self.old_man_rupee_values = slot_data["old_man_rupee_values"]
        self.dungeon_entrances = {f"{a} entrance": f"enter {b}"
                                  for a, b in slot_data["dungeon_entrances"].items()}
        self.portal_connections = slot_data["subrosia_portals"]
        self.shop_rupee_requirements = slot_data["shop_rupee_requirements"]
        self.shop_prices = slot_data["shop_costs"]

        return True
