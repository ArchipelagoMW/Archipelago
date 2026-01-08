import functools
import itertools
import logging
import os
from threading import Event
from typing import Any, Dict, Iterable, List, Optional, Set, TextIO, Union
from typing_extensions import override

from BaseClasses import CollectionState, Item, ItemClassification, Location, \
    LocationProgressType, MultiWorld, Region, Tutorial
from NetUtils import Hint
from worlds.AutoWorld import WebWorld, World
from .client import SubversionSNIClient
from .item import IMPORTANT_ITEM_ID, SubversionItem, name_to_id as _item_name_to_id, names_for_item_pool
from .location import SubversionLocation, name_to_id as _loc_name_to_id
from .logic import choose_torpedo_bay, cs_to_loadout
from .options import SubversionAutoHints, SubversionOptions, SubversionShortGame, make_sv_game
from .patch_utils import GenData, ItemRomData, make_gen_data
from .rom import SubversionDeltaPatch

from subversion_rando.connection_data import area_doors
from subversion_rando.game import Game as SvGame
from subversion_rando.item_data import Item as SvItem, Items, unique_items
from subversion_rando.item_marker import ItemMarker
from subversion_rando.loadout import Loadout
from subversion_rando.location_data import get_location_ids, new_locations
from subversion_rando.logic_locations import location_logic
from subversion_rando.logic_goal import can_win
from subversion_rando.logic_updater import updateLogic
from subversion_rando.main_generation import daphne_gate_spoiler
from subversion_rando.trick_data import trick_name_lookup

_ = SubversionSNIClient  # load the module to register the handler


class SubversionWebWorld(WebWorld):
    theme = "ice"
    tutorials = [
        Tutorial(
            tutorial_name="Setup Guide",
            description="A guide to playing Super Metroid Subversion in Archipelago.",
            language="English",
            file_name="setup_en.md",
            link="setup/en",
            authors=["beauxq"]
        )
    ]


class SubversionWorld(World):
    """
    Following the events of Super Metroid, Samus must destroy another
    Metroid research facility built by the Space Pirates on Planet TN578.
    This time however, the Pirates are more prepared to deal with Samus
    with the development of new weapons and armor based on Verdite technologies.
    It is time once again to protect the galaxy!
    """

    game = "Subversion"
    data_version = 0  # TODO: change to 1 before release
    web = SubversionWebWorld()

    options_dataclass = SubversionOptions
    options: SubversionOptions  # type: ignore [Overridden symbol]
    # this type: ignore is because of this issue: https://github.com/python/typing/discussions/1486

    location_name_to_id = _loc_name_to_id
    item_name_to_id = _item_name_to_id

    rom_name: Union[bytes, bytearray]
    rom_name_available_event: Event

    logger: logging.Logger
    sv_game: Optional[SvGame] = None
    torpedo_bay_item: Optional[str] = None
    spaceport_excluded_locs: List[str]
    early_hints_from_option: List[str]

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)
        self.rom_name = b""
        self.rom_name_available_event = Event()
        self.logger = logging.getLogger("Subversion")
        self.spaceport_excluded_locs = []
        self.early_hints_from_option = []

    @override
    def create_item(self, name: str) -> SubversionItem:
        return SubversionItem(name, self.player)

    @override
    def create_regions(self) -> None:
        excludes = frozenset(SubversionShortGame.location_lists[self.options.progression_items.value])

        menu = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu)

        sv_game = make_sv_game(self.options, self.multiworld.seed)
        self.sv_game = sv_game

        tb_item, exc_locs = choose_torpedo_bay(
            sv_game, self.options.auto_hints.value != SubversionAutoHints.option_none, self.random
        )
        self.logger.debug(f"Subversion player {self.player} chose torpedo bay item {tb_item}")
        self.logger.debug(f"and excluded locations: {exc_locs}")
        self.torpedo_bay_item = tb_item
        self.spaceport_excluded_locs = exc_locs

        if tb_item != Items.GravityBoots.name:
            self.multiworld.early_items[self.player][Items.GravityBoots.name] = 1

        for loc_name in _loc_name_to_id:
            loc = SubversionLocation(self.player, loc_name, menu)
            menu.locations.append(loc)

            def access_rule_wrapped(local_loc_name: str,
                                    local_sv_game: SvGame,
                                    p: int,
                                    collection_state: CollectionState) -> bool:
                if local_loc_name == "Torpedo Bay":
                    return True
                loadout = cs_to_loadout(local_sv_game,  collection_state, p)
                return location_logic[local_loc_name](loadout)

            access_rule = functools.partial(access_rule_wrapped,
                                            loc_name, self.sv_game, self.player)
            loc.access_rule = access_rule

            if loc_name == "Torpedo Bay":
                loc.place_locked_item(self.create_item(self.torpedo_bay_item))
            if (loc_name in self.spaceport_excluded_locs) or (loc_name in excludes):
                loc.progress_type = LocationProgressType.EXCLUDED
                self.options.exclude_locations.value.add(loc.name)

        # completion condition
        def completion_wrapped(local_sv_game: SvGame,
                               p: int,
                               collection_state: CollectionState) -> bool:
            loadout = cs_to_loadout(local_sv_game, collection_state, p)
            return can_win.access(loadout)
        completion = functools.partial(completion_wrapped, sv_game, self.player)
        self.multiworld.completion_condition[self.player] = completion

    @override
    def create_items(self) -> None:
        count_sjb = 0  # 1 SJB is progression, the rest are not
        count_la = 0  # 10 large ammo are prog, rest not
        excluded_tb_item = False  # 1 item is placed before fill algorithm
        for name in names_for_item_pool():
            if name == self.torpedo_bay_item and not excluded_tb_item:
                # this item is created and placed in create_regions
                excluded_tb_item = True
                continue
            this_item = self.create_item(name)
            if name == Items.SpaceJumpBoost.name:
                if count_sjb == 0:
                    this_item.classification = ItemClassification.progression
                count_sjb += 1
            elif name == Items.LargeAmmo.name:
                if count_la < 10:
                    this_item.classification = ItemClassification.progression
                count_la += 1
            self.multiworld.itempool.append(this_item)

    @override
    def fill_hook(self,
                  progitempool: List[Item],
                  usefulitempool: List[Item],
                  filleritempool: List[Item],
                  fill_locations: List[Location]) -> None:
        # The objective here is to create a bias towards the player receiving missiles before super missiles.
        # In this fill algorithm, the item being placed earlier tends to be picked up later in progression.
        # The fill algorithm places items from this list in reverse order.
        # We want supers to be placed before missiles, which means we want supers to come after missiles in this list.
        super_i = -1
        missile_i = -1
        for i, item in enumerate(progitempool):
            if item.name == Items.Super.name and item.player == self.player:
                super_i = i
            if item.name == Items.Missile.name and item.player == self.player:
                missile_i = i

        if super_i == -1 or missile_i == -1:
            # -1 means it's in Torpedo Bay, we already put that bias somewhere else
            return
        if super_i < missile_i:
            progitempool[super_i], progitempool[missile_i] = progitempool[missile_i], progitempool[super_i]
            self.logger.debug("swapped missile and super, so super should be placed first")
        else:
            self.logger.debug("super was already being placed earlier")

    def first_progression_items(self, sv_game: SvGame, auto_hints: SubversionAutoHints) -> List[str]:
        """ names of items that I'm expected to receive first """
        # TODO: does generation know the hint cost?
        # I might want to lower these if the hint cost is lower.
        # (I think I don't want to raise them if the hint cost is higher.)
        if auto_hints.value == SubversionAutoHints.option_normal:
            target_location_count = 11  # + torpedo bay makes 12
        else:  # option_light
            target_location_count = 5
        self.logger.debug(f"subversion player {self.player} auto hinting to {target_location_count} locations")
        base_loadout = (Items.spaceDrop, area_doors["SunkenNestL"])

        # This set is only referenced for unique items so it doesn't matter whether non-unique items go in it.
        items_in_my_own_locations: Set[str] = set()

        def minimize(items: Iterable[SvItem]) -> List[str]:
            """
            remove as many items as we can while keeping access to enough locations

            then filter to items not in my own locations
            """
            items_excluded: Set[SvItem] = set()
            for item in items:
                items_excluded.add(item)
                candidate_items = filter(lambda it: it not in items_excluded, items)
                loadout = Loadout(sv_game, itertools.chain(base_loadout, candidate_items))
                locs = new_locations().values()
                updateLogic(locs, loadout)
                if sum(loc["inlogic"] for loc in locs) < target_location_count:
                    # can't exclude that item because it lowers the location count too low
                    items_excluded.remove(item)
            minimized = [item.name for item in items if item in unique_items and item not in items_excluded]
            self.logger.debug(f"{minimized=}")
            minimized = [item_name for item_name in minimized if item_name not in items_in_my_own_locations]
            self.logger.debug(f"not in my locations: {minimized}")
            return minimized

        items_picked_up: List[SvItem] = []
        loadout = Loadout(sv_game, base_loadout)
        unused_locations = new_locations().values()
        for sphere in self.multiworld.get_spheres():
            my_items_in_this_sphere: List[SvItem] = []
            for loc in sphere:
                if (
                    isinstance(loc.item, SubversionItem) and
                    loc.item.player == self.player
                ):
                    my_items_in_this_sphere.append(loc.item.sv_item)
                    if loc.player == self.player:
                        items_in_my_own_locations.add(loc.item.sv_item.name)
            my_items_in_this_sphere.sort()  # there's a PR to do this inside get_spheres, then won't need it here
            self.random.shuffle(my_items_in_this_sphere)
            for item in my_items_in_this_sphere:
                items_picked_up.append(item)
                loadout.append(item)
                updateLogic(unused_locations, loadout)
                if sum(loc["inlogic"] for loc in unused_locations) >= target_location_count:
                    self.logger.debug(f"early items: {[it.name for it in items_picked_up]}")
                    return minimize(items_picked_up)
        return minimize(items_picked_up)

    def _set_early_hints_from_options(self, sv_game: SvGame) -> None:
        auto_hints_option = self.options.auto_hints
        if auto_hints_option.value:
            hint_items = self.first_progression_items(sv_game, auto_hints_option)
            self.logger.debug(f"{hint_items=}")
            self.early_hints_from_option = hint_items

    @override
    def generate_output(self, output_directory: str) -> None:
        assert self.sv_game, "can't call generate_output without create_regions"

        self._set_early_hints_from_options(self.sv_game)

        troll_ammo = bool(self.options.troll_ammo.value)
        item_rom_data = ItemRomData(self.player, troll_ammo, self.multiworld.player_name)
        item_markers: Dict[int, ItemMarker] = {}
        for loc in self.multiworld.get_locations():
            item_rom_data.register(loc)

            if loc.player == self.player:
                assert isinstance(loc, SubversionLocation), f"{loc=}"
                item = loc.item
                assert isinstance(item, Item)
                marker = self.options.item_markers.get_marker(item)
                sv_loc_ids = get_location_ids(loc.sv_loc)
                for loc_id in sv_loc_ids:
                    item_markers[loc_id] = marker
        assert len(item_markers) == 131, f"{len(item_markers)=}"
        self.sv_game.item_markers = item_markers

        # set rom name
        from Utils import __version__
        rom_name = bytearray(
            f'SV{__version__.replace(".", "")[0:3]}_{self.player}_{self.multiworld.seed:11}',
            'utf8'
        )[:21]
        rom_name.extend(b" " * (21 - len(rom_name)))
        assert len(rom_name) == 21, f"{rom_name=}"
        self.rom_name = rom_name
        self.rom_name_available_event.set()

        gen_data = GenData(item_rom_data.get_jsonable_data(), self.sv_game, self.player, self.rom_name)

        out_file_base = self.multiworld.get_out_file_name_base(self.player)

        patch_file_name = os.path.join(output_directory, f"{out_file_base}{SubversionDeltaPatch.patch_file_ending}")
        patch = SubversionDeltaPatch(patch_file_name,
                                     player=self.player,
                                     player_name=self.multiworld.player_name[self.player],
                                     gen_data=make_gen_data(gen_data))
        patch.write()

        self.logger.debug(f"Subversion player {self.player} finished generate_output")

    @override
    def write_spoiler_header(self, spoiler_handle: TextIO) -> None:
        def bool_to_text(variable: bool) -> str:
            return "Yes" if variable else "No"

        assert self.sv_game, "need info from earlier in generation to write spoiler"
        logic = self.sv_game.options.logic

        player_name = self.multiworld.get_player_name(self.player)
        spoiler_handle.write(f"\ntricks in logic for Subversion player {self.player} {player_name}:\n")

        for trick, trick_name in trick_name_lookup.items():
            spoiler_handle.write(f"  {trick_name:23}: {bool_to_text(trick in logic)}\n")

        spoiler_handle.write(f"\nplayer {self.player} {daphne_gate_spoiler(self.sv_game)}\n")

        # TODO: area rando connections, objective rando info

    @override
    def modify_multidata(self, multidata: Dict[str, Any]) -> None:
        import base64
        # wait for self.rom_name to be available.
        self.rom_name_available_event.wait()
        rom_name = self.rom_name
        assert len(rom_name) == 21, f"{rom_name=}"
        new_name = base64.b64encode(rom_name).decode()
        multidata["connect_names"][new_name] = multidata["connect_names"][self.multiworld.player_name[self.player]]

        precollected_hints: Dict[int, Set[Hint]] = multidata["precollected_hints"]

        def precollect_hint(location: Location) -> None:
            """ This is mostly copied from `write_multidata` but with ID for hidden item name. """
            assert location.item and location.address
            hint = Hint(location.item.player, location.player, location.address,
                        IMPORTANT_ITEM_ID, False, "", location.item.flags)
            precollected_hints[location.player].add(hint)
            if location.item.player not in self.multiworld.groups:
                precollected_hints[location.item.player].add(hint)
            else:
                players_in_group = self.multiworld.groups[location.item.player].get("players")
                assert not (players_in_group is None)
                for player in players_in_group:
                    precollected_hints[player].add(hint)

        hidden_item_name_hints = frozenset(self.early_hints_from_option)
        for location in self.multiworld.get_filled_locations():
            item = location.item
            # TODO: this probably won't work for item links
            if item and item.player == self.player:
                # my item is in this location
                if (
                    item.name not in self.options.start_hints and
                    item.name in hidden_item_name_hints
                ):
                    precollect_hint(location)

    @override
    def get_filler_item_name(self) -> str:
        return "Small Ammo"
